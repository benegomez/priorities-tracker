---
ticket: docs/user-stories/002-user-authentication/tickets/frontend/ticket.md
layer: frontend
depends-on: docs/user-stories/002-user-authentication/tickets/backend/ticket.md
progress: 0 / 52 tasks completed
---

# Plan de Desarrollo — [FE] User Authentication — Login, Logout & Sesión

> Marca cada tarea con `- [x]` al completarla. Actualiza `progress` en el frontmatter.

## Fase 1 · Prerequisitos
- [ ] Endpoints backend disponibles y respondiendo: `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`, `GET /api/v1/auth/me`
- [ ] `git pull origin main` y crear branch: `git checkout -b feature/user-authentication-frontend`
- [ ] Leer `.amazonq/rules/frontend-standards.md`
- [ ] Verificar que `NEXT_PUBLIC_API_URL=http://localhost:8089` está en `.env.local`

## Fase 2 · Schema de Validación (Zod)
_Archivo: `apps/frontend/src/features/auth/schemas/login-schema.ts`_
- [ ] Definir `loginSchema` con `email: z.string().email()` y `password: z.string().min(1)`
- [ ] Mensajes de error en español: "Email inválido", "La contraseña es requerida"
- [ ] Exportar tipo `LoginFormValues = z.infer<typeof loginSchema>`

## Fase 3 · Servicio API
_Archivo: `apps/frontend/src/features/auth/services/auth-service.ts`_
- [ ] Implementar función `login(data: LoginFormValues): Promise<LoginResponse>` — consume `POST /api/v1/auth/login`
- [ ] Implementar función `logout(): Promise<void>` — consume `POST /api/v1/auth/logout`
- [ ] Implementar función `refreshToken(token: string): Promise<RefreshResponse>` — consume `POST /api/v1/auth/refresh`
- [ ] Implementar función `getMe(): Promise<MeResponse>` — consume `GET /api/v1/auth/me`
- [ ] Definir interfaces TypeScript: `LoginResponse`, `RefreshResponse`, `MeResponse`
- [ ] Manejo de errores tipado por status code (401, 403, 429) — sin `any`
- [ ] URL base desde `process.env.NEXT_PUBLIC_API_URL` — nunca hardcoded

## Fase 4 · Zustand Store
_Archivo: `apps/frontend/src/store/auth-store.ts`_
- [ ] Definir interface `AuthStore` con `user`, `setUser`, `clearUser`
- [ ] Implementar store con `create<AuthStore>()`
- [ ] `user` contiene `id`, `email`, `role`, `organization_id`, `full_name` — o `null` si no autenticado
- [ ] Exportar tipo `UserRole = 'administrator' | 'manager' | 'employee'`

## Fase 5 · Hooks TanStack Query
_Archivos: `apps/frontend/src/features/auth/hooks/`_

### useLogin.ts
- [ ] `useMutation` sobre `authService.login`
- [ ] `onSuccess`: llamar `setUser` en Zustand + redirigir según `role` (`/employee/dashboard`, `/manager/dashboard`, `/admin/dashboard`)
- [ ] `onError`: extraer mensaje del response (genérico para 401, específico para 403 y 429)

### useLogout.ts
- [ ] `useMutation` sobre `authService.logout`
- [ ] `onSuccess`: llamar `clearUser` en Zustand + redirigir a `/auth/login`
- [ ] `onSettled`: siempre limpiar store (incluso si el request falla)

### useCurrentUser.ts
- [ ] `useQuery` con `queryKey: ['auth', 'me']`
- [ ] `enabled: true` solo si hay indicación de sesión activa (cookie presente)
- [ ] Usar para rehidratar sesión al recargar la página

## Fase 6 · AuthProvider
_Archivo: `apps/frontend/src/providers/AuthProvider.tsx`_
- [ ] Componente client que wrappea la app
- [ ] Al montar: llama `useCurrentUser` para rehidratar sesión desde cookie
- [ ] Si `getMe` retorna 401: llamar `clearUser` en Zustand
- [ ] Renderizar `children` siempre (no bloquear render por auth)

## Fase 7 · Componente LoginForm
_Archivo: `apps/frontend/src/features/auth/components/LoginForm.tsx`_
- [ ] Campos `email` e `input[type="password"]` con toggle de visibilidad
- [ ] Validación con `loginSchema` (Zod) mediante `react-hook-form`
- [ ] Botón "Iniciar sesión" con estado loading mientras `useLogin.isPending`
- [ ] Error 401: mostrar "Credenciales inválidas"
- [ ] Error 403: mostrar "Usuario inactivo. Contacta a tu administrador"
- [ ] Error 429: mostrar "Demasiados intentos. Intenta en X segundos" (leer `Retry-After` del header)
- [ ] `<form>` semántico con `<label>` asociado a cada `<input>`
- [ ] `aria-label` en botón de toggle de contraseña
- [ ] Mensajes de error con `role="alert"`
- [ ] `autoFocus` en campo email al cargar

## Fase 8 · Páginas y Layout
_Archivos: `apps/frontend/src/app/`_
- [ ] Crear `app/auth/layout.tsx` — layout sin sidebar para rutas de auth
- [ ] Crear `app/auth/login/page.tsx` — Server Component que renderiza `<LoginForm />`
- [ ] Crear `app/auth/login/loading.tsx` — skeleton de la pantalla de login
- [ ] Crear `app/(employee)/dashboard/page.tsx` — placeholder con "Dashboard Empleado"
- [ ] Crear `app/(manager)/dashboard/page.tsx` — placeholder con "Dashboard Manager"
- [ ] Crear `app/(admin)/dashboard/page.tsx` — placeholder con "Dashboard Administrador"

## Fase 9 · Middleware (Protección de Rutas)
_Archivo: `apps/frontend/src/middleware.ts`_
- [ ] Leer cookie de sesión en cada request
- [ ] `/auth/login` → redirigir a dashboard si ya autenticado
- [ ] `/employee/*` → requiere `role = 'employee' | 'administrator'`, sino 403 o redirect a login
- [ ] `/manager/*` → requiere `role = 'manager' | 'administrator'`
- [ ] `/admin/*` → requiere `role = 'administrator'`
- [ ] Cualquier ruta protegida sin sesión → redirect a `/auth/login`
- [ ] Configurar `matcher` en `middleware.ts` para excluir assets estáticos

## Fase 10 · Tests
_Archivos: `apps/frontend/src/tests/`_

### Unit / Component Tests (vitest + Testing Library)
- [ ] `test_LoginForm_renders_email_and_password_fields`
- [ ] `test_LoginForm_shows_loading_state_while_submitting`
- [ ] `test_LoginForm_shows_error_message_on_401`
- [ ] `test_LoginForm_shows_error_message_on_403_inactive_user`
- [ ] `test_LoginForm_shows_rate_limit_message_on_429`
- [ ] `test_login_schema_rejects_invalid_email`
- [ ] `test_login_schema_rejects_empty_password`
- [ ] `test_login_schema_accepts_valid_input`
- [ ] `test_useLogin_on_success_updates_auth_store`
- [ ] `test_useLogout_on_success_clears_auth_store`
- [ ] `test_AuthProvider_restores_session_from_cookie_on_mount`

### E2E Tests (Playwright)
- [ ] `test_login_employee_redirects_to_employee_dashboard`
- [ ] `test_login_manager_redirects_to_manager_dashboard`
- [ ] `test_login_admin_redirects_to_admin_dashboard`
- [ ] `test_login_invalid_credentials_shows_error`
- [ ] `test_logout_clears_session_and_redirects_to_login`
- [ ] `test_protected_route_unauthenticated_redirects_to_login`
- [ ] `test_authenticated_user_cannot_access_login_page`
- [ ] `test_employee_cannot_access_manager_routes`
- [ ] `test_manager_cannot_access_admin_routes`

## Fase 11 · Accesibilidad
- [ ] `<form>` semántico con `<label>` asociado a cada input (for/id)
- [ ] `aria-label` en botón de toggle de contraseña
- [ ] Mensajes de error con `role="alert"`
- [ ] Navegación por teclado completa (Tab entre campos, Enter para submit)
- [ ] Focus en el campo email al cargar la página (`autoFocus`)

## Fase 12 · Verificación
- [ ] `npm run build` en `apps/frontend/` — sin errores TypeScript
- [ ] `npm run lint` — sin errores ESLint
- [ ] Verificar en navegador: estado loading, error 401, error 403, error 429 y estado success
- [ ] Verificar redirección por rol: employee → `/employee/dashboard`, manager → `/manager/dashboard`, admin → `/admin/dashboard`
- [ ] Verificar que ruta protegida sin sesión redirige a `/auth/login`
- [ ] Verificar rehidratación de sesión al recargar la página

## Fase 13 · Entrega
- [ ] Commit: `git commit -m "feat(auth): implement login form, session management and role-based routing"`
- [ ] Push: `git push origin feature/user-authentication-frontend`
- [ ] Abrir PR — NO hacer merge sin validación
