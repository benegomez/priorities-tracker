# PR: feat: US-007 CRS Calculation & Dashboard

## Summary

Implements the Commitment Reliability Score (CRS) — the platform's key differentiator. The CRS measures how reliably an employee fulfills their weekly commitments.

## What Changed

### Backend — CRS Module
- **CRSCalculationService** with formula v1.0 (4 components):
  - 40% priority completion rate
  - 30% task completion rate
  - 20% historical consistency (avg last 4 weeks)
  - 10% carryover penalty
- Re-ponders without history (50/37.5/12.5)
- Trend: ±5 points vs average → improving/stable/declining
- Risk level: >=75 low, >=60 moderate, <60 high
- **GET /api/v1/crs/current** — current score
- **GET /api/v1/crs/history** — historical scores
- Integrated with `SubmitCheckOutUseCase` (best-effort, non-blocking)
- 17 unit tests covering all edge cases

### Frontend — CRS Dashboard
- `/employee/crs` page with CRSScoreCard, CRSTrendIndicator, CRSHistoryChart
- CRSEmptyState when no data
- Loading skeleton

### Fixes included
- Middleware: manager can now access `/employee/*` routes
- Navigation: manager gets "Mi Semana" group (Check-In, Check-Out, Mi CRS)
- CheckOutPriorityCard: cascading checkbox logic (mark priority → marks all tasks, mark last task → marks priority)

### Documentation
- US-007 story, tickets, plan (all done)
- CRS module docs updated with implementation details
- Traceability matrix updated
- Technical debt: TD-012 closed, TD-020/TD-021 registered
- Fixed US-004/US-006 plan/ticket statuses

## ADR References
- ADR-010 (DDD)
- ADR-006 (FastAPI backend)

## Risk Level
**Critical** — CRS is a core business flow

## Testing Evidence
- Backend: 96 tests passed, 2 skipped (Monday validation in dev)
- Frontend: 47 tests passed
- CRS calculator: 17 unit tests (>95% coverage)
- Manual verification: score 68.75 for 1/2 priorities completed

## Business Rules Validated
- BR-009: CRS calculated automatically on Check-Out submit ✅
- BR-010: CRS not manually modifiable (no PATCH/PUT) ✅
- BR-011: Auditable (formula_version stored) ✅
- BR-012: CRS recalculated when Check-Out exists ✅

## Closes
- TD-012 (CRS calculation placeholder)
