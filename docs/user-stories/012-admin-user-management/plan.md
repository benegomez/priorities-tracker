---
story: 012-admin-user-management
status: pending
branch: feature/012-admin-user-management
risk_level: High
complexity: M
created: 2025-01-27
---

# Plan de Implementación — US-012: Admin User Management

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Backend | Módulo `users` + 5 endpoints + generación de contraseña temporal + tests |
| 2 | Frontend | Página `/admin/users` + tabla + modales crear/editar + cambio de estado + tests |

**Branch único:** `feature/012-admin-user-management`

---

## Fase 1 — Backend

### 1.1 Estructura del módulo `users`

- [ ] Crear directorios y `__init__.py`:
  - `modules/users/api/`
  - `modules/users/application/commands/`
  - `modules/users/application/queries/`
  - `modules/users/domain/entities/`
  - `modules/users/domain/repositories/`
  - `modules/users/infrastructure/repositories/`
  - `modules/users/tests/unit/`
  - `modules/users/tests/integration/`

### 1.2 Domain — entidad y repositorio interface

- [ ] `domain/entities/user.py` — User entity con campos completos (id, org_id, manager_id, email, role, status, first_name, last_name)
- [ ] `domain/repositories/user_management_repository.py` — interface con métodos: `list_users`, `get_by_id`, `get_by_email`, `create`, `update`, `update_status`

### 1.3 Infrastructure — `user_management_repo_impl.py`

- [ ] `list_users(org_id, role?, status?, page, page_size)` — SELECT con LEFT JOIN a manager, paginado
- [ ] `get_by_id(user_id, org_id)` — SELECT con manager_name
- [ ] `email_exists(email, org_id)` — check unicidad por organización
- [ ] `manager_exists(manager_id, org_id)` — validar que manager_id pertenece a la org
- [ ] `create(...)` — INSERT + retorna fila creada
- [ ] `update(user_id, org_id, **fields)` — UPDATE con COALESCE
- [ ] `update_status(user_id, org_id, status)` — UPDATE status

### 1.4 Application — Commands

- [ ] `create_user.py` — `CreateUserUseCase`:
  - Validar email único (BR-NEW-04)
  - Validar manager_id existe en la org (si se provee)
  - Generar contraseña temporal
  - Hashear con bcrypt
  - Persistir y retornar con `temporary_password`
- [ ] `update_user.py` — `UpdateUserUseCase`:
  - Validar que el usuario existe en la org
  - Validar BR-NEW-02 (no cambiar propio rol)
  - Actualizar campos parcialmente
- [ ] `update_user_status.py` — `UpdateUserStatusUseCase`:
  - Validar BR-NEW-01 (no auto-desactivación)
  - Actualizar status

### 1.5 Application — Queries

- [ ] `get_users.py` — `GetUsersUseCase`: lista paginada con filtros
- [ ] `get_user_by_id.py` — `GetUserByIdUseCase`: detalle con manager_name, 404 si no existe en org

### 1.6 API — Schemas

- [ ] `schemas.py`:
  - `UserCreate`, `UserUpdate`, `UserStatusUpdate`
  - `UserResponse`, `UserCreatedResponse` (con `temporary_password`)
  - `UserListResponse` (paginado)
  - `UserStatusResponse`

### 1.7 API — Router

- [ ] `router.py` — 5 endpoints con `require_roles("administrator")`:
  - `GET /users` — lista paginada
  - `POST /users` — crear usuario
  - `GET /users/{id}` — detalle
  - `PATCH /users/{id}` — editar
  - `PATCH /users/{id}/status` — cambiar estado

### 1.8 Registrar router en `main.py`

- [ ] Importar y registrar `users_router` con prefix `/api/v1`

### 1.9 Tests — Unit

- [ ] `test_create_user_returns_user_with_temporary_password`
- [ ] `test_create_user_raises_409_on_duplicate_email`
- [ ] `test_create_user_raises_404_on_invalid_manager`
- [ ] `test_update_user_raises_409_on_self_role_change`
- [ ] `test_deactivate_user_raises_409_on_self_deactivation`
- [ ] `test_generate_temporary_password_meets_complexity`

### 1.10 Tests — Integration (endpoints)

- [ ] `test_get_users_returns_only_org_users`
- [ ] `test_get_users_filters_by_role`
- [ ] `test_post_user_creates_and_returns_201`
- [ ] `test_post_user_returns_409_on_duplicate_email`
- [ ] `test_patch_user_updates_fields`
- [ ] `test_patch_status_deactivates_user`
- [ ] `test_patch_status_409_on_self_deactivation`
- [ ] `test_employee_gets_403`
- [ ] `test_manager_gets_403`
- [ ] `test_cross_tenant_returns_403`

### 1.11 Verificación Backend

- [ ] Todos los tests pasan (`pytest apps/backend`)
- [ ] `GET /api/v1/users` retorna lista de la organización
- [ ] `POST /api/v1/users` crea usuario y retorna `temporary_password`
- [ ] `PATCH /api/v1/users/{id}/status` activa/desactiva
- [ ] 403 para employee y manager
- [ ] 409 en duplicado de email
- [ ] 409 en auto-desactivación

---

## Fase 2 — Frontend

### 2.1 Feature module `users`

- [ ] Crear directorios: `features/users/{services,hooks,components}`

### 2.2 Service — `user-service.ts`

- [ ] Types: `UserResponse`, `UserCreatedResponse`, `UserListResponse`, `UserCreate`, `UserUpdate`
- [ ] Funciones: `list`, `create`, `getById`, `update`, `updateStatus`

### 2.3 Hooks

- [ ] `useUsers.ts` — `useQuery` con filtros `{ role?, status?, page? }`
- [ ] `useCreateUser.ts` — `useMutation` + invalidate `['users']`
- [ ] `useUpdateUser.ts` — `useMutation` update + `useMutation` updateStatus

### 2.4 Componentes

- [ ] `UserStatusBadge.tsx` — badge verde "Activo" / rojo "Inactivo"
- [ ] `UserTable.tsx` — tabla con columnas: Nombre, Email, Rol, Estado, Manager, Acciones (Editar, Activar/Desactivar)
  - Filtros por rol y estado
  - Paginación
  - Botón "Nuevo Usuario" en header
- [ ] `UserFormModal.tsx` — modal crear/editar con Zod validation
  - Campos: email, first_name, last_name, role (select), manager_id (select managers)
  - Al crear exitosamente: mostrar modal con contraseña temporal + botón copiar

### 2.5 Página `/admin/users`

- [ ] `app/(authenticated)/admin/users/page.tsx`
  - Header + botón "Nuevo Usuario"
  - `UserTable` con datos de `useUsers`
  - `UserFormModal` para crear/editar
  - Confirmación antes de cambiar estado

### 2.6 Navegación

- [ ] `config/navigation.ts` — agregar `{ icon: Users, label: "Usuarios", href: "/admin/users" }` en sección admin

### 2.7 Tests

- [ ] `test_UserTable_renders_users_list`
- [ ] `test_UserTable_shows_empty_state`
- [ ] `test_UserFormModal_validates_required_fields`
- [ ] `test_UserFormModal_shows_temp_password_on_create`
- [ ] `test_UserStatusBadge_renders_active`
- [ ] `test_UserStatusBadge_renders_inactive`
- [ ] `test_users_page_renders_with_data`

### 2.8 Verificación Frontend

- [ ] `npx next build --no-lint` sin errores
- [ ] `npm test` — todos los tests pasan
- [ ] `/admin/users` muestra tabla paginada
- [ ] Filtros por rol y estado funcionan
- [ ] Modal crear muestra contraseña temporal al éxito
- [ ] Modal editar precarga datos del usuario
- [ ] Cambio de estado funciona con confirmación
- [ ] Errores 409/404 se muestran en el formulario
- [ ] Link "Usuarios" visible en sidebar para administradores

---

## Gate Final — PR

- [ ] Backend: todos los unit + integration tests pasan
- [ ] Frontend: todos los component tests pasan
- [ ] Build sin errores (BE + FE)
- [ ] CRUD completo funcional desde la UI
- [ ] Contraseña temporal mostrada una sola vez
- [ ] 403 para employee y manager
- [ ] Multi-tenant enforced
- [ ] PR creado con resumen, nivel de riesgo High
