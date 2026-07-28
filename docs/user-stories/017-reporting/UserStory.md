---
id: 017-reporting
persona: Manager + Employee
fr: FR-029, FR-030, FR-031
bounded-context: Reliability
status: done
created: 2025-01-28
enriched: 2025-01-28
completed: 2025-01-28
pr: "#17"
merge_commit: 23dd6bc
---

# US-017: Reporting

## [original]

**Como** manager y empleado,
**quiero** acceder a reportes de cumplimiento individual, de equipo y de proyecto,
**para** entender tendencias de ejecución, identificar patrones de riesgo y tomar decisiones informadas sobre el equipo.

### Contexto

El módulo `reporting` no existe. Requiere implementación completa: backend (módulo FastAPI con 3 endpoints) y frontend (3 páginas de reporte). Los datos ya existen en las tablas de `priorities`, `checkins`, `checkouts` y `crs_scores`.

### Notas iniciales
- 3 endpoints nuevos: reporte individual, de equipo y de proyecto
- Manager accede a reportes de equipo y proyecto; employee solo al propio
- Los reportes son de solo lectura — no modifican datos
- No requiere migración de base de datos — consulta tablas existentes

---

## [enhanced]

### User Journey

**Manager:**
1. Accede a `/manager/reports` → ve reporte de equipo (cumplimiento promedio, tendencia semanal, top performers, miembros en riesgo)
2. Accede a `/manager/reports/project/{id}` → ve reporte de proyecto (prioridades activas/completadas por fase, cumplimiento)

**Employee:**
1. Accede a `/employee/reports` → ve su reporte individual (historial de prioridades, tasa de cumplimiento, evolución CRS)

---

### Business Value

- **Problema:** No hay forma de ver tendencias históricas de cumplimiento más allá del CRS puntual.
- **Beneficio:** Managers identifican patrones (quién mejora, quién declina, qué proyectos concentran riesgos). Employees ven su propio historial de cumplimiento.

---

### Priority

**High** — FR-029, FR-030, FR-031 son requerimientos core del MVP.

---

### FR de Referencia

- **FR-029** — The system shall generate employee reports
- **FR-030** — The system shall generate team reports
- **FR-031** — The system shall generate project reports

---

### Bounded Context

Reliability → Módulo nuevo: `reporting`

---

### Endpoints Nuevos

| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| `GET` | `/api/v1/reports/individual` | employee, manager, administrator | Reporte del empleado autenticado |
| `GET` | `/api/v1/reports/team` | manager, administrator | Reporte del equipo del manager |
| `GET` | `/api/v1/reports/project/{project_id}` | manager, administrator | Reporte de un proyecto |

---

### Schemas de Respuesta

**IndividualReport**
```json
{
  "employee": { "id": "uuid", "first_name": "Ana", "last_name": "García" },
  "period_weeks": 8,
  "total_priorities": 24,
  "completed_priorities": 20,
  "completion_rate": 83.3,
  "carried_over_count": 4,
  "crs_current": 85.0,
  "crs_trend": "stable",
  "weekly_breakdown": [
    { "week_start": "2025-01-06", "committed": 3, "completed": 3, "carried_over": 0, "crs": 92.0 }
  ]
}
```

**TeamReport**
```json
{
  "team_size": 5,
  "period_weeks": 8,
  "avg_completion_rate": 78.5,
  "avg_crs": 81.2,
  "members": [
    { "id": "uuid", "first_name": "Ana", "last_name": "García", "completion_rate": 90.0, "crs": 88.0, "trend": "improving" }
  ],
  "weekly_breakdown": [
    { "week_start": "2025-01-06", "checkins_submitted": 4, "checkouts_submitted": 3, "avg_completion": 80.0 }
  ]
}
```

**ProjectReport**
```json
{
  "project": { "id": "uuid", "name": "CRM Implementation", "status": "active" },
  "period_weeks": 8,
  "total_priorities": 45,
  "completed_priorities": 38,
  "completion_rate": 84.4,
  "phases": [
    { "id": "uuid", "name": "Desarrollo", "total_priorities": 20, "completed_priorities": 18, "completion_rate": 90.0 }
  ]
}
```

---

### Business Rules Aplicables

- **BR-013** — Employee solo ve su propio reporte individual
- **BR-014** — Manager solo ve su equipo
- **BR-016** — Multi-tenant: `organization_id` del JWT
- **BR-017** — Todos los aggregates pertenecen a una organización

---

### Acceptance Criteria

**Escenario 1 — Employee ve su reporte individual**
```gherkin
Given un employee autenticado con check-ins previos
When hace GET /api/v1/reports/individual
Then recibe su tasa de cumplimiento y breakdown semanal
```

**Escenario 2 — Manager ve reporte de equipo**
```gherkin
Given un manager con reportes directos
When hace GET /api/v1/reports/team
Then recibe cumplimiento promedio y detalle por miembro
```

**Escenario 3 — Manager ve reporte de proyecto**
```gherkin
Given un proyecto con prioridades en múltiples fases
When hace GET /api/v1/reports/project/{id}
Then recibe cumplimiento total y desglose por fase
```

**Escenario 4 — Employee no puede ver reporte de equipo**
```gherkin
Given un employee autenticado
When hace GET /api/v1/reports/team
Then recibe 403 Forbidden
```

---

### Non-Functional Requirements

- **NFR-001** — Requiere Bearer JWT válido
- **NFR-002** — No requiere migración de base de datos
- **NFR-003** — Parámetro `?weeks=N` (default 8, max 52) para controlar el período

---

### Dependencies

- **Técnicas:**
  - Tablas existentes: `priorities`, `checkins`, `checkouts`, `crs_scores`, `projects`, `project_phases`
  - Módulos existentes: `crs`, `checkin`, `checkout`, `priorities`, `projects`
- **Funcionales:**
  - US-001 (Check-In) ✅, US-003 (Check-Out) ✅, US-007 (CRS) ✅

---

### Nivel de Riesgo

**Medium** — Solo lectura, sin modificación de datos. Riesgo en queries de agregación multi-tabla.

---

### Complejidad Estimada

**L**

| Factor | Detalle |
|---|---|
| Capas afectadas | Backend (módulo nuevo) + Frontend (3 páginas nuevas) |
| Endpoints nuevos | 3 |
| Módulo backend nuevo | `reporting` completo (router, schemas, queries) |
| Páginas frontend nuevas | `/employee/reports`, `/manager/reports`, `/manager/reports/project/[id]` |
| Migraciones | No requerida |
| Tests requeridos | Medium: 6 BE integration + 6 FE component tests |
