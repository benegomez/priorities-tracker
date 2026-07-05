# Pull Request — US-001 Weekly Check-In Creation

**URL para crear PR:** https://github.com/benegomez/priorities-tracker/pull/new/feature/001-weekly-checkin-creation

**Base:** `main`
**Branch:** `feature/001-weekly-checkin-creation`

---

## Título

```
feat: US-001 Weekly Check-In Creation
```

## Descripción

### Resumen

Implementación completa de la US-001: Weekly Check-In Creation.

Permite a un colaborador crear su Check-In semanal, agregar prioridades con tareas, y enviarlo para visibilidad del manager.

### Cambios

#### Fase 1 — Database
- Migración Alembic con 5 tablas: `projects`, `project_phases`, `check_ins`, `priorities`, `tasks`
- Partial unique index `uq_check_ins_employee_week` (BR-001)
- CHECK constraints para todos los enums de estado
- Columnas de auditoría + soft delete

#### Fase 2 — Backend
- 2 módulos: `checkin`, `priorities`
- 5 endpoints: GET /checkins/current, POST /checkins, POST /checkins/{id}/submit, POST /priorities, POST /priorities/{id}/tasks
- 5 use cases con validación de BR-001, BR-003, BR-004, BR-005, BR-013, BR-016
- Domain entities con state machines
- 16 unit tests + 8 integration tests (24/24 passing)

#### Fase 3 — Frontend
- Shared API client con auth token injection
- Features: checkins (service, schema, hooks, 3 components), priorities (service, schemas, hooks, 5 components)
- Página `/employee/checkin` con rendering condicional (sin checkin → form, draft → builder, submitted → read-only)
- Accesibilidad: aria-labels, aria-live, aria-disabled, keyboard navigation
- 28 component + schema tests (37 total frontend tests passing)

### Nivel de Riesgo

**Critical** — Flujo core del producto (Check-In semanal)

### Business Rules Validadas

| BR | Descripción | Validación |
|---|---|---|
| BR-001 | Un check-in por semana por empleado | Partial unique index + use case |
| BR-003 | Prioridad debe pertenecer a una fase | Use case validation |
| BR-004 | Fase debe pertenecer a proyecto activo | Use case validation |
| BR-005 | Tarea debe pertenecer a una prioridad | Use case validation |
| BR-013 | Empleado solo ve sus propias prioridades | Ownership check |
| BR-016 | Aislamiento multi-tenant | organization_id from JWT |

### Evidencia de Tests

- Backend: 24/24 tests passing (16 unit + 8 integration)
- Frontend: 37/37 tests passing (18 component + 10 schema + 9 existing)
- Functional verification via curl: all endpoints respond correctly

### ADRs Referenciados

- ADR-003 (Modular Monolith)
- ADR-006 (FastAPI + Python 3.13)
- ADR-007 (Next.js 15 + TypeScript)
- ADR-008 (API First)
- ADR-009 (OpenAPI Contract First)
- ADR-010 (DDD)

### Impacto en Documentación

- `plan.md` actualizado con las 3 fases completadas
- Tickets DB/BE/FE actualizados a `status: done`
