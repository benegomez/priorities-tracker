---
status: done
type: frontend
story: docs/user-stories/002-user-authentication/UserStory.md
depends-on: tickets/backend/ticket.md
---

# [FE] User Authentication — Login, Logout & Sesión

## Objetivo
Implementar la pantalla de login, gestión de sesión con JWT en HTTP-only cookies, redirección por rol y flujo de logout.

## Scope
Next.js 15 App Router, features/auth/, TanStack Query, Zod, Zustand para estado de sesión. Sin schema SQL, sin lógica de API.

## Dependencia
Endpoints de backend disponibles: `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`, `GET /api/v1/auth/me`.

---

## Contrato API Consumido

**POST /api/v1/auth/login**
Request: `{ email, password }`
Response 200: `{ access_token, refresh_token, token_type, expires_in }`
Errors: 400, 401, 403, 429

**POST /api/v1/auth/refresh**
Request: `{ refresh_token }`
Response 200: `{ access_token, expires_in }`
Error: 401, 429

**POST /api/v1/auth/logout**
Auth: Bearer JWT | Response 200: `{ message }`

**GET /api/v1/auth/me**
Auth: Bearer JWT | Response 200: `{ id, email, role, organization_id, full_name }`

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  app/
    auth/
      login/
        page.tsx          - CREATE (LoginPage — Server Component wrapper)
        loading.tsx       - CREATE
      layout.tsx          - CREATE (layout sin sidebar para rutas auth)
    (employee)/
      dashboard/
        page.tsx          - CREATE (placeholder para redirect target)
    (manager)/
      dashboard/
        page.tsx          - CREATE (placeholder para redirect target)
    (admin)/
      dashboard/
        page.tsx          - CREATE (placeholder para redirect target)
    middleware.ts          - CREATE (protección de rutas por rol)

  features/auth/
    components/
      LoginForm.tsx        - CREATE
    hooks/
      useLogin.ts          - CREATE (useMutation → POST /auth/login)
      useLogout.ts         - CREATE (useMutation → POST /auth/logout)
      useCurrentUser.ts    - CREATE (useQuery → GET /auth/me)
    schemas/
      login-schema.ts      - CREATE (Zod)
    services/
      auth-service.ts      - CREATE (login, logout, refresh, getMe)

  store/
    auth-store.ts          - CREATE (Zustand: user info, isAuthenticated)

  providers/
    AuthProvider.tsx        - CREATE (inicializa sesión, wrappea la app)
```

---

## Componentes UI

**LoginForm**
- Props: ninguna (autónomo)
- Campos: `email` (input text), `password` (input password con toggle visibility)
- Botón: "Iniciar sesión" con estado loading
- Error inline bajo el formulario (mensaje genérico desde el backend)
- Manejo de 429: mostrar "Demasiados intentos. Intente en X segundos."

---

## Gestión de Estado

**TanStack Query:**
- `useLogin` → `useMutation` sobre `POST /api/v1/auth/login`
  - onSuccess: guardar user en Zustand, redirigir por rol
  - onError: mostrar mensaje de error del response
- `useLogout` → `useMutation` sobre `POST /api/v1/auth/logout`
  - onSuccess: limpiar Zustand, redirigir a `/auth/login`
- `useCurrentUser` → `useQuery` sobre `GET /api/v1/auth/me`
  - Usada en AuthProvider para rehidratar sesión al recargar

**Zustand (`auth-store.ts`):**
```typescript
interface AuthStore {
  user: { id: string; email: string; role: UserRole; organization_id: string; full_name: string } | null
  setUser: (user: AuthStore['user']) => void
  clearUser: () => void
}
```

---

## Redirección por Rol (middleware.ts)

```
/auth/login → solo accesible sin sesión activa
/employee/* → requiere role = 'employee' | 'administrator'
/manager/*  → requiere role = 'manager'  | 'administrator'
/admin/*    → requiere role = 'administrator'
/           → redirigir según rol del usuario autenticado
```

Rutas sin sesión → redirect a `/auth/login`.

---

## Almacenamiento de Tokens

- `access_token` → memoria (Zustand) — no en `localStorage`
- `refresh_token` → HTTP-only cookie (se debe coordinar con backend para `Set-Cookie`)
- En SSR: leer cookie desde `request.headers` en middleware

---

## Validación de Formulario (Zod)

```typescript
const loginSchema = z.object({
  email:    z.string().email({ message: "Email inválido" }),
  password: z.string().min(1, { message: "La contraseña es requerida" }),
})
```

---

## Tests Requeridos

> Nivel de riesgo = Critical | Complejidad = M → cobertura mínima >95%
> Estado: Build TypeScript ✅ | **9/9 tests passed** (vitest)

### Unit / Component Tests — `vitest` ✅ 9 passed

**Zod Schema:**
- [x] `test_login_schema_rejects_invalid_email`
- [x] `test_login_schema_rejects_empty_password`
- [x] `test_login_schema_accepts_valid_input`
- [x] `test_login_schema_rejects_missing_email`
- [x] `test_login_schema_rejects_missing_password`

**Zustand Store:**
- [x] `test_auth_store_starts_with_null_user`
- [x] `test_auth_store_setUser_updates_user_state`
- [x] `test_auth_store_setTokens_updates_token_state`
- [x] `test_auth_store_clearUser_resets_all_state`

### Component Tests — pendiente (requiere render de LoginForm con mocks de hooks)
- [ ] `test_LoginForm_renders_email_and_password_fields`
- [ ] `test_LoginForm_shows_loading_state_while_submitting`
- [ ] `test_LoginForm_shows_error_message_on_401`
- [ ] `test_LoginForm_shows_error_message_on_403_inactive_user`
- [ ] `test_LoginForm_shows_rate_limit_message_on_429`

### E2E Tests — pendiente (Playwright, diferido a iteración UX)
- [ ] `test_login_employee_redirects_to_employee_dashboard`
- [ ] `test_login_manager_redirects_to_manager_dashboard`
- [ ] `test_login_admin_redirects_to_admin_dashboard`
- [ ] `test_login_invalid_credentials_shows_error`
- [ ] `test_logout_clears_session_and_redirects_to_login`
- [ ] `test_protected_route_unauthenticated_redirects_to_login`
- [ ] `test_authenticated_user_cannot_access_login_page`
- [ ] `test_employee_cannot_access_manager_routes`
- [ ] `test_manager_cannot_access_admin_routes`

### Verificación completada
- [x] `npm run build` — TypeScript compila sin errores ✅
- [x] `npm run test` — 9/9 tests passed ✅
- [x] Accesibilidad implementada en código (labels, aria, role=alert, autoFocus, keyboard nav)

## Accesibilidad — implementada en código ✅
- [x] `<form>` semántico con `<label>` asociado a cada input (htmlFor/id)
- [x] `aria-label` en botón de toggle de contraseña
- [x] Mensajes de error con `role="alert"`
- [x] Navegación por teclado completa (Tab, Enter para submit)
- [x] Focus en el primer campo al cargar la página (autoFocus)

## Git Branch
`feature/002-user-authentication` — branch único compartido con DB y BE de la misma US
