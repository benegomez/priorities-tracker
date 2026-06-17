---
description: "Estándares de base de datos para Priorities Tracker. PostgreSQL + SQLAlchemy 2 + Alembic."
globs: **/*.sql, **/migrations/**/*.py, **/models/**/*.py
alwaysApply: false
---

# Database Standards — Priorities Tracker

## Stack Oficial

- PostgreSQL
- SQLAlchemy 2.0 (async ORM)
- Alembic (migraciones versionadas)

---

## Convenciones de Nomenclatura

| Elemento | Convención | Ejemplo |
|---|---|---|
| Tablas | `snake_case` plural | `users`, `project_phases`, `planning_cycles` |
| Columnas | `snake_case` | `created_at`, `deleted_by` |
| PK | `pk_<table>` | `pk_users` |
| FK | `fk_<table>_<referenced_table>` | `fk_priorities_projects` |
| Índices | `idx_<table>_<column>` | `idx_users_team_id` |
| Unique | `uq_<table>_<column>` | `uq_users_email` |
| Migraciones | `YYYYMMDDHHMI_description.py` | `202501151030_create_users_table.py` |

---

## Tipos de Datos

- `TIMESTAMPTZ` para todos los timestamps — nunca `TIMESTAMP` sin zona horaria
- `UUID` para PKs públicas e IDs expuestos en API
- `BIGSERIAL` para claves internas de alto volumen si aplica
- `NOT NULL` por defecto — nullable solo cuando es intencional y documentado

---

## Columnas de Auditoría (Obligatorias en Entidades de Negocio)

```sql
created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
deleted_at  TIMESTAMPTZ NULL       -- soft delete
deleted_by  UUID NULL              -- soft delete
```

---

## Soft Delete

- Nunca eliminar físicamente registros funcionales de negocio
- Marcar con `deleted_at` y `deleted_by`
- Todos los queries de lectura deben filtrar `WHERE deleted_at IS NULL` por defecto

---

## Integridad Referencial

- FK explícitas con comportamiento `ON DELETE` definido en cada caso
- Check constraints para invariantes de dominio
- Transacciones explícitas para operaciones multi-tabla

---

## Índices

- Indexar todas las columnas FK
- `CREATE INDEX CONCURRENTLY` en tablas con datos (no bloqueante)
- Índices parciales para subconjuntos filtrados frecuentemente
- Eliminar índices no utilizados

---

## Queries

- Queries parametrizadas siempre — nunca interpolación de strings SQL
- `SELECT` con columnas explícitas — nunca `SELECT *`
- `LIMIT` en todas las queries potencialmente grandes
- `EXPLAIN ANALYZE` antes de publicar queries complejas

---

## Migraciones (Alembic)

- Archivos versionados con timestamp + descripción
- Incluir siempre función `upgrade()` y `downgrade()`
- Probar rollback antes de desplegar en producción
- No hacer cambios de schema en horario de alta carga
- Columnas grandes: migración multi-paso con backfill

---

## Prohibido

- `SELECT *` en código de aplicación
- Interpolación de strings en SQL
- `TRUNCATE` en código de aplicación
- Contraseñas en texto plano en la base de datos
- Cambios de schema sin migración versionada
- Acceso directo a la base de datos desde fuera de la capa de repositorios

---

## Jerarquía del Modelo de Datos

```
organizations
  └── teams
        └── users
              └── planning_cycles (check-in → check-out)
                    └── priorities
                          └── tasks

projects
  └── project_phases
        └── priorities (FK)

crs_scores (calculado por planning cycle y usuario)
```

---

## Referencias

- [docs/05-database/postgres-naming-conventions.md](../../docs/05-database/postgres-naming-conventions.md)
- [docs/05-database/soft-delete-strategy.md](../../docs/05-database/soft-delete-strategy.md)
- [docs/05-database/alembic-guidelines.md](../../docs/05-database/alembic-guidelines.md)
- [docs/05-database/indexes-strategy.md](../../docs/05-database/indexes-strategy.md)
- [docs/05-database/audit-columns-strategy.md](../../docs/05-database/audit-columns-strategy.md)
- [docs/05-database/full-ddl-specification.md](../../docs/05-database/full-ddl-specification.md)
