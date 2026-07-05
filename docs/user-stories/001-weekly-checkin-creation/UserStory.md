---
id: 001-weekly-checkin-creation
persona: Colaborador Individual
fr: FR-014, FR-015, FR-016
bounded-context: Commitment
status: enriched
created: 2025-01-06
enriched: 2025-01-06
---

# US-001: Weekly Check-In Creation

## [original]

**Como** colaborador individual,
**quiero** registrar mis prioridades y compromisos para la semana,
**para** comunicar claramente qué voy a entregar y mantener a mi manager informado sin necesidad de reuniones de status.

### Contexto

Cada lunes, el colaborador enfrenta el mismo problema: su manager no sabe en qué está trabajando a menos que se lo pregunte directamente. Esto genera interrupciones, reuniones innecesarias y una sensación de microgestión. El colaborador necesita una forma simple y rápida de declarar sus compromisos semanales — en menos de 5 minutos — y que esa información quede visible para su manager de forma inmediata.

### Notas iniciales
- El proceso debe ser completable en menos de 5 minutos (principio de simplicidad extrema del producto)
- Solo puede existir un Check-In por empleado por semana (BR-001)
- Las prioridades deben estar asociadas a un proyecto y una fase (BR-003, BR-004)
- El Check-In inicia en estado `draft` y se envía explícitamente (`submitted`)
- Es el punto de entrada de toda la cadena de valor del producto

---

## [enhanced]

### User Journey

- **Usuario principal:** Colaborador Individual (employee)
- **Objetivo principal:** Registrar sus compromisos semanales en menos de 5 minutos para que su manager tenga visibilidad inmediata sin necesidad de pedirla
- **Flujo principal:**
  1. El colaborador accede a la plataforma al inicio de la semana
  2. Crea un nuevo Check-In para la semana actual
  3. Agrega una o más prioridades, cada una asociada a un proyecto y fase
  4. Opcionalmente agrega tareas a cada prioridad
  5. Envía el Check-In — queda en estado `submitted`
  6. El manager visualiza los compromisos en su dashboard sin haber pedido un reporte

---

### Business Value

- **Problema que resuelve:** El manager no sabe en qué está trabajando cada persona de su equipo a menos que lo pregunte explícitamente, generando interrupciones, reuniones de status y microgestión. El colaborador pierde tiempo respondiendo solicitudes de actualización en lugar de ejecutar.
- **Beneficio esperado:** El colaborador declara sus compromisos una vez, en minutos. El manager obtiene visibilidad inmediata y estructurada del trabajo comprometido para la semana, eliminando la necesidad de preguntar.

---

### Priority

**Critical**
Es el primer paso de la cadena de valor del producto. Sin Check-In no hay datos, sin datos no hay Check-Out, sin Check-Out no hay CRS. Es la historia que valida la propuesta de valor central del producto.

---

### FR de Referencia

- **FR-014** — Check-In Creation: Employees shall be able to create weekly Check-Ins
- **FR-015** — Priority Creation: Employees shall be able to create priorities
- **FR-016** — Task Creation: Employees shall be able to create tasks associated with priorities

---

### Bounded Context

Commitment → Módulos: `checkin`, `priorities`

---

### Entidades Involucradas

- **WeeklyCheckIn:** `id`, `employee_id`, `organization_id`, `week_period`, `status` (draft → submitted → closed)
- **Priority:** `id`, `phase_id`, `owner_id`, `organization_id`, `week_period`, `title`, `description`, `status` (draft → planned)
- **Task:** `id`, `priority_id`, `organization_id`, `title`, `status` (pending)
- **ProjectPhase:** `id`, `project_id` — requerida para asociar prioridades (BR-003, BR-004)
- **Project:** `id`, `organization_id`, `status` — debe estar `active` para ser seleccionable

---

### Business Rules Aplicables

- **BR-001** — Un empleado solo puede tener un Check-In por semana. Intentar crear un segundo retorna `409 Conflict`
- **BR-003** — Una prioridad debe pertenecer a una fase
- **BR-004** — Una fase debe pertenecer a un proyecto
- **BR-005** — Una tarea debe pertenecer a una prioridad
- **BR-013** — Un empleado solo ve sus propias prioridades
- **BR-016** — Ningún usuario puede acceder a datos de otra organización
- **BR-017** — Todos los agregados pertenecen a una organización

---

### Transiciones de Estado

```
WeeklyCheckIn:  Draft → Submitted
Priority:       (nueva) → Draft → Planned  (al submit del Check-In)
Task:           (nueva) → Pending
```

---

### Contrato API Preliminar

**POST /api/v1/checkins**
Crea un nuevo Check-In en estado `draft`.

```json
Request:
{
  "week_start": "2025-01-06"
}

Response 201:
{
  "id": "uuid",
  "employee_id": "uuid",
  "week_start": "2025-01-06",
  "status": "draft",
  "created_at": "2025-01-06T08:00:00Z",
  "updated_at": "2025-01-06T08:00:00Z"
}
```
Errores: `409` si ya existe Check-In para esa semana, `401` sin auth, `403` rol incorrecto

---

**POST /api/v1/priorities**
Agrega una prioridad al Check-In activo del empleado.

```json
Request:
{
  "checkin_id": "uuid",
  "phase_id": "uuid",
  "title": "Completar diseño de arquitectura",
  "description": "Revisar y aprobar el diseño técnico del módulo de autenticación",
  "priority_level": "high"
}

Response 201:
{
  "id": "uuid",
  "checkin_id": "uuid",
  "phase_id": "uuid",
  "owner_id": "uuid",
  "title": "Completar diseño de arquitectura",
  "status": "draft",
  "priority_level": "high",
  "created_at": "2025-01-06T08:00:00Z"
}
```
Errores: `404` si checkin_id o phase_id no existen, `403` si la fase no pertenece a la organización

---

**POST /api/v1/priorities/{id}/tasks**
Agrega una tarea a una prioridad.

```json
Request:
{
  "title": "Revisar documentación de JWT"
}

Response 201:
{
  "id": "uuid",
  "priority_id": "uuid",
  "title": "Revisar documentación de JWT",
  "status": "pending",
  "created_at": "2025-01-06T08:00:00Z"
}
```

---

**POST /api/v1/checkins/{id}/submit**
Envía el Check-In. Transiciona de `draft` a `submitted`.

```json
Request: {} (vacío)

Response 200:
{
  "id": "uuid",
  "status": "submitted",
  "submitted_at": "2025-01-06T08:30:00Z"
}
```
Errores: `409` si no tiene al menos una prioridad, `404` si el checkin no existe

---

### Acceptance Criteria

**Escenario 1 — Colaborador crea un Check-In exitosamente**
```gherkin
Given un empleado autenticado sin Check-In para la semana actual
When envía POST /api/v1/checkins con week_start válido
Then el sistema retorna 201 con el Check-In en estado "draft"
  And el Check-In queda asociado al employee_id del token
  And el Check-In queda asociado al organization_id del token
```

**Escenario 2 — No se permite duplicar Check-In en la misma semana (BR-001)**
```gherkin
Given un empleado con un Check-In ya existente para la semana del 2025-01-06
When intenta crear un segundo Check-In con el mismo week_start
Then el sistema retorna 409 Conflict
  And el mensaje de error referencia BR-001
  And no se crea ningún registro adicional
```

**Escenario 3 — Prioridad requiere fase válida (BR-003, BR-004)**
```gherkin
Given un empleado con un Check-In en draft
When intenta agregar una prioridad con phase_id de un proyecto inactivo o de otra organización
Then el sistema retorna 403 Forbidden
  And no se crea la prioridad
```

**Escenario 4 — Empleado solo ve sus propios Check-Ins (BR-013)**
```gherkin
Given dos empleados A y B en la misma organización
  And el empleado A tiene un Check-In creado
When el empleado B intenta acceder al Check-In de A via GET /api/v1/checkins/{id}
Then el sistema retorna 403 Forbidden
```

**Escenario 5 — Envío exitoso del Check-In**
```gherkin
Given un empleado con un Check-In en draft que tiene al menos una prioridad
When envía POST /api/v1/checkins/{id}/submit
Then el sistema retorna 200 con status "submitted"
  And las prioridades del Check-In transicionan a estado "planned"
  And el manager del empleado puede ver el Check-In en su dashboard
```

**Escenario 6 — No se puede enviar un Check-In vacío**
```gherkin
Given un empleado con un Check-In en draft sin ninguna prioridad agregada
When intenta enviarlo via POST /api/v1/checkins/{id}/submit
Then el sistema retorna 409 Conflict
  And el Check-In permanece en estado "draft"
```

**Escenario 7 — Aislamiento multi-tenant (BR-016)**
```gherkin
Given un empleado de la organización A con token válido
When intenta crear un Check-In usando phase_id de la organización B
Then el sistema retorna 403 Forbidden
  And no se registra ningún acceso cross-tenant
```

---

### Non-Functional Requirements

- **NFR-001 — Authentication:** Todo endpoint del Check-In requiere Bearer JWT válido
- **NFR-002 — Authorization:** Solo empleados y managers pueden interactuar con Check-Ins; el rol se valida desde el token
- **NFR-004 — Response Time:** Creación y submit del Check-In deben responder en < 500ms bajo carga normal
- **NFR-008 — Data Integrity:** Un Check-In submitted no puede volver a draft; la transición es irreversible
- **NFR-009 — Auditability:** Los eventos `checkin.created` y `checkin.submitted` deben quedar en el audit log con `user_id`, `organization_id` y `timestamp`
- **NFR-010 — Simplicity:** El flujo completo (crear Check-In + agregar prioridades + submit) debe ser ejecutable en < 5 minutos

---

### Dependencies

- **Técnicas:**
  - Módulo `auth` — JWT válido con `employee_id`, `organization_id` y `role` en el payload
  - Módulo `projects` — Proyectos activos y sus fases deben existir para poder crear prioridades
  - Módulo `users` — El empleado debe existir y estar activo en la organización
  - Migración Alembic — Tablas `check_ins`, `priorities`, `tasks` deben existir
- **Funcionales:**
  - La estructura organizacional (usuarios, equipos, proyectos, fases) debe estar configurada antes de que el empleado pueda hacer su primer Check-In
  - No tiene dependencia de Check-Out ni CRS — es el punto de partida

---

### Success Metrics

- **Check-In Completion Rate:** Porcentaje de empleados elegibles que envían su Check-In cada semana → target > 90%
- **North Star — Commitment Completion Rate:** Esta historia establece el numerador y denominador de la métrica principal: prioridades comprometidas vs. completadas

---

### Nivel de Riesgo

**Critical**
Módulo `checkin` es siempre Critical por definición (testing-standards.md). Es además el flujo más importante del producto.

---

### Complejidad Estimada

**L**

| Factor | Detalle |
|---|---|
| Capas afectadas | DB + Backend + Frontend (3 capas completas) |
| Endpoints | 4 endpoints (POST checkin, POST priority, POST task, POST submit) |
| Entidades | 3 nuevas: WeeklyCheckIn, Priority, Task |
| Business Rules | BR-001, BR-003, BR-004, BR-005, BR-013, BR-016, BR-017 (7 reglas) |
| Tests requeridos | Critical: Unit + Integration + Contract + E2E + Security, cobertura >95% |
| Justificación | Múltiples entidades nuevas con state machine, 7 BRs, E2E obligatorio por ser flujo Critical, y es prerequisito de toda la cadena de valor |

---

### Data Model (Tablas Involucradas)

**check_ins** *(nueva)*
```sql
CREATE TABLE check_ins (
    id              UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID         NOT NULL REFERENCES organizations(id),
    employee_id     UUID         NOT NULL REFERENCES users(id),
    week_period     DATE         NOT NULL,           -- lunes ISO de la semana
    status          VARCHAR(20)  NOT NULL DEFAULT 'draft',
    submitted_at    TIMESTAMPTZ  NULL,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ  NULL,
    deleted_by      UUID         NULL,
    CONSTRAINT uq_check_ins_employee_week UNIQUE (employee_id, week_period),
    CONSTRAINT ck_check_ins_status CHECK (status IN ('draft','submitted','closed'))
);
CREATE INDEX idx_check_ins_organization_id ON check_ins (organization_id);
CREATE INDEX idx_check_ins_employee_id     ON check_ins (employee_id);
```

**priorities** *(nueva — scope de esta US: draft + planned)*
```sql
CREATE TABLE priorities (
    id              UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID         NOT NULL REFERENCES organizations(id),
    check_in_id     UUID         NOT NULL REFERENCES check_ins(id),
    phase_id        UUID         NOT NULL REFERENCES project_phases(id),
    owner_id        UUID         NOT NULL REFERENCES users(id),
    week_period     DATE         NOT NULL,
    title           VARCHAR(300) NOT NULL,
    description     TEXT         NULL,
    priority_level  VARCHAR(10)  NOT NULL DEFAULT 'medium',
    status          VARCHAR(20)  NOT NULL DEFAULT 'draft',
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ  NULL,
    deleted_by      UUID         NULL,
    CONSTRAINT ck_priorities_level  CHECK (priority_level IN ('low','medium','high')),
    CONSTRAINT ck_priorities_status CHECK (status IN ('draft','planned','in_progress','completed','carried_over'))
);
CREATE INDEX idx_priorities_organization_id ON priorities (organization_id);
CREATE INDEX idx_priorities_check_in_id     ON priorities (check_in_id);
CREATE INDEX idx_priorities_phase_id        ON priorities (phase_id);
CREATE INDEX idx_priorities_owner_id        ON priorities (owner_id);
```

**tasks** *(nueva)*
```sql
CREATE TABLE tasks (
    id              UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID         NOT NULL REFERENCES organizations(id),
    priority_id     UUID         NOT NULL REFERENCES priorities(id),
    title           VARCHAR(300) NOT NULL,
    description     TEXT         NULL,
    status          VARCHAR(20)  NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ  NULL,
    deleted_by      UUID         NULL,
    CONSTRAINT ck_tasks_status CHECK (status IN ('pending','in_progress','completed','cancelled'))
);
CREATE INDEX idx_tasks_organization_id ON tasks (organization_id);
CREATE INDEX idx_tasks_priority_id     ON tasks (priority_id);
```

> **Nota naming:** La API expone `week_start` (legible para el cliente); internamente la columna se llama `week_period`. El valor siempre es el lunes ISO de la semana (`YYYY-MM-DD`).

---

### Open Questions / Decisiones Pendientes

| # | Pregunta | Decisión ||
|---|---|---|---|
| OQ-1 | ¿Puede un `manager` crear un Check-In en nombre de un empleado? | No — solo el propio `employee` puede crear su Check-In. Un manager puede consultarlo. | ADR-010 / BR-013 |
| OQ-2 | ¿Se permite crear prioridades sin Check-In explícito (floating)? | No — toda prioridad de esta US debe tener `check_in_id`. Prioridades sin checkin son out-of-scope. | BR-003 |
| OQ-3 | ¿Cuántas prioridades máximas por Check-In? | Sin límite duro en MVP. Candidato a BR futuro. | — |
| OQ-4 | ¿Qué pasa si el proyecto de la fase es desactivado después de crear la prioridad? | La prioridad permanece válida; se valida el estado del proyecto solo en el momento de creación. | — |

---

### Siguiente Paso

Ejecutar `/create-tickets 001-weekly-checkin-creation`
