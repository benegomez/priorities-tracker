---
id: 019-manager-checkin-history
persona: Manager
fr: FR-028
bounded-context: Commitment + Reliability
status: pending
created: 2025-07-28
enriched: 2025-07-28
---

# US-019: Manager — Historial de Check-Ins por Semana

## [original]

**Como** manager de equipo,
**quiero** ver el historial semanal de un colaborador y poder hacer clic en cualquier semana para ver el detalle de su check-in (prioridades y tareas),
**para** entender el patrón de trabajo de la persona a lo largo del tiempo y preparar conversaciones 1:1 con contexto histórico real.

### Contexto

La vista `/manager/team/[employeeId]` ya muestra el CRS histórico en tabla (semana, score, tendencia, riesgo) y el check-in de la semana actual. Esta US extiende esa vista para que cada fila del historial sea clickeable y muestre el check-in de esa semana específica, reemplazando la sección "Check-In de la Semana" con el detalle de la semana seleccionada.

### Notas iniciales
- El historial CRS ya existe (`MemberCRSHistory`) — se convierte en interactivo
- El backend solo tiene `GET /teams/my-team/{id}/checkin` para la semana actual — necesita un nuevo endpoint que acepte `week_start` como query param
- La semana actual se selecciona por defecto al cargar la página
- No requiere migración de base de datos

---

## [enhanced]

### User Journey

- **Usuario principal:** Manager
- **Objetivo principal:** Revisar el check-in de cualquier semana pasada de un colaborador
- **Flujo principal:**
  1. El manager está en `/manager/team/{employeeId}`
  2. Ve la tabla de historial CRS con las últimas 8 semanas
  3. Hace clic en una fila de semana → la fila se resalta como seleccionada
  4. La sección inferior muestra el check-in de esa semana: prioridades, estado, tareas
  5. Si no hay check-in para esa semana → mensaje informativo
  6. La semana actual está seleccionada por defecto al cargar

---

### Business Value

- **Problema que resuelve:** El manager solo puede ver el check-in de la semana actual. Para preparar una 1:1 necesita contexto de semanas anteriores — qué se comprometió, qué completó, qué arrastró.
- **Beneficio esperado:** El manager puede navegar el historial completo de compromisos de un colaborador sin salir de la pantalla, con el CRS y el check-in de cada semana correlacionados visualmente.

---

### Priority

**High**
Extiende directamente US-016 (ya completada). Cierra el loop de visibilidad histórica que el CRS por sí solo no da — el score dice "cuánto cumplió", el check-in dice "qué se comprometió".

---

### FR de Referencia

- **FR-028** — Managers shall be able to review employee-level information
- **FR-033** — The system shall maintain historical CRS information

---

### Bounded Context

Commitment (checkin) → Módulos: `teams`, `checkin`

---

### Endpoints

| Método | Endpoint | Estado | Descripción |
|---|---|---|---|
| `GET` | `/api/v1/teams/my-team/{id}/crs?weeks=8` | ✅ existente | CRS actual + historial |
| `GET` | `/api/v1/teams/my-team/{id}/checkin?week_start=YYYY-MM-DD` | 🆕 nuevo | Check-in de una semana específica |

El endpoint nuevo es una extensión del existente: agrega `week_start` como query param opcional. Si no se pasa, usa la semana actual (comportamiento actual preservado).

---

### Business Rules Aplicables

- **BR-014** — Un manager solo ve su equipo (`validate_direct_report`)
- **BR-016** — Multi-tenant: `organization_id` del JWT

---

### Diseño de la Vista

**Tabla de historial CRS (interactiva):**
- Mismas columnas: Semana | Score | Tendencia | Riesgo
- Cada fila es clickeable → cursor pointer, hover highlight
- Fila seleccionada → fondo resaltado (ring o bg-primary/10)
- Semana actual seleccionada por defecto

**Sección Check-In (dinámica):**
- Título: "Check-In — Semana {week_start seleccionada}"
- Loading skeleton mientras carga
- Si hay check-in → `MemberCheckInView` (componente existente)
- Si no hay check-in → "No hay check-in registrado para esta semana"

---

### Acceptance Criteria

**Escenario 1 — Semana actual seleccionada por defecto**
```gherkin
Given un manager en /manager/team/{employeeId}
When la página carga
Then la semana actual está seleccionada en la tabla de historial
  And el check-in de la semana actual se muestra en la sección inferior
```

**Escenario 2 — Manager selecciona una semana pasada**
```gherkin
Given un manager viendo el historial de un colaborador
When hace clic en una fila de semana pasada
Then esa fila queda resaltada como seleccionada
  And la sección inferior muestra el check-in de esa semana
  And el título de la sección refleja la semana seleccionada
```

**Escenario 3 — Semana sin check-in**
```gherkin
Given una semana en el historial sin check-in registrado
When el manager hace clic en esa fila
Then ve el mensaje "No hay check-in registrado para esta semana"
```

**Escenario 4 — Endpoint con week_start**
```gherkin
Given un manager autenticado
When hace GET /teams/my-team/{id}/checkin?week_start=2025-06-30
Then recibe el check-in de esa semana con prioridades y tareas
  And si no existe retorna 404
```

**Escenario 5 — Acceso no autorizado**
```gherkin
Given un manager intentando ver un empleado que no es su reporte directo
When hace GET /teams/my-team/{id}/checkin?week_start=...
Then recibe 403 Forbidden
```

---

### Non-Functional Requirements

- **NFR-001** — Requiere Bearer JWT válido con rol manager o administrator
- **NFR-002** — No requiere migración de base de datos
- **NFR-003** — El cambio al endpoint existente es backward-compatible (week_start opcional)

---

### Dependencies

- **Técnicas:**
  - US-016 completada ✅ — página `/manager/team/[employeeId]` existente
  - `MemberCRSHistory` existente — se extiende para ser interactivo
  - `MemberCheckInView` existente — se reutiliza sin cambios
  - `useTeamMemberCheckIn` existente — se extiende para aceptar `week_start`
- **Funcionales:**
  - US-008 ✅, US-015 ✅, US-016 ✅

---

### Nivel de Riesgo

**Medium**

---

### Complejidad Estimada

**S**

| Factor | Detalle |
|---|---|
| Capas afectadas | Backend (1 endpoint modificado) + Frontend (2 componentes + 1 hook + 1 página) |
| Endpoints nuevos | 0 nuevos — 1 modificado (week_start opcional) |
| Componentes nuevos | 0 — reutiliza existentes, extiende MemberCRSHistory |
| Migraciones | No requerida |
| Tests requeridos | Medium: 3 BE integration + 4 FE component/hook tests |
