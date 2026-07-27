---
status: pending
type: backend
story: docs/user-stories/016-manager-individual-view/UserStory.md
risk_level: Medium
complexity: S
---

# [BE] US-016 — Manager Individual View: Integration Tests

## Objetivo

Agregar tests de integración para los endpoints que alimentan la vista individual del manager. La implementación ya existe.

## Endpoints a testear

- `GET /api/v1/teams/my-team/{id}/crs` — CRS actual + historial de un reporte directo
- `GET /api/v1/teams/my-team/{id}/checkin` — ya cubierto en US-015; agregar caso de CRS sin datos

## Archivo a Crear

```
apps/backend/src/modules/teams/tests/integration/test_team_member_detail_endpoints.py
```

## Tests Requeridos (5 tests)

- `test_get_member_crs_returns_current_and_history` — GET /my-team/{id}/crs retorna current + history
- `test_get_member_crs_employee_gets_403` — rol employee → 403
- `test_get_member_crs_403_for_non_direct_report` — UUID aleatorio → 403
- `test_get_member_crs_weeks_param_limits_history` — ?weeks=2 retorna máximo 2 semanas
- `test_get_member_crs_no_crs_returns_null_current` — empleado sin CRS calculado → current: null, history: []

## Criterios de Aceptación

- [ ] 5 tests pasando
- [ ] Tests existentes del módulo teams siguen pasando
