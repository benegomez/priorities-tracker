# Pull Request — US-004 Design System & UI Shell

**URL:** https://github.com/benegomez/priorities-tracker/pull/new/feature/004-design-system-ui-shell

**Base:** `main`
**Branch:** `feature/004-design-system-ui-shell`

---

## Título

```
feat: US-004 Design System & UI Shell
```

## Resumen

Implementación completa del sistema de diseño y shell de navegación para Priorities Tracker. Establece los fundamentos visuales (Tailwind v4, Inter, shadcn/ui) y el layout responsive (sidebar retráctil, header, mobile nav) que todas las páginas heredan.

## Cambios

### Fase 1 — Design Foundations
- Tailwind v4 con `@theme` design tokens (paleta azul, tipografía Inter, spacing)
- PostCSS config con `@tailwindcss/postcss`
- `cn()` utility (clsx + tailwind-merge)
- 9 componentes shadcn/ui: Button, Card, Input, Badge, Dialog, AlertDialog, Select, Tooltip, Skeleton
- `components.json` para shadcn/ui CLI

### Fase 2 — Layout Shell
- `AppShell` con Sidebar + Header + MobileNav
- Sidebar retráctil: 240px expandido, 64px colapsado, oculto en mobile
- Header con avatar (iniciales), nombre, rol badge, hamburger en mobile
- MobileNav overlay con Escape/click-outside close
- Navigation config por rol (employee, manager, administrator)
- UI store con persist en localStorage
- Route group `(authenticated)/` wrapping employee/manager/admin
- Login page restyled con card centrada

### Fixes incluidos
- Login/Logout hooks ahora setean/limpian cookies para middleware
- Backend: `priorities_count` en CheckInResponse
- Backend: skip Monday validation en development
- Frontend: trailing slash fix en checkin service
- Next.js dev indicator deshabilitado

## Nivel de Riesgo

**Medium** — Cambios visuales y de layout, sin lógica de negocio nueva

## Evidencia de Tests

- Frontend: 47/47 tests passing (10 nuevos de layout + 37 existentes)
- Build: `npm run build` sin errores
- Responsive verificado en desktop, tablet y mobile

## Archivos Clave

| Archivo | Propósito |
|---|---|
| `src/app/globals.css` | Design tokens Tailwind v4 |
| `src/components/layout/Sidebar.tsx` | Sidebar retráctil |
| `src/components/layout/AppShell.tsx` | Layout composition |
| `src/config/navigation.ts` | Menú por rol |
| `src/app/(authenticated)/layout.tsx` | Route group layout |
