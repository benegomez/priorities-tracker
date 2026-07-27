---
id: 015-manager-weekly-view
persona: Manager
fr: FR-027
bounded-context: Commitment + Reliability
status: done
created: 2025-01-28
enriched: 2025-01-28
completed: 2025-01-28
pr: "#15"
merge-commit: 83bbf0f
---

# US-015: Manager Weekly View

## [original]

**Como** manager de equipo,
**quiero** ver una vista semanal consolidada de mi equipo con el estado de check-ins, prioridades y riesgos de cada colaborador,
**para** identificar rápidamente quién está al día, qué compromisos están en riesgo y dónde necesito intervenir sin tener que revisar a cada persona individualmente.

### Contexto

La página `/manager/weekly` existe pero es un placeholder. El backend ya expone `GET /api/v1/teams/my-team` con el estado semanal de cada miembro (check-in status, checkout status, CRS). El endpoint `GET /api/v1/teams/my-team/{id}/checkin` permite ver las prioridades de un miembro específico.

Esta US implementa la vista semanal real: una tabla expandible donde el manager ve el estado de toda la semana de su equipo de un vistazo.

### Notas iniciales
- Solo rol `manager` y `administrator` acceden a esta vista
- Usa endpoints ya existentes — no requiere nuevos endpoints backend
- La vista muestra: nombre, estado check-in, estado check-out, cantidad de prioridades, CRS
- Al expandir una fila se muestran las prioridades del colaborador para la semana
- No requiere migración de base de datos

---

## [enhanced]

### User Journey

- **Usuario principal:** Manager
- **Objetivo principal:** Obtener visibilidad semanal del equipo en menos de 2 minutos
- **Flujo principal:**
  1. El manager accede a `/manager/weekly`
  2. Ve una tabla con todos sus reportes directos y su estado semanal
  3. Identifica de un vistazo quién hizo check-in, quién hizo check-out, CRS de cada uno
  4. Expande la fila de un colaborador para ver sus prioridades de la semana
  5. Identifica prioridades en riesgo (status `in_progress` o `planned` con check-out ya enviado)

---

### Business Value

- **Problema que resuelve:** El manager no tiene una vista consolidada de la semana — debe entrar al perfil de cada colaborador individualmente.
- **Beneficio esperado:** En una sola pantalla el manager responde: ¿quién cumplió?, ¿qué está en riesgo?, ¿quién no hizo check-in?

---

### Priority

**High**
FR-027 es un requerimiento core del manager. La vista semanal es la segunda pantalla más importante después del dashboard de equipo.

---

### FR de Referencia

- **FR-027** — Managers shall be able to review weekly activity across the team

---

### Bounded Context

Commitment (checkin) + Reliability (CRS) → Módulos: `teams`, `checkin`

---

### Endpoints Utilizados (ya implementados)

| Método | Endpoint | Uso |
|---|---|---|
| `GET` | `/api/v1/teams/my-team` | Lista de miembros con CRS y week_status |
| `GET` | `/api/v1/teams/my-team/{id}/checkin` | Prioridades del check-in de un miembro |

---

### Business Rules Aplicables

- **BR-014** — Un manager solo ve su equipo
- **BR-016** — Multi-tenant: `organization_id` del JWT

---

### Diseño de la Vista

**Tabla principal** — una fila por colaborador:

| Colaborador | Check-In | Check-Out | Prioridades | CRS | Tendencia |
|---|---|---|---|---|---|
| Ana García | ✅ Enviado | ✅ Enviado | 4 | 87 | ↑ |
| Juan López | ✅ Enviado | ⏳ Pendiente | 3 | 72 | → |
| María Pérez | ❌ Sin check-in | — | — | 65 | ↓ |

**Fila expandible** — al hacer clic en una fila con check-in:
- Lista de prioridades con título, estado y proyecto/fase
- Badge de estado por prioridad (completed, in_progress, planned, carried_over)

**Resumen superior:**
- Total miembros
- Hicieron check-in: N/Total
- Hicieron check-out: N/Total
- Prioridades en riesgo (in_progress sin check-out)

---

### Acceptance Criteria

**Escenario 1 — Manager ve estado semanal**
```gherkin
Given un manager autenticado con reportes directos
When accede a /manager/weekly
Then ve una tabla con todos sus reportes directos
  And cada fila muestra check-in status, check-out status y CRS
```

**Escenario 2 — Manager expande prioridades**
```gherkin
Given un colaborador con check-in enviado
When el manager hace clic en su fila
Then se expanden las prioridades de esa semana
  And cada prioridad muestra título, estado y proyecto
```

**Escenario 3 — Colaborador sin check-in**
```gherkin
Given un colaborador que no hizo check-in esta semana
When el manager ve la tabla
Then la fila muestra "Sin check-in" en estado de alerta
  And la fila no es expandible
```

**Escenario 4 — Equipo vacío**
```gherkin
Given un manager sin reportes directos
When accede a /manager/weekly
Then ve un mensaje indicando que no tiene equipo asignado
```

---

### Non-Functional Requirements

- **NFR-001** — Requiere Bearer JWT válido con rol manager o administrator
- **NFR-002** — No requiere migración de base de datos
- **NFR-003** — No requiere nuevos endpoints backend

---

### Dependencies

- **Técnicas:**
  - `GET /api/v1/teams/my-team` — ya implementado ✅
  - `GET /api/v1/teams/my-team/{id}/checkin` — ya implementado ✅
  - Hooks `useMyTeam`, `useTeamMemberCheckIn` — ya implementados ✅
- **Funcionales:**
  - US-008 (Manager Team Visibility) — completada ✅
  - US-001 (Weekly Check-In) — completada ✅

---

### Nivel de Riesgo

**Medium**
No hay cambios de backend. El riesgo está en la UX de la vista expandible y el manejo de estados vacíos.

---

### Complejidad Estimada

**M**

| Factor | Detalle |
|---|---|
| Capas afectadas | Frontend únicamente |
| Endpoints nuevos | 0 — reutiliza existentes |
| Componentes nuevos | WeeklyMemberRow, WeeklyPrioritiesExpanded, WeeklySummaryBar |
| Hooks nuevos | useWeeklyView (orquesta useMyTeam + useTeamMemberCheckIn lazy) |
| Migraciones | No requerida |
| Tests requeridos | Medium: 6+ component tests |
