---
story: docs/user-stories/018-manager-team-crs/UserStory.md
status: pending
---

# Plan — US-018 Manager Team CRS View

## Contexto

Página `/manager/crs` existe en el menú de navegación pero no tiene implementación.
Solo requiere frontend — reutiliza `useTeamReport` y componentes existentes.

## Phase 1 — Frontend (`/develop-plan fe`)

1. Crear `app/(authenticated)/manager/crs/page.tsx`
   - `useTeamReport(8)` para datos
   - 3 `ReportStatCard` (CRS promedio, en riesgo, total)
   - Tabla ordenada por CRS ascendente con `TeamCRSBadge` + `CRSTrendIndicator`
   - Navegación a `/manager/team/[id]` al clic
   - Empty state + loading skeleton
2. Crear `tests/manager-team-crs.test.tsx` con 4 tests
