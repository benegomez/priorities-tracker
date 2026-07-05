---
status: done
type: database
story: docs/user-stories/001-weekly-checkin-creation/UserStory.md
risk_level: Critical
complexity: L
---

# [DB] US-001 — Weekly Check-In Creation

## Objetivo

Crear el schema físico PostgreSQL para las entidades `check_ins`, `priorities` y `tasks` que soportan el flujo de planificación semanal, junto con las tablas prerequisito `projects` y `project_phases` que aún no existen en el schema.

## Scope

Solo schema PostgreSQL + migración Alembic. Sin endpoints, sin lógica de negocio, sin UI.

---

## Prerequisitos

Las tablas `organizations` y `users` ya existen (migración `202606231109`). Las tablas `projects` y `project_phases` **no existen** y deben crearse en esta misma migración porque son FK obligatorias de `priorities`.

---

## Cambios al Schema

### Tabla: `projects`

```sql
CREATE TABLE projects (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID        NOT NULL REFERENCES organizations(id),
    name            VARCHAR(255) NOT NULL,
    description     TEXT        NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'draft'
                                CHECK (status IN ('draft', 'active', 'on_hold', 'completed', 'archived')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ NULL,
    deleted_by      UUID        NULL
);
```

**Índices:**
```sql
CREATE INDEX idx_projects_organization_id ON projects (organization_id);
CREATE INDEX idx_projects_status ON projects (status) WHERE deleted_at IS NULL;
```

---

### Tabla: `project_phases`

```sql
CREATE TABLE project_phases (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID        NOT NULL REFERENCES organizations(id),
    project_id      UUID        NOT NULL REFERENCES projects(id),
    name            VARCHAR(255) NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'planned'
                                CHECK (status IN ('planned', 'active', 'completed', 'cancelled')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ NULL,
    deleted_by      UUID        NULL
);
```

**Índices:**
```sql
CREATE INDEX idx_project_phases_organization_id ON project_phases (organization_id);
CREATE INDEX idx_project_phases_project_id ON project_phases (project_id);
```

---

### Tabla: `check_ins`

```sql
CREATE TABLE check_ins (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID        NOT NULL REFERENCES organizations(id),
    employee_id     UUID        NOT NULL REFERENCES users(id),
    week_start      DATE        NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'draft'
                                CHECK (status IN ('draft', 'submitted', 'closed')),
    submitted_at    TIMESTAMPTZ NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ NULL,
    deleted_by      UUID        NULL
);
```

**Índices:**
```sql
-- Enforcement de BR-001: un solo check-in activo por empleado por semana
CREATE UNIQUE INDEX uq_check_ins_employee_week
    ON check_ins (employee_id, week_start)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_check_ins_organization_id ON check_ins (organization_id);
CREATE INDEX idx_check_ins_employee_id ON check_ins (employee_id);
CREATE INDEX idx_check_ins_week_start ON check_ins (week_start);
```

> El índice único parcial `uq_check_ins_employee_week` permite soft-delete sin violar la constraint.

---

### Tabla: `priorities`

```sql
CREATE TABLE priorities (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID        NOT NULL REFERENCES organizations(id),
    checkin_id      UUID        NOT NULL REFERENCES check_ins(id),
    phase_id        UUID        NOT NULL REFERENCES project_phases(id),
    owner_id        UUID        NOT NULL REFERENCES users(id),
    week_start      DATE        NOT NULL,
    title           VARCHAR(255) NOT NULL,
    description     TEXT        NULL,
    priority_level  VARCHAR(10) NOT NULL DEFAULT 'medium'
                                CHECK (priority_level IN ('low', 'medium', 'high')),
    status          VARCHAR(20) NOT NULL DEFAULT 'draft'
                                CHECK (status IN ('draft', 'planned', 'in_progress',
                                                  'completed', 'carried_over')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ NULL,
    deleted_by      UUID        NULL
);
```

**Índices:**
```sql
CREATE INDEX idx_priorities_organization_id ON priorities (organization_id);
CREATE INDEX idx_priorities_checkin_id ON priorities (checkin_id);
CREATE INDEX idx_priorities_phase_id ON priorities (phase_id);
CREATE INDEX idx_priorities_owner_id ON priorities (owner_id);
CREATE INDEX idx_priorities_week_start ON priorities (week_start);
CREATE INDEX idx_priorities_status ON priorities (status) WHERE deleted_at IS NULL;
```

---

### Tabla: `tasks`

```sql
CREATE TABLE tasks (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID        NOT NULL REFERENCES organizations(id),
    priority_id     UUID        NOT NULL REFERENCES priorities(id),
    title           VARCHAR(255) NOT NULL,
    description     TEXT        NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending'
                                CHECK (status IN ('pending', 'in_progress',
                                                  'completed', 'cancelled')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ NULL,
    deleted_by      UUID        NULL
);
```

**Índices:**
```sql
CREATE INDEX idx_tasks_organization_id ON tasks (organization_id);
CREATE INDEX idx_tasks_priority_id ON tasks (priority_id);
CREATE INDEX idx_tasks_status ON tasks (status) WHERE deleted_at IS NULL;
```

---

## Migración Alembic

Archivo: `apps/backend/src/shared/database/migrations/202506231200_create_projects_checkins_priorities_tasks.py`

Debe implementar:
- `upgrade()` — crear tablas en orden: `projects` → `project_phases` → `check_ins` → `priorities` → `tasks`
- `downgrade()` — eliminar en orden inverso: `tasks` → `priorities` → `check_ins` → `project_phases` → `projects`

Revisión: `202506231200`
Down revision: `202606231109` (migración de auth)

---

## Decisiones de Diseño

| Decisión | Justificación |
|---|---|
| Columna `week_start` (no `week_period`) | Mismo nombre en API y DB — elimina confusión de mapping |
| `priority_level` sin `critical` | Alineado con domain-standards.md: solo `low`, `medium`, `high` |
| Partial unique index con `WHERE deleted_at IS NULL` | Permite soft-delete sin violar unicidad (BR-001) |
| `projects` y `project_phases` en esta migración | Son FK obligatorias de `priorities`; no existen aún en el schema |
| `organization_id` en todas las tablas | BR-017 + multi-tenant isolation |
| FK naming: `checkin_id` | Consistente con tabla origen `check_ins` sin guión bajo extra |

---

## Criterios de Aceptación

- [x] Tabla `projects` creada con campos, constraints y enums correctos
- [x] Tabla `project_phases` creada con FK a `projects`
- [x] Tabla `check_ins` creada con todos los campos y constraints
- [x] Tabla `priorities` creada con FKs a `check_ins`, `project_phases`, `users`
- [x] Tabla `tasks` creada con FK a `priorities`
- [x] `organization_id` presente y con FK en las cinco tablas
- [x] Columnas de auditoría en todas las tablas (`created_at`, `updated_at`, `deleted_at`, `deleted_by`)
- [x] Partial unique index `uq_check_ins_employee_week` creado (BR-001)
- [x] Todos los índices FK creados
- [x] Enums implementados como CHECK constraints
- [x] Migración `upgrade()` ejecuta sin errores
- [x] Migración `downgrade()` revierte completamente sin errores
- [x] Re-ejecutar `upgrade()` después de `downgrade()` funciona sin errores

---

## Dependencias

- Migración `202606231109` (organizations, users) debe existir
- Debe completarse y mergearse **antes** del ticket backend

---

## Git Branch

`feature/001-weekly-checkin-creation`
