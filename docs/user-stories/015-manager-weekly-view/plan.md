---
id: 015-manager-weekly-view
status: pending
created: 2025-01-28
---

# Plan US-015 — Manager Weekly View

## Fase 1 — Backend Tests

- [ ] Crear `tests/integration/test_team_weekly_endpoints.py`
  - [ ] `test_get_my_team_returns_members_with_week_status`
  - [ ] `test_get_my_team_employee_gets_403`
  - [ ] `test_get_my_team_returns_empty_when_no_direct_reports`
  - [ ] `test_get_team_member_checkin_returns_priorities`
  - [ ] `test_get_team_member_checkin_404_when_no_checkin`
  - [ ] `test_get_team_member_checkin_403_for_non_direct_report`
- [ ] Verificar tests existentes del módulo teams siguen pasando

## Fase 2 — Frontend

- [ ] Crear `features/teams/components/WeeklySummaryBar.tsx`
- [ ] Crear `features/teams/components/WeeklyMemberRow.tsx`
- [ ] Modificar `app/(authenticated)/manager/weekly/page.tsx`
- [ ] Crear `tests/manager-weekly.test.tsx` (7 tests)
- [ ] Verificar 98+ tests totales pasando
- [ ] Verificar build `npx next build --no-lint`
