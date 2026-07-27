---
status: done
type: frontend
story: docs/user-stories/015-manager-weekly-view/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Medium
complexity: M
---

# [FE] US-015 — Manager Weekly View UI

## Objetivo

Implementar la página `/manager/weekly` con vista semanal consolidada del equipo: estado de check-in/check-out, prioridades expandibles y resumen superior.

## Scope

Reemplazar el placeholder actual de `/manager/weekly/page.tsx` con la implementación real. Reutilizar hooks existentes (`useMyTeam`, `useTeamMemberCheckIn`).

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  features/teams/
    components/
      WeeklySummaryBar.tsx        # barra de resumen: N/Total check-ins, check-outs
      WeeklyMemberRow.tsx         # fila expandible por colaborador
  app/(authenticated)/manager/
    weekly/
      page.tsx                    # MODIFY — reemplazar placeholder
  tests/
    manager-weekly.test.tsx       # tests de componentes
```

---

## Componentes

### WeeklySummaryBar
Props: `{ total: number, checkins: number, checkouts: number }`
Muestra: "Check-Ins: 3/5 · Check-Outs: 2/5"

### WeeklyMemberRow
Props: `{ member: TeamMember, isExpanded: boolean, onToggle: () => void }`
- Fila con: nombre, badge check-in, badge check-out, CRS, tendencia
- Si `isExpanded` y tiene check-in → carga y muestra prioridades con `useTeamMemberCheckIn`
- Si no tiene check-in → fila no expandible, muestra alerta "Sin check-in"

### page.tsx (weekly)
- Carga `useMyTeam`
- Calcula resumen (total, checkins, checkouts)
- Renderiza `WeeklySummaryBar` + tabla con `WeeklyMemberRow` por miembro
- Estado vacío si no hay miembros

---

## Tests Requeridos (7 tests)

- `WeeklySummaryBar renders correct counts`
- `WeeklySummaryBar shows all members checked in`
- `WeeklyMemberRow renders member name and checkin badge`
- `WeeklyMemberRow shows alert when no checkin`
- `WeeklyMemberRow is not expandable without checkin`
- `WeeklyMemberRow calls onToggle when clicked with checkin`
- `WeeklyPage shows empty state when no members`

---

## Criterios de Aceptación

- [ ] `/manager/weekly` muestra tabla real (no placeholder)
- [ ] `WeeklySummaryBar` muestra conteos correctos
- [ ] Fila con check-in es expandible → muestra prioridades
- [ ] Fila sin check-in muestra alerta y no es expandible
- [ ] Estado vacío cuando no hay reportes directos
- [ ] 7 tests pasando
- [ ] 98+ tests totales frontend pasando
- [ ] Build exitoso
