---
id: 002-user-authentication
persona: Colaborador Individual
fr: NFR-001, NFR-002
bounded-context: Organization
status: enriched
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

- **Usuario principal:** Todo usuario de la plataforma — `employee`, `manager` o `administrator`
- **Objetivo principal:** Autenticarse con email y contraseña, obtener acceso al sistema según su rol, y mantener la sesión activa de forma segura sin reingresar credenciales constantemente
- **Flujo principal:**
  1. El usuario accede a `/auth/login`
  2. Ingresa email y contraseña
  3. El sistema valida las credenciales contra la BD (bcrypt)
  4. Verifica que el usuario esté activo (`status = active`)
  5. Emite Access Token (15 min) + Refresh Token (7 días) con payload `{ sub, organization_id, role, exp }`
  6. El frontend almacena el access token en memoria (Zustand) y el refresh token en HTTP-only cookie
  7. El usuario es redirigido a su dashboard según rol: `employee → /employee/dashboard`, `manager → /manager/dashboard`, `administrator → /admin/dashboard`
  8. Cuando el access token expira, el sistema renueva transparentemente usando el refresh token
  9. Al hacer logout, el refresh token es revocado en BD y el usuario es redirigido a `/auth/login`

---

### Business Value

- **Problema que resuelve:** Sin autenticación, cualquier persona podría acceder a los compromisos, CRS y datos de desempeño de cualquier organización. Sin identificar el rol, no es posible mostrar la UI correcta ni aplicar las reglas de acceso que protegen la privacidad de los datos.
- **Beneficio esperado:** Cada persona accede exclusivamente a sus datos y funcionalidades. El `organization_id` en el JWT garantiza aislamiento multi-tenant en todos los módulos. El rol determina qué ve y qué puede hacer cada usuario desde el primer request. Habilita la medición de WAU y Check-In Completion Rate.

---

### Priority

**Critical**
Prerequisito técnico absoluto de todas las demás historias del MVP. Sin auth funcional ninguna otra US puede implementarse, ejecutarse ni testearse.

---

### FR de Referencia

- **NFR-001** — Authentication: The platform shall require authentication for all users
- **NFR-002** — Authorization: The platform shall enforce role-based access control
- **NFR-003** — Data Protection: Sensitive information shall be protected in transit and at rest
- **NFR-009** — Auditability: Important actions shall be auditable

> Auth no tiene FR numérico propio pero es prerequisito de FR-001 al FR-035. Es un NFR elevado a capacidad core del MVP.

---

### Bounded Context

Organization → Módulo: `auth`

---

### Entidades Involucradas

- **User:** `id UUID PK`, `organization_id UUID FK NOT NULL`, `email VARCHAR(255) UNIQUE NOT NULL`, `hashed_password TEXT NOT NULL`, `role VARCHAR(20) NOT NULL CHECK(role IN ('administrator','manager','employee'))`, `status VARCHAR(20) NOT NULL DEFAULT 'active'`, `first_name VARCHAR(100)`, `last_name VARCHAR(100)`, `manager_id UUID FK NULL`, `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`, `deleted_at TIMESTAMPTZ NULL`, `deleted_by UUID NULL`

- **Organization:** `id UUID PK`, `name VARCHAR(255) NOT NULL`, `code VARCHAR(50) UNIQUE NOT NULL`, `status VARCHAR(20) NOT NULL DEFAULT 'active'` — determina el tenant del usuario

- **RefreshToken** (value object persistido): `id UUID PK`, `user_id UUID FK NOT NULL`, `token_hash TEXT NOT NULL UNIQUE`, `expires_at TIMESTAMPTZ NOT NULL`, `revoked_at TIMESTAMPTZ NULL`, `created_at TIMESTAMPTZ NOT NULL` — necesario para invalidar sesiones individuales

---

### Business Rules Aplicables

- **BR-016** — Ningún usuario puede acceder a datos de otra organización → el `organization_id` del JWT es la única fuente de verdad del tenant en cada request
- **BR-017** — Todos los aggregates pertenecen a una organización → validado en cada módulo consumidor vía el token que este módulo emite
- **BR-013** — Un empleado solo ve sus propias prioridades (enforcement en módulo `priorities`, no en `auth`)
- **BR-014** — Un manager solo ve su equipo (enforcement en módulos consumidores)
- **BR-015** — Un administrador puede ver toda la organización (enforcement en módulos consumidores)

> Las BRs de acceso (BR-013..BR-017) no se validan en `auth` — se validan en cada módulo usando `organization_id` y `role` del JWT emitido aquí.

---

### Transiciones de Estado

```
Sesión:
  Anónimo          → Autenticado       (login exitoso con credenciales válidas)
  Autenticado      → Anónimo           (logout explícito o refresh token expirado)
  Access expirado  → Renovado          (refresh exitoso con refresh token válido)
  Refresh expirado → Anónimo           (re-login requerido)

Usuario:
  active           → puede autenticarse
  inactive         → login bloqueado → 403 Forbidden
```

---

### Contrato API Preliminar

**POST /api/v1/auth/login**
```json
Request:
{
  "email":    "ana@empresa.com",
  "password": "secreto"
}

Response 200:
{
  "access_token":  "<jwt>",
  "refresh_token": "<jwt>",
  "token_type":    "bearer",
  "expires_in":    900
}

Errors: 400 (campos vacíos), 401 (credenciales inválidas — mensaje genérico),
        403 (usuario inactivo), 429 (rate limit excedido)
```

**POST /api/v1/auth/refresh**
```json
Request:
{ "refresh_token": "<jwt>" }

Response 200:
{ "access_token": "<jwt>", "expires_in": 900 }

Errors: 401 (token inválido/expirado/revocado), 429 (rate limit)
```

**POST /api/v1/auth/logout**
```json
Request: {} (vacío — token en Authorization header)
Response 200: { "message": "logged out" }
Errors: 401 (token inválido)
```

**GET /api/v1/auth/me**
```json
Response 200:
{
  "id":              "uuid",
  "email":           "ana@empresa.com",
  "role":            "employee",
  "organization_id": "uuid",
  "full_name":       "Ana López"
}
Errors: 401 (no autenticado)
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
Given un usuario activo con email "ana@empresa.com" y contraseña correcta en la BD
When envía POST /api/v1/auth/login con esas credenciales
Then el sistema retorna 200 con access_token y refresh_token
  And el access_token decodificado contiene sub, organization_id, role y exp
  And se registra evento de auditoría "auth.login_success" con user_id, organization_id, ip y timestamp
```

**Escenario 2 — Login fallido con credenciales incorrectas**
```gherkin
Given un usuario con email válido pero contraseña incorrecta
When envía POST /api/v1/auth/login
Then el sistema retorna 401 con mensaje genérico "Invalid credentials"
  And el mensaje NO especifica si el email o la contraseña son incorrectos
  And se registra evento de auditoría "auth.login_failed"
```

**Escenario 3 — Usuario inactivo no puede autenticarse**
```gherkin
Given un usuario con status "inactive" en la organización
When envía POST /api/v1/auth/login con credenciales correctas
Then el sistema retorna 403 Forbidden
  And no se emite ningún token
  And no se registra evento de login_success
```

**Escenario 4 — Refresh token renueva el access token**
```gherkin
Given un usuario autenticado con access_token expirado y refresh_token válido y no revocado
When envía POST /api/v1/auth/refresh con el refresh_token
Then el sistema retorna 200 con un nuevo access_token
  And el nuevo access_token contiene el mismo organization_id y role
  And se registra evento "auth.token_refreshed"
```

**Escenario 5 — Logout invalida la sesión**
```gherkin
Given un usuario autenticado con access_token y refresh_token válidos
When envía POST /api/v1/auth/logout con su access_token en el header
Then el sistema retorna 200 con { "message": "logged out" }
  And el refresh_token queda con revoked_at = now() en la BD
  And un intento posterior de usar ese refresh_token retorna 401
```

**Escenario 6 — Redirección por rol tras login**
```gherkin
Given un usuario con role "manager" que hace login exitoso
When el frontend procesa la respuesta del login
Then el usuario es redirigido a /manager/dashboard
  And no puede acceder a /admin/* (retorna 403)
  And no puede ver datos de /employee/* de otro usuario (retorna 403)
```

**Escenario 7 — Rate limiting en intentos fallidos**
```gherkin
Given un cliente que envía 5 intentos de login fallidos en menos de 1 minuto
When envía el sexto intento
Then el sistema retorna 429 Too Many Requests
  And el response incluye header Retry-After con los segundos de espera
```

**Escenario 8 — Aislamiento multi-tenant**
```gherkin
Given dos organizaciones distintas con usuarios en cada una
When el usuario de la organización A se autentica y obtiene su JWT
Then su JWT contiene el organization_id de la organización A
  And cualquier request con ese token solo puede acceder a datos de la organización A
  And intentar acceder a datos de la organización B retorna 403
```

---

### Non-Functional Requirements

- **NFR-001 — Authentication:** Todos los endpoints protegidos validan el JWT antes de ejecutar lógica de negocio; validación en `dependencies.py` de cada módulo
- **NFR-002 — Authorization:** El `role` del token determina las operaciones permitidas; enforcement en `dependencies.py` de cada módulo consumidor
- **NFR-003 — Data Protection:** Contraseñas almacenadas con bcrypt (nunca texto plano); tokens transmitidos solo por HTTPS; refresh token en HTTP-only cookie
- **NFR-004 — Response Time:** Login debe responder en < 500ms bajo carga normal
- **NFR-009 — Auditability:** Registrar `auth.login_success`, `auth.login_failed`, `auth.logout`, `auth.token_refreshed` con `user_id`, `organization_id`, `ip`, `timestamp`
- **NFR-012 — Observability:** Logs estructurados con `correlation_id` en cada request de auth

---

### Dependencies

- **Técnicas:**
  - Tabla `organizations` debe existir antes de crear `users`
  - Tabla `users` con campos `email`, `hashed_password`, `role`, `status`, `organization_id`
  - Tabla `refresh_tokens` nueva
  - Variables de entorno `JWT_SECRET`, `JWT_REFRESH_SECRET`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`, `JWT_REFRESH_TOKEN_EXPIRE_DAYS`
  - Librería `passlib[bcrypt]` o `bcrypt` directamente
  - Librería `python-jose` o `PyJWT` para firma de tokens
  - Middleware de rate limiting (`slowapi`)
- **Funcionales:**
  - Al menos 1 usuario seed por rol debe existir en la BD para poder probar el flujo
  - Es prerequisito de **todas** las historias del MVP sin excepción

---

### Success Metrics

- **Weekly Active Users (WAU):** Auth es la puerta de entrada; sin login funcional no hay usuarios activos medibles
- **Check-In Completion Rate:** Solo medible cuando los usuarios pueden autenticarse y ejecutar su check-in — auth habilita directamente esta métrica (target >90%)

---

### Nivel de Riesgo

**Critical**
Módulo `auth` es siempre Critical por definición (testing-standards.md). Expone credenciales, emite tokens de acceso a toda la plataforma y es el principal vector de ataque del sistema.

---

### Complejidad Estimada

**M**

| Factor | Detalle |
|---|---|
| Capas afectadas | DB + Backend + Frontend (3 capas) |
| Endpoints | 4 endpoints nuevos: login, refresh, logout, me |
| Entidades | 1 existente creada (User con password), 1 valor nuevo persistido (RefreshToken), 1 tabla base (Organization) |
| Business Rules | BR-013, BR-014, BR-015, BR-016, BR-017 (BR-016 y BR-017 se aplican directamente en `auth`; las demás en módulos consumidores) |
| Tests requeridos | Critical: Unit + Integration + Contract + E2E + Security, cobertura >95% |
| Justificación | Scope funcional moderado (login/logout/refresh/me) pero nivel de riesgo eleva los requisitos. Sin state machines complejas ni múltiples entidades nuevas. La complejidad técnica real está en seguridad: hashing, rate limiting, HTTP-only cookies, auditoría, aislamiento cross-tenant. |

---

### Siguiente Paso

Ejecutar `/create-tickets 002-user-authentication`
