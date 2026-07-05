# Priorities API

## Base Path

```
/api/v1/priorities
```

## Estado: ✅ Parcialmente implementado (US-001)

---

## Endpoints Implementados

### POST /api/v1/priorities

Crea una nueva prioridad asociada a un check-in.

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `create_priority` |
| Status exitoso | 201 Created |

**Request body:**
```json
{
  "checkin_id": "uuid",
  "phase_id": "uuid",
  "title": "Implementar login",
  "description": "Flujo completo de autenticación",
  "priority_level": "high"
}
```

**Response 201:**
```json
{
  "id": "uuid",
  "checkin_id": "uuid",
  "phase_id": "uuid",
  "owner_id": "uuid",
  "organization_id": "uuid",
  "title": "Implementar login",
  "description": "Flujo completo de autenticación",
  "priority_level": "high",
  "status": "draft",
  "week_start": "2025-01-06",
  "created_at": "2025-01-06T08:00:00Z",
  "updated_at": "2025-01-06T08:00:00Z"
}
```

**Errores:**
- `400` — Validación de campos (título vacío, level inválido)
- `401` — Token inválido
- `403` — Check-in no pertenece al empleado, o fase de otra organización
- `404` — Check-in o fase no encontrados
- `409` — Check-in ya fue submitted (no acepta nuevas prioridades)

---

### POST /api/v1/priorities/{id}/tasks

Crea una tarea asociada a una prioridad.

| Campo | Valor |
|---|---|
| Auth | Bearer JWT |
| operation_id | `create_task` |
| Status exitoso | 201 Created |

**Request body:**
```json
{
  "title": "Crear endpoint de login",
  "description": "Con validación JWT"
}
```

**Response 201:**
```json
{
  "id": "uuid",
  "priority_id": "uuid",
  "organization_id": "uuid",
  "title": "Crear endpoint de login",
  "description": "Con validación JWT",
  "status": "pending",
  "created_at": "2025-01-06T08:00:00Z",
  "updated_at": "2025-01-06T08:00:00Z"
}
```

**Errores:**
- `400` — Título vacío
- `401` — Token inválido
- `403` — Prioridad no pertenece al empleado
- `404` — Prioridad no encontrada

---

## Business Rules Enforced

| BR | Endpoint | Comportamiento |
|---|---|---|
| BR-003 | POST /priorities | Valida phase_id existe |
| BR-004 | POST /priorities | Valida proyecto de la fase está `active` |
| BR-005 | POST /{id}/tasks | Valida priority_id existe |
| BR-013 | Ambos | Ownership check (employee) |
| BR-016 | Ambos | Cross-tenant isolation |

---

## Schemas Pydantic

- `PriorityCreate` — `{ checkin_id, phase_id, title, description?, priority_level }`
- `PriorityResponse` — response completo con tasks[]
- `TaskCreate` — `{ title, description? }`
- `TaskResponse` — `{ id, priority_id, organization_id, title, description, status, timestamps }`

---

## Endpoints Pendientes (futuras US)

| Método | Endpoint | Propósito |
|---|---|---|
| GET | /api/v1/priorities | Listar prioridades del empleado |
| GET | /api/v1/priorities/{id} | Detalle de una prioridad |
| PATCH | /api/v1/priorities/{id} | Actualizar estado/campos |
| POST | /api/v1/priorities/{id}/carry-over | Continuar a siguiente semana |
| PATCH | /api/v1/priorities/{id}/tasks/{task_id} | Actualizar tarea |
