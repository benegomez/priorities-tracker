# Priorities Module

## Objetivo

Gestionar compromisos semanales (prioridades) y trabajo ejecutable (tareas).

---

## Estado de Implementación

| Componente | Estado |
|---|---|
| Domain entities | ✅ Priority + Task |
| Repository interfaces | ✅ 2 ABCs |
| Repository impls (SQLAlchemy async) | ✅ 2 implementados |
| Use cases | ✅ 2 implementados |
| API router | ✅ 2 endpoints |
| Unit tests | ✅ 8 tests |

---

## Estructura de Archivos

```
modules/priorities/
├── api/
│   ├── router.py           # POST /priorities, POST /priorities/{id}/tasks
│   └── schemas.py          # PriorityCreate, PriorityResponse, TaskCreate, TaskResponse
├── application/
│   └── commands/
│       ├── create_priority.py   # CreatePriorityUseCase
│       └── create_task.py       # CreateTaskUseCase
├── domain/
│   ├── entities/
│   │   ├── priority.py         # Priority dataclass
│   │   └── task.py             # Task dataclass
│   └── repositories/
│       ├── priority_repository.py  # ABC interface
│       └── task_repository.py      # ABC interface
├── infrastructure/
│   └── repositories/
│       ├── priority_repository_impl.py  # SQLAlchemy async
│       └── task_repository_impl.py      # SQLAlchemy async
└── tests/
    └── unit/
        └── test_priority_use_cases.py
```

---

## Ownership

| Entidad | Módulo owner |
|---|---|
| Project | `projects` (futuro) |
| ProjectPhase | `projects` (futuro) |
| Priority | `priorities` ✅ |
| Task | `priorities` ✅ |

---

## Entidades

### Priority

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | PK |
| checkin_id | UUID | FK → check_ins |
| phase_id | UUID | FK → project_phases |
| owner_id | UUID | FK → users |
| organization_id | UUID | FK → organizations |
| week_start | date | Semana del compromiso |
| title | str | Título (max 255, no vacío) |
| description | str | null | Descripción opcional |
| priority_level | str | `low` / `medium` / `high` |
| status | str | State machine |
| created_at | datetime | Auditoría |
| updated_at | datetime | Auditoría |

#### State Machine — Priority

```
draft → planned → in_progress → completed
                       └──────→ carried_over
```

### Task

| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | PK |
| priority_id | UUID | FK → priorities |
| organization_id | UUID | FK → organizations |
| title | str | Título (max 255, no vacío) |
| description | str | null | Descripción opcional |
| status | str | State machine |
| created_at | datetime | Auditoría |
| updated_at | datetime | Auditoría |

#### State Machine — Task

```
pending → in_progress → completed
              └──────→ cancelled
```

---

## Casos de Uso Implementados

### CreatePriorityUseCase

- Valida checkin existe y pertenece al empleado (BR-013)
- Valida checkin en status `draft` (no acepta prioridades si ya submitted)
- Valida phase existe y pertenece a la misma organización (BR-016)
- Valida project de la phase está `active` (BR-004)
- Persiste priority con status `draft`

### CreateTaskUseCase

- Valida priority existe y pertenece al empleado (BR-005, BR-013)
- Persiste task con status `pending`

---

## Reglas de Negocio

| BR | Descripción | Validación |
|---|---|---|
| BR-003 | Prioridad debe pertenecer a una fase | FK + use case |
| BR-004 | Fase debe pertenecer a proyecto activo | Query en use case |
| BR-005 | Tarea debe pertenecer a una prioridad | FK + use case |
| BR-013 | Empleado solo ve sus propias prioridades | Ownership check |
| BR-016 | Aislamiento multi-tenant | organization_id from JWT |

---

## Relación con Check-In

Durante Check-In (status `draft`):
1. Empleado crea prioridades asociadas al check-in
2. Cada prioridad requiere seleccionar fase (→ proyecto)
3. Tareas se agregan inline a cada prioridad

Al submit del Check-In:
- Prioridades transicionan de `draft` → `planned`

---

## Relación con CRS (futuro)

El módulo CRS utilizará:
- Prioridades comprometidas vs completadas
- Tareas comprometidas vs completadas
- Prioridades con carry-over

---

## Endpoints Pendientes (futuras US)

- `GET /api/v1/priorities` — listar prioridades del empleado
- `PATCH /api/v1/priorities/{id}` — actualizar estado
- `POST /api/v1/priorities/{id}/carry-over` — continuar a siguiente semana
- `PATCH /api/v1/priorities/{id}/tasks/{task_id}` — actualizar tarea
