---
story: 004-design-system-ui-shell
status: pending
branch: feature/004-design-system-ui-shell
risk_level: Medium
complexity: L
created: 2026-07-05
---

# Plan de Implementación — US-004: Design System & UI Shell

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | FE-1 Foundations | Tailwind config + Inter font + shadcn/ui (9 componentes) + cn() |
| 2 | FE-2 Layout Shell | Sidebar + Header + AppShell + MobileNav + responsive + migración + tests |

**Branch único:** `feature/004-design-system-ui-shell`
**Commits:** secuenciales por fase (`feat(design):`, `feat(layout):`, `test(layout):`)

---

## Fase 1 — Design Foundations ✅

### 1.1 Dependencias

- [x] Instalar: `clsx`, `tailwind-merge`, `class-variance-authority`
- [x] Instalar: `lucide-react`
- [x] Instalar: `@radix-ui/react-slot`, `@radix-ui/react-dialog`, `@radix-ui/react-alert-dialog`, `@radix-ui/react-select`, `@radix-ui/react-tooltip`
- [x] Instalar: `@tailwindcss/postcss` (Tailwind v4)
- [x] Verificar `npm install` sin errores

### 1.2 Tailwind v4 Config + PostCSS

- [x] Tailwind v4 CSS-based config en `globals.css` con `@theme` block:
  - [x] Paleta custom (primary, primary-dark, primary-light, accent, success, danger, surface, border)
  - [x] Font family: Inter como sans default
  - [x] Border radius: lg (0.5rem), xl (0.75rem)
  - [x] Spacing: sidebar (240px), sidebar-collapsed (64px)
- [x] Crear `postcss.config.js` (`@tailwindcss/postcss` + autoprefixer)

### 1.3 CSS Variables + Globals

- [x] Crear `src/app/globals.css`:
  - [x] `@import "tailwindcss"` (v4 syntax)
  - [x] `@theme` block con design tokens
  - [x] Base styles: body font, antialiased, border-color

### 1.4 Fuente Inter

- [x] Modificar `src/app/layout.tsx`:
  - [x] Import `Inter` from `next/font/google`
  - [x] Configurar con `subsets: ['latin']`, `variable: '--font-inter'`
  - [x] Agregar `className={inter.variable}` al `<html>`
  - [x] Import `globals.css`

### 1.5 Utilidades

- [x] Crear `src/lib/utils.ts` con `cn()` helper (clsx + twMerge)

### 1.6 shadcn/ui Config

- [x] Crear `components.json` con paths y aliases

### 1.7 Componentes shadcn/ui

- [x] `src/components/ui/button.tsx` — variantes: default, outline, ghost, destructive; sizes: sm, default, lg, icon
- [x] `src/components/ui/card.tsx` — Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter
- [x] `src/components/ui/input.tsx` — rounded-lg, focus ring primary
- [x] `src/components/ui/badge.tsx` — variantes: default, success, warning, danger, outline
- [x] `src/components/ui/dialog.tsx` — Dialog con overlay, close button, animations
- [x] `src/components/ui/alert-dialog.tsx` — AlertDialog con Action/Cancel
- [x] `src/components/ui/select.tsx` — Select con Radix UI, rounded-lg
- [x] `src/components/ui/tooltip.tsx` — Tooltip dark bg, rounded-md
- [x] `src/components/ui/skeleton.tsx` — Pulse animation

### 1.8 Verificación

- [x] `npm run build` sin errores
- [x] `npm test` — 37/37 tests passing
- [x] Componentes importables desde `@/components/ui/*`
- [x] `cn()` exportado desde `@/lib/utils`

### 1.9 Commit

```
feat(design): add design tokens, Tailwind v4 config, Inter font, and shadcn/ui components
```

---

## Fase 2 — Layout Shell ✅

### 2.1 UI Store

- [ ] Modificar `src/store/ui-store.ts`:
  - [ ] Agregar `sidebarCollapsed: boolean` (default: false)
  - [ ] Agregar `mobileNavOpen: boolean` (default: false)
  - [ ] Agregar `toggleSidebar()`, `setSidebarCollapsed()`, `setMobileNavOpen()`
  - [ ] Persistir `sidebarCollapsed` en localStorage (Zustand persist)

### 2.2 Navigation Config

- [ ] Crear `src/config/navigation.ts`:
  - [ ] Tipos: `NavItem`, `NavGroup`
  - [ ] `employeeNav`: Mi Semana (Check-In, Dashboard), Proyectos (Mis Proyectos), Reportes (Mi CRS)
  - [ ] `managerNav`: Mi Equipo (Vista de Equipo, Vista Semanal), Proyectos, Reportes (CRS del Equipo, Reportes)
  - [ ] `adminNav`: Organización (Usuarios, Equipos, Proyectos), Reportes (Reportes Generales)
  - [ ] Helper `getNavigationForRole(role: UserRole): NavGroup[]`

### 2.3 Layout Components

- [ ] Crear `src/components/layout/SidebarItem.tsx`:
  - [ ] Props: icon, label, href, active, collapsed
  - [ ] Active state: `bg-primary-light text-primary border-l-2 border-primary`
  - [ ] Collapsed: solo icono + Tooltip
  - [ ] Hover: `bg-gray-100`
  - [ ] `aria-current="page"` cuando activo

- [ ] Crear `src/components/layout/SidebarGroup.tsx`:
  - [ ] Props: title, children, collapsed
  - [ ] Expandido: label uppercase + items
  - [ ] Colapsado: separador visual (hr)

- [ ] Crear `src/components/layout/Sidebar.tsx`:
  - [ ] Props: navigation (NavGroup[])
  - [ ] Logo arriba: "Priorities Tracker" expandido, "PT" colapsado
  - [ ] Renderiza SidebarGroups con SidebarItems
  - [ ] Botón toggle abajo (ChevronLeft/ChevronRight)
  - [ ] Width: 240px expandido, 64px colapsado
  - [ ] `transition-all duration-200 ease-in-out`
  - [ ] `aria-expanded` en toggle button
  - [ ] Hidden en mobile (`hidden md:flex`)

- [ ] Crear `src/components/layout/Header.tsx`:
  - [ ] Lee user de `useAuthStore`
  - [ ] Mobile: hamburger button (Menu icon) a la izquierda
  - [ ] Desktop: espacio vacío a la izquierda
  - [ ] Derecha: avatar circle (iniciales) + nombre + Badge con rol
  - [ ] Height: `h-16`, border-bottom
  - [ ] Hamburger solo visible en `md:hidden`

- [ ] Crear `src/components/layout/MobileNav.tsx`:
  - [ ] Overlay: `fixed inset-0 z-50 bg-black/50`
  - [ ] Panel: `fixed left-0 top-0 h-full w-72 bg-white`
  - [ ] Close button (X) arriba a la derecha
  - [ ] Renderiza navegación completa (como sidebar expandido)
  - [ ] Click en overlay → cierra
  - [ ] Escape → cierra
  - [ ] Click en nav item → navega + cierra
  - [ ] `aria-modal="true"`, `role="dialog"`
  - [ ] Transition: slide-in from left

- [ ] Crear `src/components/layout/AppShell.tsx`:
  - [ ] Props: navigation (NavGroup[]), children
  - [ ] Composición: Sidebar + Header + main content
  - [ ] Content area: `ml-60` (expandido), `ml-16` (colapsado), `ml-0` (mobile)
  - [ ] Content padding: `p-6`
  - [ ] Content max-width: `max-w-4xl` (lectura cómoda)
  - [ ] MobileNav renderizado condicionalmente

### 2.4 Route Group Layout

- [ ] Crear `src/app/(authenticated)/layout.tsx`:
  - [ ] `"use client"`
  - [ ] Lee rol del usuario de `useAuthStore` o cookie
  - [ ] Llama `getNavigationForRole(role)`
  - [ ] Renderiza `<AppShell navigation={nav}>{children}</AppShell>`

- [ ] Mover `src/app/employee/` dentro de `src/app/(authenticated)/employee/`
- [ ] Mover `src/app/manager/` dentro de `src/app/(authenticated)/manager/`
- [ ] Mover `src/app/admin/` dentro de `src/app/(authenticated)/admin/`
- [ ] Verificar que `src/app/auth/` NO está dentro de (authenticated)

### 2.5 Migración de Páginas

- [ ] `/employee/checkin/page.tsx`:
  - [ ] Remover wrapper div con `max-w-3xl mx-auto p-6 space-y-6` (layout lo provee)
  - [ ] Mantener toda la lógica funcional intacta

- [ ] `/employee/dashboard/page.tsx`:
  - [ ] Reemplazar con contenido usando Card component:
    - [ ] Heading "Dashboard"
    - [ ] Card: "Próximamente: métricas de tu semana"

### 2.6 Responsive Detection

- [ ] En AppShell: detectar breakpoint inicial con `window.matchMedia`
  - [ ] `≥1280px` → sidebar expandido
  - [ ] `≥768px <1280px` → sidebar colapsado
  - [ ] `<768px` → sidebar oculto (solo mobile nav)
- [ ] Listener para resize (actualizar estado si cambia breakpoint)

### 2.7 Verificación Visual

- [ ] Desktop (≥1280px): sidebar expandido, navegación visible, content con margin
- [ ] Tablet (768-1279px): sidebar colapsado, iconos con tooltip
- [ ] Mobile (<768px): sin sidebar, hamburger en header, overlay nav funcional
- [ ] Login page: sin sidebar, centrada
- [ ] Check-in page: funcional dentro del nuevo layout
- [ ] Navegación entre páginas funciona correctamente

### 2.8 Tests

- [ ] `test_Sidebar_renders_navigation_groups`
- [ ] `test_Sidebar_collapses_on_toggle_click`
- [ ] `test_Sidebar_shows_tooltips_when_collapsed`
- [ ] `test_Sidebar_highlights_active_item`
- [ ] `test_Header_renders_user_name_and_role`
- [ ] `test_Header_shows_hamburger_on_mobile`
- [ ] `test_MobileNav_opens_on_hamburger_click`
- [ ] `test_MobileNav_closes_on_overlay_click`
- [ ] `test_MobileNav_closes_on_escape`
- [ ] `test_navigation_config_returns_correct_items_for_employee`
- [ ] `test_navigation_config_returns_correct_items_for_manager`
- [ ] `test_ui_store_toggles_sidebar_state`

### 2.9 Commits

```
feat(design): add ui-store sidebar state and navigation config
feat(layout): implement Sidebar, Header, AppShell, and MobileNav
feat(layout): add (authenticated) route group layout
feat(layout): migrate employee pages to new layout shell
test(layout): add component tests for layout shell
```

---

## Gate Final — PR

- [ ] Todos los tests pasan (existentes + nuevos de layout)
- [ ] No hay errores de TypeScript (`npm run build`)
- [ ] Responsive verificado en 3 breakpoints
- [ ] Login page sin sidebar
- [ ] Check-in page funcional dentro del layout
- [ ] Navegación funcional entre páginas
- [ ] Sidebar persiste estado entre recargas
- [ ] Accesibilidad: keyboard nav, aria attributes
- [ ] PR creado con resumen y evidencia visual

---

## Orden de Ejecución

```
/develop-plan foundations  → Fase 1 (tokens + shadcn/ui)
/develop-plan layout       → Fase 2 (shell + responsive + migración + tests)
/git-flow pr               → PR único con las 2 fases
```
