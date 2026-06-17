---
description: Genera un plan de desarrollo detallado con checkboxes (plan.md) para cada ticket de una user story. Acepta filtro opcional de capa (database | backend | frontend).
---

Por favor crea el plan de desarrollo del ticket: $ARGUMENTS

## Parseo de Argumentos

`$ARGUMENTS` puede ser:

| Formato | Comportamiento |
|---|---|
| `<story-id>` | Genera planes para las tres capas |
| `<story-id> database` o `<story-id> db` | Solo plan database |
| `<story-id> backend` o `<story-id> be` | Solo plan backend |
| `<story-id> frontend` o `<story-id> fe` | Solo plan frontend |

## Paso 1 — Cargar Tickets

- Localiza la carpeta de la story y lee `tickets/<capa>/ticket.md` para cada capa solicitada.
- Si falta algún ticket, advierte al usuario y pide ejecutar `/create-tickets` primero.

## Paso 2 — Escribir Planes

Guarda cada plan como `plan.md` junto al `ticket.md` correspondiente. Si ya existe, sobreescribir.

---

## Template Database

```markdown
---
ticket: <ruta/database/ticket.md>
layer: database
progress: 0 / <total> tasks completed
---

# Plan de Desarrollo — [DB] <Feature Name>

> Marca cada tarea con `- [x]` al completarla. Actualiza `progress` en el frontmatter.

## Fase 1 · Prerequisitos
- [ ] PostgreSQL corriendo: `docker compose ps`
- [ ] Última versión del branch principal: `git pull origin main`
- [ ] Crear branch: `git checkout -b <branch-name>`

## Fase 2 · Migración Alembic
_Archivo: `apps/backend/src/shared/database/migrations/<YYYYMMDDHHMI>_<descripcion>.py`_
- [ ] Crear archivo de migración con timestamp correcto
- [ ] Implementar `upgrade()` con los cambios del ticket
- [ ] Implementar `downgrade()` que revierte los cambios
- [ ] Verificar que toda entidad de negocio tiene `organization_id`
- [ ] Verificar columnas de auditoría: `created_at`, `updated_at`, `deleted_at`, `deleted_by`
- [ ] Agregar índices para todas las FK: `idx_<tabla>_<columna>`
- [ ] Tipos de datos correctos: `TIMESTAMPTZ` (no TIMESTAMP), `UUID` para PKs

## Fase 3 · Ejecutar y Verificar
- [ ] Aplicar migración: `docker compose exec api alembic upgrade head`
- [ ] Verificar schema: conectar a BD y revisar tablas/columnas
- [ ] Verificar idempotencia: re-ejecutar migración sin errores
- [ ] Probar rollback: `alembic downgrade -1` y re-aplicar

## Fase 4 · Criterios de Aceptación
<un checkbox por criterio del ticket>

## Fase 5 · Entrega
- [ ] Commit: `git commit -m "feat(db): <descripción>"`
- [ ] Push: `git push origin <branch-name>`
- [ ] Abrir PR — NO hacer merge sin validación
```

---

## Template Backend

```markdown
---
ticket: <ruta/backend/ticket.md>
layer: backend
depends-on: <ruta/database/ticket.md>
progress: 0 / <total> tasks completed
---

# Plan de Desarrollo — [BE] <Feature Name>

> Marca cada tarea con `- [x]` al completarla. Actualiza `progress` en el frontmatter.

## Fase 1 · Prerequisitos
- [ ] Ticket database mergeado y migración aplicada
- [ ] `git pull origin main` y crear branch: `git checkout -b <branch-name>`
- [ ] Leer `.amazonq/rules/backend-standards.md` y `domain-standards.md`

## Fase 2 · Contrato OpenAPI
_Antes de escribir código — ADR-009_
- [ ] Definir schema `<Entity>Create` en `api/schemas.py`
- [ ] Definir schema `<Entity>Response` en `api/schemas.py`
- [ ] Verificar que todos los campos siguen las convenciones Pydantic v2
- [ ] Documentar endpoint en `router.py` con `summary`, `description`, `operation_id`, `tags`, `responses`

## Fase 3 · Dominio
_Archivo: `domain/entities/<entity>.py`_
- [ ] Implementar/modificar entidad con validaciones de dominio
- [ ] Validar transiciones de estado contra la máquina de estados
- [ ] Lanzar `BusinessRuleViolation` con referencia BR-XXX para cada regla violada
- [ ] Sin dependencias de FastAPI ni SQLAlchemy en el dominio

## Fase 4 · Repositorio
_Archivo: `infrastructure/repositories/<entity>_repo_impl.py`_
- [ ] Implementar métodos del repositorio con `AsyncSession`
- [ ] Filtrar siempre por `organization_id` (multi-tenant)
- [ ] Filtrar `deleted_at IS NULL` en todas las queries de lectura
- [ ] `SELECT` con columnas explícitas — sin `SELECT *`

## Fase 5 · Caso de Uso
_Archivo: `application/commands/<action>_command.py`_
- [ ] Implementar caso de uso con `UnitOfWork`
- [ ] Sin lógica de negocio en el router — todo aquí o en dominio
- [ ] Validar RBAC antes de cualquier query
- [ ] Extraer `organization_id` del token — nunca del body

## Fase 6 · Router
_Archivo: `api/router.py`_
- [ ] Agregar endpoint con `Depends(get_current_user)`
- [ ] Delegar toda lógica al caso de uso
- [ ] Retornar status codes correctos (201 para creación, 200 para acciones)

## Fase 7 · Tests
_Archivos en `tests/unit/` e `tests/integration/`_
<un checkbox por test case del ticket>
- [ ] Tests unitarios del caso de uso (mocks de repositorios)
- [ ] Tests de integración del repositorio (testcontainers)
- [ ] Tests de endpoint con `httpx.AsyncClient`
- [ ] Verificar que endpoint sin auth retorna `401`
- [ ] Verificar que rol incorrecto retorna `403`

## Fase 8 · Verificación
- [ ] `docker compose exec api python -m pytest modules/<module>/tests/ -v`
- [ ] Linting: `ruff check apps/backend/src/modules/<module>/`
- [ ] Type check: `mypy apps/backend/src/modules/<module>/`
- [ ] Sin errores en `docker compose up`

## Fase 9 · Entrega
- [ ] Commit: `git commit -m "feat(<module>): <descripción>"`
- [ ] Push: `git push origin <branch-name>`
- [ ] Abrir PR — NO hacer merge sin validación del usuario
```

---

## Template Frontend

```markdown
---
ticket: <ruta/frontend/ticket.md>
layer: frontend
depends-on: <ruta/backend/ticket.md>
progress: 0 / <total> tasks completed
---

# Plan de Desarrollo — [FE] <Feature Name>

> Marca cada tarea con `- [x]` al completarla. Actualiza `progress` en el frontmatter.

## Fase 1 · Prerequisitos
- [ ] Endpoint backend disponible y respondiendo correctamente
- [ ] `git pull origin main` y crear branch: `git checkout -b <branch-name>`
- [ ] Leer `.amazonq/rules/frontend-standards.md`

## Fase 2 · Schema de Validación (Zod)
_Archivo: `features/<module>/schemas/<feature>-schema.ts`_
- [ ] Definir schema Zod alineado con el contrato API del ticket
- [ ] Tipos correctos (UUID como string, fechas como string ISO)
- [ ] Mensajes de error descriptivos en español

## Fase 3 · Servicio API
_Archivo: `services/<feature>-service.ts`_
- [ ] Función async tipada que consume el endpoint
- [ ] Manejo de errores con tipos (no `any`)
- [ ] URL relativa — nunca `localhost` hardcodeado

## Fase 4 · Hook TanStack Query
_Archivo: `features/<module>/hooks/use<Feature>.ts`_
- [ ] `useQuery` para lectura con `queryKey` descriptivo
- [ ] `useMutation` para escritura con `onSuccess` e invalidación de cache
- [ ] Tipos TypeScript explícitos en request y response

## Fase 5 · Componentes
_Archivos en `features/<module>/components/`_
- [ ] Componente con `function` keyword y named export
- [ ] Props tipadas con interface TypeScript
- [ ] Estados loading/error/success visualmente distintos
- [ ] HTML semántico + aria-labels

## Fase 6 · Página
_Archivo: `app/<role>/<route>/page.tsx`_
- [ ] Wrapping en `Suspense` con fallback
- [ ] `error.tsx` en la misma ruta para Error Boundary
- [ ] `use client` solo si es necesario (Web APIs)

## Fase 7 · Tests
_Archivos en `tests/`_
<un checkbox por test case del ticket>
- [ ] Test de renderizado correcto
- [ ] Test de estado de carga
- [ ] Test de estado de error

## Fase 8 · Verificación
- [ ] `npm run build` — sin errores TypeScript
- [ ] `npm run lint` — sin errores ESLint
- [ ] Revisar en navegador: loading, error y success states

## Fase 9 · Entrega
- [ ] Commit: `git commit -m "feat(<feature>): <descripción>"`
- [ ] Push: `git push origin <branch-name>`
- [ ] Abrir PR — NO hacer merge sin validación del usuario
```

---

## Paso 3 — Confirmar

```
Planes creados para: <story-id>
  <path/database/plan.md>  -- [DB] <Feature Name>  (<N> tasks)
  <path/backend/plan.md>   -- [BE] <Feature Name>  (<N> tasks)
  <path/frontend/plan.md>  -- [FE] <Feature Name>  (<N> tasks)

Siguiente paso: /develop-plan <story-id> database
```
