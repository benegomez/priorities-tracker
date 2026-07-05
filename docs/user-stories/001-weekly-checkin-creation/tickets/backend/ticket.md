---
status: done
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

FastAPI router, Pydantic v2 schemas, casos de uso, entidades de dominio, repositorios SQLAlchemy async. Sin schema SQL, sin UI.

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

### GET /api/v1/checkins/current
**Tags:** `checkin` | **operation_id:** `get_current_checkin` | **Auth:** Bearer JWT

```
Query params: (ninguno — semana actual se calcula en el servidor)

Response 200:
{
  "id": "uuid",
  "employee_id": "uuid",
  "organization_id": "uuid",
  "week_start": "2025-01-06",
  "status": "draft",
  "submitted_at": null,
  "priorities_count": 2,
  "created_at": "2025-01-06T08:00:00Z",
  "updated_at": "2025-01-06T08:00:00Z"
}

Response 404: No check-in for current week

Errors:
  401 — token inválido o expirado
```

> Retorna el check-in de la semana actual del empleado autenticado. Si no existe, retorna 404.

---

### POST /api/v1/checkins
**Tags:** `checkin` | **operation_id:** `create_checkin` | **Auth:** Bearer JWT

```
Request body:
{
  "week_start": "2025-01-06"          // date, debe ser lunes ISO
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

---

### POST /api/v1/priorities
**Tags:** `priorities` | **operation_id:** `create_priority` | **Auth:** Bearer JWT

```
Request body:
{
  "checkin_id": "uuid",
  "phase_id":   "uuid",
  "title":      "string (max 255)",
  "description": "string | null",
  "priority_level": "low | medium | high"
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
  401, 403 (cross-tenant o checkin ajeno),
  404 (checkin_id o phase_id no encontrados),
  409 (checkin ya fue submitted — no acepta nuevas prioridades)
```

---

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
  "description": "string | null",
  "status": "pending",
  "created_at": "...",
  "updated_at": "..."
}

Errors:
  401, 403 (priority no pertenece al empleado),
  404 (priority_id no encontrado)
```

---

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
  401, 403 (checkin ajeno),
  404 (checkin no encontrado),
  409 (checkin vacío sin prioridades — debe tener al menos 1,
       o checkin ya submitted)
```

---

## Archivos a Crear / Modificar

```
apps/backend/src/modules/checkin/
  __init__.py
  api/
    __init__.py
    router.py           - CREATE (GET current, POST create, POST submit)
    schemas.py          - CREATE (CheckInCreate, CheckInResponse, CheckInSubmitResponse)
    dependencies.py     - CREATE (get_checkin_repository, get_checkin_service)
  application/
    __init__.py
    commands/
      __init__.py
      create_checkin.py         - CREATE
      submit_checkin.py         - CREATE
    queries/
      __init__.py
      get_current_checkin.py    - CREATE
  domain/
    __init__.py
    entities/
      __init__.py
      checkin.py                - CREATE (WeeklyCheckIn entity)
    repositories/
      __init__.py
      checkin_repository.py     - CREATE (interface ABC)
  infrastructure/
    __init__.py
    repositories/
      __init__.py
      checkin_repository_impl.py  - CREATE (SQLAlchemy async)

apps/backend/src/modules/priorities/
  __init__.py
  api/
    __init__.py
    router.py           - CREATE (POST priority, POST task)
    schemas.py          - CREATE (PriorityCreate, PriorityResponse, TaskCreate, TaskResponse)
    dependencies.py     - CREATE
  application/
    __init__.py
    commands/
      __init__.py
      create_priority.py        - CREATE
      create_task.py            - CREATE
  domain/
    __init__.py
    entities/
      __init__.py
      priority.py               - CREATE
      task.py                   - CREATE
    repositories/
      __init__.py
      priority_repository.py    - CREATE (interface ABC)
      task_repository.py        - CREATE (interface ABC)
  infrastructure/
    __init__.py
    repositories/
      __init__.py
      priority_repository_impl.py - CREATE
      task_repository_impl.py     - CREATE

apps/backend/src/main.py          - MODIFY (registrar routers checkin + priorities)
```

---

## Casos de Uso a Implementar

| Use Case | Responsabilidad |
|---|---|
| `GetCurrentCheckInQuery` | Busca check-in del empleado para la semana actual; retorna `None` si no existe |
| `CreateCheckInCommand` | Valida BR-001, valida `week_start` es lunes, extrae `organization_id` del token, persiste en `draft` |
| `CreatePriorityCommand` | Valida BR-003/BR-004 (fase→proyecto activo), BR-013/BR-016 (ownership + tenant), verifica checkin en `draft` |
| `CreateTaskCommand` | Valida BR-005, BR-013 (priority pertenece al empleado), persiste task en `pending` |
| `SubmitCheckInCommand` | Valida ≥1 prioridad, transiciona checkin a `submitted`, transiciona prioridades a `planned`, registra `submitted_at` |

---

## Validaciones de Dominio (en entidades/casos de uso, NO en router)

- `week_start` debe ser un lunes (`weekday() == 0`) → `ValidationException`
- `organization_id` siempre del JWT — nunca del body
- Un checkin en `submitted` no acepta nuevas prioridades → `BusinessRuleViolation`
- `title` no puede ser vacío ni solo espacios → `ValidationException`
- `priority_level` debe ser `low | medium | high` → validación Pydantic
- Phase debe pertenecer a un proyecto con `status = 'active'` → `BusinessRuleViolation`
- Phase debe pertenecer a la misma `organization_id` del token → `AuthorizationException`

---

## Tests Requeridos

> Nivel de riesgo: Critical | Complejidad: L → cobertura mínima >95%

### Unit Tests — `modules/checkin/tests/unit/`
Herramienta: `pytest` con mocks

- [x] `test_create_checkin_returns_draft_status`
- [x] `test_create_checkin_raises_br001_when_duplicate_week`
- [x] `test_create_checkin_validates_week_start_is_monday`
- [x] `test_create_checkin_extracts_org_id_from_token`
- [x] `test_submit_checkin_transitions_to_submitted`
- [x] `test_submit_checkin_raises_409_when_no_priorities`
- [x] `test_submit_checkin_raises_409_when_already_submitted`
- [x] `test_submit_checkin_transitions_priorities_to_planned`

### Unit Tests — `modules/priorities/tests/unit/`

- [x] `test_create_priority_returns_draft_status`
- [x] `test_create_priority_raises_when_checkin_not_draft`
- [x] `test_create_priority_raises_br003_when_no_phase`
- [x] `test_create_priority_raises_br004_when_project_inactive`
- [x] `test_create_priority_raises_br013_when_wrong_employee`
- [x] `test_create_priority_raises_br016_when_cross_tenant`
- [x] `test_create_task_returns_pending_status`
- [x] `test_create_task_raises_br005_when_no_priority`
- [ ] `test_create_task_raises_when_priority_not_owned` (deferred)

### Integration Tests — `modules/checkin/tests/integration/`
Herramienta: `pytest` + `httpx.AsyncClient`

- [x] `test_endpoint_post_checkin_returns_201`
- [x] `test_endpoint_post_checkin_returns_409_duplicate`
- [x] `test_endpoint_post_checkin_returns_400_non_monday`
- [x] `test_endpoint_get_current_returns_200`
- [x] `test_endpoint_get_current_returns_404_no_checkin`
- [x] `test_endpoint_submit_returns_200`
- [x] `test_endpoint_submit_returns_409_no_priorities`
- [x] `test_endpoint_post_priority_returns_201`

### Integration Tests — `modules/priorities/tests/integration/`

- [ ] (covered via checkin integration tests above)

### Contract Tests — `modules/checkin/tests/contract/`
Herramienta: `schemathesis`

- [ ] `test_checkin_endpoints_match_openapi_contract` (deferred)
- [ ] `test_priority_endpoints_match_openapi_contract` (deferred)

### Security Tests

- [ ] `test_cross_tenant_phase_returns_403` (deferred)
- [ ] `test_other_employee_checkin_returns_403` (deferred)
- [ ] `test_all_endpoints_return_401_without_token` (deferred)
- [ ] `bandit` sin findings HIGH/CRITICAL en módulos `checkin` y `priorities` (deferred)

---

## Git Branch

`feature/001-weekly-checkin-creation`
