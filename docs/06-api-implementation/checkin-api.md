# CheckIn API

## Base Path

```
/api/v1/checkins
```

## Estado: ✅ Implementado (US-001)

---

## Endpoints

### GET /api/v1/checkins/current

Obtiene el check-in de la semana actual del empleado autenticado.

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
  "week_start": "2025-01-06",
  "status": "draft",
  "submitted_at": null,
  "priorities_count": 2,
  "created_at": "2025-01-06T08:00:00Z",
  "updated_at": "2025-01-06T08:00:00Z"
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
  "week_start": "2025-01-06"
}
```

> `week_start` debe ser un lunes (ISO weekday 1).

**Response 201:**
```json
{
  "id": "uuid",
  "employee_id": "uuid",
  "organization_id": "uuid",
  "week_start": "2025-01-06",
  "status": "draft",
  "submitted_at": null,
  "priorities_count": 0,
  "created_at": "2025-01-06T08:00:00Z",
  "updated_at": "2025-01-06T08:00:00Z"
}
```

**Errores:**
- `400` — `week_start` no es lunes
- `401` — Token inválido o expirado
- `409` — BR-001: ya existe check-in para esta semana

---

### POST /api/v1/checkins/{id}/submit

Envía el check-in (transiciona a `submitted`).

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `submit_checkin` |
| Status exitoso | 200 OK |

**Request body:** vacío `{}`

**Response 200:**
```json
{
  "id": "uuid",
  "status": "submitted",
  "submitted_at": "2025-01-06T08:30:00Z"
}
```

**Errores:**
- `401` — Token inválido
- `403` — Check-in no pertenece al empleado
- `404` — Check-in no encontrado
- `409` — Check-in sin prioridades, o ya fue submitted

---

## Business Rules Enforced

| BR | Endpoint | Comportamiento |
|---|---|---|
| BR-001 | POST /checkins | 409 si duplicado |
| BR-013 | POST /{id}/submit | 403 si no es owner |
| BR-016 | Todos | organization_id from JWT |
| BR-017 | Todos | organization_id en entity |

---

## Schemas Pydantic

- `CheckInCreate` — `{ week_start: date }`
- `CheckInResponse` — response completo con priorities_count
- `CheckInSubmitResponse` — `{ id, status, submitted_at }`
