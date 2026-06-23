---
ticket: docs/user-stories/002-user-authentication/tickets/database/ticket.md
layer: database
progress: 24 / 24 tasks completed
---

# Plan de Desarrollo — [DB] User Authentication — Schema & Migrations

> Marca cada tarea con `- [x]` al completarla. Actualiza `progress` en el frontmatter.

## Fase 1 · Prerequisitos
- [x] PostgreSQL corriendo: `docker compose ps`
- [x] Última versión del branch principal: `git pull origin main`
- [x] Crear branch: `git checkout -b feature/user-authentication-database`

## Fase 2 · Migración Alembic
_Archivo: `apps/backend/src/shared/database/migrations/202606231109_auth_organizations_users_refresh_tokens.py`_

### upgrade() — tabla `organizations`
- [x] Crear tabla `organizations` con `id UUID PK`, `name`, `code UNIQUE`, `status`, `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`, `deleted_at NULL`, `deleted_by NULL`
- [x] Agregar constraint `CHECK (status IN ('active','inactive'))` en `organizations`

### upgrade() — tabla `users`
- [x] Crear (o verificar existencia de) tabla `users` con columnas completas
- [x] Agregar columnas de auditoría: `created_at`, `updated_at`, `deleted_at`, `deleted_by`
- [x] Agregar `CHECK (role IN ('administrator','manager','employee'))` en `users`
- [x] Agregar `CHECK (status IN ('active','inactive'))` en `users`

### upgrade() — tabla `refresh_tokens`
- [x] Crear tabla `refresh_tokens` con `id UUID PK`, `user_id UUID FK NOT NULL → users.id ON DELETE CASCADE`, `token_hash TEXT NOT NULL`, `expires_at TIMESTAMPTZ NOT NULL`, `revoked_at TIMESTAMPTZ NULL`, `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`

### upgrade() — índices
- [x] `uq_users_email` (partial unique index WHERE deleted_at IS NULL)
- [x] `idx_users_organization_id`
- [x] `idx_users_status`
- [x] `uq_refresh_tokens_token_hash`
- [x] `idx_refresh_tokens_user_id`
- [x] `idx_refresh_tokens_expires_at`

### downgrade()
- [x] Implementar `downgrade()`: drop índices → drop `refresh_tokens` → drop `users` → drop `organizations`

## Fase 3 · Seed
_Archivo: `apps/backend/scripts/seed_auth.py`_
- [x] Crear 2 organizaciones activas (org_a, org_b) para tests de aislamiento cross-tenant
- [x] Crear 1 usuario por rol en org_a: `administrator`, `manager`, `employee` con contraseña hasheada con bcrypt
- [x] Crear 1 usuario `employee` en org_b para tests de aislamiento
- [x] Verificar que el script es idempotente (re-ejecutable sin errores)

## Fase 4 · Ejecutar y Verificar
- [x] Aplicar migración: `alembic upgrade head` ✅
- [x] Verificar schema: `\d users` confirma columnas, tipos, constraints, FKs e índices
- [x] Verificar idempotencia: re-ejecutar migración sin cambios
- [x] Probar rollback: `alembic downgrade -1` y re-aplicar ✅
- [x] Ejecutar seed: `python scripts/seed_auth.py` ✅

## Fase 5 · Criterios de Aceptación
- [x] Tabla `users` tiene `hashed_password`, `status`, `role`, `organization_id` con tipos y restricciones correctas
- [x] Tabla `refresh_tokens` creada con `token_hash`, `user_id`, `expires_at`, `revoked_at`
- [x] `organization_id` presente en `users`
- [x] Columnas de auditoría presentes en `users` y `organizations`
- [x] Todos los índices creados (incluido `uq_users_email` parcial)
- [x] `CHECK` constraints en `role` y `status`
- [x] Migración `upgrade()` ejecuta sin errores
- [x] `downgrade()` implementado y probado
- [x] Seed crea 2 organizaciones y usuarios en ambas para tests de aislamiento cross-tenant

## Fase 6 · Entrega
- [x] Commit: `git commit -m "feat(db): add organizations, users and refresh_tokens schema for auth"`
- [x] Push: `git push origin feature/user-authentication-database`
- [x] Abrir PR — NO hacer merge sin validación
