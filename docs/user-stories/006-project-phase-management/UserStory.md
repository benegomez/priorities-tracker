---
id: US-006
title: Project & Phase Management
status: draft
priority: high
risk_level: Medium
complexity: L
created: 2026-07-05
---

# US-006 — Project & Phase Management

## [original]

**Como** administrador o manager,
**quiero** crear y gestionar proyectos con sus fases, asignar un responsable y participantes,
**para** que los colaboradores puedan asociar sus prioridades semanales a proyectos y fases reales de la organización.

### Contexto

Actualmente los proyectos y fases se crean manualmente en la base de datos (seed data). El frontend usa un `MOCK_PHASES` hardcodeado (TD-007). Esta US implementa la gestión completa de proyectos y fases con API + UI, eliminando la dependencia de datos mock y habilitando el uso real de la plataforma con múltiples proyectos.

### Notas iniciales
- Las tablas `projects` y `project_phases` ya existen en la BD (migración US-001)
- Se necesitan columnas adicionales: `owner_id` en projects, tabla `project_members`
- Solo `administrator` y `manager` pueden gestionar proyectos
- Las fases se gestionan inline dentro de la pantalla del proyecto
- State machines ya definidas: Project (Draft→Active→OnHold→Completed→Archived), Phase (Planned→Active→Completed→Cancelled)
- Esta US resuelve TD-007 (PriorityForm usa fases hardcodeadas)

---

## [enhanced]

### User Journey

- **Usuarios:** Administrator, Manager
- **Objetivo:** Gestionar el catálogo de proyectos y fases de la organización
- **Flujo principal:**
  1. Admin/Manager accede a la sección "Proyectos" desde el sidebar
  2. Ve la lista de proyectos de su organización con estado y responsable
  3. Puede crear un nuevo proyecto (nombre, descripción, responsable)
  4. Al hacer click en un proyecto, ve el detalle con sus fases y participantes
  5. Puede agregar/editar/cambiar estado de fases inline
  6. Puede agregar/remover participantes del proyecto
  7. Puede cambiar el estado del proyecto (state machine)

---

### Business Value

- **Problema que resuelve:** Sin gestión de proyectos, los colaboradores no pueden asociar prioridades a proyectos reales. El frontend usa datos mock, lo que impide el uso real de la plataforma con múltiples proyectos y equipos.
- **Beneficio esperado:** Los administradores y managers configuran la estructura de proyectos una vez. Los colaboradores seleccionan proyectos y fases reales al crear prioridades. Los reportes futuros pueden agrupar por proyecto.

---

### FR de Referencia

- **FR-010** — Project Creation
- **FR-011** — Project Maintenance
- **FR-012** — Project Activation
- **FR-013** — Phase Management

---

### Bounded Context

Organization → Módulo: `projects`

---

### Entidades Involucradas

- **Project:** `id`, `organization_id`, `owner_id` (FK→users), `name`, `description`, `status`
- **ProjectPhase:** `id`, `organization_id`, `project_id`, `name`, `status`
- **ProjectMember:** `id`, `organization_id`, `project_id`, `user_id` (nueva tabla de relación)

---

### Business Rules

- **BR-004** — Una fase debe pertenecer a un proyecto (ya implementada)
- **NUEVA** — Solo `administrator` y `manager` pueden crear/editar proyectos
- **NUEVA** — Un proyecto debe tener un `owner_id` (responsable)
- **NUEVA** — Los participantes deben pertenecer a la misma organización
- **NUEVA** — No se puede eliminar un proyecto con prioridades activas (soft delete)
- **NUEVA** — No se puede eliminar una fase con prioridades activas (soft delete)
- **BR-016** — Aislamiento multi-tenant
- **BR-017** — Todos los agregados tienen organization_id

---

### State Machines

**Project:**
```
Draft → Active → OnHold → Completed → Archived
```

**ProjectPhase:**
```
Planned → Active → Completed → Cancelled
```

Transiciones válidas:
- Project: Draft→Active, Active→OnHold, Active→Completed, OnHold→Active, Completed→Archived
- Phase: Planned→Active, Active→Completed, Active→Cancelled, Planned→Cancelled

---

### Contrato API

**GET /api/v1/projects**
Lista proyectos de la organización con paginación.

```
Query params: ?status=active&page=1&page_size=20

Response 200:
{
  "items": [
    {
      "id": "uuid",
      "name": "Proyecto Alpha",
      "description": "...",
      "status": "active",
      "owner": { "id": "uuid", "full_name": "Manager Alpha" },
      "phases_count": 3,
      "members_count": 5,
      "created_at": "..."
    }
  ],
  "total": 10,
  "page": 1,
  "page_size": 20
}
```

---

**POST /api/v1/projects**
Crea un proyecto.

```
Request:
{
  "name": "Nuevo Proyecto",
  "description": "Descripción opcional",
  "owner_id": "uuid"
}

Response 201: ProjectResponse
Errors: 401, 403 (no admin/manager), 400 (validación)
```

---

**GET /api/v1/projects/{id}**
Detalle del proyecto con fases y participantes.

```
Response 200:
{
  "id": "uuid",
  "name": "Proyecto Alpha",
  "description": "...",
  "status": "active",
  "owner": { "id": "uuid", "full_name": "Manager Alpha" },
  "phases": [
    { "id": "uuid", "name": "Descubrimiento", "status": "active" }
  ],
  "members": [
    { "id": "uuid", "full_name": "Employee Alpha", "role": "employee" }
  ],
  "created_at": "...",
  "updated_at": "..."
}
```

---

**PATCH /api/v1/projects/{id}**
Edita nombre, descripción, owner, o estado del proyecto.

```
Request:
{
  "name": "Nombre actualizado",       // opcional
  "description": "...",               // opcional
  "owner_id": "uuid",                // opcional
  "status": "active"                  // opcional (valida state machine)
}

Response 200: ProjectResponse
Errors: 401, 403, 404, 409 (transición inválida)
```

---

**POST /api/v1/projects/{id}/phases**
Crea una fase en el proyecto.

```
Request: { "name": "Nueva Fase" }
Response 201: PhaseResponse
Errors: 401, 403, 404 (project)
```

---

**PATCH /api/v1/projects/{id}/phases/{phase_id}**
Edita nombre o estado de una fase.

```
Request: { "name": "Nombre editado", "status": "active" }
Response 200: PhaseResponse
Errors: 401, 403, 404, 409 (transición inválida)
```

---

**POST /api/v1/projects/{id}/members**
Agrega un participante al proyecto.

```
Request: { "user_id": "uuid" }
Response 201: { "id": "uuid", "user_id": "uuid", "full_name": "..." }
Errors: 401, 403, 404, 409 (ya es miembro)
```

---

**DELETE /api/v1/projects/{id}/members/{user_id}**
Remueve un participante del proyecto.

```
Response 204
Errors: 401, 403, 404
```

---

**GET /api/v1/projects/phases/available**
Lista fases activas disponibles para el usuario (para el PriorityForm).

```
Response 200:
[
  { "id": "uuid", "name": "Descubrimiento", "project_name": "Proyecto Alpha" }
]
```

> Este endpoint reemplaza el MOCK_PHASES del frontend (resuelve TD-007).

---

### Acceptance Criteria

**Escenario 1 — Admin crea un proyecto**
```gherkin
Given un administrador autenticado
When crea un proyecto con nombre, descripción y owner_id
Then el proyecto se crea con status "draft"
  And el owner queda asignado
  And pertenece a la organización del token
```

**Escenario 2 — Manager lista proyectos de su organización**
```gherkin
Given un manager autenticado
When accede a GET /projects
Then ve solo los proyectos de su organización
  And cada proyecto muestra nombre, estado, owner, conteo de fases y miembros
```

**Escenario 3 — Cambio de estado respeta state machine**
```gherkin
Given un proyecto en estado "draft"
When se intenta cambiar a "completed"
Then retorna 409 (transición inválida)
  And el estado no cambia
```

**Escenario 4 — Agregar fase a un proyecto**
```gherkin
Given un proyecto existente
When se agrega una fase con nombre "Desarrollo"
Then la fase se crea con status "planned"
  And pertenece al proyecto y organización correctos
```

**Escenario 5 — Agregar participante**
```gherkin
Given un proyecto existente
When se agrega un usuario como participante
Then el usuario aparece en la lista de miembros
  And el usuario debe pertenecer a la misma organización
```

**Escenario 6 — Employee no puede gestionar proyectos**
```gherkin
Given un empleado autenticado
When intenta crear o editar un proyecto
Then retorna 403 Forbidden
```

**Escenario 7 — PriorityForm usa fases reales (TD-007)**
```gherkin
Given un empleado creando un check-in
When abre el formulario de agregar prioridad
Then el select de fases muestra datos reales de GET /projects/phases/available
  And no usa datos hardcodeados
```

---

### Non-Functional Requirements

- **NFR-002 — Authorization:** Solo admin y manager pueden gestionar proyectos
- **NFR-010 — Simplicity:** Crear un proyecto con fases debe tomar menos de 2 minutos
- **NFR-011 — Accessibility:** Formularios y tablas accesibles

---

### Dependencies

- **Técnicas:**
  - Tablas `projects` y `project_phases` ya existen
  - Nueva tabla `project_members` (migración)
  - Nueva columna `owner_id` en `projects` (migración)
  - US-002 (Auth) — roles admin/manager
- **Funcionales:**
  - Resuelve TD-007 (PriorityForm mock phases)
  - Habilita reportes por proyecto (futuro)

---

### Diseño de UX

**Pantalla de lista de proyectos** (`/admin/projects` o `/manager/projects`):
```
┌─────────────────────────────────────────────────────┐
│ Proyectos                        [+ Nuevo Proyecto] │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────┐ │
│ │ Proyecto Alpha          Active    Owner: Manager│ │
│ │ 3 fases · 5 miembros                           │ │
│ └─────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Proyecto Beta           Draft     Owner: Admin  │ │
│ │ 1 fase · 2 miembros                            │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Pantalla de detalle del proyecto** (click en un proyecto):
```
┌─────────────────────────────────────────────────────┐
│ ← Proyectos    Proyecto Alpha         Badge: Active │
│ Descripción del proyecto...                         │
│ Responsable: Manager Alpha                          │
├─────────────────────────────────────────────────────┤
│ Fases                              [+ Agregar Fase] │
│ ┌───────────────────────────────────────────┐       │
│ │ Descubrimiento    Active    [Editar] [▼]  │       │
│ │ Desarrollo        Planned   [Editar] [▼]  │       │
│ │ Pruebas           Planned   [Editar] [▼]  │       │
│ └───────────────────────────────────────────┘       │
├─────────────────────────────────────────────────────┤
│ Participantes                   [+ Agregar Miembro] │
│ ┌───────────────────────────────────────────┐       │
│ │ Employee Alpha    employee    [Remover]    │       │
│ │ Employee Beta     employee    [Remover]    │       │
│ └───────────────────────────────────────────┘       │
├─────────────────────────────────────────────────────┤
│ Estado del Proyecto                                 │
│ [Draft] [Active] [On Hold] [Completed] [Archived]   │
│         ^^^^^^^^ (actual)                           │
└─────────────────────────────────────────────────────┘
```

---

### Nivel de Riesgo

**Medium** — Nuevo módulo completo pero sin complejidad transaccional. CRUD estándar con state machines.

---

### Complejidad Estimada

**L**

| Factor | Detalle |
|---|---|
| Capas afectadas | DB (migración) + Backend (nuevo módulo) + Frontend (nuevas páginas) |
| Endpoints | 8 endpoints |
| Entidades | 1 nueva (ProjectMember) + 1 columna nueva (owner_id) |
| Business Rules | 6 reglas + state machines |
| Tests requeridos | Unit + Integration, cobertura >80% |
| UI | 2 páginas nuevas (lista + detalle) + refactor PriorityForm |

---

### Resolución de Deuda Técnica

Esta US cierra **TD-007** (PriorityForm usa fases hardcodeadas) al implementar `GET /projects/phases/available` y reemplazar `MOCK_PHASES` por datos reales.

---

### Siguiente Paso

Ejecutar `/enrich-us 006-project-phase-management` o `/create-tickets 006-project-phase-management`
