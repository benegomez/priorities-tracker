---
status: done
type: backend
story: docs/user-stories/015-manager-weekly-view/UserStory.md
risk_level: Medium
complexity: S
---

# [BE] US-015 — Manager Weekly View: Integration Tests

## Objetivo

Agregar tests de integración para los endpoints de visibilidad del manager que alimentan la vista semanal. La implementación ya existe.

## Endpoints a testear

- `GET /api/v1/teams/my-team` — lista miembros con CRS y week_status
- `GET /api/v1/teams/my-team/{id}/checkin` — check-in de un miembro específico

## Archivo a Crear

```
apps/backend/src/modules/teams/tests/integration/test_team_weekly_endpoints.py
```

## Tests Requeridos (6 tests)

- `test_get_my_team_returns_members_with_week_status` — GET /my-team retorna miembros con week_status
- `test_get_my_team_employee_gets_403` — rol employee → 403
- `test_get_my_team_returns_empty_when_no_direct_reports` — manager sin reportes → lista vacía
- `test_get_team_member_checkin_returns_priorities` — GET /my-team/{id}/checkin retorna prioridades
- `test_get_team_member_checkin_404_when_no_checkin` — sin check-in esta semana → 404
- `test_get_team_member_checkin_403_for_non_direct_report` — empleado de otro manager → 403

## Criterios de Aceptación

- [ ] 6 tests pasando
- [ ] Tests existentes del módulo teams siguen pasando
