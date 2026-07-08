---
id: US-009
title: Employee Personal Dashboard
status: enriched
priority: high
risk_level: Medium
complexity: M
created: 2026-07-07
---

# US-009 — Employee Personal Dashboard

## [original]

**Como** colaborador individual,
**quiero** ver un dashboard personal con mis prioridades activas, mi CRS actual y mi historial semanal,
**para** tener visibilidad de mi propio desempeño y estado de compromisos sin depender del manager.

### Contexto

El empleado puede crear check-ins y check-outs, pero no tiene una vista consolidada de su actividad. El CRS ya se calcula y persiste (US-007). Las prioridades y tareas ya existen. La ruta `/employee/dashboard` existe como placeholder con un Card vacío. Esta US reemplaza ese placeholder con un dashboard funcional.

---

## [enhanced]

### User Journey

- **Usuario principal:** Colaborador Individual (employee)
- **Flujo:**
  1. Empleado hace login → es redirigido a `/employee/dashboard`
  2. El dashboard carga en paralelo 3 fuentes de datos:
     - CRS actual (`GET /api/v1/crs/current`)
     - Check-in de la semana (`GET /api/v1/checkins/current`)
     - Historial CRS (`GET /api/v1/crs/history?weeks=8`)
  3. Ve su estado de la semana en una sola pantalla:
     - **Sección CRS:** score grande con badge de riesgo y tendencia
     - **Sección Semana:** estado del check-in + prioridades activas con contadores
     - **Sección Historial:** tabla de las últimas 8 semanas
  4. Si hay acciones pendientes, ve CTAs contextuales:
     - Sin check-in → "Crear Check-In"
     - Check-in en draft → "Enviar Check-In"
     - Check-in enviado, sin check-out → "Completar Check-Out"

---

### Business Value

- **Problema que resuelve:** El empleado no tiene visibilidad de su propio desempeño. Debe navegar a múltiples páginas para ver su check-in, su CRS y su historial. Esto reduce la adopción y el valor percibido del producto.
- **Beneficio esperado:** En una sola vista el empleado entiende su estado semanal y su confiabilidad histórica. Refuerza el hábito de uso y la auto-gestión.

---

### FR de Referencia

- **FR-025** — Employee Dashboard
- **FR-032** — CRS Calculation (visualización)
- **FR-033** — CRS History (visualización)

---

### Bounded Context

Commitment + Reliability → Módulos: `checkin`, `crs`

---

### Contrato API

**Sin endpoints nuevos.** Los 3 necesarios ya existen y están probados:

| Endpoint | Ya existe | Propósito |
|---|---|---|
| `GET /api/v1/checkins/current` | ✅ US-001 | Prioridades y tareas de la semana |
| `GET /api/v1/crs/current` | ✅ US-007 | Score actual, tendencia, risk_level |
| `GET /api/v1/crs/history?weeks=8` | ✅ US-007 | Historial de scores |

---

### Componentes existentes reutilizables

| Componente | Ubicación actual | Uso en dashboard |
|---|---|---|
| `CRSScoreCard` | `features/crs/components/` | Sección CRS — score + detalle |
| `CRSHistoryChart` | `features/crs/components/` | Sección historial |
| `CRSTrendIndicator` | `features/crs/components/` | Tendencia en header |
| `CRSEmptyState` | `features/crs/components/` | Cuando no hay CRS |
| `CheckInPriorityCard` | `features/checkins/components/` | Prioridades de la semana |
| `useCurrentCRS` | `features/crs/hooks/` | Query CRS actual |
| `useCRSHistory` | `features/crs/hooks/` | Query historial |
| `useCurrentCheckIn` | `features/checkins/hooks/` | Query check-in actual |

**Todos los hooks ya manejan `retry: false` para 404** — patrón establecido en el proyecto.

---

### Estructura de componentes nuevos

```
features/dashboard/
├── components/
│   ├── DashboardWeekCard.tsx      ← Estado semana + CTAs contextuales
│   └── DashboardPrioritiesList.tsx ← Lista prioridades activas con contadores
└── hooks/
    └── useDashboardData.ts        ← useQueries paralelo (CRS + checkin + history)
```

```
app/(authenticated)/employee/dashboard/
└── page.tsx   ← Reemplaza el placeholder actual
```

#### `useDashboardData` — carga paralela
```typescript
// Usa useQueries de TanStack Query para los 3 requests en paralelo
// Cada sección maneja su propio estado de loading/error independientemente
// No bloquear el dashboard completo si un endpoint falla
```

#### `DashboardWeekCard` — lógica de CTAs
```
check-in 404 (no existe)     → CTA "Crear Check-In"   → /employee/checkin/new
check-in status = "draft"    → CTA "Enviar Check-In"  → /employee/checkin
check-in status = "submitted"
  + checkout 404             → CTA "Completar Check-Out" → /employee/checkout
check-in status = "submitted"
  + checkout submitted       → Badge "Semana completada" (sin CTA)
```

**Nota:** El estado del check-out se infiere del check-in. Si el check-in está `submitted` y el CRS de la semana actual existe → checkout fue enviado. Si no hay CRS de la semana actual → checkout pendiente. Esto evita un 4to request.

#### `DashboardPrioritiesList` — contadores
```
Total: priorities.length
Completadas: priorities.filter(p => p.status === "completed").length
En progreso: priorities.filter(p => p.status === "in_progress").length
```

---

### Layout del Dashboard

```
┌─────────────────────────────────────────────────────┐
│  Dashboard                                          │
├──────────────────────┬──────────────────────────────┤
│  Mi CRS              │  Esta Semana                 │
│  ┌────────────────┐  │  ┌──────────────────────┐   │
│  │  85.1          │  │  │ Check-In: Enviado     │   │
│  │  [Confiable]   │  │  │ 3 prioridades         │   │
│  │  ↑ improving   │  │  │ 2 completadas / 1 en  │   │
│  │  Prioridades   │  │  │ progreso              │   │
│  │  2/3 · Tareas  │  │  │                       │   │
│  │  4/5           │  │  │ [Completar Check-Out] │   │
│  └────────────────┘  │  └──────────────────────┘   │
├──────────────────────┴──────────────────────────────┤
│  Prioridades Activas                                │
│  ┌─────────────────────────────────────────────┐   │
│  │ ◆ Implementar módulo auth    [high] [planned]│   │
│  │   Proyecto Alpha → Desarrollo                │   │
│  │   ○ Tarea 1  ● Tarea 2                      │   │
│  └─────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│  Historial CRS                                      │
│  Semana       Score   Tendencia   Riesgo            │
│  2026-07-07   85.1    ↑           [Bajo]            │
│  2026-06-30   78.0    →           [Bajo]            │
└─────────────────────────────────────────────────────┘
```

En mobile: columnas apiladas verticalmente (CRS → Semana → Prioridades → Historial).

---

### Business Rules

| BR | Regla | Validación |
|---|---|---|
| BR-013 | Empleado solo ve sus propias prioridades | JWT `sub` = `employee_id` en todos los endpoints |
| BR-016 | Multi-tenant | `organization_id` del JWT en todos los queries |

---

### Edge Cases

| Caso | Comportamiento esperado |
|---|---|
| Sin check-in esta semana | `DashboardWeekCard` muestra CTA "Crear Check-In" |
| Check-in en draft | Muestra prioridades + CTA "Enviar Check-In" |
| Sin CRS calculado | `CRSEmptyState` en sección CRS (componente ya existe) |
| Sin historial CRS | `CRSHistoryChart` retorna `null` cuando `items.length === 0` (ya implementado) |
| Check-in enviado + checkout pendiente | CTA "Completar Check-Out" |
| Semana completada (checkin + checkout) | Badge "Semana completada", sin CTAs |
| Error en un endpoint | Sección afectada muestra error inline, las otras siguen funcionando |
| Loading | Skeleton por sección (no bloquear toda la página) |

---

### Acceptance Criteria

**Escenario 1 — Dashboard muestra estado completo de la semana**
```gherkin
Given un empleado con check-in submitted y CRS calculado
When accede a /employee/dashboard
Then ve su CRS actual con score, badge de riesgo y tendencia
  And ve el estado del check-in (submitted)
  And ve sus prioridades activas con contadores
  And ve el historial de las últimas semanas
```

**Escenario 2 — Sin check-in esta semana**
```gherkin
Given un empleado sin check-in para la semana actual
When accede a /employee/dashboard
Then ve la sección "Esta Semana" con mensaje "No has creado tu check-in"
  And ve un botón "Crear Check-In" que navega a /employee/checkin/new
```

**Escenario 3 — Check-in en draft**
```gherkin
Given un empleado con check-in en estado draft
When accede a /employee/dashboard
Then ve sus prioridades (aunque no estén enviadas)
  And ve un CTA "Enviar Check-In" que navega a /employee/checkin
```

**Escenario 4 — Check-in enviado, checkout pendiente**
```gherkin
Given un empleado con check-in submitted y sin checkout de la semana
When accede a /employee/dashboard
Then ve sus prioridades activas
  And ve un CTA "Completar Check-Out" que navega a /employee/checkout
```

**Escenario 5 — Nuevo empleado sin CRS**
```gherkin
Given un empleado sin ningún CRS calculado
When accede a /employee/dashboard
Then ve CRSEmptyState en la sección CRS
  And la sección historial no muestra tabla (items vacíos)
  And la sección de semana funciona normalmente
```

**Escenario 6 — Carga paralela e independiente**
```gherkin
Given un empleado autenticado
When accede a /employee/dashboard
Then los 3 requests se lanzan en paralelo
  And si el endpoint de CRS falla, la sección de check-in sigue mostrando datos
  And cada sección tiene su propio skeleton de loading
```

**Escenario 7 — Solo el empleado ve su propio dashboard**
```gherkin
Given un empleado autenticado
When accede a /employee/dashboard
Then solo ve sus propias prioridades y su propio CRS
  And los endpoints retornan datos filtrados por el JWT del empleado
```

---

### Non-Functional Requirements

- **NFR-004** — Dashboard carga en < 1s (3 requests paralelos con `useQueries`)
- **NFR-011** — Empleado obtiene visibilidad de su estado en < 30 segundos desde login

---

### Technical Notes

#### Inferencia del estado de checkout
Para evitar un 4to request, el estado del checkout se infiere:
- Si `checkin.status === "submitted"` Y `crs.week_start === checkin.week_start` → checkout fue enviado
- Si `checkin.status === "submitted"` Y no hay CRS de esa semana → checkout pendiente

Esto es válido porque el CRS solo se calcula al submit del checkout (BR-009).

#### `useDashboardData` — implementación sugerida
```typescript
export function useDashboardData() {
  const results = useQueries({
    queries: [
      { queryKey: ["checkins", "current"], queryFn: getCurrentCheckIn, retry: ... },
      { queryKey: ["crs", "current"], queryFn: getCurrentCRS, retry: ... },
      { queryKey: ["crs", "history", 8], queryFn: () => getCRSHistory(8), retry: ... },
    ],
  });
  return {
    checkIn: results[0],
    crs: results[1],
    history: results[2],
  };
}
```

#### Reutilización de `CheckInPriorityCard`
El componente `CheckInPriorityCard` ya existe en `features/checkins/components/`. Reutilizarlo en `DashboardPrioritiesList` para mostrar las prioridades del dashboard — misma UI, modo read-only.

#### Página `/employee/crs` existente
La página `/employee/crs` ya existe y muestra CRS + historial. El dashboard NO la reemplaza — la complementa con el contexto semanal. El link "Ver detalle CRS" en el dashboard puede navegar a `/employee/crs`.

---

### Dependencies

- **Técnicas:**
  - `GET /api/v1/checkins/current` ✅ US-001
  - `GET /api/v1/crs/current` ✅ US-007
  - `GET /api/v1/crs/history` ✅ US-007
  - `useCurrentCRS`, `useCRSHistory`, `useCurrentCheckIn` ✅ ya existen
  - `CRSScoreCard`, `CRSHistoryChart`, `CRSEmptyState`, `CRSTrendIndicator` ✅ ya existen
  - `CheckInPriorityCard` ✅ ya existe
- **Funcionales:**
  - Requiere US-001 (check-in) ✅
  - Requiere US-007 (CRS) ✅

---

### Nivel de Riesgo

**Medium** — US 100% frontend. Los endpoints ya existen y están probados. El riesgo principal es la composición correcta de los 3 requests paralelos y el manejo de todos los edge cases de estado.

---

### Complejidad Estimada

**M**

| Factor | Detalle |
|---|---|
| Capas afectadas | Frontend únicamente |
| Endpoints nuevos | 0 — reutiliza los 3 existentes |
| Componentes nuevos | 3 (`DashboardWeekCard`, `DashboardPrioritiesList`, `useDashboardData`) |
| Componentes reutilizados | 5 (`CRSScoreCard`, `CRSHistoryChart`, `CRSEmptyState`, `CRSTrendIndicator`, `CheckInPriorityCard`) |
| Lógica | `useQueries` paralelo + inferencia estado checkout + 6 edge cases |
| Tests | Medium: unit tests de componentes + estados vacíos |
| UI | 1 página (reemplaza placeholder) con 4 secciones |

---

### Siguiente Paso

Ejecutar `/create-tickets 009-employee-dashboard`
