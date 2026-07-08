---
status: done
type: frontend
story: docs/user-stories/009-employee-dashboard/UserStory.md
depends-on: null
risk_level: Medium
complexity: M
---

# [FE] US-009 — Employee Personal Dashboard

## Objetivo

Reemplazar el placeholder de `/employee/dashboard` con un dashboard funcional que muestre al empleado su CRS actual, el estado de su semana (prioridades activas + CTAs contextuales) y su historial CRS de las últimas 8 semanas — todo en una sola vista, cargando los 3 requests en paralelo.

## Scope

1 página modificada, 1 feature module nuevo (`features/dashboard/`), 3 artefactos nuevos, 5 componentes existentes reutilizados. Sin endpoints nuevos — todo reutiliza APIs ya implementadas.

---

## Contrato API Consumido

| Método | Endpoint | Propósito | Ya existe |
|---|---|---|---|
| GET | `/api/v1/checkins/current` | Prioridades y tareas de la semana | ✅ US-001 |
| GET | `/api/v1/crs/current` | Score actual, tendencia, risk_level | ✅ US-007 |
| GET | `/api/v1/crs/history?weeks=8` | Historial de scores | ✅ US-007 |

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  features/dashboard/
    hooks/
      useDashboardData.ts           - CREATE (useQueries paralelo)
    components/
      DashboardWeekCard.tsx         - CREATE (estado semana + CTAs)
      DashboardPrioritiesList.tsx   - CREATE (lista prioridades + contadores)

  app/(authenticated)/employee/dashboard/
    page.tsx                        - MODIFY (reemplazar placeholder)
    loading.tsx                     - CREATE (skeleton por sección)
```

### Componentes existentes reutilizados (sin modificar)

| Componente | Ubicación | Uso |
|---|---|---|
| `CRSScoreCard` | `features/crs/components/` | Sección CRS — score + detalle |
| `CRSHistoryChart` | `features/crs/components/` | Sección historial |
| `CRSEmptyState` | `features/crs/components/` | Cuando no hay CRS calculado |
| `CRSTrendIndicator` | `features/crs/components/` | Tendencia en header CRS |
| `CheckInPriorityCard` | `features/checkins/components/` | Prioridades en `DashboardPrioritiesList` |

---

## Implementación

### `useDashboardData` — carga paralela

```typescript
// features/dashboard/hooks/useDashboardData.ts
import { useQueries } from "@tanstack/react-query";
import { getCurrentCheckIn } from "@/features/checkins/services/checkin-service";
import { getCurrentCRS, getCRSHistory } from "@/features/crs/services/crs-service";
import type { ApiError } from "@/lib/api-client";

const no404Retry = (failureCount: number, error: unknown) => {
  if ((error as ApiError).status === 404) return false;
  return failureCount < 2;
};

export function useDashboardData() {
  const [checkIn, crs, history] = useQueries({
    queries: [
      { queryKey: ["checkins", "current"], queryFn: getCurrentCheckIn, retry: no404Retry },
      { queryKey: ["crs", "current"], queryFn: getCurrentCRS, retry: no404Retry },
      { queryKey: ["crs", "history", 8], queryFn: () => getCRSHistory(8), retry: no404Retry },
    ],
  });
  return { checkIn, crs, history };
}
```

---

### `DashboardWeekCard` — lógica de CTAs

```
Estado del check-in → CTA mostrado:
  404 (no existe)       → "Crear Check-In"      → /employee/checkin/new
  status = "draft"      → "Enviar Check-In"     → /employee/checkin
  status = "submitted"
    + sin CRS semana    → "Completar Check-Out" → /employee/checkout
    + CRS semana actual → Badge "Semana completada" (sin CTA)
```

**Inferencia del estado de checkout** (sin 4to request):
- Si `checkin.status === "submitted"` Y `crs.week_start === checkin.week_start` → checkout enviado
- Si `checkin.status === "submitted"` Y no hay CRS de esa semana → checkout pendiente
- Válido porque el CRS solo se calcula al submit del checkout (BR-009)

---

### `DashboardPrioritiesList` — contadores

```typescript
const total = priorities.length;
const completed = priorities.filter(p => p.status === "completed").length;
const inProgress = priorities.filter(p => p.status === "in_progress").length;
```

Reutiliza `CheckInPriorityCard` para renderizar cada prioridad (modo read-only — sin checkboxes ni botones de edición).

---

### Layout del Dashboard

```
/employee/dashboard
┌─────────────────────────────────────────────────────┐
│  Dashboard                                          │
├──────────────────────┬──────────────────────────────┤
│  Mi CRS              │  Esta Semana                 │
│  CRSScoreCard        │  DashboardWeekCard           │
│  (o CRSEmptyState)   │  (estado + CTA contextual)   │
├──────────────────────┴──────────────────────────────┤
│  Prioridades Activas                                │
│  DashboardPrioritiesList                            │
│  (CheckInPriorityCard × N, read-only)               │
├─────────────────────────────────────────────────────┤
│  Historial CRS                                      │
│  CRSHistoryChart                                    │
└─────────────────────────────────────────────────────┘
```

Grid 2 columnas en desktop (CRS | Esta Semana). Mobile: columnas apiladas verticalmente.

---

### `page.tsx` — estructura

```tsx
// app/(authenticated)/employee/dashboard/page.tsx
"use client";

export default function EmployeeDashboard() {
  const { checkIn, crs, history } = useDashboardData();

  return (
    <div className="space-y-6">
      <h1>Dashboard</h1>

      {/* Grid: CRS + Semana */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section aria-label="Mi CRS">
          {/* CRSScoreCard | CRSEmptyState */}
        </section>
        <section aria-label="Esta Semana">
          {/* DashboardWeekCard */}
        </section>
      </div>

      {/* Prioridades activas */}
      <section aria-label="Prioridades Activas">
        {/* DashboardPrioritiesList */}
      </section>

      {/* Historial */}
      <section aria-label="Historial CRS">
        {/* CRSHistoryChart */}
      </section>
    </div>
  );
}
```

Cada sección maneja su propio estado de loading/error de forma independiente — si un endpoint falla, las otras secciones siguen funcionando.

---

### `loading.tsx` — skeleton

```tsx
// Skeleton por sección, no bloquear toda la página
export default function DashboardLoading() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="h-8 w-32 bg-gray-200 rounded" />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="h-48 bg-gray-200 rounded-lg" />
        <div className="h-48 bg-gray-200 rounded-lg" />
      </div>
      <div className="h-32 bg-gray-200 rounded-lg" />
      <div className="h-48 bg-gray-200 rounded-lg" />
    </div>
  );
}
```

---

## Edge Cases

| Caso | Comportamiento |
|---|---|
| Sin check-in esta semana (404) | `DashboardWeekCard`: "No has creado tu check-in" + CTA "Crear Check-In" |
| Check-in en draft | Muestra prioridades + CTA "Enviar Check-In" |
| Sin CRS calculado (404) | `CRSEmptyState` en sección CRS |
| Sin historial CRS | `CRSHistoryChart` retorna `null` (ya implementado) |
| Check-in submitted + checkout pendiente | CTA "Completar Check-Out" |
| Semana completada | Badge "Semana completada", sin CTAs |
| Error en un endpoint | Sección afectada muestra error inline, las otras siguen |

---

## Manejo de Errores

| Error API | Comportamiento UI |
|---|---|
| `404` en /checkins/current | `DashboardWeekCard` muestra CTA "Crear Check-In" |
| `404` en /crs/current | `CRSEmptyState` en sección CRS |
| `401` | Redirect a `/auth/login` (middleware existente) |
| Error de red | Sección afectada muestra mensaje de error inline |

---

## Tests Requeridos

> Nivel de riesgo: Medium → Unit tests de componentes

### Component Tests (vitest + @testing-library/react)

- [ ] `test_DashboardWeekCard_shows_create_checkin_cta_when_no_checkin`
- [ ] `test_DashboardWeekCard_shows_submit_cta_when_draft`
- [ ] `test_DashboardWeekCard_shows_checkout_cta_when_submitted_no_crs`
- [ ] `test_DashboardWeekCard_shows_completed_badge_when_week_done`
- [ ] `test_DashboardPrioritiesList_shows_correct_counters`
- [ ] `test_DashboardPrioritiesList_shows_empty_state_when_no_priorities`
- [ ] `test_dashboard_page_renders_crs_section`
- [ ] `test_dashboard_page_renders_empty_state_when_no_crs`

---

## Accesibilidad (WCAG 2.1 AA)

- [ ] Secciones con `aria-label` descriptivo
- [ ] CTAs con texto descriptivo (no solo iconos)
- [ ] Score CRS con `aria-label="Score: 85.1"`
- [ ] Tabla de historial con `<thead>` y `scope="col"`
- [ ] Navegación por teclado en CTAs

---

## Criterios de Aceptación

- [ ] `/employee/dashboard` reemplaza el placeholder con contenido real
- [ ] Los 3 requests se lanzan en paralelo (no secuencial)
- [ ] Sección CRS muestra score, badge de riesgo y tendencia (o `CRSEmptyState`)
- [ ] Sección "Esta Semana" muestra estado del check-in y CTA contextual correcto
- [ ] Sección prioridades muestra lista con contadores (total / completadas / en progreso)
- [ ] Sección historial muestra tabla de últimas 8 semanas (o vacío si no hay)
- [ ] Cada sección tiene skeleton de loading independiente
- [ ] Si un endpoint falla, las otras secciones siguen funcionando
- [ ] Responsive: grid 2 columnas en desktop, apilado en mobile
- [ ] `npm run build` sin errores
- [ ] `npm test` — todos los tests pasan

---

## Git Branch

`feature/009-employee-dashboard`
