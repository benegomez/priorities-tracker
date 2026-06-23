---
ticket: docs/user-stories/002-user-authentication/tickets/backend/ticket.md
layer: backend
depends-on: docs/user-stories/002-user-authentication/tickets/database/ticket.md
progress: 57 / 57 tasks completed
---

# Plan de Desarrollo — [BE] User Authentication — FastAPI + JWT

> Marca cada tarea con `- [x]` al completarla. Actualiza `progress` en el frontmatter.

## Fase 1 · Prerequisitos
- [x] Ticket database commiteado en el mismo branch
- [x] Continuar en branch existente: `git checkout feature/002-user-authentication`
- [x] Leer `.amazonq/rules/backend-standards.md` y `security-standards.md`
- [x] Agregar dependencias a `requirements.txt`: `bcrypt`, `python-jose[cryptography]`, `slowapi`, `email-validator`
- [x] Verificar variables de entorno en `.env`: `JWT_SECRET`, `JWT_REFRESH_SECRET`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15`, `JWT_REFRESH_TOKEN_EXPIRE_DAYS=7`
- [x] Actualizar `.env.example` con las nuevas variables (con comentarios, sin valores reales)

## Fase 2 · Contrato OpenAPI — Schemas Pydantic
_Archivo: `apps/backend/src/modules/auth/api/schemas.py`_
_Antes de escribir lógica — ADR-009_
- [x] Definir `LoginRequest`: `email: EmailStr`, `password: str` con `ConfigDict(extra="forbid")`
- [x] Definir `LoginResponse`: `access_token: str`, `refresh_token: str`, `token_type: str`, `expires_in: int`
- [x] Definir `RefreshRequest`: `refresh_token: str`
- [x] Definir `RefreshResponse`: `access_token: str`, `expires_in: int`
- [x] Definir `LogoutResponse`: `message: str`
- [x] Definir `MeResponse`: `id: UUID`, `email: str`, `role: str`, `organization_id: UUID`, `full_name: str`
- [x] Agregar `model_config` con `json_schema_extra` (ejemplos) en todos los schemas públicos

## Fase 3 · Servicios Compartidos (shared/security/)
_Archivos: `jwt_service.py` y `password_service.py`_
- [x] Implementar `PasswordService.hash_password(plain: str) -> str` con `bcrypt`
- [x] Implementar `PasswordService.verify_password(plain: str, hashed: str) -> bool`
- [x] Implementar `JwtService.create_access_token(user_id, organization_id, role) -> str` con `python-jose`
- [x] Implementar `JwtService.create_refresh_token(user_id) -> str`
- [x] Implementar `JwtService.decode_token(token: str) -> dict` — lanza excepción si expirado o firma inválida
- [x] Verificar que payload incluye obligatoriamente `sub`, `organization_id`, `role`, `exp`

## Fase 4 · Dominio
_Archivos: `domain/entities/user.py` y `domain/value_objects/refresh_token.py`_
- [x] Implementar entidad `User` con campos `id`, `organization_id`, `email`, `hashed_password`, `role`, `status`
- [x] Agregar método `is_active() -> bool` en `User`
- [x] Implementar value object `RefreshToken` con `token_hash`, `user_id`, `expires_at`, `revoked_at`
- [x] Agregar método `is_valid() -> bool` en `RefreshToken` (verifica expiración y revocación)
- [x] Sin imports de FastAPI ni SQLAlchemy en el dominio

## Fase 5 · Repositorios — Interfaces
_Archivos: `domain/repositories/user_repository.py` y `refresh_token_repository.py`_
- [x] Definir interfaz `UserRepository` con métodos: `get_by_email(email) -> User | None`, `get_by_id(id) -> User | None`
- [x] Definir interfaz `RefreshTokenRepository` con métodos: `save(token)`, `get_by_hash(hash) -> RefreshToken | None`, `revoke(hash)`

## Fase 6 · Repositorios — Implementaciones SQLAlchemy
_Archivos: `infrastructure/repositories/user_repo_impl.py` y `refresh_token_repo_impl.py`_
- [x] Implementar `UserRepositoryImpl` con `AsyncSession`, filtrar siempre `deleted_at IS NULL`
- [x] Filtrar por `organization_id` en todas las queries de `UserRepositoryImpl`
- [x] `SELECT` con columnas explícitas — sin `SELECT *`
- [x] Implementar `RefreshTokenRepositoryImpl`: `save`, `get_by_hash`, `revoke` (set `revoked_at = now()`)

## Fase 7 · Casos de Uso
_Archivos: `application/commands/`_

### LoginUseCase
- [x] Buscar usuario por email — si no existe lanzar `AuthenticationException` (mensaje genérico)
- [x] Verificar contraseña con `PasswordService.verify_password` — si falla lanzar `AuthenticationException` (mismo mensaje genérico, no distinguir cuál campo falló)
- [x] Verificar `user.is_active()` — si `False` lanzar `AuthorizationException` → HTTP 403
- [x] Emitir access token + refresh token, persistir hash del refresh token
- [x] Registrar evento `auth.login_success` con `user_id`, `organization_id`, `ip`, `timestamp`, `correlation_id`
- [x] En caso de error registrar evento `auth.login_failed`

### RefreshTokenUseCase
- [x] Buscar refresh token por hash — si no existe lanzar `AuthenticationException`
- [x] Verificar `refresh_token.is_valid()` — si revocado o expirado lanzar `AuthenticationException`
- [x] Emitir nuevo access token con mismo `organization_id` y `role`
- [x] Registrar evento `auth.token_refreshed`

### LogoutUseCase
- [x] Revocar refresh token del usuario (`revoked_at = now()`)
- [x] Registrar evento `auth.logout`

## Fase 8 · Rate Limiting
- [x] Configurar `slowapi` en `main.py`
- [x] Aplicar límite de 5 req/min por IP en `POST /api/v1/auth/login`
- [x] Aplicar límite de 5 req/min por IP en `POST /api/v1/auth/refresh`
- [x] Verificar que response 429 incluye header `Retry-After`

## Fase 9 · Router y Dependencies
_Archivos: `api/router.py` y `api/dependencies.py`_
- [x] Implementar `get_current_user` en `dependencies.py`: extrae y valida JWT del header `Authorization: Bearer`
- [x] Implementar `require_roles(*roles)` en `dependencies.py`: verifica rol del token
- [x] Registrar endpoint `POST /api/v1/auth/login` con `operation_id="login"`, sin auth, con rate limit
- [x] Registrar endpoint `POST /api/v1/auth/refresh` con `operation_id="refresh_token"`, sin auth, con rate limit
- [x] Registrar endpoint `POST /api/v1/auth/logout` con `operation_id="logout"`, `Depends(get_current_user)`
- [x] Registrar endpoint `GET /api/v1/auth/me` con `operation_id="get_current_user_info"`, `Depends(get_current_user)`
- [x] Toda lógica delegada a casos de uso — sin lógica de negocio en el router
- [x] Registrar router en `apps/backend/src/main.py`

## Fase 10 · Tests

### Unit Tests — 18/18 ✅
- [x] `test_login_valid_credentials_returns_tokens`
- [x] `test_login_invalid_password_raises_authentication_exception`
- [x] `test_login_email_not_found_raises_authentication_exception`
- [x] `test_login_inactive_user_raises_authorization_exception`
- [x] `test_login_success_emits_audit_event`
- [x] `test_login_failure_emits_audit_event`
- [x] `test_refresh_valid_token_returns_new_access_token`
- [x] `test_refresh_expired_token_raises_authentication_exception`
- [x] `test_refresh_revoked_token_raises_authentication_exception`
- [x] `test_refresh_invalid_token_raises_authentication_exception`
- [x] `test_logout_revokes_refresh_token`
- [x] `test_logout_invalid_token_raises_authentication_exception`
- [x] `test_create_access_token_contains_required_claims`
- [x] `test_decode_expired_token_raises_exception`
- [x] `test_decode_invalid_signature_raises_exception`
- [x] `test_hash_password_is_not_plaintext`
- [x] `test_verify_correct_password_returns_true`
- [x] `test_verify_wrong_password_returns_false`

### Integration Tests — 10/10 ✅
- [x] `test_endpoint_login_returns_200_with_valid_credentials`
- [x] `test_endpoint_login_returns_401_with_wrong_password`
- [x] `test_endpoint_login_returns_403_for_inactive_user`
- [x] `test_login_error_message_does_not_reveal_which_field_failed`
- [x] `test_endpoint_refresh_returns_200_with_valid_token`
- [x] `test_endpoint_refresh_returns_401_with_invalid_token`
- [x] `test_endpoint_logout_returns_200_and_revokes_token`
- [x] `test_endpoint_me_returns_user_info_with_valid_token`
- [x] `test_endpoint_me_returns_401_without_token`
- [x] `test_jwt_secret_not_present_in_response_body`

## Fase 11 · Verificación
- [x] `docker compose up` sin errores — API responde en `http://localhost:8089/health`
- [x] 28/28 tests pasan (unit + integration)
- [x] Cobertura lógica de negocio (application + domain + shared/security) ≥ 95%
- [x] API verificada manualmente: login 200, 401, 403; me 200, 401; refresh 200; logout 200

## Fase 12 · Entrega
- [ ] Commit: `git commit -m "feat(auth): implement JWT authentication with login, refresh, logout and me endpoints"`
- [ ] Push: `git push origin feature/002-user-authentication`
- [ ] Continuar en el mismo branch con el ticket frontend — NO abrir PR hasta completar todas las capas
