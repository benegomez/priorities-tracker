---
status: pending
type: database
story: docs/user-stories/013-admin-team-management/UserStory.md
depends-on: null
risk_level: Medium
complexity: S
---

# [DB] US-013 — Admin Team Management: Migración

## Objetivo

Crear la tabla `teams` y agregar la columna `team_id` en `users` para formalizar la estructura de equipos como entidad de negocio.

## Scope

1 migración Alembic con `upgrade()` y `downgrade()`.

---

## Cambios de Schema

### Nueva tabla `teams`

```sql
CREATE TABLE teams (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    manager_id      UUID NULL REFERENCES users(id),
    name            VARCHAR(200) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ NULL,
    deleted_by      UUID NULL,
    CONSTRAINT uq_teams_org_name UNIQUE (organization_id, name)
);

CREATE INDEX idx_teams_organization_id ON teams(organization_id);
CREATE INDEX idx_teams_manager_id ON teams(manager_id);
```

### Columna nueva en `users`

```sql
ALTER TABLE users ADD COLUMN team_id UUID NULL REFERENCES teams(id);
CREATE INDEX idx_users_team_id ON users(team_id);
```

---

## Archivo a Crear

```
apps/backend/src/shared/database/migrations/
  202501280900_create_teams_add_team_id_to_users.py
```

---

## Criterios de Aceptación

- [ ] `upgrade()` crea tabla `teams` con todos los constraints
- [ ] `upgrade()` agrega columna `team_id` en `users`
- [ ] `downgrade()` revierte ambos cambios en orden correcto (primero columna, luego tabla)
- [ ] `alembic upgrade head` ejecuta sin errores en contenedor
- [ ] `alembic downgrade -1` revierte sin errores

---

## Git Branch

`feature/013-admin-team-management`
