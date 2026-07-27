---
status: pending
type: backend
story: docs/user-stories/012-admin-user-management/UserStory.md
depends-on: null
risk_level: High
complexity: M
---

# [BE] US-012 — Admin User Management API

## Objetivo

Implementar el módulo `users` con 5 endpoints REST que permiten al administrador gestionar el ciclo de vida de usuarios de su organización: listar, crear, ver detalle, editar y cambiar estado (activar/desactivar).

## Scope

Módulo nuevo `users`, 5 endpoints, 0 migraciones (tabla `users` ya existe), generación de contraseña temporal, unit tests + integration tests + security tests.

---

## FR de Referencia

- FR-001 — Create users
- FR-002 — Update user information
- FR-003 — Activate/deactivate users
- FR-004 — Role assignment
- FR-005 — Team assignment (via manager_id en MVP)
- FR-006 — Manager assignment

## Business Rules Aplicables

- **BR-015** — Administrador puede ver toda la organización
- **BR-016** — Multi-tenant: `organization_id` del JWT, nunca del body
- **BR-017** — Todos los agregados pertenecen a una organización
- **BR-NEW-01** — Admin no puede desactivarse a sí mismo
- **BR-NEW-02** — Admin no puede cambiar su propio rol
- **BR-NEW-03** — Email único por organización (validar en app layer)
- **BR-NEW-04** — No crear usuario con email duplicado en la misma organización

---

## Contrato API

### GET /api/v1/users
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Query params | `page=1`, `page_size=20`, `role?`, `status?` |
| Response 200 | `UserListResponse` (paginado) |
| Response 403 | Insufficient permissions |

### POST /api/v1/users
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Request body | `UserCreate` |
| Response 201 | `UserCreatedResponse` (incluye `temporary_password`) |
| Response 409 | Email ya existe en la organización |
| Response 404 | `manager_id` no existe |

### GET /api/v1/users/{id}
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Response 200 | `UserResponse` |
| Response 404 | Usuario no existe en la organización |

### PATCH /api/v1/users/{id}
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Request body | `UserUpdate` (todos opcionales) |
| Response 200 | `UserResponse` |
| Response 409 | Intento de cambiar propio rol |
| Response 404 | Usuario no existe |

### PATCH /api/v1/users/{id}/status
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Request body | `UserStatusUpdate` |
| Response 200 | `UserStatusResponse` |
| Response 409 | Intento de desactivarse a sí mismo |
| Response 404 | Usuario no existe |

---

## Schemas Pydantic

```python
class UserCreate(BaseModel):
    email: EmailStr
    first_name: str  # max 100
    last_name: str   # max 100
    role: str        # administrator | manager | employee
    manager_id: UUID | None = None

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None
    manager_id: UUID | None = None

class UserStatusUpdate(BaseModel):
    status: str  # active | inactive

class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    role: str
    status: str
    manager_id: UUID | None
    manager_name: str | None
    created_at: datetime
    updated_at: datetime

class UserCreatedResponse(UserResponse):
    temporary_password: str  # mostrada una sola vez

class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    pages: int

class UserStatusResponse(BaseModel):
    id: UUID
    status: str
```

---

## Archivos a Crear

```
apps/backend/src/modules/users/
  __init__.py
  api/
    __init__.py
    router.py              - 5 endpoints
    schemas.py             - schemas Pydantic
    dependencies.py        - require_administrator helper
  application/
    __init__.py
    commands/
      __init__.py
      create_user.py       - CreateUserCommand + UseCase
      update_user.py       - UpdateUserCommand + UseCase
      update_user_status.py
    queries/
      __init__.py
      get_users.py         - GetUsersQuery + UseCase
      get_user_by_id.py
  domain/
    __init__.py
    entities/
      __init__.py
      user.py              - User entity (extender o reusar de auth)
    repositories/
      __init__.py
      user_management_repository.py  - interface
  infrastructure/
    __init__.py
    repositories/
      __init__.py
      user_management_repo_impl.py   - SQLAlchemy impl
  tests/
    __init__.py
    unit/
      __init__.py
      test_create_user.py
      test_update_user.py
      test_user_status.py
    integration/
      __init__.py
      test_user_endpoints.py

apps/backend/src/main.py   - MODIFY (registrar users_router)
```

---

## Implementación

### Generación de contraseña temporal

```python
import secrets
import string

def generate_temporary_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$"
    # Garantizar al menos 1 mayúscula, 1 número, 1 especial
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$"),
        *[secrets.choice(alphabet) for _ in range(length - 3)],
    ]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)
```

### Validación de email único por organización

```python
async def check_email_unique(email: str, organization_id: UUID, session) -> bool:
    result = await session.execute(
        text("SELECT 1 FROM users WHERE email = :email AND organization_id = :org_id AND deleted_at IS NULL"),
        {"email": email, "org_id": organization_id}
    )
    return result.one_or_none() is None
```

### Queries principales (UserManagementRepoImpl)

```python
# GET list con paginación y filtros
SELECT u.id, u.email, u.first_name, u.last_name, u.role, u.status,
       u.manager_id, u.created_at, u.updated_at,
       m.first_name || ' ' || m.last_name AS manager_name
FROM users u
LEFT JOIN users m ON u.manager_id = m.id
WHERE u.organization_id = :org_id
  AND u.deleted_at IS NULL
  [AND u.role = :role]
  [AND u.status = :status]
ORDER BY u.first_name, u.last_name
LIMIT :limit OFFSET :offset

# PATCH update
UPDATE users
SET first_name = COALESCE(:first_name, first_name),
    last_name  = COALESCE(:last_name, last_name),
    role       = COALESCE(:role, role),
    manager_id = COALESCE(:manager_id, manager_id),
    updated_at = now()
WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL

# PATCH status
UPDATE users
SET status = :status, updated_at = now()
WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL
```

---

## Tests Requeridos

### Unit Tests

- [ ] `test_create_user_returns_user_with_temporary_password`
- [ ] `test_create_user_raises_409_on_duplicate_email`
- [ ] `test_create_user_raises_404_on_invalid_manager`
- [ ] `test_update_user_raises_409_on_self_role_change`
- [ ] `test_deactivate_user_raises_409_on_self_deactivation`
- [ ] `test_generate_temporary_password_meets_complexity`

### Integration Tests (endpoints)

- [ ] `test_get_users_returns_only_org_users` — multi-tenant
- [ ] `test_get_users_filters_by_role`
- [ ] `test_get_users_filters_by_status`
- [ ] `test_post_user_creates_and_returns_201`
- [ ] `test_post_user_returns_409_on_duplicate_email`
- [ ] `test_patch_user_updates_fields`
- [ ] `test_patch_status_deactivates_user`
- [ ] `test_patch_status_409_on_self_deactivation`
- [ ] `test_employee_gets_403_on_all_endpoints`
- [ ] `test_manager_gets_403_on_all_endpoints`
- [ ] `test_cross_tenant_returns_403`

---

## Criterios de Aceptación

- [ ] `GET /api/v1/users` retorna lista paginada de la organización
- [ ] `POST /api/v1/users` crea usuario con contraseña temporal
- [ ] `GET /api/v1/users/{id}` retorna detalle con manager_name
- [ ] `PATCH /api/v1/users/{id}` actualiza campos parcialmente
- [ ] `PATCH /api/v1/users/{id}/status` activa/desactiva
- [ ] 409 al crear con email duplicado en la misma org
- [ ] 409 al intentar desactivarse a sí mismo
- [ ] 409 al intentar cambiar propio rol
- [ ] 403 para roles employee y manager
- [ ] Multi-tenant enforced (BR-016)
- [ ] `organization_id` nunca aceptado del body
- [ ] Tests pasan
- [ ] Router registrado en `main.py`

---

## Git Branch

`feature/012-admin-user-management`
