---
id: 014-admin-project-management
persona: Administrador
fr: FR-010, FR-011, FR-012, FR-013
bounded-context: Commitment
status: done
completed: 2025-01-28
pr: "#14"
merge_commit: a61c22e
created: 2025-01-28
enriched: 2025-01-28
---

# US-014: Admin Project Management

## [original]

**Como** administrador de la plataforma,
**quiero** gestionar los proyectos y sus fases (crear, editar, cambiar estado, gestionar participantes y fases),
**para** que los colaboradores puedan asociar sus prioridades semanales a proyectos y fases reales de la organización.

### Contexto

El módulo `projects` ya está implementado en backend y frontend. Existen 9 endpoints REST y las páginas `/admin/projects` y `/admin/projects/[id]`. Esta US formaliza la funcionalidad existente, agrega los tests de integración backend faltantes y los tests de componentes frontend, y cierra la documentación de la US.

### Notas iniciales
- Solo roles `administrator` y `manager` pueden gestionar proyectos
- Un proyecto pertenece a una organización (multi-tenant)
- Las fases pertenecen a un proyecto
- Los proyectos tienen máquina de estado: `draft → active → on_hold → completed → archived`
- Las fases tienen máquina de estado: `planned → active → completed | cancelled`
- No requiere migración de base de datos — schema ya existe

---

## [enhanced]

### User Journey

- **Usuario principal:** Administrador
- **Objetivo principal:** Crear proyectos con fases y participantes para que los empleados puedan asociar sus prioridades semanales
- **Flujo principal:**
  1. El administrador accede a `/admin/projects`
  2. Ve la lista de proyectos con nombre, estado, fases, miembros y responsable
  3. Crea un nuevo proyecto (nombre, descripción, responsable)
  4. Accede al detalle del proyecto → gestiona fases y participantes
  5. Cambia el estado del proyecto según la máquina de estado
  6. Crea y actualiza fases del proyecto

---

### Business Value

- **Problema que resuelve:** Sin proyectos y fases activos, los empleados no pueden asociar sus prioridades semanales a contexto organizacional real.
- **Beneficio esperado:** El administrador puede estructurar el trabajo en proyectos y fases, dando contexto a los compromisos semanales y habilitando reportes por proyecto.

---

### Priority

**High**
Prerequisito para que los empleados puedan crear prioridades asociadas a proyectos (BR-003, BR-004).

---

### FR de Referencia

- **FR-010** — Administrators can create projects
- **FR-011** — Administrators can edit projects
- **FR-012** — Projects can be activated and deactivated
- **FR-013** — Project phases can be created and maintained

---

### Bounded Context

Commitment → Módulo: `projects` (ya implementado — se formaliza y testea)

---

### Entidades Involucradas

**Project (tabla existente):**
```
projects
  id              UUID PK
  organization_id UUID FK → organizations
  owner_id        UUID FK → users
  name            VARCHAR(200) NOT NULL
  description     TEXT
  status          VARCHAR(50) DEFAULT 'draft'
  created_at      TIMESTAMPTZ
  updated_at      TIMESTAMPTZ
  deleted_at      TIMESTAMPTZ
```

**ProjectPhase (tabla existente):**
```
project_phases
  id              UUID PK
  organization_id UUID FK → organizations
  project_id      UUID FK → projects
  name            VARCHAR(200) NOT NULL
  status          VARCHAR(50) DEFAULT 'planned'
  created_at      TIMESTAMPTZ
  updated_at      TIMESTAMPTZ
```

**ProjectMember (tabla existente):**
```
project_members
  id              UUID PK
  organization_id UUID FK → organizations
  project_id      UUID FK → projects
  user_id         UUID FK → users
```

---

### Máquinas de Estado

**Project:**
```
draft → active → on_hold → completed → archived
              ↑_________|
```

**ProjectPhase:**
```
planned → active → completed
        ↘         ↗
         cancelled
```

---

### Business Rules Aplicables

- **BR-003** — Una prioridad debe pertenecer a una fase
- **BR-004** — Una fase debe pertenecer a un proyecto
- **BR-015** — Un administrador puede ver toda la organización
- **BR-016** — Multi-tenant: `organization_id` del JWT, nunca del body
- **BR-017** — Todos los agregados pertenecen a una organización
- **BR-NEW-09** — Solo se pueden hacer transiciones de estado válidas (máquina de estado)
- **BR-NEW-10** — El responsable (owner) del proyecto debe pertenecer a la misma organización
- **BR-NEW-11** — Un usuario no puede ser agregado dos veces como participante del mismo proyecto

---

### Contrato API (ya implementado)

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/v1/projects` | Lista paginada con filtro por status |
| `POST` | `/api/v1/projects` | Crear proyecto |
| `GET` | `/api/v1/projects/{id}` | Detalle con fases y miembros |
| `PATCH` | `/api/v1/projects/{id}` | Editar nombre, descripción, owner, status |
| `POST` | `/api/v1/projects/{id}/phases` | Crear fase |
| `PATCH` | `/api/v1/projects/{id}/phases/{phase_id}` | Editar fase |
| `POST` | `/api/v1/projects/{id}/members` | Agregar participante |
| `DELETE` | `/api/v1/projects/{id}/members/{user_id}` | Remover participante |
| `GET` | `/api/v1/projects/phases/available` | Fases disponibles para selector de prioridades |

---

### Acceptance Criteria

**Escenario 1 — Admin lista proyectos**
```gherkin
Given un administrador autenticado
When hace GET /api/v1/projects
Then recibe lista paginada con nombre, estado, phases_count, members_count
```

**Escenario 2 — Admin crea proyecto**
```gherkin
Given un administrador autenticado
When hace POST /api/v1/projects con nombre y owner_id válido
Then el sistema retorna 201 con el proyecto en estado draft
  And organization_id se toma del JWT
```

**Escenario 3 — Transición de estado válida (BR-NEW-09)**
```gherkin
Given un proyecto en estado draft
When el admin hace PATCH con status=active
Then el proyecto pasa a active y retorna 200
```

**Escenario 4 — Transición de estado inválida (BR-NEW-09)**
```gherkin
Given un proyecto en estado draft
When el admin hace PATCH con status=completed
Then el sistema retorna 409 Conflict
```

**Escenario 5 — Admin gestiona fases**
```gherkin
Given un proyecto existente
When el admin hace POST /api/v1/projects/{id}/phases con nombre
Then la fase se crea en estado planned y retorna 201
```

**Escenario 6 — Participante duplicado (BR-NEW-11)**
```gherkin
Given un usuario ya es participante del proyecto
When el admin intenta agregarlo nuevamente
Then el sistema retorna 409 Conflict
```

**Escenario 7 — RBAC employee**
```gherkin
Given un usuario con rol employee
When intenta hacer POST /api/v1/projects
Then el sistema retorna 403 Forbidden
```

---

### Non-Functional Requirements

- **NFR-001** — Todo endpoint requiere Bearer JWT válido
- **NFR-002** — Roles `administrator` y `manager` pueden gestionar proyectos
- **NFR-003** — No requiere migración — schema ya existe

---

### Dependencies

- **Técnicas:**
  - Módulo `auth` — JWT con `organization_id` y `role`
  - Módulo `projects` — ya implementado completamente
- **Funcionales:**
  - US-013 (Admin Team Management) — completada ✅
  - Es prerequisito para US-001 (Check-In) — los empleados necesitan fases activas

---

### Nivel de Riesgo

**Medium**
No hay migración. La implementación ya existe. El riesgo está en la cobertura de tests para los flujos de máquina de estado y RBAC.

---

### Complejidad Estimada

**S**

| Factor | Detalle |
|---|---|
| Capas afectadas | Backend (tests) + Frontend (tests) |
| Endpoints nuevos | 0 — ya implementados |
| Migraciones | No requerida |
| Business Rules | BR-NEW-09, BR-NEW-10, BR-NEW-11 |
| Tests requeridos | Medium: Unit (ya existen) + Integration (faltantes) + Frontend components |
