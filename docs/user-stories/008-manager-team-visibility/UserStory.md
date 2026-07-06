---
id: US-008
title: Manager Team Visibility — CRS & Check-Ins
status: enriched
priority: high
risk_level: High
complexity: L
created: 2026-07-06
---

# US-008 — Manager Team Visibility: CRS & Check-Ins

## [original]

**Como** manager de equipo,
**quiero** ver el CRS de cada miembro de mi equipo y el estado de sus check-ins semanales,
**para** tener visibilidad del cumplimiento y la actividad de mi equipo sin necesidad de preguntar individualmente ni hacer microgestión.

### Contexto

Actualmente el manager puede acceder a las rutas de empleado (check-in, check-out, CRS propio), pero no tiene una vista consolidada de su equipo. La relación manager→empleados ya existe en la BD (`users.manager_id`). El CRS individual ya se calcula y persiste. Falta exponer endpoints que permitan al manager consultar datos de sus reportes directos, y una UI que los presente de forma clara.

### Notas iniciales
- La tabla `users` tiene `manager_id` que define la relación jerárquica
- BR-014: Un manager solo ve sus equipos
- BR-016: Multi-tenant (organization_id siempre del JWT)
- FR-026: Team Dashboard
- FR-027: Weekly View
- FR-028: Individual View
- El manager NO puede modificar datos de sus empleados (solo lectura)

---

## [enhanced]

### User Journey

- **Usuario principal:** Manager de Equipo
- **Usuarios secundarios:** Administrator (puede ver todos los equipos — futuro)
- **Flujo principal:**
  1. Manager accede a `/manager/team`
  2. Ve una tabla con sus reportes directos:
     - Nombre del empleado
     - CRS actual (score numérico + badge de riesgo con color)
     - Tendencia (flecha ↑/→/↓)
     - Estado del check-in de la semana (badge: sin crear / borrador / enviado)
     - Estado del check-out de la semana (badge: sin crear / borrador / enviado)
  3. Puede hacer click en un empleado para ver detalle (`/manager/team/{id}`)
  4. En la vista de detalle ve:
     - Historial CRS (tabla con últimas 8 semanas)
     - Check-in de la semana actual (prioridades con tareas, read-only)

---

### Business Value

- **Problema que resuelve:** El manager no tiene forma de saber en qué se comprometió su equipo ni qué tan confiables son sin preguntar uno por uno. Esto genera reuniones de status innecesarias y falta de preparación para 1:1s.
- **Beneficio esperado:** El manager obtiene en menos de 2 minutos una foto completa del estado de su equipo: quién hizo check-in, quién cumple consistentemente (CRS alto), y quién necesita atención (CRS bajo o sin actividad).
- **Métrica de éxito:** Manager puede preparar un 1:1 en <5 minutos usando solo la información de la plataforma.

---

### FR de Referencia

- **FR-026** — Team Dashboard
- **FR-027** — Weekly View (estado check-in/check-out de la semana)
- **FR-028** — Individual View (detalle de un empleado)
- **FR-033** — CRS History (historial por empleado)

---

### Bounded Contexts

- **Organization** → consulta de reportes directos (`users.manager_id`)
- **Reliability** → CRS del equipo
- **Commitment** → check-ins del equipo

---

### Contrato API

#### GET /api/v1/teams/my-team

Retorna los reportes directos del manager autenticado con su estado semanal.

```
Auth: Bearer JWT (role: manager, administrator)
operation_id: get_my_team

Response 200:
{
  "members": [
    {
      "id": "uuid",
      "first_name": "Employee",
      "last_name": "Alpha",
      "email": "employee@org-alpha.com",
      "crs": {
        "score": 85.5,
        "trend": "improving",
        "risk_level": "low"
      } | null,
      "week_status": {
        "week_start": "2026-07-06",
        "checkin_status": "submitted" | "draft" | null,
        "checkout_status": "submitted" | "draft" | null
      }
    }
  ]
}

Response 200 (empty team): { "members": [] }
Response 403: Role is employee (insufficient permissions)
```

**Notas de implementación:**
- Query: `SELECT * FROM users WHERE manager_id = :current_user_id AND organization_id = :org_id AND status = 'active' AND deleted_at IS NULL`
- Para cada miembro, LEFT JOIN con `crs_scores` (latest) y `check_ins`/`check_outs` de la semana actual
- Optimización: una sola query con subqueries o 1 query principal + 2 queries batch (CRS + week status)

---

#### GET /api/v1/teams/my-team/{employee_id}/crs

Historial CRS de un reporte directo.

```
Auth: Bearer JWT (role: manager, administrator)
operation_id: get_team_member_crs

Path params: employee_id (UUID)
Query params: ?weeks=8 (default 8, max 52)

Response 200:
{
  "employee": {
    "id": "uuid",
    "first_name": "Employee",
    "last_name": "Alpha"
  },
  "current": {
    "score": 85.5,
    "trend": "improving",
    "risk_level": "low",
    "week_start": "2026-07-06"
  } | null,
  "history": [
    { "week_start": "2026-07-06", "score": 85.5, "trend": "improving", "risk_level": "low" },
    { "week_start": "2026-06-29", "score": 78.0, "trend": "stable", "risk_level": "low" }
  ]
}

Response 403: Employee is not a direct report of this manager
Response 404: Employee not found
```

**Validación de ownership:**
```sql
SELECT id FROM users
WHERE id = :employee_id
  AND manager_id = :current_user_id
  AND organization_id = :org_id
  AND deleted_at IS NULL
```
Si no retorna fila → 403 (no 404, para no revelar existencia).

---

#### GET /api/v1/teams/my-team/{employee_id}/checkin

Check-in de la semana actual de un reporte directo (read-only).

```
Auth: Bearer JWT (role: manager, administrator)
operation_id: get_team_member_checkin

Path params: employee_id (UUID)

Response 200: CheckInResponse (same schema as GET /checkins/current)
{
  "id": "uuid",
  "employee_id": "uuid",
  "organization_id": "uuid",
  "week_start": "2026-07-06",
  "status": "submitted",
  "submitted_at": "...",
  "priorities_count": 3,
  "priorities": [
    {
      "id": "uuid",
      "title": "...",
      "description": "...",
      "priority_level": "high",
      "status": "planned",
      "phase_name": "Desarrollo",
      "project_name": "Proyecto Alpha",
      "tasks": [...]
    }
  ]
}

Response 403: Employee is not a direct report of this manager
Response 404: No check-in for current week
```

**Reutilización:** La lógica de carga de prioridades+tareas ya existe en `checkin/api/router.py` (`_load_priorities_with_tasks`). Extraer a un servicio compartido o reutilizar directamente.

---

### Business Rules

| BR | Regla | Validación |
|---|---|---|
| BR-014 | Manager solo ve sus reportes directos | `WHERE manager_id = current_user.id` |
| BR-016 | Multi-tenant | `AND organization_id = :org_id` (del JWT) |
| BR-017 | Todos los agregados pertenecen a una organización | Filtro en todas las queries |
| NUEVA | Manager NO puede modificar datos de empleados | Solo endpoints GET |
| NUEVA | Solo usuarios activos en la lista | `AND status = 'active'` |
| NUEVA | 403 si employee_id no es reporte directo | No revelar existencia (403, no 404) |

---

### Edge Cases

| Caso | Comportamiento esperado |
|---|---|
| Manager sin reportes directos | `{ "members": [] }` — 200 con lista vacía |
| Empleado sin CRS calculado | `"crs": null` en la respuesta del team |
| Empleado sin check-in esta semana | `"checkin_status": null` |
| Empleado sin check-out esta semana | `"checkout_status": null` |
| Manager intenta ver empleado de otro manager | 403 Forbidden |
| Employee intenta acceder a /teams/my-team | 403 Forbidden |
| Manager intenta ver empleado de otra organización | 403 (filtro org_id) |
| Empleado inactivo | No aparece en la lista |
| Manager que también es empleado de otro manager | Puede ver su propio equipo normalmente |

---

### Acceptance Criteria

**Escenario 1 — Manager ve resumen del equipo**
```gherkin
Given un manager con 2 reportes directos activos
When accede a GET /api/v1/teams/my-team
Then ve una lista con 2 miembros
  And cada miembro tiene su CRS actual (o null si no tiene)
  And cada miembro tiene el estado de check-in/check-out de la semana
```

**Escenario 2 — Manager ve CRS historial de un empleado**
```gherkin
Given un manager con un reporte directo que tiene 4 semanas de CRS
When accede a GET /api/v1/teams/my-team/{employee_id}/crs?weeks=8
Then ve el historial de scores del empleado
  And ve el score actual con trend y risk_level
```

**Escenario 3 — Manager ve check-in de un empleado**
```gherkin
Given un manager con un reporte directo que tiene check-in submitted
When accede a GET /api/v1/teams/my-team/{employee_id}/checkin
Then ve las prioridades y tareas del empleado (read-only)
  And el schema es idéntico al de GET /checkins/current
```

**Escenario 4 — Manager no puede ver empleados de otro manager**
```gherkin
Given un manager que intenta acceder a un empleado que no es su reporte directo
When accede a GET /api/v1/teams/my-team/{other_employee_id}/crs
Then recibe 403 Forbidden
```

**Escenario 5 — Employee no puede acceder a endpoints de equipo**
```gherkin
Given un usuario con rol employee
When accede a GET /api/v1/teams/my-team
Then recibe 403 Forbidden
```

**Escenario 6 — Dashboard UI muestra tabla del equipo**
```gherkin
Given un manager autenticado
When accede a /manager/team
Then ve una tabla con columnas: Nombre, CRS, Tendencia, Check-In, Check-Out
  And los badges de CRS tienen color según risk_level
  And puede hacer click en una fila para ver detalle
```

**Escenario 7 — Detalle de empleado muestra CRS + check-in**
```gherkin
Given un manager que hace click en un empleado
When accede a /manager/team/{employee_id}
Then ve el historial CRS del empleado (tabla últimas 8 semanas)
  And ve el check-in de la semana actual con prioridades y tareas (read-only)
  And no puede editar ni modificar nada
```

**Escenario 8 — Manager sin equipo ve estado vacío**
```gherkin
Given un manager sin reportes directos
When accede a /manager/team
Then ve un mensaje: "No tienes miembros en tu equipo"
```

---

### Non-Functional Requirements

- **NFR-004** — Respuesta < 500ms para lista del equipo (hasta 15 miembros)
- **NFR-010** — Manager obtiene visibilidad en menos de 2 minutos
- **NFR-012** — Datos read-only, sin riesgo de modificación accidental

---

### Technical Notes

#### Reutilización de código existente
- `CRSRepositoryImpl.get_latest_by_employee()` y `get_history()` ya existen — reutilizar para el endpoint de CRS por empleado
- `_load_priorities_with_tasks()` en `checkin/api/router.py` — extraer o reutilizar para cargar el check-in del empleado
- `require_roles("manager", "administrator")` ya existe como dependency

#### Módulo backend
Los 3 endpoints se implementan en el módulo `teams` (nuevo) ya que la responsabilidad es "vista del equipo del manager". Alternativa: agregar al módulo existente `projects` que ya tiene `GET /projects/org-members`. Decisión: **módulo `teams`** por alineación con bounded context Organization.

#### Cálculo de week_start
Reutilizar la misma lógica que `GetCurrentCheckInUseCase`: en dev usa `date.today()`, en prod calcula el lunes de la semana actual.

#### Performance
- La query principal (my-team) debe ser eficiente para equipos de hasta 15 personas
- Usar LEFT JOINs o subqueries correlacionadas para CRS y week status en una sola roundtrip
- No hacer N+1 queries (una por miembro)

---

### Dependencies

- **Técnicas:**
  - `users.manager_id` ya existe en la BD ✅
  - CRS individual ya se calcula y persiste (US-007) ✅
  - Check-in con prioridades/tareas ya se retorna (US-001, US-005) ✅
  - `require_roles()` dependency ya existe ✅
  - Middleware ya permite manager acceder a rutas ✅
- **Funcionales:**
  - Requiere al menos un empleado con `manager_id` apuntando al manager
  - Seed data ya tiene esta relación (manager@org-alpha → employee@org-alpha)

---

### Nivel de Riesgo

**High** — Involucra acceso cross-usuario (manager ve datos de empleados). Requiere validación estricta de BR-014 y tests de seguridad para garantizar que no se filtran datos entre managers ni entre organizaciones.

---

### Complejidad Estimada

**L**

| Factor | Detalle |
|---|---|
| Capas afectadas | Backend (módulo teams, 3 endpoints) + Frontend (2 páginas) |
| Endpoints | 3 nuevos (GET my-team, GET member CRS, GET member checkin) |
| Lógica | Query por manager_id, validación ownership, aggregation semanal |
| Tests | High: Unit + Integration + Security (cross-user access) |
| UI | 2 páginas (lista equipo + detalle empleado) |
| Reutilización | Alta — CRS repo y checkin loader ya existen |

---

### Siguiente Paso

Ejecutar `/create-tickets 008-manager-team-visibility`
