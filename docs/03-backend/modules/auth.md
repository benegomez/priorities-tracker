# Auth Module

## Objetivo
Gestionar autenticación JWT y proveer los mecanismos de identidad para toda la plataforma.

## Bounded Context
Organization → `auth`

## Status
✅ Implementado (US-002)

---

## Responsabilidades
- Login con email + password (bcrypt)
- Emisión de Access Token (JWT, 15 min) + Refresh Token (7 días)
- Refresh de access token sin re-login
- Logout con revocación de refresh token
- Proveer `get_current_user` dependency para todos los módulos
- Proveer `require_roles` dependency para RBAC
- Eventos de auditoría en cada acción de auth

---

## Estructura de Archivos

```
src/modules/auth/
├── api/
│   ├── router.py          — 4 endpoints: login, refresh, logout, me
│   ├── schemas.py         — LoginRequest, LoginResponse, RefreshRequest, etc.
│   └── dependencies.py    — get_current_user, require_roles
├── application/
│   └── commands/
│       ├── login_command.py          — LoginUseCase
│       ├── refresh_token_command.py  — RefreshTokenUseCase
│       └── logout_command.py         — LogoutUseCase
├── domain/
│   ├── entities/
│   │   └── user.py                   — User entity (is_active, full_name)
│   ├── value_objects/
│   │   └── refresh_token.py          — RefreshToken (is_valid)
│   └── repositories/
│       ├── user_repository.py        — interfaz
│       └── refresh_token_repository.py — interfaz
├── infrastructure/
│   └── repositories/
│       ├── user_repo_impl.py         — SQLAlchemy async
│       └── refresh_token_repo_impl.py
└── tests/
    ├── unit/
    │   ├── test_security_services.py
    │   ├── test_use_cases.py
    │   └── test_correlation_id.py
    └── integration/
        ├── test_auth_endpoints.py
        └── test_auth_security.py
```

---

## Casos de Uso

| Use Case | Descripción |
|---|---|
| `LoginUseCase` | Valida credenciales, verifica status activo, emite tokens, registra auditoría |
| `RefreshTokenUseCase` | Valida refresh token, emite nuevo access token |
| `LogoutUseCase` | Revoca refresh token |

---

## Entidades

### User
```
id, organization_id, email, hashed_password, role, status, first_name, last_name
```
- `is_active()` → True si `status == "active"`
- `full_name` → property que concatena first + last name

### RefreshToken (value object)
```
id, user_id, token_hash, expires_at, revoked_at
```
- `is_valid()` → True si no está revocado y no expiró

---

## Dependencias

- **Consume:** tabla `users`, tabla `organizations`, tabla `refresh_tokens`
- **Provee a otros módulos:** `get_current_user`, `require_roles` (en `dependencies.py`)
- **Shared:** `jwt_service.py`, `password_service.py`, `audit_logger.py`

---

## Tests

| Tipo | Cantidad | Status |
|---|---|---|
| Unit | 20 | ✅ passed |
| Integration | 13 | ✅ passed |
| bandit (SAST) | — | ✅ 0 High/Critical |
| pip-audit | — | ✅ 0 vulnerabilidades |

---

## NFRs Implementados

- **NFR-001:** Todo endpoint protegido valida JWT via `get_current_user`
- **NFR-002:** RBAC via `require_roles` en `dependencies.py`
- **NFR-003:** Passwords con bcrypt, tokens por HTTPS
- **NFR-009:** Audit events con correlation_id
- **NFR-012:** Logs estructurados con correlation_id
