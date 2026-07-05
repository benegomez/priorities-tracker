---
status: done
type: backend
story: docs/user-stories/003-weekly-checkout/UserStory.md
depends-on: tickets/database/ticket.md
risk_level: Critical
complexity: L
---

# [BE] US-003 — Weekly Check-Out

## Objetivo

Implementar la lógica de negocio y los endpoints REST que permiten a un colaborador crear un Check-Out semanal, marcar prioridades y tareas como completadas, y enviar el cierre. El submit actualiza estados de prioridades/tareas y dispara el cálculo del CRS best-effort.

## Scope

FastAPI router, Pydantic v2 schemas, casos de uso, entidad de dominio, repositorios SQLAlchemy async. Sin schema SQL, sin UI.

## Dependencia

Ticket database mergeado y migración aplicada.

---

## FR de Referencia

- FR-022 — Check-Out Creation
- FR-023 — Completion Tracking
- FR-024 — Continuity Management

## Business Rules Aplicables

- **BR-002** — Un empleado solo puede tener un Check-Out por semana → `409`
- **BR-006** — Prioridades no completadas → `carried_over`
- **BR-007** — Tareas no completadas → `cancelled` (no se arrastran)
- **BR-008** — No puede cerrarse una prioridad inexistente
- **BR-009** — CRS se calcula automáticamente al submit
- **BR-012** — CRS se recalcula cuando existe Check-Out
- **BR-013** — Empleado solo accede a sus propios datos → `403`
- **BR-016** — Aislamiento multi-tenant → `403`
- **BR-017** — Todos los agregados tienen `organization_id`

---

## Contrato API

### GET /api/v1/checkouts/current
| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `get_current_checkout` |
| Response 200 | CheckOutResponse (con prioridades y **tareas anidadas**) |
| Response 404 | No checkout for current week |

### POST /api/v1/checkouts
| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `create_checkout` |
| Request | `{ "checkin_id": "uuid" }` |
| Response 201 | CheckOutResponse (draft, con prioridades y **tareas** cargadas) |
| Errors | 401, 403, 404 (checkin), 409 (BR-002, checkin not submitted) |

### PATCH /api/v1/checkouts/{id}/priorities/{priority_id}
| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `mark_priority_completed` |
| Request | `{ "completed": true }` |
| Response 200 | `{ "priority_id": "uuid", "completed": true }` |
| Errors | 401, 403, 404, 409 (checkout already submitted) |

### PATCH /api/v1/checkouts/{id}/tasks/{task_id}
| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `mark_task_completed` |
| Request | `{ "completed": true }` |
| Response 200 | `{ "task_id": "uuid", "completed": true }` |
| Errors | 401, 403, 404, 409 (checkout already submitted) |

### POST /api/v1/checkouts/{id}/submit
| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `submit_checkout` |
| Request | `{ "notes": "string|null", "lessons_learned": "string|null" }` |
| Response 200 | CheckOutSubmitResponse (con summary incluyendo tasks) |
| Errors | 401, 403, 404, 409 (already submitted) |

### Response Schema: CheckOutPriorityItem (con tareas anidadas)

```json
{
  "id": "uuid",
  "title": "string",
  "status": "planned",
  "priority_level": "high",
  "completed": false,
  "tasks": [
    { "id": "uuid", "title": "string", "status": "pending", "completed": false }
  ]
}
```

---

## Archivos a Crear / Modificar

```
apps/backend/src/modules/checkout/
  __init__.py
  api/
    __init__.py
    router.py               - 5 endpoints
    schemas.py              - CheckOutCreate, CheckOutResponse, MarkCompletedRequest,
                              CheckOutSubmitRequest, CheckOutSubmitResponse
  application/
    __init__.py
    commands/
      __init__.py
      create_checkout.py    - CreateCheckOutUseCase
      mark_priority.py      - MarkPriorityCompletedUseCase
      mark_task.py          - MarkTaskCompletedUseCase
      submit_checkout.py    - SubmitCheckOutUseCase
    queries/
      __init__.py
      get_current_checkout.py - GetCurrentCheckOutUseCase
  domain/
    __init__.py
    entities/
      __init__.py
      checkout.py           - WeeklyCheckOut dataclass
    repositories/
      __init__.py
      checkout_repository.py - ABC interface
  infrastructure/
    __init__.py
    repositories/
      __init__.py
      checkout_repository_impl.py - SQLAlchemy async

apps/backend/src/main.py    - MODIFY (registrar checkout_router)
```

---

## Casos de Uso

| Use Case | Responsabilidad |
|---|---|
| `GetCurrentCheckOutUseCase` | Busca checkout de la semana actual; retorna con prioridades/tareas |
| `CreateCheckOutUseCase` | Valida BR-002, valida checkin submitted, carga prioridades, crea draft |
| `MarkPriorityCompletedUseCase` | Valida ownership, checkout en draft, marca completed flag |
| `MarkTaskCompletedUseCase` | Valida ownership, checkout en draft, marca completed flag |
| `SubmitCheckOutUseCase` | Transiciona checkout a submitted, actualiza prioridades (completed/carried_over), actualiza tareas (completed/cancelled), dispara CRS best-effort |

---

## Lógica del Submit (transacción atómica)

```python
# Dentro de una transacción:
1. Validar checkout existe, pertenece al empleado, está en draft
2. Para cada prioridad del checkout:
   - Si marcada completed → priority.status = "completed"
   - Si NO marcada → priority.status = "carried_over"
3. Para cada tarea:
   - Si marcada completed → task.status = "completed"
   - Si NO marcada → task.status = "cancelled"
4. checkout.status = "submitted"
5. checkout.submitted_at = now()
6. Guardar notes y lessons_learned
7. COMMIT

# Después del commit (best-effort):
8. Calcular CRS (si módulo disponible)
   - Si falla → log warning, no revertir
```

---

## Modelo de datos para tracking de completados

Opción elegida: **Columna `completed_in_checkout` (boolean) en `priorities` y `tasks`**

Agregar a la migración:
```sql
ALTER TABLE priorities ADD COLUMN completed_in_checkout UUID NULL REFERENCES check_outs(id);
ALTER TABLE tasks ADD COLUMN completed_in_checkout UUID NULL REFERENCES check_outs(id);
```

Cuando el usuario marca una prioridad/tarea como completada en el checkout, se setea `completed_in_checkout = checkout_id`. Al submit, se usa este campo para determinar qué transicionar.

---

## Pendiente: Tareas en Check-Out — RESUELTO

Las tareas se muestran anidadas dentro de cada prioridad en la UI del Check-Out, con checkboxes individuales para marcar completadas.

### Backend ✅
- `tasks: list[CheckOutTaskItem]` agregado al schema `CheckOutPriorityItem`
- `_load_priorities_for_checkout` carga tareas de cada prioridad con su flag `completed_in_checkout`

### Frontend ✅
- Tipo `CheckOutTaskItem` agregado al service
- Componente `CheckOutTaskItem` con checkbox que llama a `PATCH /checkouts/{id}/tasks/{task_id}`
- `CheckOutPriorityCard` renderiza tareas anidadas
- Summary calcula `tasks_total` y `tasks_completed` desde `priorities[].tasks[]`

---

## Tests Requeridos

> Nivel de riesgo: Critical → cobertura >95%

### Unit Tests

- [ ] `test_create_checkout_returns_draft_with_priorities`
- [ ] `test_create_checkout_raises_br002_when_duplicate`
- [ ] `test_create_checkout_raises_when_checkin_not_submitted`
- [ ] `test_create_checkout_raises_403_when_wrong_employee`
- [ ] `test_mark_priority_completed_updates_flag`
- [ ] `test_mark_priority_raises_409_when_checkout_submitted`
- [ ] `test_mark_task_completed_updates_flag`
- [ ] `test_mark_task_raises_404_when_not_found`
- [ ] `test_submit_transitions_completed_priorities`
- [ ] `test_submit_transitions_unmarked_to_carried_over`
- [ ] `test_submit_transitions_unmarked_tasks_to_cancelled`
- [ ] `test_submit_raises_409_when_already_submitted`
- [ ] `test_submit_calculates_summary_correctly`
- [ ] `test_submit_crs_failure_does_not_revert_checkout`

### Integration Tests

- [ ] `test_endpoint_post_checkout_returns_201`
- [ ] `test_endpoint_post_checkout_returns_409_duplicate`
- [ ] `test_endpoint_get_current_returns_200`
- [ ] `test_endpoint_get_current_returns_404`
- [ ] `test_endpoint_patch_priority_returns_200`
- [ ] `test_endpoint_patch_task_returns_200`
- [ ] `test_endpoint_submit_returns_200_with_summary`
- [ ] `test_endpoint_submit_returns_409_already_submitted`

### Security Tests

- [ ] `test_cross_tenant_checkout_returns_403`
- [ ] `test_other_employee_checkout_returns_403`
- [ ] `test_all_endpoints_return_401_without_token`

---

## Git Branch

`feature/003-weekly-checkout`
