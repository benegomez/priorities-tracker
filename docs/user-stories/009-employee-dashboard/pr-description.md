# PR #9 — US-009: Employee Personal Dashboard

## Summary

Replaces the placeholder `/employee/dashboard` page with a fully functional personal dashboard that shows the employee their CRS, weekly status, active priorities, and CRS history — all in a single view with parallel data loading.

## Type of Change

- [x] New feature (non-breaking)
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation only

## Risk Level

**Medium** — Frontend-only change. No new endpoints. Reuses 3 existing APIs (all tested in US-001 and US-007).

## What Changed

### New Files (5)
| File | Purpose |
|---|---|
| `features/dashboard/hooks/useDashboardData.ts` | `useQueries` — 3 parallel requests |
| `features/dashboard/components/DashboardWeekCard.tsx` | Week status + contextual CTAs |
| `features/dashboard/components/DashboardPrioritiesList.tsx` | Priority list with counters |
| `app/(authenticated)/employee/dashboard/loading.tsx` | Skeleton per section |
| `src/tests/dashboard.test.tsx` | 8 component tests |

### Modified Files (1)
| File | Change |
|---|---|
| `app/(authenticated)/employee/dashboard/page.tsx` | Replaced placeholder with full implementation |

### Reused Without Modification (5)
`CRSScoreCard`, `CRSHistoryChart`, `CRSEmptyState`, `CRSTrendIndicator`, `CheckInPriorityCard`

## Key Design Decisions

1. **Checkout state inference** — Instead of a 4th API request, checkout status is inferred: if `crs.week_start === checkin.week_start` → checkout was submitted (valid because CRS only calculates on checkout submit per BR-009).

2. **Independent sections** — Each section handles its own loading/error state. If one endpoint fails, the others still render.

3. **Contextual CTAs** — The "Esta Semana" card shows the most relevant action based on current state:
   - No check-in → "Crear Check-In"
   - Draft → "Enviar Check-In"
   - Submitted, no checkout → "Completar Check-Out"
   - Complete → Badge "Semana completada"

## APIs Consumed (all pre-existing)

| Endpoint | Module | Status |
|---|---|---|
| `GET /api/v1/checkins/current` | checkin | ✅ US-001 |
| `GET /api/v1/crs/current` | crs | ✅ US-007 |
| `GET /api/v1/crs/history?weeks=8` | crs | ✅ US-007 |

## Testing Evidence

- **Component tests:** 8 new tests, all passing
- **Total tests:** 55/55 ✅
- **Build:** `npx next build --no-lint` successful
- **Edge cases covered:** no checkin, draft, submitted+no checkout, complete, no CRS, empty history

## FR Coverage

- FR-025 — Employee Dashboard ✅

## Screenshots / Verification

Dashboard renders 4 sections:
1. CRS score card (or empty state)
2. Week status with contextual CTA
3. Active priorities with counters
4. CRS history table (last 8 weeks)

Responsive: 2-column grid on desktop, stacked on mobile.
