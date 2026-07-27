---
id: 016-manager-individual-view
persona: Manager
fr: FR-028
bounded-context: Commitment + Reliability
status: enriched
created: 2025-01-28
enriched: 2025-01-28
---

# US-016: Manager Individual View

## [original]

**Como** manager de equipo,
**quiero** ver el perfil detallado de un colaborador individual con su CRS actual, historial de confiabilidad y check-in de la semana,
**para** preparar conversaciones 1:1 más efectivas y entender el patrón de cumplimiento de cada persona a lo largo del tiempo.

### Contexto

La ruta `/manager/team/[employeeId]` ya está implementada con CRS actual, historial CRS (tabla de semanas) y check-in de la semana actual con prioridades. Esta US formaliza la implementación existente con tests de integración (BE) y tests de componentes (FE).

### Notas iniciales
- Solo rol `manager` y `administrator` acceden a esta vista
- El empleado debe ser reporte directo del manager (BR-014)
- Reutiliza endpoints ya existentes: `GET /teams/my-team/{id}/crs` y `GET /teams/my-team/{id}/checkin`
- No requiere nuevos endpoints ni migración de base de datos
- La página ya está implementada — esta US agrega cobertura de tests

---

## [enhanced]

### User Journey

- **Usuario principal:** Manager
- **Objetivo principal:** Entender el perfil de cumplimiento de un colaborador específico
- **Flujo principal:**
  1. El manager accede a `/manager/team` (vista de equipo)
  2. Hace clic en el nombre de un colaborador → navega a `/manager/team/{employeeId}`
  3. Ve el CRS actual con badge de score y tendencia
  4. Ve el historial de CRS de las últimas 8 semanas en tabla
  5. Ve el check-in de la semana actual con prioridades y tareas
  6. Si el colaborador no hizo check-in → mensaje informativo

---

### Business Value

- **Problema que resuelve:** El manager no tiene un lugar centralizado para revisar el historial de cumplimiento de un colaborador antes de una reunión 1:1.
- **Beneficio esperado:** En una sola pantalla el manager ve: ¿cuál es el CRS actual?, ¿está mejorando o declinando?, ¿en qué se comprometió esta semana?

---

### Priority

**High**
FR-028 es el complemento directo de FR-027 (Weekly View). Cierra el loop de visibilidad del manager: de la vista agregada del equipo al detalle individual.

---

### FR de Referencia

- **FR-028** — Managers shall be able to review employee-level information
- **FR-033** — The system shall maintain historical CRS information

---

### Bounded Context

Commitment (checkin) + Reliability (CRS) → Módulos: `teams`, `crs`

---

### Endpoints Utilizados (ya implementados)

| Método | Endpoint | Uso |
|---|---|---|
| `GET` | `/api/v1/teams/my-team/{id}/crs?weeks=8` | CRS actual + historial |
| `GET` | `/api/v1/teams/my-team/{id}/checkin` | Check-in de la semana actual |

---

### Business Rules Aplicables

- **BR-014** — Un manager solo ve su equipo (validate_direct_report)
- **BR-016** — Multi-tenant: `organization_id` del JWT

---

### Diseño de la Vista

**Sección CRS:**
- Badge con score actual y nivel de riesgo
- Indicador de tendencia (↑ Mejorando / → Estable / ↓ Declinando)
- Semana de referencia
- Tabla de historial: semana | score | tendencia | riesgo

**Sección Check-In de la Semana:**
- Estado del check-in (draft / submitted)
- Lista de prioridades con título, estado, proyecto/fase
- Tareas por prioridad con estado
- Si no hay check-in → mensaje "No ha creado check-in esta semana"

---

### Acceptance Criteria

**Escenario 1 — Manager ve CRS de un colaborador**
```gherkin
Given un manager autenticado con un reporte directo con CRS calculado
When accede a /manager/team/{employeeId}
Then ve el score CRS actual con badge y tendencia
  And ve el historial de las últimas semanas en tabla
```

**Escenario 2 — Manager ve check-in de la semana**
```gherkin
Given un colaborador con check-in enviado esta semana
When el manager accede a su perfil individual
Then ve las prioridades del check-in con título y estado
```

**Escenario 3 — Colaborador sin check-in**
```gherkin
Given un colaborador que no hizo check-in esta semana
When el manager accede a su perfil individual
Then ve un mensaje informativo indicando que no hay check-in
```

**Escenario 4 — Acceso no autorizado**
```gherkin
Given un manager intentando ver un empleado que no es su reporte directo
When hace GET /teams/my-team/{id}/crs o /checkin
Then recibe 403 Forbidden
```

---

### Non-Functional Requirements

- **NFR-001** — Requiere Bearer JWT válido con rol manager o administrator
- **NFR-002** — No requiere migración de base de datos
- **NFR-003** — No requiere nuevos endpoints backend

---

### Dependencies

- **Técnicas:**
  - `GET /api/v1/teams/my-team/{id}/crs` — ya implementado ✅
  - `GET /api/v1/teams/my-team/{id}/checkin` — ya implementado ✅
  - Hooks `useTeamMemberCRS`, `useTeamMemberCheckIn` — ya implementados ✅
  - Componentes `MemberCRSHistory`, `MemberCheckInView` — ya implementados ✅
- **Funcionales:**
  - US-008 (Manager Team Visibility) — completada ✅
  - US-015 (Manager Weekly View) — completada ✅

---

### Nivel de Riesgo

**Medium**
Endpoints ya implementados y probados parcialmente en US-015. El riesgo está en la cobertura de los casos edge (sin CRS, sin check-in, acceso no autorizado).

---

### Complejidad Estimada

**S**

| Factor | Detalle |
|---|---|
| Capas afectadas | Backend (tests) + Frontend (tests) |
| Endpoints nuevos | 0 — reutiliza existentes |
| Componentes nuevos | 0 — página ya implementada |
| Migraciones | No requerida |
| Tests requeridos | Medium: 5 BE integration + 5 FE component tests |
