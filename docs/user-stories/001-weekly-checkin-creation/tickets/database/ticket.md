---
status: todo
type: database
story: docs/user-stories/001-weekly-checkin-creation/UserStory.md
risk_level: Critical
complexity: L
---

# [DB] US-001 — Weekly Check-In Creation

## Objetivo

Crear el schema físico PostgreSQL para las entidades `check_ins`, `priorities` y `tasks` que soportan el flujo de planificación semanal. Estas tres tablas son el fundamento de toda la cadena de valor del producto.

## Scope

Solo schema PostgreSQL + migración Alembic. Sin endpoints, sin lógica de negocio, sin UI.

---

## Cambios al Schema

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
CREATE UNIQUE INDEX uq_check_ins_employee_week
    ON check_ins (employee_id, week_start)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_check_ins_organization_id ON check_ins (organization_id);
CREATE INDEX idx_check_ins_employee_id     ON check_ins (employee_id);
CREATE INDEX idx_check_ins_week_start      ON check_ins (week_start);
```

> El índice único `uq_check_ins_employee_week` es el enforcement de BR-001 a nivel de base de datos.

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
    priority_level  VARCHAR(20) NOT NULL DEFAULT 'medium'
                                CHECK (priority_level IN ('low', 'medium', 'high', 'critical')),
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
CREATE INDEX idx_priorities_checkin_id      ON priorities (checkin_id);
CREATE INDEX idx_priorities_phase_id        ON priorities (phase_id);
CREATE INDEX idx_priorities_owner_id        ON priorities (owner_id);
CREATE INDEX idx_priorities_week_start      ON priorities (week_start);
CREATE INDEX idx_priorities_status          ON priorities (status) WHERE deleted_at IS NULL;
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
CREATE INDEX idx_tasks_priority_id     ON tasks (priority_id);
CREATE INDEX idx_tasks_status          ON tasks (status) WHERE deleted_at IS NULL;
```

---

## Migración Alembic

Archivo: `apps/backend/src/shared/database/migrations/<YYYYMMDDHHMI>_create_checkins_priorities_tasks.py`

Debe implementar:
- `upgrade()` — crear las tres tablas en orden: `check_ins` → `priorities` → `tasks`
- `downgrade()` — eliminar en orden inverso: `tasks` → `priorities` → `check_ins`

---

## Criterios de Aceptación

- [ ] Tabla `check_ins` creada con todos los campos, constraints y tipos correctos
- [ ] Tabla `priorities` creada con todos los campos, constraints y tipos correctos
- [ ] Tabla `tasks` creada con todos los campos, constraints y tipos correctos
- [ ] `organization_id` presente y con FK en las tres tablas
- [ ] Columnas de auditoría presentes en las tres tablas (`created_at`, `updated_at`, `deleted_at`, `deleted_by`)
- [ ] Índice único `uq_check_ins_employee_week` creado (enforcement de BR-001)
- [ ] Todos los índices FK creados
- [ ] Enums de status implementados como CHECK constraints
- [ ] Migración `upgrade()` ejecuta sin errores sobre BD vacía
- [ ] Migración `downgrade()` revierte completamente sin errores
- [ ] Re-ejecutar `upgrade()` después de `downgrade()` funciona sin errores

## Dependencias

Ninguna propia de esta US. Las tablas `organizations`, `users`, `projects` y `project_phases` deben existir previamente (prerequisito de estructura organizacional).

Debe completarse y mergearse antes del ticket backend.
