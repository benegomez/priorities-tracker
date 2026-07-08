---
story: 009-employee-dashboard
status: done
branch: feature/009-employee-dashboard
risk_level: Medium
complexity: M
created: 2026-07-07
---

# Plan de Implementación — US-009: Employee Personal Dashboard

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Frontend | `useDashboardData` + `DashboardWeekCard` + `DashboardPrioritiesList` + página |

**Branch único:** `feature/009-employee-dashboard`
**Nota:** No hay fase de backend ni DB — los 3 endpoints ya existen (US-001, US-007).

---

## Fase 1 — Frontend

### 1.1 Feature module `dashboard`

- [x] Crear directorios:
  - [x] `apps/frontend/src/features/dashboard/`
  - [x] `apps/frontend/src/features/dashboard/hooks/`
  - [x] `apps/frontend/src/features/dashboard/components/`

### 1.2 Hook — `useDashboardData`

- [x] `features/dashboard/hooks/useDashboardData.ts`
  - [x] `useQueries` con los 3 queries en paralelo
  - [x] `retry: false` para 404 en los 3 (patrón establecido en el proyecto)
  - [x] Retorna `{ checkIn, crs, history }` con tipos de TanStack Query

### 1.3 Componente — `DashboardWeekCard`

- [x] `features/dashboard/components/DashboardWeekCard.tsx`
  - [x] Recibe `checkIn` (data | undefined) y `crs` (data | undefined) como props
  - [x] Lógica de CTAs:
    - [x] `checkIn === undefined` (404) → CTA "Crear Check-In" → `/employee/checkin/new`
    - [x] `checkIn.status === "draft"` → CTA "Enviar Check-In" → `/employee/checkin`
    - [x] `checkIn.status === "submitted"` + `crs?.week_start !== checkIn.week_start` → CTA "Completar Check-Out" → `/employee/checkout`
    - [x] `checkIn.status === "submitted"` + `crs?.week_start === checkIn.week_start` → Badge "Semana completada"
  - [x] Muestra contadores: total / completadas / en progreso
  - [x] Loading skeleton cuando `isLoading`

### 1.4 Componente — `DashboardPrioritiesList`

- [x] `features/dashboard/components/DashboardPrioritiesList.tsx`
  - [x] Recibe `priorities: CheckInPriorityItem[]`
  - [x] Contadores: total, completadas (`status === "completed"`), en progreso (`status === "in_progress"`)
  - [x] Reutiliza `CheckInPriorityCard` para cada prioridad (read-only)
  - [x] Estado vacío cuando `priorities.length === 0`

### 1.5 Página — `dashboard/page.tsx`

- [x] `app/(authenticated)/employee/dashboard/page.tsx`
  - [x] Reemplazar placeholder actual (Card vacío con "Próximamente")
  - [x] `"use client"` + `useDashboardData()`
  - [x] Grid 2 columnas desktop / apilado mobile: `grid-cols-1 md:grid-cols-2`
  - [x] Sección CRS: `CRSScoreCard` si hay data, `CRSEmptyState` si 404
  - [x] Sección semana: `DashboardWeekCard`
  - [x] Sección prioridades: `DashboardPrioritiesList` (solo si hay check-in)
  - [x] Sección historial: `CRSHistoryChart` (ya maneja `items.length === 0`)
  - [x] Cada sección con `aria-label` descriptivo
  - [x] Link "Ver detalle CRS" → `/employee/crs`

### 1.6 Loading skeleton — `dashboard/loading.tsx`

- [x] `app/(authenticated)/employee/dashboard/loading.tsx`
  - [x] Skeleton por sección con `animate-pulse`
  - [x] Refleja el layout real (grid 2 cols + 2 secciones full-width)

### 1.7 Tests — Component (vitest + @testing-library/react)

- [x] `test_DashboardWeekCard_shows_create_checkin_cta_when_no_checkin`
- [x] `test_DashboardWeekCard_shows_submit_cta_when_draft`
- [x] `test_DashboardWeekCard_shows_checkout_cta_when_submitted_no_crs`
- [x] `test_DashboardWeekCard_shows_completed_badge_when_week_done`
- [x] `test_DashboardWeekCard_shows_skeleton_when_loading`
- [x] `test_DashboardPrioritiesList_shows_correct_counters`
- [x] `test_DashboardPrioritiesList_shows_empty_state_when_no_priorities`
- [x] `test_DashboardPrioritiesList_renders_priority_titles`

### 1.8 Verificación

- [x] `npx next build --no-lint` sin errores
- [x] `npm test` — 55/55 tests pasan (47 existentes + 8 nuevos)
- [x] `/employee/dashboard` muestra contenido real (no placeholder)
- [x] Los 3 requests se lanzan en paralelo (`useQueries`)
- [x] CRS section muestra score + badge + tendencia
- [x] Semana section muestra CTA correcto según estado
- [x] Prioridades section muestra lista con contadores
- [x] Historial section muestra tabla
- [x] `CRSEmptyState` aparece cuando no hay CRS
- [x] CTA "Crear Check-In" navega correctamente
- [x] CTA "Completar Check-Out" navega correctamente
- [x] Responsive: grid en desktop, apilado en mobile

### 1.9 Commits

```
feat(dashboard): add useDashboardData hook with parallel queries
feat(dashboard): add DashboardWeekCard and DashboardPrioritiesList components
feat(dashboard): replace employee dashboard placeholder with full implementation
test(dashboard): add component tests for dashboard week card and priorities list
```

---

## Gate Final — PR

- [x] 8 component tests pasan
- [x] `npm run build` sin errores
- [x] Dashboard carga con datos reales del empleado
- [x] Todos los edge cases de estado funcionan (sin check-in, sin CRS, draft, submitted)
- [x] Secciones independientes (fallo de un endpoint no rompe las otras)
- [x] Responsive verificado
- [ ] PR creado con resumen, nivel de riesgo Medium, evidencia de tests

---

## Orden de Ejecución

```
/develop-plan fe    → Fase 1 (dashboard completo)
/git-flow pr        → PR único
```
