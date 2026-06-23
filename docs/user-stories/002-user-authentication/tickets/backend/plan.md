---
ticket: docs/user-stories/002-user-authentication/tickets/backend/ticket.md
layer: backend
depends-on: docs/user-stories/002-user-authentication/tickets/database/ticket.md
progress: 0 / 57 tasks completed
---

# Plan de Desarrollo — [BE] User Authentication — FastAPI + JWT

> Marca cada tarea con `- [x]` al completarla. Actualiza `progress` en el frontmatter.

## Fase 1 · Prerequisitos
- [ ] Ticket database mergeado, migración aplicada y seed ejecutado
- [ ] `git pull origin main` y crear branch: `git checkout -b feature/user-authentication-backend`
- [ ] Leer `.amazonq/rules/backend-standards.md` y `security-standards.md`
- [ ] Agregar dependencias a `requirements.txt`: `passlib[bcrypt]`, `python-jose[cryptography]`, `slowapi`
- [ ] Verificar variables de entorno en `.env`: `JWT_SECRET`, `JWT_REFRESH_SECRET`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15`, `JWT_REFRESH_TOKEN_EXPIRE_DAYS=7`
- [ ] Actualizar `.env.example` con las nuevas variables (con comentarios, sin valores reales)

## Fase 2 · Contrato OpenAPI — Schemas Pydantic
_Archivo: `apps/backend/src/modules/auth/api/schemas.py`_
_Antes de escribir lógica — ADR-009_
- [ ] Definir `LoginRequest`: `email: EmailStr`, `password: str` con `ConfigDict(extra="forbid")`
- [ ] Definir `LoginResponse`: `access_token: str`, `refresh_token: str`, `token_type: str`, `expires_in: int`
- [ ] Definir `RefreshRequest`: `refresh_token: str`
- [ ] Definir `RefreshResponse`: `access_token: str`, `expires_in: int`
- [ ] Definir `LogoutResponse`: `message: str`
- [ ] Definir `MeResponse`: `id: UUID`, `email: str`, `role: str`, `organization_id: UUID`, `full_name: str`
- [ ] Agregar `model_config` con `json_schema_extra` (ejemplos) en todos los schemas públicos

## Fase 3 · Servicios Compartidos (shared/security/)
_Archivos: `jwt_service.py` y `password_service.py`_
- [ ] Implementar `PasswordService.hash_password(plain: str) -> str` con `passlib[bcrypt]`
- [ ] Implementar `PasswordService.verify_password(plain: str, hashed: str) -> bool`
- [ ] Implementar `JwtService.create_access_token(user_id, organization_id, role) -> str` con `python-jose`
- [ ] Implementar `JwtService.create_refresh_token(user_id) -> str`
- [ ] Implementar `JwtService.decode_token(token: str) -> dict` — lanza excepción si expirado o firma inválida
- [ ] Verificar que payload incluye obligatoriamente `sub`, `organization_id`, `role`, `exp`

## Fase 4 · Dominio
_Archivos: `domain/entities/user.py` y `domain/value_objects/refresh_token.py`_
- [ ] Implementar entidad `User` con campos `id`, `organization_id`, `email`, `hashed_password`, `role`, `status`
- [ ] Agregar método `is_active() -> bool` en `User`
- [ ] Implementar value object `RefreshToken` con `token_hash`, `user_id`, `expires_at`, `revoked_at`
- [ ] Agregar método `is_valid() -> bool` en `RefreshToken` (verifica expiración y revocación)
- [ ] Sin imports de FastAPI ni SQLAlchemy en el dominio

## Fase 5 · Repositorios — Interfaces
_Archivos: `domain/repositories/user_repository.py` y `refresh_token_repository.py`_
- [ ] Definir interfaz `UserRepository` con métodos: `get_by_email(email) -> User | None`, `get_by_id(id) -> User | None`
- [ ] Definir interfaz `RefreshTokenRepository` con métodos: `save(token)`, `get_by_hash(hash) -> RefreshToken | None`, `revoke(hash)`

## Fase 6 · Repositorios — Implementaciones SQLAlchemy
_Archivos: `infrastructure/repositories/user_repo_impl.py` y `refresh_token_repo_impl.py`_
- [ ] Implementar `UserRepositoryImpl` con `AsyncSession`, filtrar siempre `deleted_at IS NULL`
- [ ] Filtrar por `organization_id` en todas las queries de `UserRepositoryImpl`
- [ ] `SELECT` con columnas explícitas — sin `SELECT *`
- [ ] Implementar `RefreshTokenRepositoryImpl`: `save`, `get_by_hash`, `revoke` (set `revoked_at = now()`)

## Fase 7 · Casos de Uso
_Archivos: `application/commands/`_

### LoginUseCase
- [ ] Buscar usuario por email — si no existe lanzar `AuthenticationException` (mensaje genérico)
- [ ] Verificar contraseña con `PasswordService.verify_password` — si falla lanzar `AuthenticationException` (mismo mensaje genérico, no distinguir cuál campo falló)
- [ ] Verificar `user.is_active()` — si `False` lanzar `AuthorizationException` → HTTP 403
- [ ] Emitir access token + refresh token, persistir hash del refresh token
- [ ] Registrar evento `auth.login_success` con `user_id`, `organization_id`, `ip`, `timestamp`, `correlation_id`
- [ ] En caso de error registrar evento `auth.login_failed`

### RefreshTokenUseCase
- [ ] Buscar refresh token por hash — si no existe lanzar `AuthenticationException`
- [ ] Verificar `refresh_token.is_valid()` — si revocado o expirado lanzar `AuthenticationException`
- [ ] Emitir nuevo access token con mismo `organization_id` y `role`
- [ ] Registrar evento `auth.token_refreshed`

### LogoutUseCase
- [ ] Revocar refresh token del usuario (`revoked_at = now()`)
- [ ] Registrar evento `auth.logout`

## Fase 8 · Rate Limiting
- [ ] Configurar `slowapi` en `main.py`
- [ ] Aplicar límite de 5 req/min por IP en `POST /api/v1/auth/login`
- [ ] Aplicar límite de 5 req/min por IP en `POST /api/v1/auth/refresh`
- [ ] Verificar que response 429 incluye header `Retry-After`

## Fase 9 · Router y Dependencies
_Archivos: `api/router.py` y `api/dependencies.py`_
- [ ] Implementar `get_current_user` en `dependencies.py`: extrae y valida JWT del header `Authorization: Bearer`
- [ ] Implementar `require_roles(*roles)` en `dependencies.py`: verifica rol del token
- [ ] Registrar endpoint `POST /api/v1/auth/login` con `operation_id="login"`, sin auth, con rate limit
- [ ] Registrar endpoint `POST /api/v1/auth/refresh` con `operation_id="refresh_token"`, sin auth, con rate limit
- [ ] Registrar endpoint `POST /api/v1/auth/logout` con `operation_id="logout"`, `Depends(get_current_user)`
- [ ] Registrar endpoint `GET /api/v1/auth/me` con `operation_id="get_current_user_info"`, `Depends(get_current_user)`
- [ ] Toda lógica delegada a casos de uso — sin lógica de negocio en el router
- [ ] Registrar router en `apps/backend/src/main.py`

## Fase 10 · Tests
_Archivos: `modules/auth/tests/`_

### Unit Tests
- [ ] `test_login_valid_credentials_returns_tokens`
- [ ] `test_login_invalid_password_raises_authentication_exception`
- [ ] `test_login_email_not_found_raises_authentication_exception`
- [ ] `test_login_inactive_user_raises_authorization_exception`
- [ ] `test_login_empty_email_raises_validation_error`
- [ ] `test_login_empty_password_raises_validation_error`
- [ ] `test_login_success_emits_audit_event`
- [ ] `test_login_failure_emits_audit_event`
- [ ] `test_refresh_valid_token_returns_new_access_token`
- [ ] `test_refresh_expired_token_raises_authentication_exception`
- [ ] `test_refresh_revoked_token_raises_authentication_exception`
- [ ] `test_refresh_invalid_token_raises_authentication_exception`
- [ ] `test_logout_revokes_refresh_token`
- [ ] `test_logout_invalid_token_raises_authentication_exception`
- [ ] `test_create_access_token_contains_required_claims`
- [ ] `test_decode_expired_token_raises_exception`
- [ ] `test_decode_invalid_signature_raises_exception`
- [ ] `test_hash_password_is_not_plaintext`
- [ ] `test_verify_correct_password_returns_true`
- [ ] `test_verify_wrong_password_returns_false`

### Integration Tests
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

### Contract Tests
- [ ] `test_auth_openapi_schema_is_valid`
- [ ] `test_login_response_matches_contract`
- [ ] `test_refresh_response_matches_contract`
- [ ] `test_me_response_matches_contract`

### Security Tests
- [ ] `bandit` sin findings HIGH/CRITICAL en módulo `auth` y `shared/security`
- [ ] `pip-audit` sin vulnerabilidades conocidas
- [ ] `test_login_error_message_does_not_reveal_which_field_failed`
- [ ] `test_jwt_secret_not_present_in_response_body`
- [ ] `test_refresh_token_from_org_a_cannot_be_used_in_org_b_context`
- [ ] `test_user_from_org_a_cannot_authenticate_as_user_from_org_b`
- [ ] `test_correlation_id_present_in_audit_log_events`

## Fase 11 · Verificación
- [ ] `docker compose exec api python -m pytest modules/auth/tests/ -v --cov=modules/auth --cov-report=term-missing`
- [ ] Verificar cobertura ≥ 95% en módulo `auth`
- [ ] Linting: `ruff check apps/backend/src/modules/auth/ apps/backend/src/shared/security/`
- [ ] Type check: `mypy apps/backend/src/modules/auth/`
- [ ] `docker compose up` sin errores — API responde en `http://localhost:8089/health`

## Fase 12 · Entrega
- [ ] Commit: `git commit -m "feat(auth): implement JWT authentication with login, refresh, logout and me endpoints"`
- [ ] Push: `git push origin feature/user-authentication-backend`
- [ ] Abrir PR — NO hacer merge sin validación
