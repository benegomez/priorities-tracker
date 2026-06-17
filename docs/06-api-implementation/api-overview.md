# API Overview

## Principios

- REST First
- Versionado: /api/v1
- Multi-Tenant
- JWT + RBAC
- OpenAPI First

## Recursos

/auth
/users
/teams
/projects
/project-phases
/priorities
/tasks
/checkins
/checkouts
/crs
/reports
/planning-cycles

## Nuevo Concepto

WeeklyPlanningCycle

Agrupa:
- CheckIn
- Prioridades
- Tareas
- CheckOut
- CRS

No es una entidad persistente en el MVP.
