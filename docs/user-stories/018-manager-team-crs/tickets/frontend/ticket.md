---
status: pending
type: frontend
story: docs/user-stories/018-manager-team-crs/UserStory.md
risk_level: Low
complexity: S
---

# [FE] US-018 — Manager Team CRS View

## Objetivo

Implementar la página `/manager/crs` que muestra el CRS consolidado del equipo del manager.

## Archivos a Crear

```
apps/frontend/src/
  app/(authenticated)/manager/crs/
    page.tsx                  # /manager/crs — vista CRS del equipo
  tests/
    manager-team-crs.test.tsx # 4 tests de componente
```

## Implementación

### `/manager/crs/page.tsx`

- Usa `useTeamReport(8)` (hook existente en `features/reports/hooks/`)
- Loading skeleton mientras `isLoading`
- 3 `ReportStatCard`: CRS Promedio, Miembros en Riesgo Alto, Total Miembros
- Tabla ordenada por CRS ascendente (nulls al final)
- Cada fila: nombre clickeable → `router.push(/manager/team/${id})`
- Columnas: Miembro | CRS (`TeamCRSBadge`) | Tendencia (`CRSTrendIndicator`) | Cumplimiento
- Miembro sin CRS: "—" + badge gris "Sin datos"
- Empty state con `TeamEmptyState` cuando `members.length === 0`

## Componentes Reutilizados

| Componente | Origen |
|---|---|
| `ReportStatCard` | `features/reports/components/` |
| `TeamCRSBadge` | `features/teams/components/` |
| `CRSTrendIndicator` | `features/crs/components/` |
| `TeamEmptyState` | `features/teams/components/` |
| `useTeamReport` | `features/reports/hooks/` |

## Tests Requeridos (4 tests)

- `ManagerTeamCRSPage shows loading skeleton`
- `ManagerTeamCRSPage renders avg CRS stat`
- `ManagerTeamCRSPage renders member rows sorted by CRS`
- `ManagerTeamCRSPage shows empty state when no members`

## Criterios de Aceptación

- [ ] `/manager/crs` implementada y navegable desde el menú
- [ ] Tabla ordenada por CRS ascendente
- [ ] Clic en miembro navega a `/manager/team/[id]`
- [ ] 4 tests pasando
- [ ] 121+ tests totales frontend pasando
- [ ] Build exitoso
