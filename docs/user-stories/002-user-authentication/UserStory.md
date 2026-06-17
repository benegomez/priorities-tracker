---
id: 002-user-authentication
persona: Colaborador Individual
fr: NFR-001, NFR-002
bounded-context: Organization
status: draft
created: 2025-01-06
---

# US-002: User Authentication

## [original]

**Como** usuario de la plataforma (empleado, manager o administrador),
**quiero** iniciar sesión con mis credenciales y obtener acceso seguro al sistema,
**para** acceder a mis funcionalidades según mi rol sin comprometer la seguridad de los datos de mi organización.

### Contexto

Antes de que cualquier persona pueda registrar compromisos, ver dashboards o consultar el CRS de su equipo, necesita autenticarse. El sistema debe identificar quién es el usuario, a qué organización pertenece y qué rol tiene — esta información viaja en el JWT y es utilizada por todos los módulos del sistema para aplicar RBAC y aislamiento multi-tenant. Sin autenticación funcional, ninguna otra historia del MVP puede ejecutarse ni testearse correctamente.

### Notas iniciales
- JWT Access Token de vida corta + Refresh Token de vida larga
- El payload del JWT debe incluir `user_id`, `organization_id` y `role`
- El `organization_id` del token es la única fuente válida de tenant en todo el sistema
- Rate limiting obligatorio en `/auth/login` y `/auth/refresh` (NFR-002)
- Eventos de auditoría para login exitoso y fallido (NFR-009)
- Es prerequisito técnico de todas las demás historias del MVP

---

## [enhanced]

### User Journey

- **Usuario principal:** Toda persona que accede a la plataforma — empleado, manager o administrador
- **Objetivo principal:** Autenticarse con email y contraseña, obtener acceso al sistema según su rol, y mantener la sesión activa de forma segura sin tener que re-ingresar credenciales constantemente
- **Flujo principal:**
  1. El usuario accede a `/auth/login`
  2. Ingresa email y contraseña
  3. El sistema valida las credenciales y retorna Access Token + Refresh Token
  4. El Access Token se almacena en HTTP-only cookie
  5. El usuario es redirigido a su dashboard según su rol:
     - `employee` → `/employee/dashboard`
     - `manager` → `/manager/dashboard`
     - `administrator` → `/admin/dashboard`
  6. Cuando el Access Token expira, el sistema usa el Refresh Token transparentemente
  7. Al hacer logout, ambos tokens son invalidados y el usuario es redirigido a `/auth/login`

---

### Business Value

- **Problema que resuelve:** Sin autenticación, cualquier persona podría acceder a los compromisos, CRS y datos de desempeño de cualquier organización. Adicionalmente, sin identificar el rol del usuario, no es posible mostrar la UI correcta ni aplicar las reglas de acceso que protegen la privacidad de los datos.
- **Beneficio esperado:** Cada persona accede exclusivamente a sus datos y funcionalidades. El `organization_id` en el JWT garantiza aislamiento multi-tenant en todos los módulos. El rol determina qué ve y qué puede hacer cada usuario desde el primer request.

---

### Priority

**Critical**
Prerequisito técnico absoluto. Sin auth funcional no es posible implementar, ejecutar ni testear ninguna otra historia del MVP. US-001 (Check-In) ya tiene tickets creados que dependen de un JWT válido.

---

### FR de Referencia

- **NFR-001** — Authentication: The platform shall require authentication for all users
- **NFR-002** — Authorization: The platform shall enforce role-based access control
- **NFR-003** — Data Protection: Sensitive information shall be protected in transit and at rest
- **NFR-009** — Auditability: Important actions shall be auditable

> Nota: Auth no tiene FR numérico propio pero es prerequisito de FR-001 al FR-035. Es un NFR elevado a capacidad core del MVP.

---

### Bounded Context

Organization → Módulo: `auth`

---

### Entidades Involucradas

- **User:** `id`, `organization_id`, `email`, `hashed_password`, `role` (`administrator` | `manager` | `employee`), `status` (`active` | `inactive`)
- **Organization:** `id`, `name`, `status` — determina el tenant del usuario
- **RefreshToken** (valor): `token_hash`, `user_id`, `expires_at`, `revoked_at` — necesario para invalidar sesiones

---

### Business Rules Aplicables

- **BR-015** — Un administrador puede ver toda la organización
- **BR-014** — Un manager solo ve su equipo
- **BR-013** — Un empleado solo ve sus propias prioridades
- **BR-016** — Ningún usuario puede acceder a datos de otra organización → el `organization_id` del JWT es la única fuente de verdad del tenant
- **BR-017** — Todos los agregados pertenecen a una organización → validado en cada request mediante el token

> Las BRs de acceso (BR-013..BR-017) no se validan en `auth` — se validan en cada módulo usando el `organization_id` y `role` extraídos del JWT que este módulo emite.

---

### Transiciones de Estado

```
Sesión:  Anónimo → Autenticado (login exitoso)
         Autenticado → Anónimo (logout o token expirado sin refresh)
         Access Token expirado → Renovado (refresh exitoso)
         Refresh Token expirado → Anónimo (re-login requerido)
```

---

### Contrato API Preliminar

**POST /api/v1/auth/login**
```
Request:
{
  "email":    "usuario@empresa.com",
  "password": "contraseña"
}

Response 200:
{
  "access_token":  "<jwt>",
  "refresh_token": "<jwt>",
  "token_type":    "bearer",
  "expires_in":    900
}

Errors:
  400 — email o password vacíos
  401 — credenciales inválidas (mensaje genérico, no especificar cuál falló)
  403 — usuario inactivo
  429 — rate limit excedido
```

**POST /api/v1/auth/refresh**
```
Request:
{
  "refresh_token": "<jwt>"
}

Response 200:
{
  "access_token": "<jwt>",
  "expires_in":   900
}

Errors:
  401 — refresh token inválido o expirado
  429 — rate limit excedido
```

**POST /api/v1/auth/logout**
```
Request: {} (vacío, token en header)
Response 200: { "message": "logged out" }
Errors: 401 — token inválido
```

**GET /api/v1/auth/me**
```
Response 200:
{
  "id":              "uuid",
  "email":           "usuario@empresa.com",
  "role":            "employee",
  "organization_id": "uuid",
  "full_name":       "string"
}
Errors: 401 — no autenticado
```

**Payload JWT obligatorio:**
```json
{
  "sub":             "<user_id>",
  "organization_id": "<org_id>",
  "role":            "employee | manager | administrator",
  "exp":             "<timestamp>"
}
```

---

### Acceptance Criteria

**Escenario 1 — Login exitoso con credenciales válidas**
```gherkin
Given un usuario activo con email "ana@empresa.com" y contraseña correcta
When envía POST /api/v1/auth/login con esas credenciales
Then el sistema retorna 200 con access_token y refresh_token
  And el access_token contiene sub, organization_id, role y exp
  And se registra evento de auditoría "auth.login_success"
```

**Escenario 2 — Login fallido con credenciales incorrectas**
```gherkin
Given un usuario con email válido pero contraseña incorrecta
When envía POST /api/v1/auth/login
Then el sistema retorna 401 con mensaje genérico
  And el mensaje NO especifica si el email o la contraseña son incorrectos
  And se registra evento de auditoría "auth.login_failed"
```

**Escenario 3 — Usuario inactivo no puede acceder**
```gherkin
Given un usuario con status "inactive" en la organización
When envía POST /api/v1/auth/login con credenciales correctas
Then el sistema retorna 403 Forbidden
  And no se emite ningún token
```

**Escenario 4 — Refresh token renueva el access token**
```gherkin
Given un usuario autenticado con access_token expirado y refresh_token válido
When envía POST /api/v1/auth/refresh con el refresh_token
Then el sistema retorna 200 con un nuevo access_token
  And el nuevo access_token contiene el mismo organization_id y role
```

**Escenario 5 — Logout invalida la sesión**
```gherkin
Given un usuario autenticado con tokens válidos
When envía POST /api/v1/auth/logout con su access_token
Then el sistema retorna 200
  And el refresh_token queda invalidado
  And intentar usar ese refresh_token retorna 401
```

**Escenario 6 — Redirección por rol tras login**
```gherkin
Given un usuario con role "manager" que hace login exitoso
When el frontend procesa la respuesta
Then el usuario es redirigido a /manager/dashboard
  And no puede acceder a /admin/* ni a /employee/* de otro usuario
```

**Escenario 7 — Rate limiting en login**
```gherkin
Given un cliente que envía 6 intentos de login fallidos en menos de 1 minuto
When envía el séptimo intento
Then el sistema retorna 429 Too Many Requests
  And incluye header Retry-After con los segundos de espera
```

---

### Non-Functional Requirements

- **NFR-001 — Authentication:** Todos los endpoints protegidos validan el JWT antes de ejecutar lógica de negocio
- **NFR-002 — Authorization:** El rol del token determina las operaciones permitidas en cada módulo; validación en `dependencies.py` de cada módulo
- **NFR-003 — Data Protection:** Contraseñas almacenadas con bcrypt (nunca en texto plano); tokens transmitidos solo por HTTPS; almacenados en HTTP-only cookies
- **NFR-004 — Response Time:** Login debe responder en < 500ms
- **NFR-009 — Auditability:** Registrar `auth.login_success`, `auth.login_failed`, `auth.logout`, `auth.token_refreshed` con `user_id`, `organization_id`, `ip`, `timestamp`

---

### Dependencies

- **Técnicas:**
  - Tabla `users` con campos `email`, `hashed_password`, `role`, `status`, `organization_id` debe existir
  - Tabla `organizations` debe existir
  - Variables de entorno `JWT_SECRET` y `JWT_REFRESH_SECRET` configuradas
  - Librería de hashing de contraseñas (`bcrypt` o `passlib`)
- **Funcionales:**
  - Al menos un usuario seed debe existir en la BD para poder probar el login
  - Es prerequisito de **todas** las historias del MVP sin excepción

---

### Success Metrics

- **Weekly Active Users (WAU):** Esta historia es la puerta de entrada que permite medir cuántos usuarios activos tiene la plataforma cada semana
- **Check-In Completion Rate:** Solo puede medirse cuando los usuarios pueden autenticarse y registrar su check-in — auth habilita la métrica

---

### Nivel de Riesgo

**Critical**
Módulo `auth` es siempre Critical por definición (testing-standards.md). Expone credenciales, emite tokens de acceso a toda la plataforma y es vector de ataque principal.

---

### Complejidad Estimada

**M**

| Factor | Detalle |
|---|---|
| Capas afectadas | DB + Backend + Frontend (3 capas) |
| Endpoints | 4 endpoints (login, refresh, logout, me) |
| Entidades | 1 existente modificada (User + password), 1 valor nuevo (RefreshToken) |
| Business Rules | BR-013, BR-014, BR-015, BR-016, BR-017 (aplicadas en otros módulos vía token) |
| Tests requeridos | Critical: Unit + Integration + Contract + E2E + Security, cobertura >95% |
| Justificación | Aunque el scope funcional es M (login/logout/refresh), el nivel de riesgo eleva los tests a Critical. La complejidad técnica es moderada — sin state machines complejas ni múltiples entidades nuevas — pero los requisitos de seguridad (hashing, rate limiting, HTTP-only cookies, audit) agregan superficie. |

---

### Siguiente Paso

Ejecutar `/create-tickets 002-user-authentication`
