---
status: done
type: frontend
story: docs/user-stories/010-logout/UserStory.md
depends-on: null
risk_level: Low
complexity: S
---

# [FE] US-010 — Logout Button in Header

## Objetivo

Agregar un dropdown al avatar del usuario en el Header con la opción "Cerrar sesión" que invoque el hook `useLogout()` ya existente.

## Scope

1 componente nuevo (`UserMenu`), 1 componente modificado (`Header`). Sin endpoints nuevos, sin lógica nueva — solo conecta UI con hook existente.

---

## Contrato API Consumido

| Método | Endpoint | Ya existe |
|---|---|---|
| POST | `/api/v1/auth/logout` | ✅ US-002 |

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  components/layout/
    UserMenu.tsx              - CREATE (dropdown con "Cerrar sesión")
    Header.tsx                - MODIFY (reemplazar bloque estático con UserMenu)
```

---

## Implementación

### `UserMenu.tsx`

```typescript
// components/layout/UserMenu.tsx
"use client";

// Props: user (AuthUser | null)
// State: open (boolean) — toggle dropdown
// Action: useLogout().mutate() on click "Cerrar sesión"
// Loading: show "Cerrando..." when isPending
// Trigger: avatar + nombre (clickeable)
// Dropdown: positioned below trigger, closes on click outside
```

**Elementos del dropdown:**
- "Cerrar sesión" con icono `LogOut` de lucide-react
- Loading state: texto "Cerrando..." + disabled cuando `isPending`

**Comportamiento:**
- Click en trigger → toggle dropdown
- Click en "Cerrar sesión" → `mutate()`
- Click fuera → cierra dropdown
- Escape → cierra dropdown

### `Header.tsx` — Modificación

Reemplazar el bloque estático:
```tsx
{/* User info (actual) */}
<div className="flex items-center gap-3">
  <div className="hidden sm:block text-right">...</div>
  <div className="flex h-9 w-9 ...">...</div>
</div>
```

Con:
```tsx
<UserMenu />
```

---

## Edge Cases

| Caso | Comportamiento |
|---|---|
| Token expirado | `onSettled` limpia todo y redirige (ya implementado en hook) |
| Error de red | `onSettled` limpia todo y redirige (fail-safe) |
| Double-click | `isPending` deshabilita el botón |
| Click fuera del dropdown | Cierra el dropdown |
| Tecla Escape | Cierra el dropdown |

---

## Tests Requeridos

> Nivel de riesgo: Low → Unit tests

- [ ] `test_UserMenu_renders_avatar_and_name`
- [ ] `test_UserMenu_opens_dropdown_on_click`
- [ ] `test_UserMenu_shows_logout_option`

---

## Accesibilidad (WCAG 2.1 AA)

- [ ] Trigger con `aria-expanded` y `aria-haspopup="menu"`
- [ ] Dropdown con `role="menu"`
- [ ] Items con `role="menuitem"`
- [ ] Navegación por teclado (Escape cierra)
- [ ] Focus trap dentro del dropdown cuando abierto

---

## Criterios de Aceptación

- [ ] Avatar/nombre en Header es clickeable
- [ ] Click abre dropdown con opción "Cerrar sesión"
- [ ] Click en "Cerrar sesión" invoca logout y redirige a /auth/login
- [ ] Botón muestra loading state durante logout
- [ ] Click fuera cierra el dropdown
- [ ] Funciona para los 3 roles (employee, manager, administrator)
- [ ] `npm run build` sin errores
- [ ] `npm test` — todos los tests pasan

---

## Git Branch

`feature/010-logout`
