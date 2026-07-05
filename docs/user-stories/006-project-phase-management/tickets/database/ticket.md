---
status: done
type: database
story: docs/user-stories/006-project-phase-management/UserStory.md
depends-on: null
risk_level: Medium
complexity: S
---

# [DB] US-006 — Project & Phase Management Schema

## Objetivo

Agregar columna `owner_id` a `projects` y crear tabla `project_members` para soportar asignación de responsable y participantes.

## Scope

Solo migración Alembic. Las tablas `projects` y `project_phases` ya existen.

---

## Cambios al Schema

### ALTER: `projects` — agregar `owner_id`

```sql
ALTER TABLE projects ADD COLUMN owner_id UUID NULL REFERENCES users(id);
CREATE INDEX idx_projects_owner_id ON projects (owner_id);
```

> Nullable inicialmente para no romper datos existentes. La API lo requiere en creación.

---

### Nueva tabla: `project_members`

```sql
CREATE TABLE project_members (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID        NOT NULL REFERENCES organizations(id),
    project_id      UUID        NOT NULL REFERENCES projects(id),
    user_id         UUID        NOT NULL REFERENCES users(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ NULL,
    deleted_by      UUID        NULL
);
```

**Índices:**
```sql
CREATE UNIQUE INDEX uq_project_members_project_user
    ON project_members (project_id, user_id)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_project_members_organization_id ON project_members (organization_id);
CREATE INDEX idx_project_members_project_id ON project_members (project_id);
CREATE INDEX idx_project_members_user_id ON project_members (user_id);
```

---

## Migración Alembic

Archivo: `apps/backend/src/shared/database/migrations/202507051300_add_project_owner_and_members.py`

- `upgrade()`:
  - ALTER `projects` ADD COLUMN `owner_id`
  - CREATE TABLE `project_members`
  - CREATE indexes
- `downgrade()`:
  - DROP TABLE `project_members`
  - ALTER `projects` DROP COLUMN `owner_id`

Revisión: `202507051300`
Down revision: `202507051200`

---

## Criterios de Aceptación

- [ ] Columna `owner_id` agregada a `projects` con FK a `users`
- [ ] Tabla `project_members` creada con constraints
- [ ] Partial unique index `uq_project_members_project_user` (evita duplicados)
- [ ] Todos los índices FK creados
- [ ] Migración `upgrade()` ejecuta sin errores
- [ ] Migración `downgrade()` revierte completamente
- [ ] Re-upgrade funciona

---

## Git Branch

`feature/006-project-phase-management`
