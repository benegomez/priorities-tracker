---
ticket: docs/user-stories/002-user-authentication/tickets/frontend/ticket.md
layer: frontend
depends-on: docs/user-stories/002-user-authentication/tickets/backend/ticket.md
progress: 44 / 52 tasks completed
---

# Plan de Desarrollo — [FE] User Authentication — Login, Logout & Sesión

> Marca cada tarea con `- [x]` al completarla. Actualiza `progress` en el frontmatter.

## Fase 1 · Prerequisitos
- [x] Endpoints backend disponibles y respondiendo: `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`, `GET /api/v1/auth/me`
- [x] Continuar en branch existente: `git checkout feature/002-user-authentication`
- [x] Leer `.amazonq/rules/frontend-standards.md`
- [x] Verificar que `NEXT_PUBLIC_API_URL=http://localhost:8089` está en `.env.local`

## Fase 2 · Schema de Validación (Zod)
_Archivo: `apps/frontend/src/features/auth/schemas/login-schema.ts`_
- [x] Definir `loginSchema` con `email: z.string().email()` y `password: z.string().min(1)`
- [x] Mensajes de error en español: "Email inválido", "La contraseña es requerida"
- [x] Exportar tipo `LoginFormValues = z.infer<typeof loginSchema>`

## Fase 3 · Servicio API
_Archivo: `apps/frontend/src/features/auth/services/auth-service.ts`_
- [x] Implementar función `login(data: LoginFormValues): Promise<LoginResponse>`
- [x] Implementar función `logout(): Promise<void>`
- [x] Implementar función `refreshToken(token: string): Promise<RefreshResponse>`
- [x] Implementar función `getMe(): Promise<MeResponse>`
- [x] Definir interfaces TypeScript: `LoginResponse`, `RefreshResponse`, `MeResponse`
- [x] Manejo de errores tipado por status code (401, 403, 429) — sin `any`
- [x] URL base desde `process.env.NEXT_PUBLIC_API_URL` — nunca hardcoded

## Fase 4 · Zustand Store
_Archivo: `apps/frontend/src/store/auth-store.ts`_
- [x] Definir interface `AuthStore` con `user`, `setUser`, `clearUser`
- [x] Implementar store con `create<AuthStore>()`
- [x] `user` contiene `id`, `email`, `role`, `organization_id`, `full_name` — o `null` si no autenticado
- [x] Exportar tipo `UserRole = 'administrator' | 'manager' | 'employee'`

## Fase 5 · Hooks TanStack Query
_Archivos: `apps/frontend/src/features/auth/hooks/`_

### useLogin.ts
- [x] `useMutation` sobre `authService.login`
- [x] `onSuccess`: llamar `setUser` en Zustand + redirigir según `role`
- [x] `onError`: extraer mensaje del response (genérico para 401, específico para 403 y 429)

### useLogout.ts
- [x] `useMutation` sobre `authService.logout`
- [x] `onSuccess`: llamar `clearUser` en Zustand + redirigir a `/auth/login`
- [x] `onSettled`: siempre limpiar store (incluso si el request falla)

### useCurrentUser.ts
- [x] `useQuery` con `queryKey: ['auth', 'me']`
- [x] `enabled: true` solo si hay indicación de sesión activa (token presente)
- [x] Usar para rehidratar sesión al recargar la página

## Fase 6 · AuthProvider
_Archivo: `apps/frontend/src/providers/AuthProvider.tsx`_
- [x] Componente client que wrappea la app con QueryClientProvider
- [x] Renderizar `children` siempre (no bloquear render por auth)

## Fase 7 · Componente LoginForm
_Archivo: `apps/frontend/src/features/auth/components/LoginForm.tsx`_
- [x] Campos `email` e `input[type="password"]` con toggle de visibilidad
- [x] Validación con `loginSchema` (Zod) mediante `react-hook-form`
- [x] Botón "Iniciar sesión" con estado loading mientras `useLogin.isPending`
- [x] Error 401: mostrar "Credenciales inválidas"
- [x] Error 403: mostrar "Usuario inactivo. Contacta a tu administrador"
- [x] Error 429: mostrar "Demasiados intentos. Intenta en X segundos"
- [x] `<form>` semántico con `<label>` asociado a cada `<input>`
- [x] `aria-label` en botón de toggle de contraseña
- [x] Mensajes de error con `role="alert"`
- [x] `autoFocus` en campo email al cargar

## Fase 8 · Páginas y Layout
_Archivos: `apps/frontend/src/app/`_
- [x] Crear `app/auth/layout.tsx` — layout sin sidebar para rutas de auth
- [x] Crear `app/auth/login/page.tsx` — Server Component que renderiza `<LoginForm />`
- [x] Crear `app/auth/login/loading.tsx` — skeleton de la pantalla de login
- [x] Crear `app/employee/dashboard/page.tsx` — placeholder
- [x] Crear `app/manager/dashboard/page.tsx` — placeholder
- [x] Crear `app/admin/dashboard/page.tsx` — placeholder

## Fase 9 · Middleware (Protección de Rutas)
_Archivo: `apps/frontend/src/middleware.ts`_
- [x] Leer cookie de sesión en cada request
- [x] `/auth/login` → redirigir a dashboard si ya autenticado
- [x] `/employee/*` → requiere `role = 'employee' | 'administrator'`
- [x] `/manager/*` → requiere `role = 'manager' | 'administrator'`
- [x] `/admin/*` → requiere `role = 'administrator'`
- [x] Cualquier ruta protegida sin sesión → redirect a `/auth/login`
- [x] Configurar `matcher` en `middleware.ts` para excluir assets estáticos

## Fase 10 · Tests
_9/9 tests passed con vitest_

### Unit / Component Tests (vitest + Testing Library) — 9 passed ✅
- [x] `test_login_schema_rejects_invalid_email`
- [x] `test_login_schema_rejects_empty_password`
- [x] `test_login_schema_accepts_valid_input`
- [x] `test_login_schema_rejects_missing_email`
- [x] `test_login_schema_rejects_missing_password`
- [x] `test_auth_store_starts_with_null_user`
- [x] `test_auth_store_setUser_updates_user_state`
- [x] `test_auth_store_setTokens_updates_token_state`
- [x] `test_auth_store_clearUser_resets_all_state`

### Component render tests — pendiente
- [ ] `test_LoginForm_renders_email_and_password_fields`
- [ ] `test_LoginForm_shows_loading_state_while_submitting`
- [ ] `test_LoginForm_shows_error_message_on_401`
- [ ] `test_LoginForm_shows_error_message_on_403_inactive_user`
- [ ] `test_LoginForm_shows_rate_limit_message_on_429`

### E2E Tests (Playwright) — pendiente
- [ ] Tests de flujo completo (diferido a iteración UX)

## Fase 11 · Accesibilidad
- [x] `<form>` semántico con `<label>` asociado a cada input (for/id)
- [x] `aria-label` en botón de toggle de contraseña
- [x] Mensajes de error con `role="alert"`
- [x] Navegación por teclado completa (Tab entre campos, Enter para submit)
- [x] Focus en el campo email al cargar la página (`autoFocus`)

## Fase 12 · Verificación
- [x] `npm run build` en `apps/frontend/` — sin errores TypeScript ✅
- [x] `npm run test` — 9/9 tests passed ✅
- [ ] Verificar en navegador: estado loading, error 401, error 403, error 429 y estado success
- [ ] Verificar redirección por rol
- [ ] Verificar que ruta protegida sin sesión redirige a `/auth/login`

## Fase 13 · Entrega
- [ ] Commit: `git commit -m "feat(auth): implement login form, session management and role-based routing"`
- [ ] Push: `git push origin feature/002-user-authentication`
- [ ] Abrir PR ahora que todas las capas están completas — NO hacer merge sin validación
