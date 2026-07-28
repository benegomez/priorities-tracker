---
status: done
type: backend
completed: 2025-01-28
pr: "#17"
merge_commit: 23dd6bc
story: docs/user-stories/017-reporting/UserStory.md
risk_level: Medium
complexity: L
---

# [BE] US-017 — Reporting: Backend Module

## Objetivo

Implementar el módulo `reporting` completo con 3 endpoints de solo lectura que agregan datos de prioridades, check-ins, check-outs y CRS.

## Estructura a Crear

```
apps/backend/src/modules/reporting/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── router.py          # 3 endpoints GET
│   └── schemas.py         # IndividualReport, TeamReport, ProjectReport
├── application/
│   ├── __init__.py
│   └── queries/
│       ├── __init__.py
│       ├── individual_report_query.py
│       ├── team_report_query.py
│       └── project_report_query.py
├── infrastructure/
│   ├── __init__.py
│   └── repositories/
│       ├── __init__.py
│       └── reporting_repository_impl.py
└── tests/
    ├── __init__.py
    └── integration/
        ├── __init__.py
        └── test_reporting_endpoints.py
```

## Endpoints

### GET /api/v1/reports/individual
- Roles: `employee`, `manager`, `administrator`
- Query param: `?weeks=8` (default 8, max 52)
- Retorna: `IndividualReport` del usuario autenticado

### GET /api/v1/reports/team
- Roles: `manager`, `administrator`
- Query param: `?weeks=8`
- Retorna: `TeamReport` del equipo del manager autenticado

### GET /api/v1/reports/project/{project_id}
- Roles: `manager`, `administrator`
- Query param: `?weeks=8`
- Retorna: `ProjectReport` del proyecto (validar que pertenece a la organización)

## Registro en main.py

Agregar en `apps/backend/src/main.py`:
```python
from src.modules.reporting.api.router import router as reporting_router
app.include_router(reporting_router, prefix="/api/v1")
```

## Tests Requeridos (6 tests)

```
apps/backend/src/modules/reporting/tests/integration/test_reporting_endpoints.py
```

- `test_individual_report_returns_breakdown` — GET /reports/individual retorna weekly_breakdown
- `test_individual_report_employee_can_access` — rol employee → 200
- `test_team_report_returns_members` — GET /reports/team retorna lista de miembros
- `test_team_report_employee_gets_403` — rol employee → 403
- `test_project_report_returns_phases` — GET /reports/project/{id} retorna fases
- `test_project_report_unknown_project_returns_404` — proyecto inexistente → 404

## Criterios de Aceptación

- [ ] Módulo `reporting` creado con estructura Clean Architecture
- [ ] 3 endpoints registrados en `main.py`
- [ ] 6 tests de integración pasando
- [ ] Tests existentes siguen pasando
