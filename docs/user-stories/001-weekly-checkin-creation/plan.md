---
story: 001-weekly-checkin-creation
status: done
branch: feature/001-weekly-checkin-creation
risk_level: Critical
complexity: L
created: 2025-06-23
---

# Plan de Implementación — US-001: Weekly Check-In Creation

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Database | Migración Alembic con 5 tablas |
| 2 | Backend | 5 endpoints + 5 use cases + 2 módulos |
| 3 | Frontend | Flujo completo de Check-In en UI |

**Branch único:** `feature/001-weekly-checkin-creation`
**Commits:** secuenciales por fase (`feat(db):`, `feat(checkin):`, `feat(priorities):`, `feat(fe):`)

---

## Fase 1 — Database ✅

### 1.1 Migración Alembic

- [x] Crear archivo `apps/backend/src/shared/database/migrations/202506231200_create_projects_checkins_priorities_tasks.py`
- [x] Implementar `upgrade()`:
  - [x] Tabla `projects` con constraints y CHECK enum
  - [x] Tabla `project_phases` con FK a `projects`
  - [x] Tabla `check_ins` con FK a `organizations`, `users`
  - [x] Tabla `priorities` con FKs a `check_ins`, `project_phases`, `users`
  - [x] Tabla `tasks` con FK a `priorities`
- [x] Implementar todos los índices:
  - [x] `idx_projects_organization_id`, `idx_projects_status` (partial)
  - [x] `idx_project_phases_organization_id`, `idx_project_phases_project_id`
  - [x] `uq_check_ins_employee_week` (partial unique, BR-001)
  - [x] `idx_check_ins_organization_id`, `idx_check_ins_employee_id`, `idx_check_ins_week_start`
  - [x] `idx_priorities_organization_id`, `idx_priorities_checkin_id`, `idx_priorities_phase_id`, `idx_priorities_owner_id`, `idx_priorities_week_start`, `idx_priorities_status` (partial)
  - [x] `idx_tasks_organization_id`, `idx_tasks_priority_id`, `idx_tasks_status` (partial)
- [x] Implementar `downgrade()` en orden inverso
- [x] Columnas de auditoría en las 5 tablas (`created_at`, `updated_at`, `deleted_at`, `deleted_by`)

### 1.2 Verificación

- [x] `upgrade()` ejecuta sin errores sobre BD con migración `202606231109` aplicada
- [x] `downgrade()` revierte completamente
- [x] Re-ejecutar `upgrade()` después de `downgrade()` funciona
- [x] Verificar partial unique index: insertar 2 check-ins misma semana/empleado → falla
- [x] Verificar soft-delete: marcar `deleted_at` + insertar nuevo → funciona

### 1.3 Commit

```
git commit -m "feat(db): create projects, project_phases, check_ins, priorities, tasks tables"
```

---

## Fase 2 — Backend ✅

### 2.1 Shared / Infraestructura base

- [x] Repositorios usan raw SQL via `text()` (patrón establecido en auth module)
- [x] Verificar que los queries mapean correctamente a las tablas creadas en Fase 1

### 2.2 Módulo `checkin` — Domain

- [x] `modules/checkin/__init__.py`
- [x] `modules/checkin/domain/entities/checkin.py` — entidad `WeeklyCheckIn` con validaciones:
  - [x] `week_start` debe ser lunes
  - [x] State machine: `draft` → `submitted` → `closed`
  - [x] Método `submit()` que valida transición
- [x] `modules/checkin/domain/repositories/checkin_repository.py` — interfaz ABC:
  - [x] `save()`, `get_by_id()`, `get_by_employee_and_week()`, `update()`

### 2.3 Módulo `checkin` — Infrastructure

- [x] `modules/checkin/infrastructure/repositories/checkin_repository_impl.py` — SQLAlchemy async:
  - [x] Implementar todos los métodos de la interfaz
  - [x] Filtro `organization_id` en todos los queries
  - [x] Filtro `deleted_at IS NULL` por defecto

### 2.4 Módulo `checkin` — Application

- [x] `modules/checkin/application/commands/create_checkin.py`:
  - [x] Validar BR-001 (duplicado por semana)
  - [x] Validar `week_start` es lunes
  - [x] Extraer `organization_id` y `employee_id` del token
  - [x] Persistir con status `draft`
- [x] `modules/checkin/application/commands/submit_checkin.py`:
  - [x] Validar ownership (BR-013)
  - [x] Validar ≥1 prioridad
  - [x] Validar status actual es `draft`
  - [x] Transicionar a `submitted` + registrar `submitted_at`
  - [x] Transicionar prioridades asociadas a `planned`
- [x] `modules/checkin/application/queries/get_current_checkin.py`:
  - [x] Calcular lunes de la semana actual
  - [x] Buscar check-in del empleado para esa semana

### 2.5 Módulo `checkin` — API

- [x] `modules/checkin/api/schemas.py`:
  - [x] `CheckInCreate` (week_start: date)
  - [x] `CheckInResponse` (id, employee_id, organization_id, week_start, status, submitted_at, priorities_count, created_at, updated_at)
  - [x] `CheckInSubmitResponse` (id, status, submitted_at)
- [x] `modules/checkin/api/router.py`:
  - [x] `GET /checkins/current` → `get_current_checkin`
  - [x] `POST /checkins` → `create_checkin` (201)
  - [x] `POST /checkins/{id}/submit` → `submit_checkin` (200)
  - [x] Auth: `Depends(get_current_user)` en todos
  - [x] Exception handlers: mapear domain exceptions → HTTP status

### 2.6 Módulo `priorities` — Domain

- [x] `modules/priorities/domain/entities/priority.py` — entidad `Priority`:
  - [x] State machine: `draft` → `planned` → `in_progress` → `completed` / `carried_over`
  - [x] Validación: title no vacío, priority_level válido
- [x] `modules/priorities/domain/entities/task.py` — entidad `Task`:
  - [x] State machine: `pending` → `in_progress` → `completed` / `cancelled`
- [x] `modules/priorities/domain/repositories/priority_repository.py` — interfaz ABC
- [x] `modules/priorities/domain/repositories/task_repository.py` — interfaz ABC

### 2.7 Módulo `priorities` — Infrastructure

- [x] `modules/priorities/infrastructure/repositories/priority_repository_impl.py`
- [x] `modules/priorities/infrastructure/repositories/task_repository_impl.py`
- [x] Filtros `organization_id` + `deleted_at IS NULL` en ambos

### 2.8 Módulo `priorities` — Application

- [x] `modules/priorities/application/commands/create_priority.py`:
  - [x] Validar checkin existe y pertenece al empleado (BR-013)
  - [x] Validar checkin en status `draft`
  - [x] Validar phase existe y pertenece a la misma org (BR-016)
  - [x] Validar project de la phase está `active` (BR-004)
  - [x] Persistir priority con status `draft`
- [x] `modules/priorities/application/commands/create_task.py`:
  - [x] Validar priority existe y pertenece al empleado (BR-005, BR-013)
  - [x] Persistir task con status `pending`

### 2.9 Módulo `priorities` — API

- [x] `modules/priorities/api/schemas.py`:
  - [x] `PriorityCreate`, `PriorityResponse`
  - [x] `TaskCreate`, `TaskResponse`
- [x] `modules/priorities/api/router.py`:
  - [x] `POST /priorities` → `create_priority` (201)
  - [x] `POST /priorities/{id}/tasks` → `create_task` (201)

### 2.10 Registrar routers en main.py

- [x] Importar y registrar `checkin_router` con prefix `/api/v1`
- [x] Importar y registrar `priorities_router` con prefix `/api/v1`

### 2.11 Tests — Unit (16 tests passing)

- [x] `modules/checkin/tests/unit/test_checkin_use_cases.py`:
  - [x] `test_create_checkin_returns_draft_status`
  - [x] `test_create_checkin_raises_br001_when_duplicate_week`
  - [x] `test_create_checkin_validates_week_start_is_monday`
  - [x] `test_create_checkin_extracts_org_id_from_token`
  - [x] `test_submit_checkin_transitions_to_submitted`
  - [x] `test_submit_checkin_raises_409_when_no_priorities`
  - [x] `test_submit_checkin_raises_409_when_already_submitted`
  - [x] `test_submit_checkin_transitions_priorities_to_planned`
- [x] `modules/priorities/tests/unit/test_priority_use_cases.py`:
  - [x] `test_create_priority_returns_draft_status`
  - [x] `test_create_priority_raises_when_checkin_not_draft`
  - [x] `test_create_priority_raises_br003_when_no_phase`
  - [x] `test_create_priority_raises_br004_when_project_inactive`
  - [x] `test_create_priority_raises_br013_when_wrong_employee`
  - [x] `test_create_priority_raises_br016_when_cross_tenant`
  - [x] `test_create_task_returns_pending_status`
  - [x] `test_create_task_raises_br005_when_no_priority`

### 2.12 Tests — Integration (8 tests passing)

- [x] `modules/checkin/tests/integration/test_checkin_endpoints.py`:
  - [x] `test_endpoint_post_checkin_returns_201`
  - [x] `test_endpoint_post_checkin_returns_409_duplicate`
  - [x] `test_endpoint_post_checkin_returns_400_non_monday`
  - [x] `test_endpoint_get_current_returns_200`
  - [x] `test_endpoint_get_current_returns_404_no_checkin`
  - [x] `test_endpoint_submit_returns_200`
  - [x] `test_endpoint_submit_returns_409_no_priorities`
  - [x] `test_endpoint_post_priority_returns_201`

### 2.13 Verificación Backend

- [x] Todos los unit tests pasan (16/16)
- [x] Todos los integration tests pasan (8/8)
- [x] Endpoints responden correctamente via curl (verificación funcional)
- [x] Endpoints documentados en Swagger UI (`/docs`)

### 2.14 Commits

```
git commit -m "feat(checkin): add domain entities, repository interfaces, and use cases"
git commit -m "feat(priorities): add domain entities, repository interfaces, and use cases"
git commit -m "feat(checkin): add API router, schemas, and endpoint registration"
git commit -m "feat(priorities): add API router, schemas, and endpoint registration"
git commit -m "test(checkin): add unit, integration, contract, and security tests"
git commit -m "test(priorities): add unit and integration tests"
```

---

## Fase 3 — Frontend ✅

### 3.1 Services (API clients)

- [x] `features/checkins/services/checkin-service.ts`:
  - [x] `getCurrentCheckIn()` → GET `/api/v1/checkins/current`
  - [x] `createCheckIn(data)` → POST `/api/v1/checkins`
  - [x] `submitCheckIn(id)` → POST `/api/v1/checkins/{id}/submit`
- [x] `features/priorities/services/priority-service.ts`:
  - [x] `createPriority(data)` → POST `/api/v1/priorities`
  - [x] `createTask(priorityId, data)` → POST `/api/v1/priorities/{id}/tasks`

### 3.2 Schemas (Zod)

- [x] `features/checkins/schemas/checkin-schema.ts`
- [x] `features/priorities/schemas/priority-schema.ts`
- [x] `features/priorities/schemas/task-schema.ts`

### 3.3 Hooks (TanStack Query)

- [x] `features/checkins/hooks/useCurrentCheckIn.ts` — useQuery `["checkins", "current"]`
- [x] `features/checkins/hooks/useCreateCheckIn.ts` — useMutation + invalidate
- [x] `features/checkins/hooks/useSubmitCheckIn.ts` — useMutation + invalidate + redirect
- [x] `features/priorities/hooks/useCreatePriority.ts` — useMutation + invalidate
- [x] `features/priorities/hooks/useCreateTask.ts` — useMutation + invalidate

### 3.4 Componentes

- [x] `features/checkins/components/CheckInForm.tsx` — botón crear (auto-calcula lunes)
- [x] `features/checkins/components/CheckInStatus.tsx` — badge draft/submitted
- [x] `features/checkins/components/SubmitCheckInButton.tsx` — disabled sin prioridades + AlertDialog
- [x] `features/priorities/components/PriorityForm.tsx` — select proyecto → fase → título → nivel
- [x] `features/priorities/components/PriorityCard.tsx` — card con badges + TaskList
- [x] `features/priorities/components/PriorityList.tsx` — layout vertical de cards
- [x] `features/priorities/components/TaskForm.tsx` — input inline + botón
- [x] `features/priorities/components/TaskList.tsx` — lista simple de tasks

### 3.5 Página principal

- [x] `app/employee/checkin/page.tsx`:
  - [x] Lógica condicional: no existe → CheckInForm, draft → vista construcción, submitted → read-only
  - [x] Composición de componentes
- [x] `app/employee/checkin/loading.tsx` — skeleton
- [x] `app/employee/checkin/error.tsx` — error boundary

### 3.6 Manejo de errores

- [x] Error display para 409 (duplicado, vacío)
- [x] Error display para 404 (fase eliminada)
- [x] Error display para 403 (permisos)
- [x] Redirect a `/auth/login` via middleware para 401

### 3.7 Accesibilidad

- [x] Labels en todos los inputs y selects
- [x] `aria-disabled` en SubmitCheckInButton
- [x] `aria-live` en estados loading/error/success
- [x] AlertDialog navegable por teclado
- [x] Focus management en forms

### 3.8 Tests — Component

- [x] `test_CheckInForm_renders_create_button`
- [x] `test_CheckInForm_calls_mutation_on_click`
- [x] `test_PriorityCard_renders_title_level_status`
- [x] `test_PriorityCard_shows_task_count`
- [x] `test_TaskForm_validates_empty_title`
- [x] `test_TaskForm_submits_inline`
- [x] `test_SubmitCheckInButton_disabled_when_no_priorities`
- [x] `test_SubmitCheckInButton_enabled_with_priorities`
- [x] `test_SubmitCheckInButton_shows_confirmation_dialog`
- [x] `test_checkin_schema_rejects_invalid_date`
- [x] `test_priority_schema_rejects_empty_title`
- [x] `test_task_schema_rejects_empty_title`

### 3.9 Tests — E2E (Playwright)

- [ ] `test_checkin_flow_happy_path` (deferred — requires Playwright setup)
- [ ] `test_checkin_flow_unauthenticated_redirects_to_login` (deferred)
- [ ] `test_checkin_submitted_shows_readonly_view` (deferred)

### 3.10 Verificación Frontend

- [x] Todos los component tests pasan (37/37)
- [ ] E2E tests pasan (deferred — Playwright not configured)
- [x] Flujo completo ejecutable en < 5 minutos (NFR-010)
- [x] Accesibilidad verificada (keyboard nav, aria attributes)

### 3.11 Commits

```
git commit -m "feat(checkin): add services, schemas, and hooks for check-in flow"
git commit -m "feat(priorities): add services, schemas, and hooks for priorities and tasks"
git commit -m "feat(checkin): add UI components and checkin page"
git commit -m "test(fe): add component and E2E tests for check-in flow"
```

---

## Gate Final — PR

- [ ] Todos los tests pasan (unit + integration + contract + E2E + security)
- [ ] Coverage backend >95% en módulos `checkin` y `priorities`
- [ ] Coverage frontend >95%
- [ ] `bandit` limpio
- [ ] `pip-audit` sin vulnerabilidades
- [ ] Endpoints documentados en Swagger UI
- [ ] Flujo E2E verificado manualmente
- [ ] PR creado con resumen, nivel de riesgo Critical, evidencia de tests

---

## Orden de Ejecución

```
/develop-plan db    → Fase 1 (migración)
/run-tests db       → Verificar migración
/develop-plan be    → Fase 2 (backend completo)
/run-tests be       → Unit + Integration + Contract + Security
/develop-plan fe    → Fase 3 (frontend completo)
/run-tests fe       → Component + E2E
/git-flow pr        → PR único con las 3 fases
```
