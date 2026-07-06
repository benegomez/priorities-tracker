# PR: feat: US-008 Manager Team Visibility — CRS & Check-Ins

## Summary

Implements the manager team dashboard — the manager can now see their direct reports' CRS scores, weekly trends, and check-in/check-out status at a glance, plus drill into individual employee detail.

## What Changed

### Backend — Teams Module (new)
- **GET /api/v1/teams/my-team** — Direct reports with latest CRS + week status (4 batch queries, no N+1)
- **GET /api/v1/teams/my-team/{id}/crs** — Employee CRS history (reuses CRSRepositoryImpl)
- **GET /api/v1/teams/my-team/{id}/checkin** — Employee weekly check-in read-only (reuses priorities+tasks loader)
- Ownership validation: 403 if employee is not a direct report (BR-014)
- Role check: `require_roles("manager", "administrator")` — 403 for employee
- Multi-tenant enforced (BR-016)
- 10 unit tests passing
- Seed script for testing (`scripts/seed_checkin_checkout.py`)

### Frontend — Team Dashboard
- `/manager/team` — Table with columns: Name, CRS (colored badge), Trend (arrow), Check-In status, Check-Out status
- `/manager/team/[employeeId]` — Detail page with CRS history table + check-in priorities/tasks (read-only)
- Components: TeamTable, TeamCRSBadge, TeamWeekStatusBadge, TeamEmptyState, MemberCRSHistory, MemberCheckInView
- Reuses CRSTrendIndicator from CRS module
- Empty state when manager has no direct reports
- All read-only (no write actions)

### Documentation
- US-008 story (enriched), tickets (done), plan (done)
- Traceability matrix updated with Manager Dashboard implementation
- Teams module doc updated with actual endpoints
- TD-022 and TD-023 registered (integration/security tests + component tests)

## ADR References
- ADR-010 (DDD — Organization bounded context)

## Risk Level
**High** — Cross-user access (manager sees employee data). Requires strict BR-014 validation.

## Testing Evidence
- Backend: 10 unit tests passing (ownership validation, batch queries, edge cases)
- Security verified via curl: 403 for employee, 403 cross-manager, 401 without token
- Frontend: 47 tests passing (no regressions), build successful (15 pages)
- Functional: Manager sees Employee Alpha with CRS 71.67, check-in submitted with 3 priorities

## Business Rules Validated
- BR-014: Manager only sees direct reports ✅
- BR-016: Multi-tenant (organization_id from JWT) ✅
- Read-only: No PATCH/PUT/POST/DELETE on employee data ✅
- 403 (not 404) when employee is not a direct report ✅
- Inactive employees excluded from list ✅

## Technical Debt Registered
- TD-022: Integration + security tests not automated (verified manually)
- TD-023: Component tests for team dashboard not written
