---
id: 018-manager-team-crs
persona: Manager
fr: FR-025, FR-026
bounded-context: Reliability
status: enriched
created: 2025-01-28
enriched: 2025-01-28
---

# US-018: Manager Team CRS View

## [original]

**Como** manager,
**quiero** ver el Commitment Reliability Score de todos los miembros de mi equipo en una sola vista,
**para** identificar rápidamente quién está en riesgo, quién mejora y cuál es la confiabilidad general del equipo.

### Contexto

El menú de navegación del manager incluye "CRS del Equipo" (`/manager/crs`) pero la página no existe — actualmente produce un 404. Los datos necesarios ya están disponibles: el endpoint `GET /api/v1/reports/team` retorna `members[]` con `crs`, `trend` y `completion_rate` por miembro, y `avg_crs` del equipo. No se requieren endpoints nuevos.

### Notas iniciales
- Solo lectura — no modifica datos
- No requiere endpoints nuevos (reutiliza `GET /api/v1/reports/team`)
- Reutiliza componentes existentes: `CRSTrendIndicator`, `TeamCRSBadge`, `ReportStatCard`
- La página ya tiene entrada en el menú de navegación

---

## [enhanced]

### User Journey

1. El manager hace clic en "CRS del Equipo" en el menú lateral
2. Ve un resumen del equipo: CRS promedio, cantidad de miembros en riesgo alto, tendencia general
3. Ve una tabla con cada miembro: nombre, CRS actual, nivel de riesgo, tendencia, tasa de cumplimiento
4. La tabla está ordenada por CRS ascendente (los de mayor riesgo primero)
5. Al hacer clic en un miembro, navega a `/manager/team/[employeeId]` (vista individual ya existente)

---

### Business Value

- **Problema:** El manager no tiene una vista consolidada de confiabilidad del equipo. Debe revisar cada miembro individualmente en `/manager/team`.
- **Beneficio:** En una sola pantalla el manager identifica quién requiere atención, quién mejora y cuál es el estado general de confiabilidad del equipo.

---

### FR de Referencia

- **FR-025** — Managers can view team CRS scores
- **FR-026** — Managers can identify team members at risk

---

### Bounded Context

Reliability → Frontend only (no nuevos endpoints)

---

### Datos Disponibles (sin endpoints nuevos)

`GET /api/v1/reports/team?weeks=8` retorna:
```json
{
  "team_size": 5,
  "avg_crs": 81.2,
  "members": [
    {
      "id": "uuid",
      "first_name": "Ana",
      "last_name": "García",
      "completion_rate": 90.0,
      "crs": 88.0,
      "trend": "improving"
    }
  ]
}
```

---

### Business Rules Aplicables

- **BR-014** — Manager solo ve su equipo
- **BR-016** — Multi-tenant: `organization_id` del JWT

---

### Diseño de la Página `/manager/crs`

**Header:**
- Título: "CRS del Equipo"

**Stats (3 tarjetas `ReportStatCard`):**
- CRS Promedio del equipo (`avg_crs`)
- Miembros en riesgo alto (count donde `crs < 60` o `crs == null`)
- Total de miembros (`team_size`)

**Tabla de miembros** (ordenada por CRS ascendente — mayor riesgo primero):

| Miembro | CRS | Nivel | Tendencia | Cumplimiento |
|---|---|---|---|---|
| Ana García | 88.0 | 🟢 Confiable | ↑ Mejorando | 90% |
| Juan López | 54.0 | 🔴 Riesgo Alto | ↓ Declinando | 62% |

- Clic en fila → navega a `/manager/team/[id]`
- Miembros sin CRS calculado muestran "—" con badge gris "Sin datos"

**Empty state:** cuando el equipo no tiene miembros o no hay datos CRS.

---

### Acceptance Criteria

**Escenario 1 — Manager ve CRS del equipo**
```gherkin
Given un manager autenticado con equipo de 4 miembros
When navega a /manager/crs
Then ve CRS promedio del equipo
  And ve tabla con CRS individual de cada miembro
  And la tabla está ordenada por CRS ascendente
```

**Escenario 2 — Miembro sin CRS**
```gherkin
Given un miembro del equipo sin check-outs registrados
When el manager ve la tabla de CRS
Then ese miembro aparece con "—" en la columna CRS
  And aparece badge "Sin datos"
```

**Escenario 3 — Clic en miembro navega a vista individual**
```gherkin
Given la tabla de CRS del equipo
When el manager hace clic en una fila
Then navega a /manager/team/[employeeId]
```

**Escenario 4 — Empty state sin miembros**
```gherkin
Given un manager sin miembros en su equipo
When navega a /manager/crs
Then ve un mensaje indicando que no hay miembros en el equipo
```

---

### Non-Functional Requirements

- **NFR-001** — Requiere Bearer JWT válido con rol `manager` o `administrator`
- **NFR-002** — No requiere endpoints nuevos — reutiliza `GET /api/v1/reports/team`
- **NFR-003** — Loading skeleton mientras carga

---

### Dependencies

- **Técnicas:**
  - Hook existente: `useTeamReport` (`features/reports/hooks/useTeamReport.ts`)
  - Componentes existentes: `CRSTrendIndicator`, `TeamCRSBadge`, `ReportStatCard`, `TeamEmptyState`
  - Navegación existente: entrada "CRS del Equipo" ya en `navigation.ts`
  - Página destino: `/manager/team/[employeeId]` ya implementada (US-016)
- **Funcionales:**
  - US-016 (Manager Individual View) ✅
  - US-017 (Reporting — `useTeamReport`) ✅

---

### Nivel de Riesgo

**Low** — Solo frontend, sin endpoints nuevos, reutiliza hooks y componentes existentes.

---

### Complejidad Estimada

**S**

| Factor | Detalle |
|---|---|
| Capas afectadas | Frontend únicamente |
| Endpoints nuevos | 0 |
| Páginas nuevas | 1 (`/manager/crs/page.tsx`) |
| Componentes nuevos | 0 (reutiliza existentes) |
| Migraciones | No requerida |
| Tests requeridos | Low: 4 component tests |
