---
status: done
type: database
story: docs/user-stories/002-user-authentication/UserStory.md
---

# [DB] User Authentication — Schema & Migrations

## Objetivo
Crear/modificar las tablas que soportan autenticación: columnas de credenciales en `users`, tabla de refresh tokens, e índices necesarios.

## Scope
Solo schema PostgreSQL + migraciones Alembic. Sin endpoints, sin lógica de negocio.

## Cambios al Schema

### Columnas nuevas en tabla existente: `users`
```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS hashed_password  TEXT         NOT NULL DEFAULT '';
ALTER TABLE users ADD COLUMN IF NOT EXISTS status           VARCHAR(20)  NOT NULL DEFAULT 'active';
-- Verificar: id, organization_id, email (uq), role ya deben existir desde US-001 o se crean aquí
```

Definición completa de `users` si la tabla no existe aún:
```sql
users
  - id              UUID          PK        NOT NULL  DEFAULT gen_random_uuid()
  - organization_id UUID          FK        NOT NULL  → organizations.id
  - email           VARCHAR(255)  UNIQUE    NOT NULL
  - hashed_password TEXT                   NOT NULL
  - role            VARCHAR(20)            NOT NULL  CHECK (role IN ('administrator','manager','employee'))
  - status          VARCHAR(20)            NOT NULL  DEFAULT 'active' CHECK (status IN ('active','inactive'))
  - first_name      VARCHAR(100)           NOT NULL
  - last_name       VARCHAR(100)           NOT NULL
  - manager_id      UUID          FK NULL            → users.id
  - created_at      TIMESTAMPTZ            NOT NULL  DEFAULT now()
  - updated_at      TIMESTAMPTZ            NOT NULL  DEFAULT now()
  - deleted_at      TIMESTAMPTZ            NULL
  - deleted_by      UUID                   NULL
```

### Tabla nueva: `refresh_tokens`
```sql
refresh_tokens
  - id          UUID          PK  NOT NULL  DEFAULT gen_random_uuid()
  - user_id     UUID          FK  NOT NULL  → users.id  ON DELETE CASCADE
  - token_hash  TEXT              NOT NULL
  - expires_at  TIMESTAMPTZ       NOT NULL
  - revoked_at  TIMESTAMPTZ       NULL
  - created_at  TIMESTAMPTZ       NOT NULL  DEFAULT now()
```

> No requiere `organization_id` directo (se obtiene a través de `user_id → users.organization_id`).
> No requiere soft delete columns — se invalida con `revoked_at`.

### Índices
```sql
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS uq_users_email
  ON users (email) WHERE deleted_at IS NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_organization_id
  ON users (organization_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_status
  ON users (status);

CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS uq_refresh_tokens_token_hash
  ON refresh_tokens (token_hash);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_refresh_tokens_user_id
  ON refresh_tokens (user_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_refresh_tokens_expires_at
  ON refresh_tokens (expires_at);
```

### Tabla: `organizations` (si no existe)
```sql
organizations
  - id         UUID          PK  NOT NULL  DEFAULT gen_random_uuid()
  - name       VARCHAR(255)       NOT NULL
  - code       VARCHAR(50)   UNIQUE NOT NULL
  - status     VARCHAR(20)        NOT NULL DEFAULT 'active'
  - created_at TIMESTAMPTZ        NOT NULL DEFAULT now()
  - updated_at TIMESTAMPTZ        NOT NULL DEFAULT now()
  - deleted_at TIMESTAMPTZ        NULL
  - deleted_by UUID               NULL
```

## Migración Alembic

Archivo: `apps/backend/src/shared/database/migrations/<YYYYMMDDHHMI>_auth_users_and_refresh_tokens.py`

Debe incluir:
- `upgrade()`: crear `organizations` (si no existe), crear/alterar `users`, crear `refresh_tokens`, crear todos los índices
- `downgrade()`: drop índices, drop `refresh_tokens`, revertir columnas en `users`

## Seed Mínimo

Script: `scripts/seed_auth.py`

Crear al menos:
- 2 organizaciones activas (necesarias para validar aislamiento cross-tenant del Escenario 8)
- 1 usuario por cada rol (`administrator`, `manager`, `employee`) con contraseña hasheada en organización A
- 1 usuario adicional en organización B para tests de aislamiento multi-tenant

## Criterios de Aceptación
- [x] Tabla `users` tiene `hashed_password`, `status`, `role`, `organization_id` con tipos y restricciones correctas
- [x] Tabla `refresh_tokens` creada con `token_hash`, `user_id`, `expires_at`, `revoked_at`
- [x] `organization_id` presente en `users`
- [x] Columnas de auditoría presentes en `users` y `organizations` (`created_at`, `updated_at`, `deleted_at`, `deleted_by`)
- [x] Todos los índices creados (incluido `uq_users_email` parcial)
- [x] `CHECK` constraints en `role` y `status`
- [x] Migración `upgrade()` ejecuta sin errores
- [x] `downgrade()` implementado y probado
- [x] Seed crea 2 organizaciones y usuarios en ambas para soportar tests de aislamiento cross-tenant
- [x] Seed ejecuta sin errores y produce usuarios utilizables para tests

## Dependencias
Ninguna. Debe completarse antes del ticket backend.
