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
| Unit tests | ✅ 8 tests |
| Integration tests | ✅ 8 tests |

---

## Estructura de Archivos

```
modules/checkin/
├── api/
│   ├── router.py           # GET /current, POST /, POST /{id}/submit
│   └── schemas.py          # CheckInCreate, CheckInResponse, CheckInSubmitResponse
├── application/
│   ├── commands/
│   │   ├── create_checkin.py    # CreateCheckInUseCase
│   │   └── submit_checkin.py    # SubmitCheckInUseCase
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
| week_start | date | Lunes de la semana (validado) |
| status | str | `draft` → `submitted` → `closed` |
| submitted_at | datetime | null | Timestamp de envío |
| priorities_count | int | Cantidad de prioridades asociadas |
| created_at | datetime | Auditoría |
| updated_at | datetime | Auditoría |

### State Machine

```
draft → submitted → closed
```

- `draft`: Check-In creado, acepta prioridades
- `submitted`: Enviado, read-only, prioridades transicionan a `planned`
- `closed`: Cerrado por Check-Out (futuro)

---

## Casos de Uso Implementados

### CreateCheckInUseCase

- Valida `week_start` es lunes
- Valida BR-001 (un check-in por semana por empleado)
- Extrae `organization_id` del JWT
- Persiste con status `draft`

### SubmitCheckInUseCase

- Valida ownership (BR-013)
- Valida ≥1 prioridad asociada
- Valida status actual es `draft`
- Transiciona a `submitted` + registra `submitted_at`
- Transiciona prioridades asociadas a `planned`

### GetCurrentCheckInUseCase

- Calcula lunes de la semana actual
- Busca check-in del empleado para esa semana
- Retorna `None` si no existe (→ 404 en API)

---

## Reglas de Negocio

| BR | Descripción | Validación |
|---|---|---|
| BR-001 | Solo un Check-In por semana por empleado | Partial unique index + use case |
| BR-013 | Empleado solo accede a sus propios check-ins | Ownership check en use case |
| BR-016 | Aislamiento multi-tenant | organization_id from JWT |
| BR-017 | Todo aggregate tiene organization_id | Columna obligatoria |

---

## Dependencias

- `priorities` module (para contar prioridades y transicionar estado)
- `shared/security` (JWT, CurrentUser)
- `shared/database` (AsyncSession)
- `shared/exceptions` (BusinessRuleViolation, ValidationException)
