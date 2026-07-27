---
status: pending
type: frontend
story: docs/user-stories/016-manager-individual-view/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Medium
complexity: S
---

# [FE] US-016 — Manager Individual View: Component Tests

## Objetivo

Agregar tests de componentes para la página `/manager/team/[employeeId]` y sus componentes reutilizables. La implementación ya existe.

## Scope

La página `apps/frontend/src/app/(authenticated)/manager/team/[employeeId]/page.tsx` ya está implementada con:
- `MemberCRSHistory` — tabla de historial CRS
- `MemberCheckInView` — lista de prioridades del check-in
- `TeamCRSBadge` + `CRSTrendIndicator` — badge y tendencia del CRS actual

## Archivo a Crear

```
apps/frontend/src/tests/manager-individual.test.tsx
```

## Tests Requeridos (5 tests)

- `MemberCRSHistory renders history table rows` — tabla con filas por semana
- `MemberCRSHistory shows empty state when no history` — mensaje sin historial
- `MemberCheckInView renders priorities list` — lista de prioridades con título
- `MemberCheckInView shows empty message when no priorities` — sin prioridades registradas
- `TeamMemberDetailPage shows loading skeleton` — skeleton mientras carga

## Criterios de Aceptación

- [ ] 5 tests pasando
- [ ] 110+ tests totales frontend pasando
- [ ] Build exitoso
