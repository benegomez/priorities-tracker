---
status: done
type: frontend
story: docs/user-stories/004-design-system-ui-shell/UserStory.md
depends-on: tickets/foundations/ticket.md
risk_level: Medium
complexity: L
---

# [FE-2] US-004 — Layout Shell (Sidebar + Header + Responsive)

## Objetivo

Implementar el shell de navegación completo: sidebar retráctil con navegación por rol, header con avatar, mobile navigation, y migrar las páginas existentes al nuevo layout.

## Scope

Componentes de layout, store de UI, configuración de navegación por rol, responsive behavior, migración de páginas existentes. Sin nuevos endpoints ni lógica de negocio.

## Dependencia

Ticket FE-1 (foundations) completado — Tailwind config, shadcn/ui, y cn() disponibles.

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
├── config/
│   └── navigation.ts                  - CREATE (menú por rol)
├── store/
│   └── ui-store.ts                    - MODIFY (agregar sidebar state)
├── components/
│   └── layout/
│       ├── Sidebar.tsx                - CREATE
│       ├── SidebarItem.tsx            - CREATE
│       ├── SidebarGroup.tsx           - CREATE
│       ├── Header.tsx                 - CREATE
│       ├── AppShell.tsx               - CREATE
│       └── MobileNav.tsx              - CREATE
├── app/
│   ├── (authenticated)/
│   │   └── layout.tsx                 - CREATE (wraps employee/, manager/, admin/)
│   ├── employee/
│   │   ├── layout.tsx                 - DELETE or MODIFY (usar (authenticated) layout)
│   │   ├── checkin/page.tsx           - MODIFY (remover estilos inline, usar layout)
│   │   └── dashboard/page.tsx         - MODIFY (contenido básico con nuevo layout)
│   └── auth/
│       └── login/page.tsx             - VERIFY (sin sidebar, layout centrado)
└── tests/
    └── layout.test.tsx                - CREATE (component tests)
```

---

## Configuración de Navegación (config/navigation.ts)

```typescript
import { ClipboardCheck, LayoutDashboard, FolderOpen, TrendingUp, Users, Building2 } from "lucide-react";

export interface NavItem {
  label: string;
  href: string;
  icon: LucideIcon;
}

export interface NavGroup {
  title: string;
  items: NavItem[];
}

export const employeeNav: NavGroup[] = [
  {
    title: "Mi Semana",
    items: [
      { label: "Check-In", href: "/employee/checkin", icon: ClipboardCheck },
      { label: "Dashboard", href: "/employee/dashboard", icon: LayoutDashboard },
    ],
  },
  {
    title: "Proyectos",
    items: [
      { label: "Mis Proyectos", href: "/employee/projects", icon: FolderOpen },
    ],
  },
  {
    title: "Reportes",
    items: [
      { label: "Mi CRS", href: "/employee/crs", icon: TrendingUp },
    ],
  },
];

export const managerNav: NavGroup[] = [...];
export const adminNav: NavGroup[] = [...];
```

---

## UI Store (store/ui-store.ts)

Agregar al store existente o crear uno nuevo:

```typescript
interface UIStore {
  sidebarCollapsed: boolean;
  mobileNavOpen: boolean;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setMobileNavOpen: (open: boolean) => void;
}
```

- Persistir `sidebarCollapsed` en `localStorage` via Zustand persist
- `mobileNavOpen` no se persiste (siempre cerrado al cargar)

---

## Componentes de Layout

### AppShell.tsx

Composición principal:

```
┌──────────────────────────────────────┐
│ Sidebar │ Header                     │
│         │────────────────────────────│
│         │                            │
│         │ {children}                 │
│         │                            │
└──────────────────────────────────────┘
```

- Recibe `children` (contenido de la página)
- Lee `sidebarCollapsed` del store
- En mobile: sin sidebar, solo header con hamburger

### Sidebar.tsx

| Prop | Tipo | Descripción |
|---|---|---|
| `navigation` | `NavGroup[]` | Items de navegación según rol |

Comportamiento:
- Expandido: 240px, muestra icono + texto + group labels
- Colapsado: 64px, solo iconos con Tooltip
- Logo arriba (texto "PT" cuando colapsado, "Priorities Tracker" expandido)
- Botón collapse/expand abajo
- Item activo: `bg-primary-light text-primary border-l-2 border-primary`
- Transición: `transition-all duration-200 ease-in-out`

### Header.tsx

| Prop | Tipo | Descripción |
|---|---|---|
| — | — | Lee user del AuthStore |

Contenido:
- Mobile: hamburger button (izquierda)
- Desktop: vacío a la izquierda (o breadcrumb futuro)
- Derecha: avatar circle (iniciales) + nombre + rol badge
- Height: `h-16`
- Border bottom: `border-b border-border`

### MobileNav.tsx

- Overlay `fixed inset-0 z-50 bg-black/50`
- Panel lateral izquierdo con navegación completa
- Close button (X) arriba a la derecha
- Click en overlay cierra
- Escape cierra
- Focus trap dentro del panel

### SidebarGroup.tsx

- Label del grupo en `text-xs uppercase text-secondary tracking-wider`
- Solo visible cuando sidebar está expandido
- Cuando colapsado: separador visual (línea fina)

### SidebarItem.tsx

- Icono (20px) + texto
- Active state: highlight azul
- Hover: `bg-gray-100`
- Cuando colapsado: solo icono + Tooltip con el label

---

## Route Group: (authenticated)/layout.tsx

```typescript
export default function AuthenticatedLayout({ children }) {
  // Determinar navegación según rol del usuario
  // Renderizar AppShell con la navegación correcta
  return <AppShell navigation={navForRole}>{children}</AppShell>
}
```

Las carpetas `employee/`, `manager/`, `admin/` se mueven dentro de `(authenticated)/` para heredar el layout automáticamente.

---

## Responsive Behavior

| Breakpoint | Sidebar | Header | Content margin-left |
|---|---|---|---|
| `≥1280px` | Expandido (240px) | Normal | `ml-60` |
| `≥768px` | Colapsado (64px) | Normal | `ml-16` |
| `<768px` | Oculto | Hamburger visible | `ml-0` |

El sidebar detecta el breakpoint inicial via `window.matchMedia` y ajusta el estado default.

---

## Migración de Páginas Existentes

### /employee/checkin/page.tsx

- Remover `className="max-w-3xl mx-auto p-6 space-y-6"` del wrapper (el layout lo provee)
- Mantener toda la lógica funcional intacta
- El layout agrega el padding y max-width

### /employee/dashboard/page.tsx

- Agregar contenido placeholder con el nuevo estilo:
  - Heading "Dashboard"
  - Card con mensaje "Próximamente: métricas de tu semana"

### /auth/login

- NO usar el (authenticated) layout
- Mantener centrado sin sidebar (ya funciona así)

---

## Criterios de Aceptación

### Layout Shell
- [ ] `AppShell` renderiza Sidebar + Header + Content correctamente
- [ ] Sidebar muestra navegación agrupada según rol del usuario
- [ ] Sidebar se colapsa/expande con botón toggle
- [ ] Sidebar colapsado muestra solo iconos con tooltip
- [ ] Header muestra avatar (iniciales) + nombre + rol del usuario
- [ ] Logo visible en sidebar (texto completo expandido, iniciales colapsado)

### Responsive
- [ ] En `≥1280px`: sidebar expandido por defecto
- [ ] En `≥768px <1280px`: sidebar colapsado por defecto
- [ ] En `<768px`: sidebar oculto, hamburger en header
- [ ] MobileNav se abre como overlay al click en hamburger
- [ ] MobileNav se cierra con click en overlay, botón X, o Escape
- [ ] Content area ocupa todo el ancho disponible en mobile

### Navegación
- [ ] Items de navegación correctos para rol `employee`
- [ ] Item activo resaltado visualmente
- [ ] Click en item navega a la ruta correcta
- [ ] En mobile: click en item cierra el MobileNav y navega

### Transiciones
- [ ] Sidebar collapse/expand animado (200ms ease-in-out)
- [ ] MobileNav overlay fade-in/out
- [ ] Hover states en items de navegación

### Integración
- [ ] `/employee/checkin` renderiza dentro del layout con sidebar
- [ ] `/employee/dashboard` renderiza dentro del layout con sidebar
- [ ] `/auth/login` renderiza SIN sidebar (layout centrado)
- [ ] Navegación funcional entre páginas

### Persistencia
- [ ] Estado collapsed/expanded se persiste en localStorage
- [ ] Al recargar, el sidebar mantiene su estado anterior

### Accesibilidad
- [ ] Sidebar navegable por teclado (Tab entre items)
- [ ] `aria-expanded` en botón de toggle
- [ ] `aria-current="page"` en item activo
- [ ] MobileNav: focus trap, `aria-modal="true"`, Escape cierra
- [ ] Tooltips en modo colapsado accesibles

---

## Tests Requeridos

### Component Tests (vitest + @testing-library/react)

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

---

## Git Branch

`feature/004-design-system-ui-shell`

## Commits sugeridos

```
feat(design): add ui-store sidebar state and navigation config
feat(layout): implement Sidebar, Header, AppShell, and MobileNav
feat(layout): add (authenticated) route group layout
feat(layout): migrate employee pages to new layout shell
test(layout): add component tests for layout shell
```
