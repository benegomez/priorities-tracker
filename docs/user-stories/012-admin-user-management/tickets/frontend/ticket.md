---
status: pending
type: frontend
story: docs/user-stories/012-admin-user-management/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: High
complexity: M
---

# [FE] US-012 — Admin User Management UI

## Objetivo

Implementar el panel de gestión de usuarios en `/admin/users` para que el administrador pueda listar, crear, editar y activar/desactivar usuarios de su organización desde la interfaz.

## Scope

1 página de lista con tabla, 1 modal de creación, 1 modal de edición, 1 confirmación de cambio de estado, 1 service, 3 hooks TanStack Query. Sin nueva infraestructura.

## Dependencia

Endpoints backend `GET/POST/PATCH /api/v1/users` disponibles (ticket BE).

---

## Contrato API Consumido

| Método | Endpoint | Propósito |
|---|---|---|
| GET | `/api/v1/users` | Lista paginada con filtros |
| POST | `/api/v1/users` | Crear usuario |
| GET | `/api/v1/users/{id}` | Detalle (para edición) |
| PATCH | `/api/v1/users/{id}` | Editar datos |
| PATCH | `/api/v1/users/{id}/status` | Activar/desactivar |

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  features/users/
    services/
      user-service.ts              - CREATE (API client)
    hooks/
      useUsers.ts                  - CREATE (useQuery lista)
      useCreateUser.ts             - CREATE (useMutation)
      useUpdateUser.ts             - CREATE (useMutation update + status)
    components/
      UserTable.tsx                - CREATE (tabla con acciones)
      UserFormModal.tsx            - CREATE (crear/editar)
      UserStatusBadge.tsx          - CREATE (badge active/inactive)

  app/(authenticated)/admin/users/
    page.tsx                       - CREATE

  config/navigation.ts             - MODIFY (agregar "Usuarios" en admin)
```

---

## Implementación

### `user-service.ts`

```typescript
export interface UserResponse {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'administrator' | 'manager' | 'employee';
  status: 'active' | 'inactive';
  manager_id: string | null;
  manager_name: string | null;
  created_at: string;
  updated_at: string;
}

export interface UserCreatedResponse extends UserResponse {
  temporary_password: string;
}

export interface UserListResponse {
  items: UserResponse[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface UserCreate {
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  manager_id?: string;
}

export interface UserUpdate {
  first_name?: string;
  last_name?: string;
  role?: string;
  manager_id?: string;
}

export const userService = {
  list: (params?: { page?: number; role?: string; status?: string }) =>
    apiGet<UserListResponse>('/api/v1/users', params),
  create: (data: UserCreate) =>
    apiPost<UserCreatedResponse>('/api/v1/users', data),
  getById: (id: string) =>
    apiGet<UserResponse>(`/api/v1/users/${id}`),
  update: (id: string, data: UserUpdate) =>
    apiPatch<UserResponse>(`/api/v1/users/${id}`, data),
  updateStatus: (id: string, status: 'active' | 'inactive') =>
    apiPatch<{ id: string; status: string }>(`/api/v1/users/${id}/status`, { status }),
};
```

### `useUsers.ts`

```typescript
export function useUsers(filters?: { role?: string; status?: string; page?: number }) {
  return useQuery({
    queryKey: ['users', filters],
    queryFn: () => userService.list(filters),
  });
}
```

### `useCreateUser.ts`

```typescript
export function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UserCreate) => userService.create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
}
```

### `useUpdateUser.ts`

```typescript
export function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UserUpdate }) =>
      userService.update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
}

export function useUpdateUserStatus() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: 'active' | 'inactive' }) =>
      userService.updateStatus(id, status),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
}
```

### `UserTable.tsx`

Columnas: Nombre, Email, Rol, Estado (badge), Manager, Acciones (Editar, Activar/Desactivar)

```
| Nombre       | Email              | Rol       | Estado  | Manager    | Acciones      |
|---|---|---|---|---|---|
| Juan Pérez   | juan@empresa.com   | employee  | ● Activo | Ana García | ✏️ 🔴         |
| Ana García   | ana@empresa.com    | manager   | ● Activo | —          | ✏️ 🔴         |
| Luis Mora    | luis@empresa.com   | employee  | ○ Inact. | Ana García | ✏️ 🟢         |
```

- Filtros: por rol (select) y estado (select)
- Botón "Nuevo Usuario" en header
- Paginación

### `UserFormModal.tsx`

Campos:
- Email (requerido, tipo email)
- Nombre (requerido)
- Apellido (requerido)
- Rol (select: administrator | manager | employee)
- Manager (select de usuarios con rol manager, opcional)

Validación con Zod:
```typescript
const userSchema = z.object({
  email: z.string().email('Email inválido'),
  first_name: z.string().min(1, 'Requerido').max(100),
  last_name: z.string().min(1, 'Requerido').max(100),
  role: z.enum(['administrator', 'manager', 'employee']),
  manager_id: z.string().uuid().optional(),
});
```

Al crear exitosamente → mostrar modal con contraseña temporal (una sola vez):
```
✅ Usuario creado exitosamente
Contraseña temporal: Abc123!xyz
⚠️ Guarda esta contraseña — no se mostrará nuevamente.
```

### `page.tsx` — flujo

```
/admin/users
  ├── Header: "Gestión de Usuarios" + botón "Nuevo Usuario"
  ├── Filtros: Rol | Estado
  ├── UserTable (lista paginada)
  │     ├── Acción "Editar" → abre UserFormModal en modo edición
  │     └── Acción "Desactivar/Activar" → confirmación → PATCH status
  └── UserFormModal (crear/editar)
        ├── Crear → POST → mostrar contraseña temporal → cerrar
        └── Editar → PATCH → cerrar
```

---

## Navegación

Agregar en `config/navigation.ts` para el rol `admin`:
```typescript
{ icon: Users, label: "Usuarios", href: "/admin/users" }
```

---

## Edge Cases

| Caso | Comportamiento |
|---|---|
| Lista vacía | Mensaje "No hay usuarios registrados" + botón crear |
| Email duplicado (409) | Error inline en el campo email del form |
| Desactivar propio usuario (409) | Toast de error "No puedes desactivarte a ti mismo" |
| Cambiar propio rol (409) | Toast de error "No puedes cambiar tu propio rol" |
| Contraseña temporal | Modal de confirmación con copy button, se muestra una sola vez |
| Manager_id inválido (404) | Error en el campo manager del form |

---

## Tests Requeridos

- [ ] `test_UserTable_renders_users_list`
- [ ] `test_UserTable_shows_empty_state`
- [ ] `test_UserFormModal_validates_required_fields`
- [ ] `test_UserFormModal_shows_temp_password_on_create`
- [ ] `test_UserStatusBadge_renders_active`
- [ ] `test_UserStatusBadge_renders_inactive`
- [ ] `test_users_page_renders_with_data`

---

## Criterios de Aceptación

- [ ] `/admin/users` muestra tabla paginada de usuarios
- [ ] Filtros por rol y estado funcionan
- [ ] "Nuevo Usuario" abre modal con formulario validado
- [ ] Al crear: muestra contraseña temporal en modal de confirmación
- [ ] "Editar" abre modal con datos precargados
- [ ] "Desactivar/Activar" cambia estado con confirmación
- [ ] Errores de API (409, 404) se muestran en el formulario
- [ ] Link "Usuarios" en sidebar para administradores
- [ ] `npm run build` sin errores
- [ ] Tests pasan

---

## Git Branch

`feature/012-admin-user-management`
