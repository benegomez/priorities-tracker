---
story: 003-weekly-checkout
status: done
branch: feature/003-weekly-checkout
risk_level: Critical
complexity: L
created: 2026-07-05
---

# Plan de Implementación — US-003: Weekly Check-Out

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Database | Migración Alembic con tablas `check_outs` + `crs_scores` + ALTER priorities/tasks |
| 2 | Backend | 5 endpoints + 5 use cases + módulo `checkout` |
| 3 | Frontend | Flujo completo de Check-Out en UI |

**Branch único:** `feature/003-weekly-checkout`
**Commits:** secuenciales por fase (`feat(db):`, `feat(checkout):`, `feat(fe):`)

---

## Fase 1 — Database ✅

### 1.1 Migración Alembic

- [x] Crear archivo `apps/backend/src/shared/database/migrations/202507051200_create_check_outs_crs_scores.py`
- [x] Implementar `upgrade()`:
  - [x] Tabla `check_outs` con FK a `organizations`, `users`, `check_ins`
  - [x] CHECK constraint para `status` enum (`draft`, `submitted`, `closed`)
  - [x] Partial unique index `uq_check_outs_employee_week` (BR-002)
  - [x] Tabla `crs_scores` con FK a `organizations`, `users`, `check_outs`
  - [x] CHECK constraints para `trend` y `risk_level` enums
  - [x] Partial unique index `uq_crs_scores_employee_week`
  - [x] ALTER `priorities`: agregar columna `completed_in_checkout UUID NULL REFERENCES check_outs(id)`
  - [x] ALTER `tasks`: agregar columna `completed_in_checkout UUID NULL REFERENCES check_outs(id)`
- [x] Implementar todos los índices:
  - [x] `idx_check_outs_organization_id`, `idx_check_outs_employee_id`, `idx_check_outs_checkin_id`, `idx_check_outs_week_start`
  - [x] `idx_crs_scores_organization_id`, `idx_crs_scores_employee_id`, `idx_crs_scores_checkout_id`, `idx_crs_scores_week_start`
- [x] Implementar `downgrade()` en orden inverso:
  - [x] ALTER `tasks` DROP COLUMN `completed_in_checkout`
  - [x] ALTER `priorities` DROP COLUMN `completed_in_checkout`
  - [x] DROP TABLE `crs_scores`
  - [x] DROP TABLE `check_outs`
- [x] Columnas de auditoría en ambas tablas (`created_at`, `updated_at`, `deleted_at`, `deleted_by`)

### 1.2 Verificación

- [x] `upgrade()` ejecuta sin errores
- [x] `downgrade()` revierte completamente
- [x] Re-ejecutar `upgrade()` después de `downgrade()` funciona
- [x] Partial unique index: insertar 2 check-outs misma semana/empleado → falla (BR-002)
- [x] Verificar FK de `checkin_id` funciona correctamente
- [x] Verificar columnas `completed_in_checkout` en priorities y tasks

### 1.3 Commit

```
feat(db): create check_outs, crs_scores tables and add completed_in_checkout columns
```

---

## Fase 2 — Backend ✅

### 2.1 Módulo `checkout` — Domain

- [x] `modules/checkout/__init__.py` + todos los `__init__.py` de subcarpetas
- [x] `modules/checkout/domain/entities/checkout.py` — entidad `WeeklyCheckOut`:
  - [x] Campos: id, organization_id, employee_id, checkin_id, week_start, status, submitted_at, notes, lessons_learned
  - [x] State machine: `draft` → `submitted`
  - [x] Método `submit()` que valida transición
  - [x] Validación: no puede submit si ya submitted
- [x] `modules/checkout/domain/repositories/checkout_repository.py` — interfaz ABC:
  - [x] `save()`, `get_by_id()`, `get_by_employee_and_week()`, `update()`

### 2.2 Módulo `checkout` — Infrastructure

- [x] `modules/checkout/infrastructure/repositories/checkout_repository_impl.py`:
  - [x] Implementar todos los métodos
  - [x] Filtro `organization_id` + `deleted_at IS NULL`
  - [x] Query para cargar prioridades y tareas del checkin asociado

### 2.3 Módulo `checkout` — Application

- [x] `modules/checkout/application/queries/get_current_checkout.py`:
  - [x] Calcular semana actual (dev: hoy, prod: lunes)
  - [x] Buscar checkout del empleado para esa semana

- [x] `modules/checkout/application/commands/create_checkout.py`:
  - [x] Validar BR-002 (duplicado por semana)
  - [x] Validar checkin existe y está en `submitted`
  - [x] Validar ownership (BR-013) y tenant (BR-016)
  - [x] Crear checkout en `draft`

- [x] `modules/checkout/application/commands/mark_priority.py`:
  - [x] Validar checkout existe, pertenece al empleado, está en `draft`
  - [x] Validar priority pertenece al checkin del checkout
  - [x] Setear `completed_in_checkout = checkout_id` (o NULL si desmarca)

- [x] `modules/checkout/application/commands/mark_task.py`:
  - [x] Validar checkout existe, pertenece al empleado, está en `draft`
  - [x] Validar task pertenece a una priority del checkin
  - [x] Setear `completed_in_checkout = checkout_id` (o NULL si desmarca)

- [x] `modules/checkout/application/commands/submit_checkout.py`:
  - [x] Validar checkout en `draft`, ownership
  - [x] En transacción atómica:
    - [x] Prioridades con `completed_in_checkout = checkout_id` → status `completed`
    - [x] Prioridades sin marcar → status `carried_over`
    - [x] Tareas con `completed_in_checkout = checkout_id` → status `completed`
    - [x] Tareas sin marcar → status `cancelled`
    - [x] checkout.status = `submitted`, submitted_at = now()
    - [x] Guardar notes + lessons_learned
  - [x] Después del commit (best-effort):
    - [x] Intentar calcular CRS (log info, TODO cuando módulo exista)
    - [x] Si falla → log warning, no revertir
  - [x] Retornar summary (totals + completed + carried)

### 2.4 Módulo `checkout` — API

- [x] `modules/checkout/api/schemas.py`:
  - [x] `CheckOutCreate`, `CheckOutPriorityItem`, `CheckOutResponse`
  - [x] `MarkCompletedRequest`, `MarkPriorityResponse`, `MarkTaskResponse`
  - [x] `CheckOutSubmitRequest`, `CheckOutSubmitResponse`, `CheckOutSummaryResponse`
  - [x] `tasks: list[CheckOutTaskItem]` en `CheckOutPriorityItem`

- [x] `modules/checkout/api/router.py`:
  - [x] `GET /checkouts/current` → `get_current_checkout`
  - [x] `POST /checkouts/` → `create_checkout` (201)
  - [x] `PATCH /checkouts/{id}/priorities/{priority_id}` → `mark_priority`
  - [x] `PATCH /checkouts/{id}/tasks/{task_id}` → `mark_task`
  - [x] `POST /checkouts/{id}/submit` → `submit_checkout`
  - [x] Auth: `Depends(get_current_user)` en todos
  - [x] Exception handlers: domain exceptions → HTTP status
  - [x] `_load_priorities_for_checkout` carga tareas anidadas por prioridad

### 2.5 Registrar router en main.py

- [x] Importar y registrar `checkout_router` con prefix `/api/v1`

### 2.6 Tests — Unit (7 passing)

- [x] `test_create_checkout_returns_draft`
- [x] `test_create_checkout_raises_br002_when_duplicate`
- [x] `test_create_checkout_raises_when_checkin_not_submitted`
- [x] `test_create_checkout_raises_403_when_wrong_employee`
- [x] `test_submit_transitions_to_submitted`
- [x] `test_submit_raises_409_when_already_submitted`
- [x] `test_submit_raises_403_when_wrong_employee`

### 2.7 Verificación Backend

- [x] Unit tests pasan (7/7)
- [x] Endpoints responden correctamente via curl
- [x] Submit actualiza estados de prioridades correctamente
- [x] Summary retorna conteos correctos
- [x] BR-002 enforced (409 on duplicate)

```
feat(checkout): add domain entity, repository interface, and use cases
feat(checkout): add API router, schemas, and endpoint registration
test(checkout): add unit, integration, and security tests
```

---

## Fase 3 — Frontend ✅

### 3.1 Services (API client)

- [x] `features/checkouts/services/checkout-service.ts`:
  - [x] `getCurrentCheckOut()` → GET `/api/v1/checkouts/current`
  - [x] `createCheckOut(checkinId)` → POST `/api/v1/checkouts/`
  - [x] `markPriorityCompleted(checkoutId, priorityId, completed)` → PATCH
  - [x] `markTaskCompleted(checkoutId, taskId, completed)` → PATCH
  - [x] `submitCheckOut(id, data)` → POST `/api/v1/checkouts/{id}/submit`

### 3.2 Schemas (Zod)

- [x] `features/checkouts/schemas/checkout-schema.ts`:
  - [x] `createCheckOutSchema` — `{ checkin_id: uuid }`
  - [x] `submitCheckOutSchema` — `{ notes?: string, lessons_learned?: string }`

### 3.3 Hooks (TanStack Query)

- [x] `useCurrentCheckOut` — useQuery `["checkouts", "current"]`
- [x] `useCreateCheckOut` — useMutation + invalidate
- [x] `useMarkPriority` — useMutation + invalidate
- [x] `useMarkTask` — useMutation + invalidate
- [x] `useSubmitCheckOut` — useMutation + invalidate + redirect

### 3.4 Componentes

- [x] `CheckOutForm.tsx` — botón crear (verifica checkin submitted)
- [x] `CheckOutPriorityCard.tsx` — card con checkbox prioridad + tareas anidadas
- [x] `CheckOutTaskItem.tsx` — checkbox inline para tarea (PATCH /tasks/{id})
- [x] `CheckOutNotes.tsx` — textareas para notas y lessons_learned
- [x] `CheckOutSummary.tsx` — card con stats post-submit
- [x] `SubmitCheckOutButton.tsx` — botón con confirmación modal

### 3.5 Página principal

- [x] `app/(authenticated)/employee/checkout/page.tsx`:
  - [x] Condicional: no existe → CheckOutForm, draft → vista cierre, submitted → read-only summary
  - [x] Summary calcula tasks_total y tasks_completed desde priorities[].tasks[]
- [x] `app/(authenticated)/employee/checkout/error.tsx` — error boundary

### 3.6 Navegación

- [x] Agregar "Check-Out" al menú employee en `config/navigation.ts` (grupo "Mi Semana")

### 3.7 Manejo de errores

- [x] Error display para 409 (duplicado, checkin not submitted, already submitted)
- [x] Error display para 403 (permisos)
- [x] Redirect a `/auth/login` via middleware para 401

### 3.8 Accesibilidad

- [x] Checkboxes con labels asociados (aria-label)
- [x] Estados completado/pendiente visualmente distintos (line-through)
- [x] AlertDialog navegable por teclado (aria-modal)
- [x] `aria-live` en estados error

### 3.9 Verificación Frontend

- [x] `npm run build` sin errores
- [x] `npm test` — 47/47 tests passing
- [x] Flujo completo ejecutable
- [x] Responsive: funciona en mobile y desktop

### 3.11 Commits

```
feat(checkout): add services, schemas, and hooks for check-out flow
feat(checkout): add UI components and checkout page
feat(checkout): add Check-Out to employee navigation
test(fe): add component tests for check-out flow
```

---

## Gate Final — PR

- [ ] Todos los tests pasan (unit + integration + security + component)
- [ ] Coverage backend >95% en módulo `checkout`
- [ ] `npm run build` sin errores
- [ ] Endpoints documentados en Swagger UI
- [ ] Flujo E2E verificado manualmente (crear → marcar → submit → summary)
- [ ] Submit actualiza correctamente estados de prioridades y tareas
- [ ] CRS best-effort no bloquea el submit
- [ ] PR creado con resumen, nivel de riesgo Critical, evidencia de tests

---

## Orden de Ejecución

```
/develop-plan db    → Fase 1 (migración)
/develop-plan be    → Fase 2 (backend completo)
/develop-plan fe    → Fase 3 (frontend completo)
/git-flow pr        → PR único con las 3 fases
```
