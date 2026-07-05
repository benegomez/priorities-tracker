---
status: done
type: frontend
story: docs/user-stories/007-crs-calculation/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Critical
complexity: M
---

# [FE] US-007 — CRS Dashboard

## Objetivo

Implementar la página `/employee/crs` que muestra el score actual del empleado, tendencia, nivel de riesgo, e historial de semanas anteriores.

## Scope

1 página nueva, servicios, hooks, y componentes. Sin lógica de cálculo (eso es backend).

## Dependencia

Ticket BE completado — endpoints GET /crs/current y GET /crs/history disponibles.

---

## Contrato API Consumido

| Método | Endpoint | Propósito |
|---|---|---|
| GET | /api/v1/crs/current | Score actual con trend y risk_level |
| GET | /api/v1/crs/history?weeks=8 | Historial de scores |

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  app/(authenticated)/employee/crs/
    page.tsx                              - CREATE (dashboard CRS)
    loading.tsx                           - CREATE

  features/crs/
    services/
      crs-service.ts                      - CREATE (API client)
    hooks/
      useCurrentCRS.ts                    - CREATE (useQuery)
      useCRSHistory.ts                    - CREATE (useQuery)
    components/
      CRSScoreCard.tsx                    - CREATE (score grande + risk badge)
      CRSTrendIndicator.tsx               - CREATE (flecha + label)
      CRSHistoryChart.tsx                 - CREATE (tabla/gráfico de historial)
      CRSEmptyState.tsx                   - CREATE (sin datos aún)
```

---

## Diseño de UI

```
┌─────────────────────────────────────────────────────┐
│ Mi CRS                                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │         85.5                                │    │
│  │    Commitment Reliability Score             │    │
│  │                                             │    │
│  │    Badge: Confiable     ↑ Improving         │    │
│  │    Semana del 2026-07-05                    │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │ Detalle del cálculo                         │    │
│  │ Prioridades: 2/3 completadas               │    │
│  │ Tareas: 4/5 completadas                    │    │
│  │ Arrastre: 1 prioridad                      │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │ Historial                                   │    │
│  │ Semana      Score    Tendencia    Riesgo    │    │
│  │ 2026-07-05  85.5     ↑ Improving  Low      │    │
│  │ 2026-06-28  78.0     → Stable     Low      │    │
│  │ 2026-06-21  75.0     ↓ Declining  Low      │    │
│  │ 2026-06-14  80.0     → Stable     Low      │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Componentes

### CRSScoreCard

- Score numérico grande (text-4xl font-bold)
- Color según risk_level: low=green, moderate=orange, high=red
- Badge con nivel: "Excelente", "Confiable", "Riesgo Moderado", "Riesgo Alto"
- Semana del cálculo

### CRSTrendIndicator

- Flecha: ↑ (green), → (gray), ↓ (red)
- Label: "Mejorando", "Estable", "Declinando"

### CRSHistoryChart

- Tabla con columnas: Semana, Score, Tendencia, Riesgo
- Últimas 8 semanas por defecto
- Cada fila con colores según risk_level

### CRSEmptyState

- Mensaje: "Aún no tienes un CRS calculado"
- Subtexto: "Completa tu primer Check-Out para ver tu score"

---

## Mapeo de labels

```typescript
const riskLabels = { low: "Bajo", moderate: "Moderado", high: "Alto" };
const trendLabels = { improving: "Mejorando", stable: "Estable", declining: "Declinando" };
const scoreLabels = (score: number) => {
  if (score >= 90) return "Excelente";
  if (score >= 75) return "Confiable";
  if (score >= 60) return "Riesgo Moderado";
  return "Riesgo Alto";
};
```

---

## Tests Requeridos

### Component Tests

- [ ] `test_CRSScoreCard_renders_score_and_badge`
- [ ] `test_CRSScoreCard_shows_correct_color_for_risk_level`
- [ ] `test_CRSTrendIndicator_shows_improving_arrow`
- [ ] `test_CRSTrendIndicator_shows_declining_arrow`
- [ ] `test_CRSHistoryChart_renders_rows`
- [ ] `test_CRSEmptyState_renders_message`
- [ ] `test_crs_page_shows_empty_state_when_404`
- [ ] `test_crs_page_shows_score_when_data_exists`

---

## Accesibilidad

- [ ] Score con aria-label descriptivo
- [ ] Colores acompañados de texto (no solo color para indicar riesgo)
- [ ] Tabla de historial con headers accesibles

---

## Criterios de Aceptación

- [ ] Página `/employee/crs` muestra score actual
- [ ] Badge de risk_level con color correcto
- [ ] Tendencia con flecha e indicador
- [ ] Historial muestra últimas semanas
- [ ] Empty state cuando no hay CRS calculado
- [ ] Detalle del cálculo (prioridades/tareas completadas)
- [ ] Responsive
- [ ] Accesible

---

## Git Branch

`feature/007-crs-calculation`
