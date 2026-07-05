---
status: todo
type: frontend
story: docs/user-stories/004-design-system-ui-shell/UserStory.md
depends-on: null
risk_level: Medium
complexity: M
---

# [FE-1] US-004 — Design Foundations (Tokens + shadcn/ui Setup)

## Objetivo

Configurar las bases del sistema de diseño: dependencias, Tailwind con design tokens, fuente Inter, shadcn/ui inicializado con componentes base, y utilidades compartidas.

## Scope

Configuración de herramientas, archivos de config, CSS variables, componentes shadcn/ui instalados y customizados. Sin layout ni navegación.

---

## Dependencias npm a Instalar

```bash
# shadcn/ui dependencies
npm install clsx tailwind-merge class-variance-authority
npm install lucide-react
npm install @radix-ui/react-slot
npm install @radix-ui/react-dialog
npm install @radix-ui/react-alert-dialog
npm install @radix-ui/react-select
npm install @radix-ui/react-tooltip
```

> Nota: `tailwindcss`, `zod`, `react-hook-form` ya están instalados.

---

## Archivos a Crear / Modificar

```
apps/frontend/
├── tailwind.config.ts                 - CREATE (design tokens, custom colors, font)
├── postcss.config.js                  - CREATE (si no existe)
├── components.json                    - CREATE (shadcn/ui config)
├── src/
│   ├── app/
│   │   └── globals.css                - CREATE (CSS variables + Tailwind directives)
│   ├── app/layout.tsx                 - MODIFY (agregar Inter font + globals.css import)
│   ├── lib/
│   │   └── utils.ts                   - CREATE (cn() helper)
│   └── components/ui/
│       ├── button.tsx                 - CREATE (shadcn/ui customizado)
│       ├── card.tsx                   - CREATE
│       ├── input.tsx                  - CREATE
│       ├── badge.tsx                  - CREATE
│       ├── dialog.tsx                 - CREATE
│       ├── alert-dialog.tsx           - CREATE
│       ├── select.tsx                 - CREATE
│       ├── tooltip.tsx                - CREATE
│       └── skeleton.tsx               - CREATE
└── package.json                       - MODIFY (nuevas deps)
```

---

## Design Tokens (tailwind.config.ts)

```typescript
// Colores semánticos
colors: {
  primary: {
    DEFAULT: '#2563eb',  // blue-600
    dark: '#1e40af',     // blue-800
    light: '#eff6ff',    // blue-50
  },
  accent: '#f97316',      // orange-500
  success: '#16a34a',     // green-600
  danger: '#dc2626',      // red-600
  surface: '#f9fafb',     // gray-50
  border: '#e5e7eb',      // gray-200
}

// Tipografía
fontFamily: {
  sans: ['Inter', ...defaultTheme.fontFamily.sans],
}

// Border radius
borderRadius: {
  lg: '0.5rem',
  xl: '0.75rem',
}
```

---

## CSS Variables (globals.css)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 0 0% 100%;
    --secondary: 220 14.3% 95.9%;
    --accent: 24.6 95% 53.1%;
    --success: 142.1 76.2% 36.3%;
    --destructive: 0 84.2% 60.2%;
    --border: 220 13% 91%;
    --ring: 217.2 91.2% 59.8%;
    --radius: 0.5rem;
  }
}
```

---

## Fuente Inter (layout.tsx)

```typescript
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

// En <html>: className={inter.variable}
// En tailwind.config: fontFamily.sans: ['var(--font-inter)', ...]
```

---

## cn() Helper (lib/utils.ts)

```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## Componentes shadcn/ui — Customizaciones

| Componente | Customización vs default |
|---|---|
| Button | `rounded-lg`, variantes: default (blue-600), outline, ghost, destructive |
| Card | `rounded-lg`, `border-border`, sin shadow (o `shadow-sm`) |
| Input | `rounded-lg`, focus ring `ring-primary` |
| Badge | `rounded-full`, variantes: default, success, warning, danger |
| Skeleton | Pulse animation con `bg-gray-200` |
| Dialog | `rounded-xl`, overlay `bg-black/50` |
| Select | `rounded-lg`, consistent con Input |
| Tooltip | `bg-gray-900 text-white rounded-md text-xs` |

---

## Criterios de Aceptación

- [ ] `npm install` ejecuta sin errores con nuevas dependencias
- [ ] `tailwind.config.ts` tiene paleta custom con todos los tokens definidos
- [ ] `globals.css` tiene CSS variables y Tailwind directives
- [ ] Fuente Inter carga correctamente (verificar en DevTools → Network → Fonts)
- [ ] `cn()` helper funciona y está exportado desde `@/lib/utils`
- [ ] `components.json` configurado para shadcn/ui (paths, aliases)
- [ ] 9 componentes shadcn/ui instalados y customizados en `src/components/ui/`
- [ ] Componentes renderizan correctamente (verificar con una página de prueba temporal)
- [ ] No hay errores de TypeScript ni warnings de Tailwind

---

## Git Branch

`feature/004-design-system-ui-shell`

## Commit sugerido

```
feat(design): add design tokens, Tailwind config, Inter font, and shadcn/ui components
```
