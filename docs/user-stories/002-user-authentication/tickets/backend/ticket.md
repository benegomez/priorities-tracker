---
status: todo
type: backend
story: docs/user-stories/002-user-authentication/UserStory.md
depends-on: tickets/database/ticket.md
---

# [BE] User Authentication — FastAPI + JWT

## Objetivo
Implementar los 4 endpoints de autenticación (login, refresh, logout, me) con JWT Access Token + Refresh Token, rate limiting, hashing de contraseñas y auditoría de eventos.

## Scope
FastAPI router, Pydantic schemas, casos de uso, repositorios SQLAlchemy, servicios de seguridad. Sin schema SQL, sin UI.

## Dependencia
Ticket database mergeado y migración aplicada. Seed con 2 organizaciones ejecutado. Variables `JWT_SECRET`, `JWT_REFRESH_SECRET`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`, `JWT_REFRESH_TOKEN_EXPIRE_DAYS` en `.env`.

### Librerías requeridas (agregar a `requirements.txt`)
```
passlib[bcrypt]
python-jose[cryptography]
slowapi
```

## FR de Referencia
- NFR-001 — Authentication requerida para todos los endpoints protegidos
- NFR-002 — RBAC aplicado en cada módulo mediante `role` del JWT
- NFR-003 — Contraseñas con bcrypt; tokens en HTTPS
- NFR-009 — Eventos de auditoría para login, logout, refresh
- NFR-012 — Observability: logs estructurados con `correlation_id` en cada request de auth

## Business Rules Aplicables
- BR-016 — `organization_id` del JWT es la única fuente de verdad del tenant
- BR-017 — Todo aggregate pertenece a una organización (enforcement vía token en módulos consumidores)
- BR-013/014/015 — Permisos por rol (enforcement en módulos consumidores, no en `auth`)

---

## Contrato OpenAPI (ADR-009 — definir antes de implementar)

### POST /api/v1/auth/login
**Tags:** `[auth]`
**operation_id:** `login`
**Auth:** No requerida

Request body:
```json
{
  "email": "ana@empresa.com",
  "password": "secreto"
}
```

Response 200:
```json
{
  "access_token":  "<jwt>",
  "refresh_token": "<jwt>",
  "token_type":    "bearer",
  "expires_in":    900
}
```

Responses de error: `400` (campos vacíos), `401` (credenciales inválidas — mensaje genérico), `403` (usuario inactivo), `429` (rate limit)

---

### POST /api/v1/auth/refresh
**Tags:** `[auth]`
**operation_id:** `refresh_token`
**Auth:** No requerida

Request body:
```json
{ "refresh_token": "<jwt>" }
```

Response 200:
```json
{ "access_token": "<jwt>", "expires_in": 900 }
```

Responses de error: `401` (token inválido/expirado), `429` (rate limit)

---

### POST /api/v1/auth/logout
**Tags:** `[auth]`
**operation_id:** `logout`
**Auth:** Bearer JWT requerido

Request body: `{}` (vacío)

Response 200:
```json
{ "message": "logged out" }
```

Responses de error: `401` (token inválido)

---

### GET /api/v1/auth/me
**Tags:** `[auth]`
**operation_id:** `get_current_user_info`
**Auth:** Bearer JWT requerido

Response 200:
```json
{
  "id":              "uuid",
  "email":           "ana@empresa.com",
  "role":            "employee",
  "organization_id": "uuid",
  "full_name":       "Ana López"
}
```

Responses de error: `401` (no autenticado)

---

## Archivos a Crear / Modificar

```
apps/backend/src/modules/auth/
  api/
    router.py          - CREATE
    schemas.py         - CREATE (LoginRequest, LoginResponse, RefreshRequest,
                                  RefreshResponse, LogoutResponse, MeResponse)
    dependencies.py    - CREATE (get_current_user, require_roles)
  application/
    commands/
      login_command.py          - CREATE
      refresh_token_command.py  - CREATE
      logout_command.py         - CREATE
  domain/
    entities/
      user.py               - CREATE (User entity con role, status, organization_id)
    value_objects/
      refresh_token.py      - CREATE (token_hash, user_id, expires_at, revoked_at)
    repositories/
      user_repository.py        - CREATE (interfaz: get_by_email, get_by_id)
      refresh_token_repository.py - CREATE (interfaz: save, get_by_hash, revoke)
  infrastructure/
    repositories/
      user_repo_impl.py         - CREATE (SQLAlchemy async)
      refresh_token_repo_impl.py - CREATE

apps/backend/src/shared/
  security/
    jwt_service.py      - CREATE (create_access_token, create_refresh_token,
                                   decode_token, verify_token)
    password_service.py - CREATE (hash_password, verify_password — usa passlib[bcrypt])
  logging/
    audit_logger.py     - MODIFY (agregar eventos auth.* con correlation_id)

apps/backend/src/main.py - MODIFY (registrar router de auth)
```

---

## Casos de Uso a Implementar

- `LoginUseCase` — valida credenciales, verifica status activo, emite access+refresh token, registra auditoría
- `RefreshTokenUseCase` — valida refresh token, verifica no revocado/expirado, emite nuevo access token
- `LogoutUseCase` — revoca el refresh token del usuario (`revoked_at = now()`)

---

## Validaciones de Dominio

Las siguientes validaciones van en la capa de aplicación/dominio, **nunca** solo en el router:

- Email y password no pueden estar vacíos → `ValidationException`
- Usuario no encontrado O password incorrecto → `AuthenticationException` (mensaje genérico, no distinguir cuál falló — seguridad)
- Usuario con `status = inactive` → `AuthorizationException` → HTTP 403
- Refresh token no encontrado, revocado o expirado → `AuthenticationException` → HTTP 401
- `organization_id` del usuario debe estar presente → `DomainException` si falta

---

## Configuración de Rate Limiting

Aplicar en los endpoints `/login` y `/refresh`:
- Máximo 5 intentos por minuto por IP
- Response 429 con header `Retry-After: <segundos>`
- Implementar con `slowapi` o middleware propio

Variables de entorno requeridas:
```bash
JWT_SECRET=<generar con openssl rand -hex 32>
JWT_REFRESH_SECRET=<generar con openssl rand -hex 32>
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## Tests Requeridos

> Nivel de riesgo = Critical | Complejidad = M → cobertura mínima >95%

### Unit Tests — `modules/auth/tests/unit/` ✅
Herramienta: `pytest` con mocks de repositorios
Cobertura mínima: **>95%**

**LoginUseCase:**
- [ ] `test_login_valid_credentials_returns_tokens`
- [ ] `test_login_invalid_password_raises_authentication_exception`
- [ ] `test_login_email_not_found_raises_authentication_exception`
- [ ] `test_login_inactive_user_raises_authorization_exception`
- [ ] `test_login_empty_email_raises_validation_error`
- [ ] `test_login_empty_password_raises_validation_error`
- [ ] `test_login_success_emits_audit_event`
- [ ] `test_login_failure_emits_audit_event`

**RefreshTokenUseCase:**
- [ ] `test_refresh_valid_token_returns_new_access_token`
- [ ] `test_refresh_expired_token_raises_authentication_exception`
- [ ] `test_refresh_revoked_token_raises_authentication_exception`
- [ ] `test_refresh_invalid_token_raises_authentication_exception`

**LogoutUseCase:**
- [ ] `test_logout_revokes_refresh_token`
- [ ] `test_logout_invalid_token_raises_authentication_exception`

**JwtService:**
- [ ] `test_create_access_token_contains_required_claims`
- [ ] `test_decode_expired_token_raises_exception`
- [ ] `test_decode_invalid_signature_raises_exception`

**PasswordService:**
- [ ] `test_hash_password_is_not_plaintext`
- [ ] `test_verify_correct_password_returns_true`
- [ ] `test_verify_wrong_password_returns_false`

### Integration Tests — `modules/auth/tests/integration/` ✅
Herramienta: `pytest` + `testcontainers`

- [ ] `test_user_repository_get_by_email_returns_user`
- [ ] `test_user_repository_returns_none_for_unknown_email`
- [ ] `test_user_repository_filters_inactive_users_correctly`
- [ ] `test_refresh_token_repository_save_and_retrieve_by_hash`
- [ ] `test_refresh_token_repository_revoke_sets_revoked_at`
- [ ] `test_endpoint_login_returns_200_with_valid_credentials`
- [ ] `test_endpoint_login_returns_401_with_wrong_password`
- [ ] `test_endpoint_login_returns_403_for_inactive_user`
- [ ] `test_endpoint_refresh_returns_200_with_valid_token`
- [ ] `test_endpoint_logout_returns_200_and_revokes_token`
- [ ] `test_endpoint_me_returns_user_info_with_valid_token`
- [ ] `test_endpoint_me_returns_401_without_token`
- [ ] `test_endpoint_login_returns_429_after_5_failed_attempts`

### Contract Tests — `modules/auth/tests/contract/` ✅
Herramienta: `schemathesis`

- [ ] `test_auth_openapi_schema_is_valid`
- [ ] `test_login_response_matches_contract`
- [ ] `test_refresh_response_matches_contract`
- [ ] `test_me_response_matches_contract`

### E2E Tests — `tests/e2e/` ✅
Herramienta: `Playwright`

- [ ] `test_login_flow_redirects_employee_to_employee_dashboard`
- [ ] `test_login_flow_redirects_manager_to_manager_dashboard`
- [ ] `test_login_flow_redirects_admin_to_admin_dashboard`
- [ ] `test_login_invalid_credentials_shows_error_message`
- [ ] `test_logout_redirects_to_login_page`
- [ ] `test_protected_route_unauthenticated_redirects_to_login`

### Security Tests ✅
- [ ] `bandit` sin findings HIGH/CRITICAL en módulo `auth` y `shared/security`
- [ ] `pip-audit` sin vulnerabilidades conocidas en dependencias de seguridad
- [ ] `test_login_error_message_does_not_reveal_which_field_failed`
- [ ] `test_jwt_secret_not_present_in_response_body`
- [ ] `test_refresh_token_from_org_a_cannot_be_used_in_org_b_context`
- [ ] `test_user_from_org_a_cannot_authenticate_as_user_from_org_b`
- [ ] `test_correlation_id_present_in_audit_log_events`

## Git Branch
`feature/user-authentication-backend`
