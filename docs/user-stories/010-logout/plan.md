---
story: 010-logout
status: done
branch: feature/010-logout
risk_level: Low
complexity: S
created: 2026-07-07
---

# Plan de Implementación — US-010: Logout

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Frontend | `UserMenu` component + `Header` modification |

**Branch único:** `feature/010-logout`
**Nota:** No hay fase de backend ni DB — el endpoint y la lógica ya existen (US-002).

---

## Fase 1 — Frontend

### 1.1 Componente — `UserMenu`

- [x] `components/layout/UserMenu.tsx`
  - [x] Trigger: avatar + nombre (clickeable)
  - [x] State: `open` toggle para dropdown
  - [x] Dropdown con opción "Cerrar sesión" + icono `LogOut` de lucide-react
  - [x] Invoca `useLogout().mutate()` al click
  - [x] Loading state: "Cerrando..." + disabled cuando `isPending`
  - [x] Click fuera cierra dropdown (event listener)
  - [x] Escape cierra dropdown
  - [x] `aria-expanded`, `aria-haspopup="menu"`, `role="menu"`, `role="menuitem"`

### 1.2 Modificación — `Header.tsx`

- [x] Reemplazar bloque estático de user info con `<UserMenu />`
- [x] Mantener el hamburger button para mobile sin cambios

### 1.3 Tests

- [x] `test_UserMenu_renders_avatar_and_name`
- [x] `test_UserMenu_opens_dropdown_on_click`
- [x] `test_UserMenu_shows_logout_option`

### 1.4 Verificación

- [x] `npx next build --no-lint` sin errores
- [x] `npm test` — 58/58 tests pasan (55 existentes + 3 nuevos)
- [x] Click en avatar abre dropdown
- [x] "Cerrar sesión" invoca logout y redirige a /auth/login
- [x] Loading state visible durante logout
- [x] Click fuera cierra dropdown
- [x] Funciona para los 3 roles

### 1.5 Commits

```
feat(auth): add UserMenu component with logout dropdown
test(auth): add component tests for UserMenu
```

---

## Gate Final — PR

- [x] Tests pasan (58/58)
- [x] Build sin errores
- [x] Logout funciona end-to-end (click → API → redirect)
- [x] Fail-safe: logout local funciona aunque API falle
- [ ] PR creado con resumen, nivel de riesgo Low

---

## Orden de Ejecución

```
/develop-plan fe    → Fase 1
/git-flow pr        → PR único
```
