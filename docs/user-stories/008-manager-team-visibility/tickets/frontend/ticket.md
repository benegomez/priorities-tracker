---
status: done
type: frontend
story: docs/user-stories/008-manager-team-visibility/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: High
complexity: M
---

# [FE] US-008 — Manager Team Dashboard UI

## Objetivo

Implementar las páginas `/manager/team` (lista del equipo con CRS y estado semanal) y `/manager/team/[id]` (detalle de un empleado con historial CRS y check-in read-only) para que el manager tenga visibilidad consolidada de su equipo.

## Scope

2 páginas nuevas, servicios API, hooks TanStack Query, componentes de tabla y detalle. Sin lógica de escritura (todo read-only).

## Dependencia

Endpoints backend disponibles (ticket BE mergeado).

---

## Contrato API Consumido

| Método | Endpoint | Propósito |
|---|---|---|
| GET | `/api/v1/teams/my-team` | Lista de reportes directos con CRS + week status |
| GET | `/api/v1/teams/my-team/{id}/crs` | Historial CRS de un empleado |
| GET | `/api/v1/teams/my-team/{id}/checkin` | Check-in semanal de un empleado (read-only) |

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  app/(authenticated)/manager/team/
    page.tsx                              - CREATE (tabla del equipo)
    loading.tsx                           - CREATE
    [employeeId]/
      page.tsx                            - CREATE (detalle empleado)
      loading.tsx                         - CREATE

  features/teams/
    services/
      team-service.ts                     - CREATE (API client)
    hooks/
      useMyTeam.ts                        - CREATE (useQuery)
      useTeamMemberCRS.ts                 - CREATE (useQuery)
      useTeamMemberCheckIn.ts             - CREATE (useQuery)
    components/
      TeamTable.tsx                       - CREATE (tabla principal)
      TeamMemberRow.tsx                   - CREATE (fila con CRS + badges)
      TeamCRSBadge.tsx                    - CREATE (score + color)
      TeamWeekStatusBadge.tsx             - CREATE (badge check-in/check-out)
      TeamEmptyState.tsx                  - CREATE (sin miembros)
      MemberCRSHistory.tsx                - CREATE (tabla historial)
      MemberCheckInView.tsx              - CREATE (prioridades read-only)
```

---

## Flujo de UI

```
/manager/team
    ↓ useMyTeam()
    ├── 200 (members.length > 0) → TeamTable
    │     ├── TeamMemberRow por cada miembro
    │     │     ├── Nombre (link a detalle)
    │     │     ├── TeamCRSBadge (score + color) o "—" si null
    │     │     ├── TrendIndicator (↑/→/↓)
    │     │     ├── TeamWeekStatusBadge (check-in)
    │     │     └── TeamWeekStatusBadge (check-out)
    │     └── Click en fila → navigate to /manager/team/{id}
    │
    └── 200 (members.length === 0) → TeamEmptyState

/manager/team/[employeeId]
    ↓ useTeamMemberCRS(employeeId) + useTeamMemberCheckIn(employeeId)
    ├── Sección 1: CRS del empleado
    │     ├── Score actual (CRSScoreCard reutilizado o inline)
    │     └── MemberCRSHistory (tabla últimas 8 semanas)
    │
    └── Sección 2: Check-In de la semana
          ├── 200 → MemberCheckInView (prioridades + tareas read-only)
          └── 404 → Mensaje "No ha creado check-in esta semana"
```

---

## Componentes UI

| Componente | Elementos | Comportamiento |
|---|---|---|
| `TeamTable` | Table, thead, tbody | Tabla con columnas: Nombre, CRS, Tendencia, Check-In, Check-Out |
| `TeamMemberRow` | tr, td, Link, badges | Fila clickeable que navega a detalle |
| `TeamCRSBadge` | Badge con número | Color: green (low), orange (moderate), red (high). "—" si null |
| `TeamWeekStatusBadge` | Badge | Verde "Enviado", amarillo "Borrador", gris "Sin crear" |
| `TeamEmptyState` | Card con mensaje | "No tienes miembros en tu equipo" |
| `MemberCRSHistory` | Table | Semana, Score, Tendencia, Riesgo (últimas 8 semanas) |
| `MemberCheckInView` | Cards read-only | Prioridades con tareas, sin checkboxes ni edición |

---

## Service (API Client)

```typescript
// features/teams/services/team-service.ts

export interface TeamMemberCRS {
  score: number;
  trend: string;
  risk_level: string;
}

export interface TeamMemberWeekStatus {
  week_start: string;
  checkin_status: string | null;
  checkout_status: string | null;
}

export interface TeamMember {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  crs: TeamMemberCRS | null;
  week_status: TeamMemberWeekStatus;
}

export interface TeamOverviewResponse {
  members: TeamMember[];
}

export interface TeamMemberCRSResponse {
  employee: { id: string; first_name: string; last_name: string };
  current: { score: number; trend: string; risk_level: string; week_start: string } | null;
  history: Array<{ week_start: string; score: number; trend: string; risk_level: string }>;
}

// Functions:
// getMyTeam(): Promise<TeamOverviewResponse>
// getTeamMemberCRS(employeeId: string, weeks?: number): Promise<TeamMemberCRSResponse>
// getTeamMemberCheckIn(employeeId: string): Promise<CheckInResponse>
```

---

## Hooks (TanStack Query)

| Hook | Query Key | Endpoint |
|---|---|---|
| `useMyTeam` | `["teams", "my-team"]` | GET /teams/my-team |
| `useTeamMemberCRS` | `["teams", "member-crs", employeeId]` | GET /teams/my-team/{id}/crs |
| `useTeamMemberCheckIn` | `["teams", "member-checkin", employeeId]` | GET /teams/my-team/{id}/checkin |

---

## Reutilización de Componentes Existentes

| Componente existente | Reutilización |
|---|---|
| `CRSTrendIndicator` | Reutilizar en TeamMemberRow para mostrar flecha |
| `CRSHistoryChart` | Reutilizar o adaptar para MemberCRSHistory |
| `CheckInPriorityCard` | Reutilizar en MemberCheckInView (modo read-only) |
| `Badge` (shadcn/ui) | Para status badges |

---

## Navegación

La ruta `/manager/team` ya existe como placeholder. Reemplazar el placeholder con la implementación real.

Verificar en `config/navigation.ts` que "Mi Equipo" → "Vista de Equipo" apunta a `/manager/team`.

---

## Manejo de Errores

| Error API | Comportamiento UI |
|---|---|
| `403` en /my-team | Redirect o mensaje "No tienes permisos" |
| `403` en /member/crs | Toast: "No tienes acceso a este empleado" + redirect back |
| `404` en /member/checkin | Mostrar inline: "No ha creado check-in esta semana" |
| `401` | Redirect a `/auth/login` (middleware) |

---

## Tests Requeridos

### Component Tests (vitest + @testing-library/react)

- [ ] `test_TeamTable_renders_member_rows`
- [ ] `test_TeamTable_shows_empty_state_when_no_members`
- [ ] `test_TeamMemberRow_renders_name_and_crs`
- [ ] `test_TeamMemberRow_shows_dash_when_no_crs`
- [ ] `test_TeamCRSBadge_shows_correct_color_for_risk_level`
- [ ] `test_TeamWeekStatusBadge_shows_submitted_green`
- [ ] `test_TeamWeekStatusBadge_shows_null_as_gray`
- [ ] `test_MemberCRSHistory_renders_history_rows`
- [ ] `test_MemberCheckInView_renders_priorities_readonly`
- [ ] `test_team_page_navigates_to_detail_on_click`

---

## Accesibilidad (WCAG 2.1 AA)

- [ ] Tabla con `<thead>` y `scope="col"` en headers
- [ ] Filas clickeables con `role="link"` o wrapping `<Link>`
- [ ] Badges con texto (no solo color para indicar estado)
- [ ] Score con aria-label descriptivo
- [ ] Navegación por teclado en la tabla

---

## Criterios de Aceptación

- [ ] `/manager/team` muestra tabla con reportes directos
- [ ] Cada fila muestra: nombre, CRS (score + color), tendencia, estado check-in, estado check-out
- [ ] Click en fila navega a `/manager/team/{id}`
- [ ] Detalle muestra historial CRS + check-in de la semana (read-only)
- [ ] Empty state cuando no hay miembros
- [ ] Mensaje cuando empleado no tiene check-in
- [ ] Responsive (tabla scrollable en mobile)
- [ ] No hay acciones de escritura (todo read-only)
- [ ] `npm run build` sin errores
- [ ] `npm test` — todos los tests pasan

---

## Git Branch

`feature/008-manager-team-visibility`
