---
id: 012-admin-user-management
persona: Administrador
fr: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006
bounded-context: Organization
status: enriched
created: 2025-01-27
enriched: 2025-01-27
---

# US-012: Admin User Management

## [original]

**Como** administrador de la plataforma,
**quiero** gestionar los usuarios de mi organización (crear, editar, activar/desactivar, asignar roles y equipos),
**para** mantener la estructura organizacional actualizada y controlar quién tiene acceso a la plataforma.

### Contexto

Actualmente los usuarios de prueba se crean mediante scripts de seed. No existe ninguna interfaz en la plataforma para que un administrador gestione usuarios. Esto hace que la plataforma no sea autosuficiente operativamente — cualquier cambio en la estructura de usuarios requiere intervención técnica directa en la base de datos.

El administrador necesita poder:
- Ver la lista de usuarios de su organización
- Crear nuevos usuarios con rol y equipo asignado
- Editar información de usuarios existentes (nombre, rol, equipo, manager)
- Activar o desactivar usuarios sin eliminarlos físicamente (soft delete)

### Notas iniciales
- Solo el rol `administrator` puede gestionar usuarios
- El `organization_id` siempre viene del JWT — nunca del body
- Los usuarios desactivados no pueden hacer login pero sus datos históricos se preservan
- Un usuario no puede cambiar su propio rol ni desactivarse a sí mismo
- La contraseña inicial se genera automáticamente o se envía por email (MVP: generada y mostrada una sola vez)

---

## [enhanced]

### User Journey

- **Usuario principal:** Administrador
- **Objetivo principal:** Gestionar el ciclo de vida completo de usuarios de su organización desde la plataforma, sin necesidad de intervención técnica en la base de datos
- **Flujo principal:**
  1. El administrador accede al panel de administración → sección Usuarios
  2. Ve la lista paginada de usuarios de su organización con filtros por rol y estado
  3. Puede crear un nuevo usuario (nombre, email, rol, manager asignado)
  4. Puede editar datos de un usuario existente
  5. Puede activar o desactivar un usuario
  6. Al crear, el sistema genera una contraseña temporal que se muestra una sola vez

---

### Business Value

- **Problema que resuelve:** La plataforma no es autosuficiente operativamente — agregar o modificar usuarios requiere acceso directo a la base de datos. Esto bloquea la adopción real del producto.
- **Beneficio esperado:** El administrador puede incorporar nuevos miembros del equipo, cambiar roles y gestionar accesos sin depender del equipo técnico.

---

### Priority

**High**
Es prerequisito para que la plataforma sea operable de forma autónoma. Sin esta US, el onboarding de nuevos usuarios requiere intervención técnica.

---

### FR de Referencia

- **FR-001** — Administrators can create users
- **FR-002** — Administrators can update user information
- **FR-003** — Administrators can activate and deactivate users
- **FR-004** — Role assignment: Administrator, Manager, Employee
- **FR-005** — Users can be assigned to teams (via manager assignment en MVP)
- **FR-006** — Managers can be assigned to employees

---

### Bounded Context

Organization → Módulo: `users` (nuevo módulo backend)

---

### Entidades Involucradas

- **User:** `id`, `organization_id`, `manager_id`, `email`, `hashed_password`, `role`, `status`, `first_name`, `last_name`, `created_at`, `updated_at`, `deleted_at`, `deleted_by`
  - `role`: `administrator` | `manager` | `employee`
  - `status`: `active` | `inactive`
  - La tabla ya existe — no requiere migración de schema

---

### Business Rules Aplicables

- **BR-013** — Un empleado solo ve sus propias prioridades (no aplica directamente, pero el aislamiento de datos sí)
- **BR-015** — Un administrador puede ver toda la organización
- **BR-016** — Ningún usuario puede acceder a datos de otra organización
- **BR-017** — Todos los agregados pertenecen a una organización
- **BR-NEW-01** — Un administrador no puede desactivarse a sí mismo
- **BR-NEW-02** — Un administrador no puede cambiar su propio rol
- **BR-NEW-03** — El email debe ser único dentro de la organización
- **BR-NEW-04** — No se puede crear un usuario con email ya existente en la misma organización

---

### Contrato API

**GET /api/v1/users**
Lista paginada de usuarios de la organización.
```
Query params: page=1, page_size=20, role=employee|manager|administrator, status=active|inactive
Response 200:
{
  "items": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "Juan",
      "last_name": "Pérez",
      "role": "employee",
      "status": "active",
      "manager_id": "uuid | null",
      "manager_name": "string | null",
      "created_at": "2025-01-06T08:00:00Z"
    }
  ],
  "total": 10,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

**POST /api/v1/users**
Crea un nuevo usuario.
```json
Request:
{
  "email": "nuevo@empresa.com",
  "first_name": "Ana",
  "last_name": "García",
  "role": "employee",
  "manager_id": "uuid"
}
Response 201:
{
  "id": "uuid",
  "email": "nuevo@empresa.com",
  "first_name": "Ana",
  "last_name": "García",
  "role": "employee",
  "status": "active",
  "manager_id": "uuid",
  "temporary_password": "Abc123!xyz",
  "created_at": "2025-01-27T10:00:00Z"
}
```
Errores: `409` email duplicado en la organización, `404` manager_id no existe, `403` no es administrador

**GET /api/v1/users/{id}**
Detalle de un usuario.
```json
Response 200: mismo schema que item de lista + manager_name
```
Errores: `404` no existe, `403` pertenece a otra organización

**PATCH /api/v1/users/{id}**
Actualiza datos de un usuario (parcial).
```json
Request (todos opcionales):
{
  "first_name": "Ana",
  "last_name": "García",
  "role": "manager",
  "manager_id": "uuid"
}
Response 200: UserResponse completo
```
Errores: `409` si intenta cambiar su propio rol, `404` usuario no existe

**PATCH /api/v1/users/{id}/status**
Activa o desactiva un usuario.
```json
Request: { "status": "inactive" }
Response 200: { "id": "uuid", "status": "inactive" }
```
Errores: `409` si intenta desactivarse a sí mismo, `404` usuario no existe

---

### Acceptance Criteria

**Escenario 1 — Admin lista usuarios de su organización**
```gherkin
Given un administrador autenticado
When hace GET /api/v1/users
Then recibe lista paginada de usuarios de su organización únicamente
  And no aparecen usuarios de otras organizaciones
  And no aparecen usuarios con deleted_at IS NOT NULL
```

**Escenario 2 — Admin crea un usuario exitosamente**
```gherkin
Given un administrador autenticado
When hace POST /api/v1/users con email único, nombre, rol y manager_id válido
Then el sistema retorna 201 con el usuario creado
  And la respuesta incluye temporary_password (mostrada una sola vez)
  And el usuario queda en status active
  And el organization_id se toma del JWT, no del body
```

**Escenario 3 — Email duplicado en la misma organización (BR-NEW-04)**
```gherkin
Given un usuario con email "juan@empresa.com" ya existe en la organización
When el admin intenta crear otro usuario con el mismo email
Then el sistema retorna 409 Conflict
  And no se crea ningún registro
```

**Escenario 4 — Admin desactiva un usuario**
```gherkin
Given un usuario activo con id X
When el admin hace PATCH /api/v1/users/X/status con status=inactive
Then el usuario queda en status inactive
  And el usuario no puede hacer login
  And sus datos históricos (check-ins, CRS) se preservan
```

**Escenario 5 — Admin no puede desactivarse a sí mismo (BR-NEW-01)**
```gherkin
Given el administrador con id Y está autenticado
When intenta hacer PATCH /api/v1/users/Y/status con status=inactive
Then el sistema retorna 409 Conflict
  And el administrador permanece activo
```

**Escenario 6 — Admin no puede cambiar su propio rol (BR-NEW-02)**
```gherkin
Given el administrador con id Y está autenticado
When intenta hacer PATCH /api/v1/users/Y con role=employee
Then el sistema retorna 409 Conflict
  And el rol permanece como administrator
```

**Escenario 7 — Aislamiento multi-tenant (BR-016)**
```gherkin
Given un administrador de la organización A
When intenta hacer GET /api/v1/users/{id} con id de un usuario de la organización B
Then el sistema retorna 403 Forbidden
```

**Escenario 8 — Employee/Manager no puede acceder a gestión de usuarios**
```gherkin
Given un usuario con rol employee o manager
When intenta hacer GET /api/v1/users
Then el sistema retorna 403 Forbidden
```

---

### Non-Functional Requirements

- **NFR-001** — Todo endpoint requiere Bearer JWT válido
- **NFR-002** — Solo rol `administrator` puede acceder a `/api/v1/users` (excepto GET propio perfil si se agrega en futuro)
- **NFR-003** — La contraseña temporal se genera con entropía suficiente (mínimo 12 caracteres, mayúscula + número + especial)
- **NFR-004** — La contraseña temporal se hashea con bcrypt antes de persistir — nunca se almacena en texto plano
- **NFR-005** — La lista de usuarios responde en < 500ms para organizaciones de hasta 500 usuarios

---

### Dependencies

- **Técnicas:**
  - Módulo `auth` — JWT con `organization_id` y `role=administrator` en payload
  - Tabla `users` — ya existe, no requiere migración
  - `passlib[bcrypt]` — ya en requirements.txt (usado por auth)
- **Funcionales:**
  - No tiene dependencias de otras US pendientes
  - Es prerequisito para que Team Management (US-013 futura) pueda asignar usuarios a equipos

---

### Nivel de Riesgo

**High**
Gestiona accesos y roles — impacto directo en seguridad. Requiere validación de aislamiento multi-tenant y RBAC.

---

### Complejidad Estimada

**M**

| Factor | Detalle |
|---|---|
| Capas afectadas | Backend (nuevo módulo `users`) + Frontend (panel admin) |
| Endpoints | 5 endpoints (GET list, POST, GET detail, PATCH update, PATCH status) |
| Entidades | 0 nuevas — reutiliza tabla `users` existente |
| Migraciones | No requeridas — tabla ya existe |
| Business Rules | BR-016, BR-017, BR-NEW-01, BR-NEW-02, BR-NEW-03, BR-NEW-04 |
| Tests requeridos | High: Unit + Integration + Security, cobertura >80% |

---

### Data Model

No requiere migración. La tabla `users` ya tiene todas las columnas necesarias:

```
users
  id              UUID PK
  organization_id UUID FK → organizations
  manager_id      UUID FK → users (self-referential, nullable)
  email           VARCHAR(255) — uq por organización (validar en app)
  hashed_password TEXT
  role            VARCHAR(20) CHECK IN ('administrator','manager','employee')
  status          VARCHAR(20) CHECK IN ('active','inactive')
  first_name      VARCHAR(100)
  last_name       VARCHAR(100)
  created_at      TIMESTAMPTZ
  updated_at      TIMESTAMPTZ
  deleted_at      TIMESTAMPTZ (soft delete)
  deleted_by      UUID
```

> **Nota:** No existe `uq_users_email` global — el email debe ser único por `organization_id`. La validación se hace en la capa de aplicación con query previo.

---

### Siguiente Paso

Ejecutar `/create-tickets 012-admin-user-management`
