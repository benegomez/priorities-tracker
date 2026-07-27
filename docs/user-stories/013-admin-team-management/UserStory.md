---
id: 013-admin-team-management
persona: Administrador
fr: FR-007, FR-008, FR-009
bounded-context: Organization
status: enriched
created: 2025-01-28
enriched: 2025-01-28
---

# US-013: Admin Team Management

## [original]

**Como** administrador de la plataforma,
**quiero** gestionar los equipos de mi organización (crear, editar, ver miembros y asignar usuarios a equipos),
**para** mantener la estructura organizacional actualizada y que los managers tengan visibilidad correcta de sus reportes directos.

### Contexto

Actualmente la estructura de equipos se gestiona implícitamente via `manager_id` en la tabla `users` — un empleado pertenece al "equipo" de su manager. No existe una entidad `Team` formal en la base de datos ni una interfaz para que el administrador gestione equipos como unidades organizacionales.

Esta US introduce la tabla `teams`, permite al administrador crear y editar equipos, y asignar usuarios (empleados) a un equipo. La asignación de manager al equipo se hace designando a un usuario con rol `manager` como responsable del equipo.

### Notas iniciales
- Solo el rol `administrator` puede gestionar equipos
- Un equipo pertenece a una organización
- Un usuario puede pertenecer a un solo equipo a la vez
- El manager del equipo es un usuario con rol `manager` de la misma organización
- La tabla `teams` no existe — requiere migración Alembic
- La columna `team_id` en `users` tampoco existe — requiere migración

---

## [enhanced]

### User Journey

- **Usuario principal:** Administrador
- **Objetivo principal:** Crear y gestionar equipos como unidades organizacionales formales, asignar miembros y designar managers
- **Flujo principal:**
  1. El administrador accede al panel de administración → sección Equipos
  2. Ve la lista de equipos de su organización con nombre, manager asignado y cantidad de miembros
  3. Puede crear un nuevo equipo (nombre, manager)
  4. Puede editar nombre y manager de un equipo existente
  5. Puede ver el detalle de un equipo con la lista de sus miembros
  6. Puede asignar o remover usuarios de un equipo

---

### Business Value

- **Problema que resuelve:** La estructura organizacional es implícita y difícil de gestionar. Los managers no tienen un equipo formal asignado — la visibilidad depende del `manager_id` en cada usuario individual.
- **Beneficio esperado:** El administrador puede definir equipos formales, asignar managers y miembros, y la plataforma refleja la estructura real de la organización.

---

### Priority

**High**
Prerequisito para que la visibilidad del manager (US-008) sea correcta y para que los reportes de equipo (US-014) tengan una unidad organizacional formal.

---

### FR de Referencia

- **FR-007** — Administrators can create teams
- **FR-008** — Administrators can edit teams
- **FR-009** — Administrators can assign employees to teams

---

### Bounded Context

Organization → Módulo: `teams` (módulo ya existe parcialmente — se extiende)

---

### Entidades Involucradas

**Team (nueva tabla):**
```
teams
  id              UUID PK
  organization_id UUID FK → organizations
  name            VARCHAR(200) NOT NULL
  manager_id      UUID FK → users (nullable — manager del equipo)
  created_at      TIMESTAMPTZ
  updated_at      TIMESTAMPTZ
  deleted_at      TIMESTAMPTZ (soft delete)
  deleted_by      UUID
```

**User (tabla existente — agregar columna):**
```
users
  team_id  UUID FK → teams (nullable — equipo al que pertenece)
```

---

### Business Rules Aplicables

- **BR-016** — Multi-tenant: `organization_id` del JWT, nunca del body
- **BR-017** — Todos los agregados pertenecen a una organización
- **BR-NEW-05** — El nombre del equipo debe ser único dentro de la organización
- **BR-NEW-06** — El manager asignado a un equipo debe tener rol `manager` o `administrator`
- **BR-NEW-07** — Un usuario solo puede pertenecer a un equipo a la vez (asignar a nuevo equipo remueve del anterior)
- **BR-NEW-08** — No se puede eliminar un equipo con miembros activos (soft delete solo si está vacío, o forzar reasignación)

---

### Contrato API

**GET /api/v1/teams**
Lista paginada de equipos de la organización.
```
Query params: page=1, page_size=20
Response 200:
{
  "items": [
    {
      "id": "uuid",
      "name": "Equipo Backend",
      "manager_id": "uuid | null",
      "manager_name": "string | null",
      "member_count": 4,
      "created_at": "2025-01-06T08:00:00Z"
    }
  ],
  "total": 3,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

**POST /api/v1/teams**
Crea un nuevo equipo.
```json
Request: { "name": "Equipo Backend", "manager_id": "uuid | null" }
Response 201: TeamResponse completo
```
Errores: `409` nombre duplicado en la org, `404` manager_id no existe, `400` manager no tiene rol válido

**GET /api/v1/teams/{id}**
Detalle del equipo con lista de miembros.
```json
Response 200:
{
  "id": "uuid",
  "name": "Equipo Backend",
  "manager_id": "uuid",
  "manager_name": "string",
  "member_count": 4,
  "members": [
    { "id": "uuid", "first_name": "Ana", "last_name": "García", "role": "employee", "status": "active" }
  ],
  "created_at": "...",
  "updated_at": "..."
}
```

**PATCH /api/v1/teams/{id}**
Actualiza nombre y/o manager del equipo.
```json
Request: { "name": "string | null", "manager_id": "uuid | null" }
Response 200: TeamResponse completo
```
Errores: `409` nombre duplicado, `404` equipo no existe

**POST /api/v1/teams/{id}/members**
Asigna un usuario al equipo.
```json
Request: { "user_id": "uuid" }
Response 200: { "team_id": "uuid", "user_id": "uuid" }
```
Errores: `404` usuario no existe, `409` usuario ya pertenece a este equipo

**DELETE /api/v1/teams/{id}/members/{user_id}**
Remueve un usuario del equipo (limpia `team_id` en users).
```json
Response 204 No Content
```
Errores: `404` usuario no es miembro del equipo

---

### Acceptance Criteria

**Escenario 1 — Admin lista equipos**
```gherkin
Given un administrador autenticado
When hace GET /api/v1/teams
Then recibe lista paginada de equipos de su organización
  And cada item incluye member_count y manager_name
```

**Escenario 2 — Admin crea equipo**
```gherkin
Given un administrador autenticado
When hace POST /api/v1/teams con nombre único y manager_id válido
Then el sistema retorna 201 con el equipo creado
  And el organization_id se toma del JWT
```

**Escenario 3 — Nombre duplicado (BR-NEW-05)**
```gherkin
Given un equipo "Equipo Backend" ya existe en la organización
When el admin intenta crear otro equipo con el mismo nombre
Then el sistema retorna 409 Conflict
```

**Escenario 4 — Admin asigna usuario a equipo (BR-NEW-07)**
```gherkin
Given un usuario sin equipo asignado
When el admin hace POST /api/v1/teams/{id}/members con ese user_id
Then el usuario queda con team_id = id del equipo
  And si el usuario tenía otro equipo, se remueve del anterior
```

**Escenario 5 — Admin remueve usuario de equipo**
```gherkin
Given un usuario miembro del equipo X
When el admin hace DELETE /api/v1/teams/X/members/{user_id}
Then el usuario queda con team_id = NULL
  And retorna 204
```

**Escenario 6 — RBAC**
```gherkin
Given un usuario con rol employee o manager
When intenta hacer GET /api/v1/teams
Then el sistema retorna 403 Forbidden
```

---

### Non-Functional Requirements

- **NFR-001** — Todo endpoint requiere Bearer JWT válido
- **NFR-002** — Solo rol `administrator` puede acceder a `/api/v1/teams`
- **NFR-003** — Requiere migración Alembic: tabla `teams` + columna `team_id` en `users`

---

### Dependencies

- **Técnicas:**
  - Módulo `auth` — JWT con `organization_id` y `role=administrator`
  - Módulo `teams` — ya existe con endpoints de visibilidad para manager (se extiende, no se reemplaza)
  - Migración Alembic nueva requerida
- **Funcionales:**
  - US-012 (Admin User Management) — completada ✅
  - Es prerequisito para US-014 (Reporting) con agrupación por equipo

---

### Nivel de Riesgo

**Medium**
Introduce migración de schema (tabla nueva + columna nueva). La lógica de negocio es CRUD estándar. El módulo `teams` ya existe — se extiende con nuevos endpoints de administración.

---

### Complejidad Estimada

**M**

| Factor | Detalle |
|---|---|
| Capas afectadas | DB (migración) + Backend (nuevos endpoints en módulo existente) + Frontend (panel admin) |
| Endpoints nuevos | 6 endpoints de administración |
| Entidades | 1 tabla nueva (`teams`) + 1 columna nueva (`users.team_id`) |
| Migraciones | Sí — requerida |
| Business Rules | BR-NEW-05, BR-NEW-06, BR-NEW-07, BR-NEW-08 |
| Tests requeridos | Medium: Unit + Integration, cobertura >80% |
