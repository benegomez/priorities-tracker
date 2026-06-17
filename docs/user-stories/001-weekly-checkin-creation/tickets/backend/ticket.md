---
status: todo
type: backend
story: docs/user-stories/001-weekly-checkin-creation/UserStory.md
depends-on: tickets/database/ticket.md
risk_level: Critical
complexity: L
---

# [BE] US-001 — Weekly Check-In Creation

## Objetivo

Implementar la lógica de negocio y los endpoints REST que permiten a un colaborador crear un Check-In semanal, agregar prioridades y tareas, y enviarlo. Incluye validación de todas las Business Rules del dominio y aislamiento multi-tenant.

## Scope

FastAPI router, Pydantic v2 schemas, casos de uso, entidades de dominio, repositorios SQLAlchemy. Sin schema SQL, sin UI.

## Dependencia

Ticket database mergeado y migración aplicada antes de comenzar.

---

## FR de Referencia

- FR-014 — Check-In Creation
- FR-015 — Priority Creation
- FR-016 — Task Creation

## Business Rules Aplicables

- **BR-001** — Un empleado solo puede tener un Check-In por semana → `409 Conflict`
- **BR-003** — Una prioridad debe pertenecer a una fase
- **BR-004** — Una fase debe pertenecer a un proyecto activo
- **BR-005** — Una tarea debe pertenecer a una prioridad
- **BR-013** — Un empleado solo ve sus propias prioridades → `403 Forbidden`
- **BR-016** — Ningún usuario accede a datos de otra organización → `403 Forbidden`
- **BR-017** — Todos los agregados tienen `organization_id`

---

## Contrato OpenAPI (definir ANTES de implementar — ADR-009)

### POST /api/v1/checkins
**Tags:** `checkin` | **operation_id:** `create_checkin` | **Auth:** Bearer JWT

```
Request body:
{
  "week_start": "2025-01-06"          // date, lunes de la semana
}

Response 201:
{
  "id": "uuid",
  "employee_id": "uuid",
  "organization_id": "uuid",
  "week_start": "2025-01-06",
  "status": "draft",
  "created_at": "2025-01-06T08:00:00Z",
  "updated_at": "2025-01-06T08:00:00Z"
}

Errors:
  401 — token inválido o expirado
  403 — rol no permitido
  409 — BR-001: ya existe check-in para esta semana
```

### POST /api/v1/priorities
**Tags:** `priorities` | **operation_id:** `create_priority` | **Auth:** Bearer JWT

```
Request body:
{
  "checkin_id": "uuid",
  "phase_id":   "uuid",
  "title":      "string (max 255)",
  "description": "string | null",
  "priority_level": "low | medium | high | critical"
}

Response 201:
{
  "id": "uuid",
  "checkin_id": "uuid",
  "phase_id": "uuid",
  "owner_id": "uuid",
  "organization_id": "uuid",
  "title": "string",
  "description": "string | null",
  "priority_level": "high",
  "status": "draft",
  "week_start": "2025-01-06",
  "created_at": "...",
  "updated_at": "..."
}

Errors:
  401, 403, 404 (checkin_id o phase_id no encontrados),
  409 (checkin ya fue submitted)
```

### POST /api/v1/priorities/{id}/tasks
**Tags:** `priorities` | **operation_id:** `create_task` | **Auth:** Bearer JWT

```
Request body:
{
  "title": "string (max 255)",
  "description": "string | null"
}

Response 201:
{
  "id": "uuid",
  "priority_id": "uuid",
  "organization_id": "uuid",
  "title": "string",
  "status": "pending",
  "created_at": "...",
  "updated_at": "..."
}

Errors:
  401, 403, 404 (priority_id no encontrado o no pertenece al empleado)
```

### POST /api/v1/checkins/{id}/submit
**Tags:** `checkin` | **operation_id:** `submit_checkin` | **Auth:** Bearer JWT

```
Request body: {} (vacío)

Response 200:
{
  "id": "uuid",
  "status": "submitted",
  "submitted_at": "2025-01-06T08:30:00Z"
}

Errors:
  401, 403,
  404 (checkin no encontrado),
  409 (checkin vacío sin prioridades — debe tener al menos 1)
```

---

## Archivos a Crear / Modificar

```
apps/backend/src/modules/checkin/
  api/
    router.py           - MODIFY (POST /checkins, POST /checkins/{id}/submit)
    schemas.py          - CREATE (CheckInCreate, CheckInResponse, CheckInSubmitResponse)
    dependencies.py     - MODIFY (get_checkin_repository)
  application/
    commands/
      create_checkin_command.py   - CREATE
      submit_checkin_command.py   - CREATE
  domain/
    entities/
      weekly_checkin.py           - CREATE
    repositories/
      checkin_repository.py       - CREATE (interface)
  infrastructure/
    repositories/
      checkin_repository_impl.py  - CREATE (SQLAlchemy)

apps/backend/src/modules/priorities/
  api/
    router.py           - MODIFY (POST /priorities, POST /priorities/{id}/tasks)
    schemas.py          - CREATE (PriorityCreate, PriorityResponse, TaskCreate, TaskResponse)
    dependencies.py     - MODIFY
  application/
    commands/
      create_priority_command.py  - CREATE
      create_task_command.py      - CREATE
  domain/
    entities/
      priority.py                 - CREATE
      task.py                     - CREATE
    repositories/
      priority_repository.py      - CREATE (interface)
      task_repository.py          - CREATE (interface)
  infrastructure/
    repositories/
      priority_repository_impl.py - CREATE
      task_repository_impl.py     - CREATE
```

---

## Casos de Uso a Implementar

- **CreateCheckInUseCase** — Valida BR-001, extrae `organization_id` del token, persiste CheckIn en `draft`
- **CreatePriorityUseCase** — Valida BR-003, BR-004, BR-013, BR-016, verifica que el checkin esté en `draft`
- **CreateTaskUseCase** — Valida BR-005, BR-013, verifica que la prioridad exista y pertenezca al empleado
- **SubmitCheckInUseCase** — Valida que el checkin tenga al menos 1 prioridad, transiciona a `submitted`, transiciona prioridades a `planned`, registra `submitted_at`

---

## Validaciones de Dominio (van en entidades/casos de uso, NO en router)

- `week_start` debe ser un lunes (`weekday() == 0`)
- `organization_id` siempre del JWT — nunca del body
- Un checkin en `submitted` no puede recibir nuevas prioridades
- Una prioridad en `planned` no puede recibir nuevas tareas vía este flujo
- `title` no puede ser vacío ni solo espacios
- `priority_level` debe ser uno de los valores del enum `PriorityLevel`

---

## Tests Requeridos

> Nivel de riesgo: Critical | Complejidad: L → cobertura mínima >95%

### Unit Tests — `tests/unit/` ✅
Herramienta: `pytest` con mocks

- [ ] `test_create_checkin_returns_draft_status`
- [ ] `test_create_checkin_raises_br001_when_duplicate_week`
- [ ] `test_create_checkin_extracts_org_id_from_token_not_body`
- [ ] `test_create_priority_raises_br003_when_no_phase`
- [ ] `test_create_priority_raises_br004_when_inactive_project`
- [ ] `test_create_priority_raises_br013_when_wrong_employee`
- [ ] `test_create_priority_raises_br016_when_cross_tenant_phase`
- [ ] `test_create_priority_fails_when_checkin_already_submitted`
- [ ] `test_create_task_raises_br005_when_no_priority`
- [ ] `test_submit_checkin_transitions_to_submitted`
- [ ] `test_submit_checkin_raises_409_when_no_priorities`
- [ ] `test_submit_checkin_transitions_priorities_to_planned`
- [ ] `test_week_start_must_be_monday`

### Integration Tests — `tests/integration/` ✅
Herramienta: `pytest` + `testcontainers`

- [ ] `test_checkin_repository_save_and_retrieve_by_id`
- [ ] `test_checkin_repository_filters_by_organization_id`
- [ ] `test_checkin_repository_excludes_soft_deleted`
- [ ] `test_checkin_unique_constraint_employee_week` (BR-001 a nivel DB)
- [ ] `test_priority_repository_save_and_retrieve`
- [ ] `test_priority_repository_filters_by_organization_id`
- [ ] `test_task_repository_save_and_retrieve`
- [ ] `test_uow_commit_persists_checkin_with_priorities`
- [ ] `test_uow_rollback_reverts_all_changes`
- [ ] `test_endpoint_post_checkin_returns_201`
- [ ] `test_endpoint_post_checkin_returns_409_duplicate_week`
- [ ] `test_endpoint_post_checkin_returns_401_without_token`
- [ ] `test_endpoint_post_checkin_returns_403_wrong_role`
- [ ] `test_endpoint_submit_checkin_returns_200`
- [ ] `test_endpoint_submit_checkin_returns_409_empty_checkin`

### Contract Tests — `tests/contract/` ✅
Herramienta: `schemathesis`

- [ ] `test_checkin_openapi_schema_is_valid`
- [ ] `test_post_checkin_response_matches_contract`
- [ ] `test_post_priority_response_matches_contract`
- [ ] `test_submit_checkin_response_matches_contract`

### E2E Tests — `tests/e2e/` ✅
Herramienta: `Playwright`

- [ ] `test_checkin_flow_complete_happy_path` (crear → agregar prioridades → agregar tareas → submit)
- [ ] `test_checkin_flow_unauthenticated_redirects_to_login`

### Security Tests ✅

- [ ] `bandit` sin findings HIGH/CRITICAL en módulos `checkin` y `priorities`
- [ ] `pip-audit` sin vulnerabilidades conocidas
- [ ] `test_cross_tenant_phase_returns_403`
- [ ] `test_other_employee_checkin_returns_403`

---

## Git Branch

`feature/001-weekly-checkin-creation-backend`
