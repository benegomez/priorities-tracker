# Check-In Module

## Objetivo

Gestionar el proceso de planificación semanal de los colaboradores.

El Check-In es el mecanismo mediante el cual un empleado declara sus compromisos para la semana.

---

## Estado de Implementación

| Componente | Estado |
|---|---|
| Domain entity | ✅ Implementado |
| Repository interface | ✅ Implementado |
| Repository impl (SQLAlchemy async) | ✅ Implementado |
| Use cases | ✅ 3 implementados |
| API router | ✅ 3 endpoints |
| Unit tests | ✅ 10 tests |
| Integration tests | ✅ 8 tests |
| Detail view + edit (US-005) | ✅ Implementado |

---

## Estructura de Archivos

```
modules/checkin/
├── api/
│   ├── router.py           # GET /current, POST /, POST /{id}/submit
│   └── schemas.py          # CheckInCreate, CheckInResponse, CheckInPriorityItem, CheckInTaskItem
├── application/
│   ├── commands/
│   │   ├── create_checkin.py    # CreateCheckInUseCase
│   │   └── submit_checkin.py    # SubmitCheckInUseCase (soporta re-submit)
│   └── queries/
│       └── get_current_checkin.py  # GetCurrentCheckInUseCase
├── domain/
│   ├── entities/
│   │   └── checkin.py           # WeeklyCheckIn dataclass
│   └── repositories/
│       └── checkin_repository.py  # ABC interface
├── infrastructure/
│   └── repositories/
│       └── checkin_repository_impl.py  # SQLAlchemy async
└── tests/
    ├── unit/
    │   └── test_checkin_use_cases.py
    └── integration/
        └── test_checkin_endpoints.py
```

---

## Entidad Principal

### WeeklyCheckIn

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | PK |
| employee_id | UUID | FK → users |
| organization_id | UUID | FK → organizations |
| week_start | date | Lunes de la semana (validado en producción) |
| status | str | `draft` → `submitted` → `closed` |
| submitted_at | datetime | null | Timestamp de envío (se actualiza en re-submit) |
| created_at | datetime | Auditoría |
| updated_at | datetime | Auditoría |

### State Machine

```
draft → submitted → closed
         ↺ (re-submit: actualiza submitted_at, transiciona nuevas prioridades)
```

- `draft`: Check-In creado, acepta prioridades
- `submitted`: Enviado, acepta nuevas prioridades (si no existe checkout), re-submit posible
- `closed`: Cerrado por Check-Out (futuro)

---

## Casos de Uso Implementados

### CreateCheckInUseCase

- Valida `week_start` es lunes (solo en producción)
- Valida BR-001 (un check-in por semana por empleado)
- Extrae `organization_id` del JWT
- Persiste con status `draft`

### SubmitCheckInUseCase (soporta re-submit)

- Valida ownership (BR-013)
- Valida ≥1 prioridad asociada
- **Primer submit (desde draft):** transiciona TODAS las prioridades a `planned`
- **Re-submit (desde submitted):** transiciona solo prioridades en `draft` a `planned`
- Actualiza `submitted_at` en ambos casos

### GetCurrentCheckInUseCase

- En desarrollo: busca por fecha de hoy, luego por lunes
- En producción: busca por lunes de la semana actual
- Retorna `None` si no existe (→ 404 en API)

---

## Response: GET /checkins/current

Retorna prioridades con tareas anidadas, incluyendo fase y proyecto:

```json
{
  "id": "uuid",
  "status": "submitted",
  "submitted_at": "2026-07-05T08:00:00Z",
  "priorities_count": 3,
  "priorities": [
    {
      "id": "uuid",
      "title": "Implementar login",
      "description": "Flujo completo",
      "priority_level": "high",
      "status": "planned",
      "phase_name": "Desarrollo",
      "project_name": "Proyecto Alpha",
      "tasks": [
        { "id": "uuid", "title": "Crear endpoint", "status": "pending" }
      ]
    }
  ]
}
```

---

## Reglas de Negocio

| BR | Descripción | Validación |
|---|---|---|
| BR-001 | Solo un Check-In por semana por empleado | Partial unique index + use case |
| BR-013 | Empleado solo accede a sus propios check-ins | Ownership check |
| BR-016 | Aislamiento multi-tenant | organization_id from JWT |
| BR-017 | Todo aggregate tiene organization_id | Columna obligatoria |
| NUEVA | No se puede agregar prioridades si existe checkout | Validación en create_priority |
| NUEVA | Re-submit solo transiciona prioridades en draft | Filtro en transition_to_planned |

---

## Dependencias

- `priorities` module (para contar prioridades y transicionar estado)
- `checkout` module (para verificar bloqueo en create_priority)
- `shared/security` (JWT, CurrentUser)
- `shared/database` (AsyncSession)
- `shared/exceptions` (BusinessRuleViolation, ValidationException)
