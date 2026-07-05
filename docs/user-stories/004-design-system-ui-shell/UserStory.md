---
id: US-004
title: Design System & UI Shell
status: enriched
priority: high
risk_level: Medium
complexity: L
created: 2026-07-05
---

# US-004 — Design System & UI Shell

## Narrativa

**Como** usuario de Priorities Tracker (employee, manager o administrator),
**quiero** una interfaz ejecutiva, limpia y responsive con navegación lateral retráctil,
**para** poder usar la plataforma cómodamente desde cualquier dispositivo y tamaño de pantalla.

---

## Contexto

La plataforma tiene funcionalidad implementada (auth, check-in, priorities) pero sin sistema de diseño ni layout consistente. Esta US establece los fundamentos visuales y el shell de navegación que todas las páginas heredarán.

---

## Requerimientos de Diseño

### Paleta de Colores

| Token | Valor | Uso |
|---|---|---|
| `primary` | Blue-600 (azul medio) | Acciones principales, links, sidebar activo |
| `primary-dark` | Blue-800 | Hover en botones primarios |
| `primary-light` | Blue-50 | Backgrounds sutiles, badges |
| `secondary` | Gray-500 (gris neutro) | Texto secundario, bordes, iconos inactivos |
| `accent` | Orange-500 | Notificaciones, badges de atención, CRS moderado |
| `success` | Green-600 | Confirmaciones, check-out completado, CRS alto |
| `danger` | Red-600 | Errores, alertas, CRS bajo |
| `background` | White | Fondo principal |
| `surface` | Gray-50 | Cards, sidebar background |
| `border` | Gray-200 | Bordes de cards, separadores |
| `text-primary` | Gray-900 | Texto principal |
| `text-secondary` | Gray-500 | Texto secundario, labels |

### Tipografía

| Elemento | Fuente | Peso | Tamaño |
|---|---|---|---|
| Headings | Inter | 600 (semibold) | 2xl / xl / lg |
| Body | Inter | 400 (regular) | base (16px) |
| Labels | Inter | 500 (medium) | sm (14px) |
| Captions | Inter | 400 | xs (12px) |

- Line-height espaciado para lectura (1.6 en body, 1.4 en headings)
- Letter-spacing: normal

### Iconografía

| Librería | Estilo |
|---|---|
| Lucide React | Outline, stroke-width 1.5 |

- Iconos modernos, línea fina, consistentes
- Tamaño estándar: 20px en sidebar, 16px inline

### Componentes Base (shadcn/ui)

| Componente | Estilo |
|---|---|
| Buttons | `rounded-lg` (redondeados), variantes: default, outline, ghost, destructive |
| Cards | Borde `border-gray-200`, sin sombra (o `shadow-sm` sutil), `rounded-lg` |
| Inputs | `rounded-lg`, borde gris, focus ring azul |
| Badges | `rounded-full`, variantes por color semántico |
| Dialogs | Centrados, overlay oscuro, `rounded-xl` |
| Tooltips | Fondo oscuro, texto blanco, `rounded-md` |

### Layout Shell

```
┌─────────────────────────────────────────────────────┐
│ [Logo]  Sidebar (240px)  │  Header (avatar, nombre) │
│                          │                          │
│  ┌─ Mi Semana ─────────┐ │  ┌─────────────────────┐ │
│  │ 📋 Check-In         │ │  │                     │ │
│  │ 📊 Dashboard        │ │  │   Content Area      │ │
│  └─────────────────────┘ │  │                     │ │
│  ┌─ Proyectos ─────────┐ │  │                     │ │
│  │ 📁 Mis Proyectos    │ │  │                     │ │
│  └─────────────────────┘ │  │                     │ │
│  ┌─ Reportes ──────────┐ │  │                     │ │
│  │ 📈 Mi CRS           │ │  │                     │ │
│  └─────────────────────┘ │  └─────────────────────┘ │
│                          │                          │
│  [Collapse ←]            │                          │
└─────────────────────────────────────────────────────┘
```

#### Sidebar

| Estado | Comportamiento |
|---|---|
| Expandido (desktop) | 240px, iconos + texto, grupos con label |
| Colapsado (desktop) | 64px, solo iconos con tooltip |
| Mobile (<768px) | Oculto, hamburger menu en header, overlay al abrir |

#### Header

| Elemento | Posición |
|---|---|
| Hamburger (mobile) | Izquierda |
| Page title / breadcrumb | Centro-izquierda |
| Avatar + nombre + rol | Derecha |

### Responsive Breakpoints

| Breakpoint | Comportamiento |
|---|---|
| `≥1280px` (xl) | Sidebar expandido por defecto |
| `≥768px` (md) | Sidebar colapsado por defecto, expandible |
| `<768px` (sm) | Sidebar oculto, hamburger menu |

### Adaptaciones Mobile

- Tablas → se convierten en cards apiladas
- Sidebar → hamburger menu con overlay
- Forms → full-width, inputs más grandes (touch-friendly)
- Buttons → full-width en mobile cuando aplica

### Animaciones y Transiciones

| Elemento | Transición |
|---|---|
| Sidebar collapse/expand | `transition-all duration-200 ease-in-out` |
| Page transitions | Fade suave (opacity 150ms) |
| Hover en cards/buttons | `transition-colors duration-150` |
| Skeleton loaders | Pulse animation en loading states |
| Modals | Fade-in overlay + scale-up content |

- Mínimas, funcionales, no decorativas
- Sin animaciones que bloqueen interacción

### Densidad

- Espaciado generoso entre secciones (`space-y-6`)
- Cards con padding `p-6`
- Dashboards: una métrica/card a la vez, no tablas densas
- Lectura cómoda: max-width `max-w-4xl` en contenido principal

---

## Referencia Visual

**Vercel Dashboard** — Layout limpio, sidebar minimalista, tipografía Inter, espaciado generoso, cards con bordes sutiles, paleta monocromática con acentos de color.

---

## Criterios de Aceptación

### Design Tokens
- [ ] Archivo `tailwind.config.ts` con paleta de colores custom
- [ ] Fuente Inter configurada (Google Fonts o next/font)
- [ ] Variables CSS para colores semánticos
- [ ] Configuración de shadcn/ui con theme custom

### Layout Shell
- [ ] Componente `Sidebar` con estados expandido/colapsado
- [ ] Componente `Header` con avatar y nombre del usuario
- [ ] Layout wrapper que compone Sidebar + Header + Content
- [ ] Sidebar retráctil con botón de toggle
- [ ] Grupos de navegación: "Mi Semana", "Proyectos", "Reportes"

### Responsive
- [ ] Sidebar oculto en mobile (<768px)
- [ ] Hamburger menu funcional en mobile
- [ ] Content area full-width en mobile
- [ ] Tablas se convierten en cards en mobile

### Componentes shadcn/ui Configurados
- [ ] Button (variantes: default, outline, ghost, destructive)
- [ ] Card (con borde, rounded-lg)
- [ ] Input (rounded-lg, focus ring azul)
- [ ] Badge (variantes semánticas)
- [ ] Dialog / AlertDialog
- [ ] Select
- [ ] Tooltip

### Transiciones
- [ ] Sidebar collapse/expand animado
- [ ] Hover states en botones y cards
- [ ] Skeleton loaders en páginas con data fetching

### Integración
- [ ] Página `/employee/checkin` usa el nuevo layout
- [ ] Página `/employee/dashboard` usa el nuevo layout
- [ ] Login page mantiene layout centrado (sin sidebar)

---

## Navegación por Rol

### Employee
```
Mi Semana
  ├── Check-In
  └── Dashboard

Proyectos
  └── Mis Proyectos

Reportes
  └── Mi CRS
```

### Manager
```
Mi Equipo
  ├── Vista de Equipo
  └── Vista Semanal

Proyectos
  └── Proyectos del Equipo

Reportes
  ├── CRS del Equipo
  └── Reportes
```

### Administrator
```
Organización
  ├── Usuarios
  ├── Equipos
  └── Proyectos

Reportes
  └── Reportes Generales
```

---

## Notas Técnicas

- Usar `next/font` para cargar Inter (optimizado, sin FOUT)
- Sidebar state en Zustand (`ui-store.ts`) para persistir preferencia
- CSS variables para theming (facilita futuro dark mode)
- shadcn/ui CLI para instalar componentes (`npx shadcn-ui@latest add button card ...`)
- Lucide React para iconografía consistente

---

## Dependencias

- No depende de ninguna otra US
- Todas las US futuras heredarán este layout

---

## Modo Oscuro

No incluido en esta US. Se deja preparado con CSS variables para implementar en una US futura.

---

## Git Branch

`feature/004-design-system-ui-shell`

---

## [enhanced]

### Análisis de Impacto

| Área | Impacto |
|---|---|
| Frontend | Alto — afecta todas las páginas existentes y futuras |
| Backend | Ninguno — no requiere cambios en API |
| Database | Ninguno |
| Infraestructura | Bajo — nuevas dependencias npm (lucide-react, @next/font) |

### Dependencias Técnicas Identificadas

| Dependencia | Estado | Acción |
|---|---|---|
| `shadcn/ui` | En package.json pero sin componentes instalados | Instalar componentes via CLI |
| `lucide-react` | No instalado | Agregar a dependencies |
| `tailwindcss` | No configurado con custom theme | Configurar tailwind.config.ts |
| `next/font` | Disponible (Next.js 15) | Configurar Inter en layout.tsx |
| `clsx` / `tailwind-merge` | Requerido por shadcn/ui | Instalar |
| `class-variance-authority` | Requerido por shadcn/ui | Instalar |

### Archivos Existentes Afectados

| Archivo | Cambio |
|---|---|
| `src/app/layout.tsx` | Agregar fuente Inter, CSS variables, providers |
| `src/app/employee/checkin/page.tsx` | Envolver en nuevo layout shell |
| `src/app/employee/dashboard/page.tsx` | Envolver en nuevo layout shell |
| `src/app/auth/login/page.tsx` | Mantener layout centrado (sin sidebar) |
| `src/store/auth-store.ts` | Ya existe — se usa para avatar/nombre en header |
| `src/middleware.ts` | Sin cambios — routing ya funciona |
| `package.json` | Nuevas dependencias |
| `tailwind.config.ts` | Crear con design tokens |

### Archivos Nuevos a Crear

```
src/
├── app/
│   ├── globals.css                    # CSS variables + Tailwind directives
│   └── (authenticated)/
│       └── layout.tsx                 # Layout con Sidebar + Header (employee/manager/admin)
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx                # Sidebar retráctil con navegación por rol
│   │   ├── SidebarItem.tsx            # Item individual con icono + texto
│   │   ├── SidebarGroup.tsx           # Grupo de items con label
│   │   ├── Header.tsx                 # Header con avatar, nombre, hamburger
│   │   ├── AppShell.tsx               # Composición Sidebar + Header + Content
│   │   └── MobileNav.tsx              # Overlay navigation para mobile
│   └── ui/
│       ├── button.tsx                 # shadcn/ui customizado
│       ├── card.tsx                   # shadcn/ui customizado
│       ├── input.tsx                  # shadcn/ui customizado
│       ├── badge.tsx                  # shadcn/ui customizado
│       ├── dialog.tsx                 # shadcn/ui
│       ├── alert-dialog.tsx           # shadcn/ui
│       ├── select.tsx                 # shadcn/ui
│       ├── tooltip.tsx                # shadcn/ui
│       └── skeleton.tsx               # shadcn/ui
├── store/
│   └── ui-store.ts                    # Sidebar state (collapsed/expanded)
├── lib/
│   └── utils.ts                       # cn() helper (clsx + tailwind-merge)
└── config/
    └── navigation.ts                  # Definición de menú por rol
```

### NFRs Aplicables

| NFR | Requisito | Cómo se cumple |
|---|---|---|
| NFR-010 | Procesos completables en minutos | Layout no agrega fricción, navegación directa |
| NFR-011 | Usable en desktop y mobile | Responsive breakpoints, sidebar adaptativo |

### Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Conflictos con estilos inline existentes | Alta | Medio | Migrar estilos existentes al nuevo sistema en la misma US |
| shadcn/ui requiere configuración específica de Tailwind | Media | Bajo | Seguir docs oficiales de shadcn/ui para Next.js 15 |
| Sidebar state no persiste entre recargas | Baja | Bajo | Usar `localStorage` via Zustand persist middleware |

### Estimación

| Fase | Esfuerzo |
|---|---|
| Design tokens + Tailwind config | S |
| shadcn/ui setup + componentes base | M |
| Layout shell (Sidebar + Header + AppShell) | L |
| Responsive + mobile nav | M |
| Migración de páginas existentes | S |
| Tests de componentes | M |
| **Total** | **L** |

### Orden de Implementación Sugerido

```
1. Dependencias + Tailwind config + CSS variables + Inter font
2. shadcn/ui init + componentes base (button, card, input, badge, etc.)
3. ui-store.ts (sidebar state) + navigation config por rol
4. Layout components (Sidebar, Header, AppShell, MobileNav)
5. Route group (authenticated)/layout.tsx con AppShell
6. Migrar /employee/checkin y /employee/dashboard al nuevo layout
7. Tests de componentes de layout
```

### Testing Strategy

| Nivel | Qué testear |
|---|---|
| Component tests | Sidebar render, collapse/expand, navigation items por rol |
| Component tests | Header render, avatar, hamburger visibility |
| Component tests | MobileNav overlay open/close |
| Visual | Verificar responsive en 3 breakpoints (sm, md, xl) |
| Accessibility | Keyboard navigation en sidebar, aria-labels, focus trap en mobile nav |
