---
us: 019-manager-checkin-history
status: pending
---

# Plan de Implementación — US-019

## Orden de ejecución

```
BE ticket → FE ticket → tests → PR
```

---

## Ticket BE-019: Extender endpoint checkin con week_start

**Archivo:** `apps/backend/src/modules/teams/api/router.py`

- Agregar query param `week_start: date | None = None` al endpoint `GET /my-team/{employee_id}/checkin`
- Si `week_start` es None → usar `_get_current_week_start()` (comportamiento actual)
- Si se pasa → usar el valor recibido
- Sin cambios en repositorio ni schemas

---

## Ticket FE-019: Vista interactiva de historial + check-in por semana

### 1. Hook `useTeamMemberCheckIn` — agregar parámetro `weekStart`

**Archivo:** `apps/frontend/src/features/teams/hooks/useTeamMemberCheckIn.ts`

- Agregar param `weekStart?: string`
- Incluir en query key y en la URL como `?week_start=YYYY-MM-DD`

### 2. Componente `MemberCRSHistory` — hacer filas clickeables

**Archivo:** `apps/frontend/src/features/teams/components/MemberCRSHistory.tsx`

- Agregar props `selectedWeek?: string` y `onSelectWeek?: (week: string) => void`
- Fila seleccionada → `bg-primary/10 ring-1 ring-primary/20`
- Cursor pointer en filas, hover highlight

### 3. Página `[employeeId]/page.tsx` — estado de semana seleccionada

**Archivo:** `apps/frontend/src/app/(authenticated)/manager/team/[employeeId]/page.tsx`

- Estado local `selectedWeek` inicializado con la semana actual del CRS
- Pasar `selectedWeek` y `onSelectWeek` a `MemberCRSHistory`
- Pasar `selectedWeek` a `useTeamMemberCheckIn`
- Actualizar título de la sección check-in con la semana seleccionada

---

## Tests

### Backend (3 integration tests)
- `test_get_team_member_checkin_with_week_start` — retorna check-in de semana específica
- `test_get_team_member_checkin_week_start_not_found` — 404 si no existe
- `test_get_team_member_checkin_week_start_unauthorized` — 403 si no es reporte directo

### Frontend (4 tests)
- `MemberCRSHistory` — fila clickeable llama `onSelectWeek`
- `MemberCRSHistory` — fila seleccionada tiene clase de highlight
- `TeamMemberDetailPage` — seleccionar semana actualiza el check-in mostrado
- `useTeamMemberCheckIn` — incluye week_start en query key y URL
