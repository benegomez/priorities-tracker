# CheckIn API

## Base Path

```
/api/v1/checkins
```

## Estado: ✅ Implementado (US-001, US-005)

---

## Endpoints

### GET /api/v1/checkins/current

Obtiene el check-in de la semana actual con prioridades y tareas anidadas.

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `get_current_checkin` |
| Tags | `checkin` |

**Response 200:**
```json
{
  "id": "uuid",
  "employee_id": "uuid",
  "organization_id": "uuid",
  "week_start": "2026-07-05",
  "status": "submitted",
  "submitted_at": "2026-07-05T08:00:00Z",
  "priorities_count": 2,
  "priorities": [
    {
      "id": "uuid",
      "title": "Implementar login",
      "description": "Flujo completo de autenticación",
      "priority_level": "high",
      "status": "planned",
      "phase_name": "Desarrollo",
      "project_name": "Proyecto Alpha",
      "tasks": [
        { "id": "uuid", "title": "Crear endpoint", "status": "pending" },
        { "id": "uuid", "title": "Agregar tests", "status": "pending" }
      ]
    }
  ],
  "created_at": "2026-07-05T08:00:00Z",
  "updated_at": "2026-07-05T08:00:00Z"
}
```

**Response 404:** No check-in for current week

---

### POST /api/v1/checkins

Crea un nuevo check-in semanal.

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `create_checkin` |
| Status exitoso | 201 Created |

**Request body:**
```json
{
  "week_start": "2026-07-05"
}
```

> En producción, `week_start` debe ser un lunes. En desarrollo, acepta cualquier día.

**Response 201:** mismo schema que GET /current (con priorities vacío)

**Errores:**
- `400` — `week_start` no es lunes (solo producción)
- `401` — Token inválido o expirado
- `409` — BR-001: ya existe check-in para esta semana

---

### POST /api/v1/checkins/{id}/submit

Envía el check-in. Soporta primer submit y re-submit.

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `submit_checkin` |
| Status exitoso | 200 OK |

**Request body:** vacío `{}`

**Comportamiento:**
- **Primer submit (desde draft):** transiciona TODAS las prioridades a `planned`
- **Re-submit (desde submitted):** transiciona solo prioridades en `draft` a `planned`, no afecta las ya en `planned`
- Actualiza `submitted_at` en ambos casos

**Response 200:**
```json
{
  "id": "uuid",
  "status": "submitted",
  "submitted_at": "2026-07-05T08:30:00Z"
}
```

**Errores:**
- `401` — Token inválido
- `403` — Check-in no pertenece al empleado
- `404` — Check-in no encontrado
- `409` — Check-in sin prioridades, o en estado `closed`

---

## Business Rules Enforced

| BR | Endpoint | Comportamiento |
|---|---|---|
| BR-001 | POST /checkins | 409 si duplicado |
| BR-013 | POST /{id}/submit | 403 si no es owner |
| BR-016 | Todos | organization_id from JWT |
| NUEVA | POST /priorities (submitted) | Permite agregar si no existe checkout |
| NUEVA | POST /{id}/submit (re-submit) | Solo transiciona draft → planned |

---

## Schemas Pydantic

- `CheckInCreate` — `{ week_start: date }`
- `CheckInTaskItem` — `{ id, title, status }`
- `CheckInPriorityItem` — `{ id, title, description, priority_level, status, phase_name, project_name, tasks[] }`
- `CheckInResponse` — response completo con priorities_count + priorities[]
- `CheckInSubmitResponse` — `{ id, status, submitted_at }`
