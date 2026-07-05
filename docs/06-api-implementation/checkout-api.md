# CheckOut API

## Base Path

```
/api/v1/checkouts
```

## Estado: ✅ Implementado (US-003)

---

## Endpoints

### GET /api/v1/checkouts/current

Obtiene el check-out de la semana actual con prioridades y tareas (con flag completed).

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `get_current_checkout` |

**Response 200:**
```json
{
  "id": "uuid",
  "checkin_id": "uuid",
  "employee_id": "uuid",
  "organization_id": "uuid",
  "week_start": "2026-07-05",
  "status": "draft",
  "submitted_at": null,
  "notes": null,
  "lessons_learned": null,
  "priorities": [
    {
      "id": "uuid",
      "title": "Implementar login",
      "status": "planned",
      "priority_level": "high",
      "completed": false,
      "tasks": [
        { "id": "uuid", "title": "Crear endpoint", "status": "pending", "completed": false }
      ]
    }
  ],
  "created_at": "...",
  "updated_at": "..."
}
```

**Response 404:** No check-out for current week

---

### POST /api/v1/checkouts

Crea un check-out en estado `draft` cargando prioridades y tareas del check-in.

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `create_checkout` |
| Status exitoso | 201 Created |

**Request body:**
```json
{
  "checkin_id": "uuid"
}
```

**Response 201:** mismo schema que GET /current

**Errores:**
- `401` — Token inválido
- `403` — Check-in no pertenece al empleado (BR-013), cross-tenant (BR-016)
- `404` — Check-in no encontrado
- `409` — BR-002: ya existe check-out para esta semana
- `409` — Check-in no está en estado `submitted`

---

### PATCH /api/v1/checkouts/{id}/priorities/{priority_id}

Marca o desmarca una prioridad como completada.

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `mark_priority_completed` |

**Request body:**
```json
{ "completed": true }
```

**Response 200:**
```json
{ "priority_id": "uuid", "completed": true }
```

**Errores:**
- `401`, `403` (no es owner)
- `404` — Priority no encontrada o no pertenece al check-in
- `409` — Check-out ya submitted

---

### PATCH /api/v1/checkouts/{id}/tasks/{task_id}

Marca o desmarca una tarea como completada.

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `mark_task_completed` |

**Request body:**
```json
{ "completed": true }
```

**Response 200:**
```json
{ "task_id": "uuid", "completed": true }
```

**Errores:**
- `401`, `403` (no es owner)
- `404` — Task no encontrada o no pertenece al check-in
- `409` — Check-out ya submitted

---

### POST /api/v1/checkouts/{id}/submit

Envía el check-out. Transiciona estados de prioridades y tareas atómicamente.

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `submit_checkout` |

**Request body:**
```json
{
  "notes": "Buena semana",
  "lessons_learned": "Enfocarme en menos prioridades"
}
```

**Lógica del submit:**
- Prioridades marcadas completed → status `completed`
- Prioridades NO marcadas → status `carried_over` (BR-006)
- Tareas marcadas completed → status `completed`
- Tareas NO marcadas → status `cancelled` (BR-007)
- CRS se calcula best-effort post-commit (BR-009)

**Response 200:**
```json
{
  "id": "uuid",
  "status": "submitted",
  "submitted_at": "2026-07-05T18:00:00Z",
  "summary": {
    "priorities_total": 3,
    "priorities_completed": 2,
    "priorities_carried": 1,
    "tasks_total": 5,
    "tasks_completed": 4
  }
}
```

**Errores:**
- `401`, `403` (no es owner)
- `404` — Check-out no encontrado
- `409` — Ya fue submitted

---

## Business Rules Enforced

| BR | Endpoint | Comportamiento |
|---|---|---|
| BR-002 | POST /checkouts | 409 si duplicado |
| BR-006 | POST /{id}/submit | Prioridades no marcadas → carried_over |
| BR-007 | POST /{id}/submit | Tareas no marcadas → cancelled |
| BR-008 | PATCH priorities | 404 si prioridad no existe |
| BR-009 | POST /{id}/submit | CRS best-effort post-commit |
| BR-013 | Todos | Ownership check |
| BR-016 | Todos | organization_id from JWT |

---

## Schemas Pydantic

- `CheckOutCreate` — `{ checkin_id: UUID }`
- `MarkCompletedRequest` — `{ completed: bool }`
- `CheckOutPriorityItem` — `{ id, title, status, priority_level, completed, tasks[] }`
- `CheckOutTaskItem` — `{ id, title, status, completed }`
- `CheckOutResponse` — full response con priorities + tasks
- `MarkPriorityResponse` — `{ priority_id, completed }`
- `MarkTaskResponse` — `{ task_id, completed }`
- `CheckOutSubmitRequest` — `{ notes, lessons_learned }`
- `CheckOutSubmitResponse` — `{ id, status, submitted_at, summary }`
- `CheckOutSummaryResponse` — `{ priorities_total/completed/carried, tasks_total/completed }`
