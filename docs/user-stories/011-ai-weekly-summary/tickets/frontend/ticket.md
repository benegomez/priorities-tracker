---
status: done
type: frontend
story: docs/user-stories/011-ai-weekly-summary/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Medium
complexity: S
---

# [FE] US-011 — AI Weekly Team Summary UI (with Cache Indicators)

## Objetivo

Implementar una página `/manager/ai-summary` donde el manager puede generar un resumen ejecutivo semanal de su equipo. La UI indica claramente si el resumen fue generado por IA, viene del cache, o es un fallback calculado. Incluye botón "Regenerar" para invalidar cache.

## Scope

1 página nueva, 1 service function, 1 hook, 2-3 componentes, badges de origen. Sin lógica compleja — consume el endpoint y muestra el resultado con indicadores visuales.

## Dependencia

Endpoint backend `POST /api/v1/ai/team-summary` disponible (ticket BE).

---

## Contrato API Consumido

| Método | Endpoint | Propósito |
|---|---|---|
| POST | `/api/v1/ai/team-summary` | Genera o retorna resumen cacheado |

### Request

```typescript
{ regenerate?: boolean }  // default false
```

### Response

```typescript
interface TeamSummaryResponse {
  summary: string;
  generated_at: string;
  model: string | null;
  data_snapshot: DataSnapshot;
  fallback: boolean;
  cached: boolean;
}
```

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  features/ai/
    services/
      ai-service.ts                  - CREATE (API client)
    hooks/
      useTeamSummary.ts              - CREATE (useMutation)
    components/
      AISummaryCard.tsx              - CREATE (resumen + métricas + badges)
      AISummaryEmptyState.tsx        - CREATE (antes de generar)

  app/(authenticated)/manager/ai-summary/
    page.tsx                         - CREATE
    loading.tsx                      - CREATE

  config/navigation.ts              - MODIFY (agregar link "Resumen IA")
```

---

## Implementación

### `ai-service.ts`

```typescript
export interface DataSnapshot {
  team_size: number;
  week_start: string;
  avg_crs: number;
  total_priorities: number;
  completed_priorities: number;
  completion_rate: number;
}

export interface TeamSummaryResponse {
  summary: string;
  generated_at: string;
  model: string | null;
  data_snapshot: DataSnapshot;
  fallback: boolean;
  cached: boolean;
}

export function generateTeamSummary(regenerate = false): Promise<TeamSummaryResponse> {
  return apiPost<TeamSummaryResponse>("/api/v1/ai/team-summary", { regenerate });
}
```

### `useTeamSummary.ts`

```typescript
export function useTeamSummary() {
  return useMutation({
    mutationFn: (regenerate: boolean = false) => generateTeamSummary(regenerate),
  });
}
```

### `AISummaryCard.tsx`

Muestra:
- **Resumen** (texto del LLM o fallback)
- **Badge de origen:**
  - 🟢 "Generado por IA" — `fallback=false` y `cached=false`
  - 🔵 "Desde cache" — `cached=true` (con timestamp de generación)
  - ⚪ "Resumen automático" — `fallback=true`
- **Modelo** usado (si no es fallback): "gpt-4o-mini"
- **Métricas** del `data_snapshot`: team_size, avg_crs, completion_rate, total/completed priorities
- **Timestamp** de generación (`generated_at`)
- **Botón "Regenerar"** — visible cuando `cached=true` o siempre como opción

### `AISummaryEmptyState.tsx`

- Icono de IA (Sparkles)
- Texto: "Genera un resumen ejecutivo de tu equipo con IA"
- Botón "Generar Resumen"

### `page.tsx` — flujo

```
/manager/ai-summary
  ├── Estado inicial: AISummaryEmptyState con botón "Generar Resumen"
  │     └── Click → mutate(false) → loading
  │
  ├── Loading: spinner + "Generando resumen..." (puede tardar hasta 15s)
  │
  ├── Resultado: AISummaryCard
  │     ├── Badge de origen (IA / cache / fallback)
  │     ├── Texto del resumen
  │     ├── Métricas
  │     └── Botón "Regenerar" → mutate(true) → loading → nuevo resultado
  │
  └── Error: mensaje + botón "Reintentar"
```

---

## Badges de Origen (diseño visual)

| Estado | Badge | Color | Texto |
|---|---|---|---|
| `fallback=false, cached=false` | 🟢 | green | "Generado por IA" |
| `cached=true` | 🔵 | blue | "Desde cache · {generated_at}" |
| `fallback=true` | ⚪ | gray | "Resumen automático (sin IA)" |

---

## Navegación

Agregar en `config/navigation.ts` para el rol `manager`:
```typescript
{ icon: Sparkles, label: "Resumen IA", href: "/manager/ai-summary" }
```

---

## Edge Cases

| Caso | Comportamiento |
|---|---|
| Antes de generar | Empty state con botón |
| Generando (primera vez) | Spinner "Generando resumen..." (hasta 15s) |
| Resultado desde cache | Badge azul "Desde cache" + botón "Regenerar" |
| Resultado IA fresco | Badge verde "Generado por IA" |
| Resultado fallback | Badge gris "Resumen automático" + botón "Regenerar" |
| Regenerando | Spinner reemplaza resultado anterior |
| Error de red | Mensaje de error + botón "Reintentar" |
| 403 | Redirect o mensaje "No tienes permisos" |

---

## Tests Requeridos

- [ ] `test_AISummaryCard_renders_summary_text`
- [ ] `test_AISummaryCard_shows_ai_badge_when_fresh`
- [ ] `test_AISummaryCard_shows_cache_badge`
- [ ] `test_AISummaryCard_shows_fallback_badge`
- [ ] `test_AISummaryCard_shows_metrics`
- [ ] `test_AISummaryCard_shows_regenerate_button`
- [ ] `test_empty_state_shows_generate_button`

---

## Criterios de Aceptación

- [ ] `/manager/ai-summary` muestra botón "Generar Resumen"
- [ ] Click genera el resumen (loading visible)
- [ ] Resultado muestra texto + métricas + badge de origen
- [ ] Badge verde para IA fresca, azul para cache, gris para fallback
- [ ] Botón "Regenerar" visible, invoca con `regenerate=true`
- [ ] Error muestra mensaje + botón reintentar
- [ ] Link "Resumen IA" en sidebar para managers
- [ ] `npm run build` sin errores
- [ ] `npm test` — todos los tests pasan

---

## Git Branch

`feature/011-ai-weekly-summary`
