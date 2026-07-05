---
status: done
type: backend
story: docs/user-stories/005-checkin-detail-edit/UserStory.md
depends-on: null
risk_level: High
complexity: S
---

# [BE] US-005 — Check-In Detail & Edit (Backend Changes)

## Objetivo

Modificar los use cases existentes para permitir: (1) agregar prioridades a un Check-In en estado `submitted`, (2) re-submit que transiciona solo prioridades nuevas (en `draft`) a `planned`, y (3) retornar prioridades con tareas anidadas en `GET /checkins/current`.

## Scope

Modificar 3 archivos existentes. Sin nuevos endpoints, sin nuevas tablas.

---

## Cambios Requeridos

### 1. `modules/priorities/application/commands/create_priority.py`

**Cambio:** Relajar validación — permitir agregar prioridades cuando check-in está en `submitted` (no solo `draft`).

**Antes:**
```python
if checkin.status != "draft":
    raise BusinessRuleViolation("Cannot add priorities to a submitted check-in")
```

**Después:**
```python
if checkin.status not in ("draft", "submitted"):
    raise BusinessRuleViolation("Cannot add priorities to a closed check-in")
```

**Restricción adicional:** Verificar que NO existe un Check-Out para la misma semana/empleado. Si existe → `409 Conflict` con mensaje "Check-In is locked by an existing Check-Out".

---

### 2. `modules/checkin/application/commands/submit_checkin.py`

**Cambio:** Permitir re-submit. Solo transicionar prioridades que están en `draft` a `planned`. No afectar prioridades ya en `planned` o estados posteriores.

**Antes:**
```python
if self.status != "draft":
    raise BusinessRuleViolation("BR-001: Check-in can only be submitted from draft status")
```

**Después:**
```python
if self.status not in ("draft", "submitted"):
    raise BusinessRuleViolation("Check-in can only be submitted from draft or submitted status")
```

**Lógica de re-submit:**
- Si status es `draft` → transicionar TODAS las prioridades a `planned` (comportamiento actual)
- Si status es `submitted` → transicionar solo prioridades con `status = 'draft'` a `planned`
- Actualizar `submitted_at` con timestamp actual

---

### 3. `modules/checkin/api/router.py` — GET /checkins/current

**Cambio:** Retornar prioridades con tareas anidadas en el response.

**Agregar:** Query de prioridades + tareas similar a `_load_priorities_for_checkout` del módulo checkout.

**Response actualizado:**
```json
{
  "id": "uuid",
  "employee_id": "uuid",
  "organization_id": "uuid",
  "week_start": "2026-07-05",
  "status": "submitted",
  "submitted_at": "2026-07-05T08:00:00Z",
  "priorities_count": 3,
  "priorities": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string|null",
      "priority_level": "high",
      "status": "planned",
      "tasks": [
        { "id": "uuid", "title": "string", "status": "pending" }
      ]
    }
  ],
  "created_at": "...",
  "updated_at": "..."
}
```

---

### 4. `modules/checkin/api/schemas.py`

**Agregar schemas:**
```python
class CheckInTaskItem(BaseModel):
    id: UUID
    title: str
    status: str

class CheckInPriorityItem(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    priority_level: str
    status: str
    tasks: list[CheckInTaskItem] = []
```

**Modificar `CheckInResponse`:** agregar `priorities: list[CheckInPriorityItem] = []`

---

## Business Rules

| Regla | Validación |
|---|---|
| No eliminar/modificar prioridades existentes | No se expone endpoint de DELETE/PATCH para prioridades |
| No editar si existe Check-Out | `create_priority` verifica ausencia de checkout |
| Re-submit solo transiciona draft → planned | `submit_checkin` filtra por status='draft' |
| Prioridades nuevas inician en draft | Comportamiento existente de `create_priority` |

---

## Tests Requeridos

### Unit Tests (modificar existentes + agregar nuevos)

- [ ] `test_create_priority_allows_submitted_checkin` (nuevo)
- [ ] `test_create_priority_raises_409_when_checkout_exists` (nuevo)
- [ ] `test_submit_checkin_resubmit_transitions_only_draft_priorities` (nuevo)
- [ ] `test_submit_checkin_resubmit_updates_submitted_at` (nuevo)
- [ ] `test_submit_checkin_resubmit_does_not_affect_planned_priorities` (nuevo)

### Integration Tests

- [ ] `test_endpoint_post_priority_returns_201_on_submitted_checkin` (nuevo)
- [ ] `test_endpoint_post_priority_returns_409_when_checkout_exists` (nuevo)
- [ ] `test_endpoint_submit_resubmit_returns_200` (nuevo)
- [ ] `test_endpoint_get_current_returns_priorities_with_tasks` (nuevo)

---

## Criterios de Aceptación

- [ ] `POST /priorities` acepta check-in en `submitted` (no solo `draft`)
- [ ] `POST /priorities` retorna 409 si existe Check-Out para la semana
- [ ] `POST /checkins/{id}/submit` permite re-submit desde `submitted`
- [ ] Re-submit solo transiciona prioridades en `draft` → `planned`
- [ ] Re-submit no afecta prioridades ya en `planned` o posteriores
- [ ] Re-submit actualiza `submitted_at`
- [ ] `GET /checkins/current` retorna prioridades con tareas anidadas
- [ ] Todos los tests existentes siguen pasando
- [ ] Nuevos tests pasan

---

## Git Branch

`feature/005-checkin-detail-edit`
