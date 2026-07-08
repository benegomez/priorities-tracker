---
id: US-010
title: Logout — Cerrar Sesión
status: enriched
priority: high
risk_level: Low
complexity: S
created: 2026-07-07
---

# US-010 — Logout: Cerrar Sesión

## [original]

**Como** usuario autenticado (employee, manager o administrator),
**quiero** poder cerrar mi sesión desde la interfaz,
**para** proteger mi cuenta cuando dejo de usar la plataforma.

### Contexto

El backend ya tiene `POST /api/v1/auth/logout` implementado (revoca el refresh token). El frontend ya tiene `useLogout` hook y `logout()` service function. Lo que falta es **un botón visible en la UI** que invoque el logout. Actualmente no hay forma de cerrar sesión desde la interfaz — el usuario tendría que borrar cookies manualmente.

---

## [enhanced]

### User Journey

- **Usuario principal:** Cualquier usuario autenticado (employee, manager, administrator)
- **Flujo:**
  1. Usuario hace click en su avatar/nombre en el Header
  2. Se despliega un dropdown con la opción "Cerrar sesión"
  3. Al hacer click en "Cerrar sesión":
     - Se invoca `POST /api/v1/auth/logout` (revoca refresh token)
     - Se limpian cookies (`access_token`, `user_role`)
     - Se limpia el Zustand store (`clearUser()`)
     - Se redirige a `/auth/login`
  4. Si el request de logout falla (red, token expirado), el logout local se ejecuta de todas formas (`onSettled`)

---

### Business Value

- **Problema que resuelve:** Sin botón de logout, el usuario no puede cerrar sesión de forma segura. Esto es un requisito básico de seguridad y usabilidad.
- **Beneficio esperado:** El usuario puede proteger su cuenta al terminar de usar la plataforma, especialmente en dispositivos compartidos.

---

### FR de Referencia

- Requisito implícito de seguridad — toda aplicación autenticada debe permitir logout
- Evento de auditoría `auth.logout` ya implementado en backend

---

### Bounded Context

Organization → Módulo: `auth`

---

### Contrato API

**Ya existe — sin cambios:**

| Método | Endpoint | Status | Propósito |
|---|---|---|---|
| POST | `/api/v1/auth/logout` | ✅ US-002 | Revoca refresh token |

Request body: `{ "refresh_token": "<token>" }`
Response: `{ "message": "logged out" }`
Auth: Bearer JWT requerido

---

### Código existente reutilizable

| Artefacto | Ubicación | Estado |
|---|---|---|
| `POST /auth/logout` endpoint | `modules/auth/api/router.py` | ✅ Implementado |
| `LogoutUseCase` | `modules/auth/application/commands/logout_command.py` | ✅ Implementado |
| `logout()` service | `features/auth/services/auth-service.ts` | ✅ Implementado |
| `useLogout()` hook | `features/auth/hooks/useLogout.ts` | ✅ Implementado |
| `clearUser()` | `store/auth-store.ts` | ✅ Implementado |

**Lo único que falta:** Un botón en la UI que invoque `useLogout().mutate()`.

---

### Implementación

#### Opción elegida: Dropdown en el Header

Agregar un dropdown al avatar/nombre del usuario en el `Header` component con la opción "Cerrar sesión".

```
Header (actual):
  [Hamburger]  ────────────────────  [Nombre] [Badge rol] [Avatar]

Header (con logout):
  [Hamburger]  ────────────────────  [Nombre] [Badge rol] [Avatar ▼]
                                                            └── Dropdown
                                                                ├── Mi perfil (futuro)
                                                                └── Cerrar sesión
```

#### Componente: `UserMenu`

```
components/layout/UserMenu.tsx
  - Trigger: avatar + nombre (clickeable)
  - Dropdown con:
    - "Cerrar sesión" → invoca useLogout().mutate()
  - Usa Popover o DropdownMenu de shadcn/ui (si existe) o un simple state toggle
```

#### Modificación: `Header.tsx`

Reemplazar el bloque estático de user info con el nuevo `UserMenu` component.

---

### Edge Cases

| Caso | Comportamiento |
|---|---|
| Logout con token expirado | `onSettled` limpia cookies y redirige de todas formas |
| Error de red en logout | `onSettled` limpia cookies y redirige (fail-safe) |
| Double-click en logout | `useMutation` previene ejecución duplicada (isPending) |
| Usuario ya deslogueado (cookie borrada) | Middleware redirige a login antes de llegar al botón |

---

### Acceptance Criteria

**Escenario 1 — Logout exitoso**
```gherkin
Given un usuario autenticado
When hace click en su avatar y selecciona "Cerrar sesión"
Then se invoca POST /auth/logout
  And se limpian las cookies (access_token, user_role)
  And se limpia el store de Zustand
  And se redirige a /auth/login
```

**Escenario 2 — Logout con error de red (fail-safe)**
```gherkin
Given un usuario autenticado con conexión inestable
When hace click en "Cerrar sesión" y el request falla
Then se limpian las cookies y el store de todas formas (onSettled)
  And se redirige a /auth/login
```

**Escenario 3 — Botón visible para todos los roles**
```gherkin
Given un usuario con cualquier rol (employee, manager, administrator)
When está en cualquier página autenticada
Then ve el botón de logout accesible desde el Header
```

**Escenario 4 — Prevención de double-click**
```gherkin
Given un usuario que hace click en "Cerrar sesión"
When el request está en progreso
Then el botón muestra estado de loading y no permite otro click
```

---

### Non-Functional Requirements

- **NFR-001** — Logout completa en < 2s (incluyendo redirect)
- **NFR-002** — Fail-safe: siempre limpia estado local aunque el backend falle

---

### Technical Notes

#### shadcn/ui disponible
El proyecto ya tiene `dialog.tsx`, `tooltip.tsx`, `button.tsx`. Para el dropdown se puede usar un simple `Popover` o un div con state toggle — no es necesario instalar un componente nuevo de shadcn.

#### `useLogout` ya implementa `onSettled`
El hook existente ya hace:
1. Llama `logout(accessToken, refreshToken)`
2. En `onSettled` (siempre, éxito o error): `clearUser()` + borra cookies + `router.push("/auth/login")`

Solo falta invocarlo desde un botón.

---

### Dependencies

- **Técnicas:**
  - `POST /api/v1/auth/logout` ✅ US-002
  - `useLogout()` hook ✅ US-002
  - `logout()` service ✅ US-002
  - `clearUser()` store ✅ US-002
  - `Header.tsx` ✅ US-004
- **Funcionales:**
  - Requiere US-002 (auth) ✅

---

### Nivel de Riesgo

**Low** — Todo el backend y la lógica frontend ya existen. Solo se agrega un botón que invoca código existente.

---

### Complejidad Estimada

**S**

| Factor | Detalle |
|---|---|
| Capas afectadas | Frontend únicamente (1 componente nuevo + 1 modificado) |
| Endpoints nuevos | 0 |
| Lógica nueva | 0 — solo conecta UI con hook existente |
| Tests | Low: 2-3 component tests |
| UI | 1 componente nuevo (`UserMenu`), 1 modificado (`Header`) |

---

### Siguiente Paso

Ejecutar `/create-tickets 010-logout`
