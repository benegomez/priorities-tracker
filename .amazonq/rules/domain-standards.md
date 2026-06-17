---
description: "Estándares de dominio para Priorities Tracker. DDD, bounded contexts, entidades, reglas de negocio, máquinas de estado y CRS según ADR-010."
globs: "**/domain/**/*.py, **/modules/**/*.py"
alwaysApply: false
---

# Domain Standards — Priorities Tracker

## Principio Rector

El dominio de negocio —no las capas técnicas— es el principio organizador del sistema.

> "Business domains drive architecture." — ADR-010

---

## Bounded Contexts

El backend se organiza en cuatro contextos. Cada uno es dueño de sus entidades, reglas, APIs y persistencia.

| Contexto | Módulos | Responsabilidad |
|---|---|---|
| **Organization** | `users`, `teams` | Estructura organizacional, roles, asignaciones |
| **Commitment** | `projects`, `priorities`, `checkin` | Proyectos, fases, compromisos semanales |
| **Execution** | `checkout`, `priorities` (estado) | Resultados, carry-over, actualización de avance |
| **Reliability** | `crs`, `reporting` | CRS, métricas, reportes de confiabilidad |

### Reglas de aislamiento
- Un módulo **no importa entidades** de otro módulo directamente
- Comunicación entre contextos: solo por interfaces/contratos o eventos
- Escrituras cross-context: **prohibidas**
- Lecturas cross-context: permitidas solo por interfaces aprobadas

---

## Jerarquía del Dominio

```
Organization
  └── Team
        └── User
              └── WeeklyCheckIn  ──── WeeklyCheckOut
                    └── Priority
                          └── Task

Project
  └── ProjectPhase
        └── Priority (FK a phase)

CommitmentReliabilityScore (calculado por usuario + semana)
```

### Domain Services
- `CommitmentScoringService` — calcula el CRS
- `RiskDetectionService` — detecta prioridades en riesgo
- `PriorityContinuationService` — gestiona el carry-over

---

## Entidades Principales

### User
```
id, organization_id, manager_id, role, status
```
- `role`: `administrator` | `manager` | `employee`

### Project
```
id, organization_id, name, description, status
```
- Validaciones: `name` y `organization_id` obligatorios

### ProjectPhase
```
id, project_id, name, status
```

### Priority
```
id, phase_id, owner_id, week_period, title, description, status
```
- Validaciones: `phase_id` y `owner_id` obligatorios

### Task
```
id, priority_id, title, status
```

### WeeklyCheckIn
```
id, employee_id, week_period, status
```

### WeeklyCheckOut
```
id, employee_id, week_period, status
```

### CommitmentReliabilityScore
```
employee_id, week_period, score, trend, risk_level, formula_version
```

---

## Máquinas de Estado (Obligatorias)

El agente debe respetar estas transiciones. Cambios de estado fuera de estos flujos son inválidos.

### Project
```
Draft → Active → OnHold → Completed → Archived
```

### ProjectPhase
```
Planned → Active → Completed → Cancelled
```

### Priority
```
Draft → Planned → InProgress → Completed
                      └──────→ CarriedOver
```

### Task
```
Pending → InProgress → Completed
              └──────→ Cancelled
```

### CheckIn
```
Draft → Submitted → Closed
```

### CheckOut
```
Draft → Submitted → Closed
```

---

## Reglas de Negocio (Business Rules)

Estas reglas deben validarse en la capa de dominio o aplicación, **nunca** solo en el router.

### Planificación
- **BR-001** — Un empleado solo puede tener un Check-In por semana
- **BR-002** — Un empleado solo puede tener un Check-Out por semana
- **BR-003** — Una prioridad debe pertenecer a una fase
- **BR-004** — Una fase debe pertenecer a un proyecto
- **BR-005** — Una tarea debe pertenecer a una prioridad

### Ejecución
- **BR-006** — Una prioridad puede continuar (carry-over) a la siguiente semana
- **BR-007** — Las tareas completadas no se copian automáticamente en carry-over
- **BR-008** — No puede cerrarse una prioridad inexistente

### CRS
- **BR-009** — El CRS se calcula automáticamente al hacer Check-Out
- **BR-010** — El CRS no puede modificarse manualmente
- **BR-011** — Toda ejecución de CRS debe ser auditable
- **BR-012** — El CRS se recalcula cuando existe Check-Out

### Seguridad y acceso
- **BR-013** — Un empleado solo ve sus propias prioridades
- **BR-014** — Un manager solo ve su equipo
- **BR-015** — Un administrador puede ver toda la organización

### Multi-tenant
- **BR-016** — Ningún usuario puede acceder a datos de otra organización
- **BR-017** — Todos los agregados pertenecen a una organización

---

## Invariantes de Dominio

Las siguientes condiciones deben ser verdaderas en todo momento:

- Toda fase pertenece a un proyecto válido y activo
- Toda prioridad pertenece a una fase válida
- Toda tarea pertenece a una prioridad válida
- Un Check-Out no puede existir sin un Check-In previo para la misma semana
- El CRS siempre es calculado automáticamente, nunca ingresado manualmente
- Todo aggregate incluye `organization_id`

---

## Fórmula CRS (v1.0)

```
CRS = (0.40 × cumplimiento_prioridades)
    + (0.30 × cumplimiento_tareas)
    + (0.20 × consistencia_historica)
    + (0.10 × factor_arrastre)
```

### Escala de interpretación

| Rango | Nivel | Acción |
|---|---|---|
| 90–100 | Excelente | — |
| 75–89 | Confiable | Monitoreo normal |
| 60–74 | Riesgo moderado | Atención preventiva |
| 0–59 | Riesgo alto | Seguimiento requerido |

### Tendencias
- `Improving` — score subiendo respecto a semanas anteriores
- `Stable` — sin variación significativa
- `Declining` — score bajando

### Regla de versionado
- Almacenar `formula_version = "v1.0"` junto a cada cálculo
- Permite auditoría y evolución futura de la fórmula sin perder historia

---

## Enums del Dominio

Usar siempre estos valores exactos en código y base de datos:

| Enum | Valores |
|---|---|
| `UserRole` | `administrator`, `manager`, `employee` |
| `ProjectStatus` | `draft`, `active`, `on_hold`, `completed`, `archived` |
| `PhaseStatus` | `planned`, `active`, `completed`, `cancelled` |
| `PriorityStatus` | `draft`, `planned`, `in_progress`, `completed`, `carried_over` |
| `TaskStatus` | `pending`, `in_progress`, `completed`, `cancelled` |
| `CheckInStatus` | `draft`, `submitted`, `closed` |
| `CheckOutStatus` | `draft`, `submitted`, `closed` |
| `CRSTrend` | `improving`, `stable`, `declining` |
| `RiskLevel` | `low`, `moderate`, `high` |

---

## Excepciones de Dominio

Usar la jerarquía correcta — nunca lanzar excepciones genéricas de Python desde la capa de dominio:

| Excepción | Cuándo usarla |
|---|---|
| `DomainException` | Base para todas las excepciones de dominio |
| `ValidationException` | Datos inválidos en entidad |
| `AuthorizationException` | Acción no permitida para el rol |
| `BusinessRuleViolation` | Violación de una BR (BR-001..BR-017) |

---

## Multi-Tenant

- Todo aggregate raíz debe tener `organization_id`
- El repositorio base `OrganizationScopedRepository` filtra automáticamente por `organization_id`
- El `organization_id` se extrae del JWT en cada request — **nunca** se acepta del body
- Ningún query puede omitir el filtro de `organization_id`

---

## Reglas Obligatorias

- No mezclar lógica de infraestructura (ORM, HTTP) en entidades de dominio
- Las entidades de dominio no dependen de FastAPI ni SQLAlchemy
- Los value objects son inmutables
- Toda violación de BR lanza `BusinessRuleViolation` con referencia explícita (ej. `BR-001`)
- Los cambios de estado de entidades se validan contra la máquina de estado antes de persistir

---

## Referencias

- [docs/02-arquitectura/ADR/ADR-010-Domain-Driven-Design-Strategy-Enterprise-Final.md](../../docs/02-arquitectura/ADR/ADR-010-Domain-Driven-Design-Strategy-Enterprise-Final.md)
- [docs/04-domain/domain-model.md](../../docs/04-domain/domain-model.md)
- [docs/04-domain/entities.md](../../docs/04-domain/entities.md)
- [docs/04-domain/state-machines.md](../../docs/04-domain/state-machines.md)
- [docs/04-domain/business-rules.md](../../docs/04-domain/business-rules.md)
- [docs/04-domain/invariants.md](../../docs/04-domain/invariants.md)
- [docs/04-domain/crs-formula.md](../../docs/04-domain/crs-formula.md)
- [docs/04-domain/ubiquitous-language.md](../../docs/04-domain/ubiquitous-language.md)
