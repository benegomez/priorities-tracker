# Auth API

## Resumen

Módulo de autenticación de Priorities Tracker. Gestiona login, refresh de tokens, logout e información del usuario autenticado.

**Prefijo:** `/api/v1/auth`
**Tags:** `auth`
**Implementación:** `apps/backend/src/modules/auth/`

---

## Endpoints

### POST /api/v1/auth/login

**operation_id:** `login`
**Auth:** No requerida
**Rate limit:** 5 req/min por IP (configurable via `RATELIMIT_ENABLED`)

**Request body:**
```json
{
  "email": "ana@empresa.com",
  "password": "secreto"
}
```

**Response 200:**
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Responses de error:**
| Status | Detalle |
|---|---|
| 400 | Campos vacíos o formato inválido (email) |
| 401 | "Invalid credentials" — mensaje genérico, no revela qué campo falló |
| 403 | "User account is inactive" |
| 429 | Rate limit excedido — incluye header `Retry-After` |

---

### POST /api/v1/auth/refresh

**operation_id:** `refresh_token`
**Auth:** No requerida
**Rate limit:** 5 req/min por IP

**Request body:**
```json
{ "refresh_token": "<jwt>" }
```

**Response 200:**
```json
{ "access_token": "<jwt>", "expires_in": 900 }
```

**Responses de error:**
| Status | Detalle |
|---|---|
| 401 | "Invalid or expired refresh token" |
| 429 | Rate limit excedido |

---

### POST /api/v1/auth/logout

**operation_id:** `logout`
**Auth:** Bearer JWT requerido

**Request body:**
```json
{ "refresh_token": "<jwt>" }
```

**Response 200:**
```json
{ "message": "logged out" }
```

**Responses de error:**
| Status | Detalle |
|---|---|
| 401 | Token inválido o ausente |

**Comportamiento:** Revoca el refresh token (`revoked_at = now()`) para que no pueda reutilizarse.

---

### GET /api/v1/auth/me

**operation_id:** `get_current_user_info`
**Auth:** Bearer JWT requerido

**Response 200:**
```json
{
  "id": "uuid",
  "email": "ana@empresa.com",
  "role": "employee",
  "organization_id": "uuid",
  "full_name": "Ana López"
}
```

**Responses de error:**
| Status | Detalle |
|---|---|
| 401 | "Not authenticated" o "User not found" |

---

## JWT Payload

```json
{
  "sub": "<user_id>",
  "organization_id": "<org_id>",
  "role": "employee | manager | administrator",
  "exp": "<timestamp>",
  "type": "access"
}
```

- **Access Token:** vida 15 min (configurable via `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Refresh Token:** vida 7 días (configurable via `JWT_REFRESH_TOKEN_EXPIRE_DAYS`)
- **Algoritmo:** HS256
- **Secretos:** `JWT_SECRET` (access), `JWT_REFRESH_SECRET` (refresh)

---

## Seguridad

- Contraseñas almacenadas con `bcrypt`
- Mensaje de error en login es genérico — nunca revela si el email o la contraseña son incorrectos
- El `organization_id` se extrae del JWT, nunca del request body
- Rate limiting en `/login` y `/refresh` para mitigar ataques de fuerza bruta
- Refresh tokens hasheados (SHA-256) antes de persistirse en BD
- Eventos de auditoría: `auth.login_success`, `auth.login_failed`, `auth.logout`, `auth.token_refreshed`

---

## Dependencias Compartidas

- `apps/backend/src/shared/security/jwt_service.py` — creación y decodificación de tokens
- `apps/backend/src/shared/security/password_service.py` — hashing y verificación de contraseñas
- `apps/backend/src/modules/auth/api/dependencies.py` — `get_current_user`, `require_roles` (usados por todos los módulos)
