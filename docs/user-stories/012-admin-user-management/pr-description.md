# PR #12 — US-012: Admin User Management

**Branch:** `feature/012-admin-user-management` → `main`

## Summary

Implements full user lifecycle management for the Administrator role. Admins can create users (with auto-generated temporary password), edit user data including password reset, assign roles and managers, and activate/deactivate users — all from the admin panel without requiring direct database access.

## Type of Change

- [x] New feature (non-breaking)
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation only

## Risk Level

**High** — Manages access and roles with direct security impact. Multi-tenant isolation and RBAC enforced at every layer.

## What Changed

### Backend — New Module `users`

| File | Purpose |
|---|---|
| `domain/entities/user_detail.py` | `UserDetail` dataclass |
| `domain/repositories/user_management_repository.py` | Abstract repository interface |
| `infrastructure/repositories/user_management_repo_impl.py` | SQLAlchemy impl — raw SQL with `text()`, `CAST(:manager_id AS uuid)` fix for nullable UUID |
| `application/commands/create_user.py` | `CreateUserUseCase` + `generate_temporary_password()` (cryptographic entropy, 12+ chars) |
| `application/commands/update_user.py` | `UpdateUserUseCase` + `UpdateUserStatusUseCase` — BR-NEW-01, BR-NEW-02 enforced |
| `application/queries/get_users.py` | `GetUsersUseCase` + `GetUserByIdUseCase` |
| `api/schemas.py` | `UserCreate`, `UserUpdate` (with `new_password`), `UserResponse`, `UserCreatedResponse`, `UserListResponse`, `UserStatusResponse` |
| `api/router.py` | 5 endpoints, all under `require_roles("administrator")` |
| `tests/unit/test_user_management.py` | 12 unit tests |
| `tests/integration/test_user_endpoints.py` | 11 integration tests |
| `main.py` | Registered `users_router` at `/api/v1` |

### Frontend — New Feature `users`

| File | Purpose |
|---|---|
| `features/users/services/user-service.ts` | Types + 5 API functions |
| `features/users/hooks/useUsers.ts` | `useUsers`, `useCreateUser`, `useUpdateUser`, `useUpdateUserStatus` |
| `features/users/components/UserTable.tsx` | Table with role/status filters, pagination, edit/toggle actions |
| `features/users/components/UserFormModal.tsx` | Create/edit modal — password field visible only in edit mode |
| `features/users/components/TempPasswordModal.tsx` | One-time temporary password display with copy button |
| `features/users/components/UserStatusBadge.tsx` | Active/inactive badge |
| `app/(authenticated)/admin/users/page.tsx` | Full CRUD page |
| `tests/user-management.test.tsx` | 13 component tests |

## Key Design Decisions

1. **Temporary password** — Generated with `secrets` module (cryptographic entropy). Shown once in `TempPasswordModal` after creation. Hashed with bcrypt before persisting — never stored in plain text.

2. **Password reset on edit** — `new_password` is optional in `PATCH /api/v1/users/{id}`. SQL uses `COALESCE(:hashed_password, hashed_password)` so omitting the field leaves the existing password untouched.

3. **Email uniqueness** — No DB-level unique constraint on `(email, organization_id)`. Validated in application layer with a pre-check query before insert.

4. **Nullable UUID fix** — `CAST(:manager_id AS uuid)` in SQLAlchemy `text()` queries prevents `AmbiguousParameterError` when `manager_id` is `None`.

5. **Token caching in integration tests** — `_TOKEN_CACHE` dict avoids repeated logins that would hit the auth rate limiter during test runs.

6. **No migrations** — `users` table already exists with all required columns including `manager_id` (self-referential FK).

## Business Rules Enforced

| BR | Description | Where |
|---|---|---|
| BR-NEW-01 | Admin cannot deactivate their own account | `UpdateUserStatusUseCase` → `409` |
| BR-NEW-02 | Admin cannot change their own role | `UpdateUserUseCase` → `409` |
| BR-NEW-03/04 | Email must be unique per organization | `CreateUserUseCase` pre-check → `409` |
| BR-016 | Multi-tenant: `organization_id` from JWT only | Repository base filter |
| BR-015 | Administrator can view entire organization | RBAC dependency |

## API Contract

```
GET    /api/v1/users                  → UserListResponse (paginated, filterable by role/status)
POST   /api/v1/users                  → UserCreatedResponse (includes temporary_password)
GET    /api/v1/users/{id}             → UserResponse
PATCH  /api/v1/users/{id}             → UserResponse (new_password optional)
PATCH  /api/v1/users/{id}/status      → UserStatusResponse
```

All endpoints: `403` for non-administrator roles, `organization_id` always from JWT.

## Testing Evidence

- **Backend unit:** 12/12 passing
- **Backend integration:** 11/11 passing
- **Frontend components:** 13 new — 79/79 total passing
- **Build:** `npx next build --no-lint` successful — 18 pages
- **Functional:** Verified via curl — create, edit, password reset, activate/deactivate, BR-NEW-01, BR-NEW-02, RBAC 403

## FR Coverage

- FR-001 — Administrators can create users ✅
- FR-002 — Administrators can update user information ✅
- FR-003 — Administrators can activate and deactivate users ✅
- FR-004 — Role assignment ✅
- FR-005 — Team assignment via manager_id ✅
- FR-006 — Manager assignment ✅
