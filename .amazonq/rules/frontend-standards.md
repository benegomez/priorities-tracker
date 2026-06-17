---
description: "Estándares de desarrollo frontend para Priorities Tracker. Next.js 15 + TypeScript + shadcn/ui + TailwindCSS."
globs: apps/frontend/**/*
alwaysApply: false
---

# Frontend Standards — Priorities Tracker

## Stack Oficial

- Next.js 15 (App Router)
- TypeScript
- shadcn/ui (componentes)
- TailwindCSS (estilos)
- TanStack Query (data fetching y server state)
- Zustand (local/UI state)
- Zod (validación de formularios)
- Vitest + Testing Library (unit/component tests)
- Playwright (E2E)

---

## Estructura de Proyecto

```
src/
├── app/                  # Next.js App Router
│   ├── auth/
│   ├── employee/
│   ├── manager/
│   └── admin/
├── features/             # Módulos por dominio de negocio
│   ├── auth/
│   ├── users/
│   ├── teams/
│   ├── projects/
│   ├── priorities/
│   ├── tasks/
│   ├── checkins/
│   ├── checkouts/
│   ├── crs/
│   ├── reports/
│   └── ai/
├── components/           # Componentes reutilizables
│   ├── ui/               # shadcn/ui base
│   ├── layout/
│   ├── forms/
│   ├── tables/
│   └── charts/
├── hooks/                # Custom hooks globales
├── services/             # Clientes API
│   ├── api-client.ts
│   ├── auth-service.ts
│   ├── priority-service.ts
│   └── crs-service.ts
├── store/                # Zustand stores
│   ├── auth-store.ts
│   └── ui-store.ts
├── lib/                  # Utilidades puras
├── types/                # TypeScript interfaces globales
├── providers/
├── styles/
└── tests/
```

---

## Reglas Obligatorias

### Componentes
- Componentes funcionales siempre — sin clases
- `function` keyword, no `const` para componentes exportados
- Named exports en todos los componentes
- Interfaces TypeScript sobre `type` para props

### Organización
- Lógica de negocio en `features/`, no en `components/`
- `components/` solo para UI genérica reutilizable
- Directorios en `kebab-case`

### Data Fetching
- TanStack Query para todo estado del servidor (fetch, cache, invalidation)
- `useQuery` para lectura, `useMutation` para escritura
- Zustand solo para estado UI/local (modales, filtros, selecciones temporales)
- Minimizar `useEffect` — preferir RSC y TanStack Query
- Minimizar `use client` — solo cuando se necesita acceso a Web APIs

### Formularios
- Zod para definición de schemas de validación
- `useActionState` o `react-hook-form` con Zod resolver
- Errores de formulario siempre tipados

### Manejo de Errores
- Early returns para condiciones de error
- Error Boundaries con `error.tsx` y `global-error.tsx`
- Errores esperados como valores de retorno (no `try/catch` en Server Actions)
- Mensajes de error amigables para el usuario desde `services/`

### Accesibilidad
- Objetivo mínimo: WCAG 2.1 AA
- HTML semántico
- Navegación por teclado
- Compatibilidad con lectores de pantalla

### Performance
- Imágenes en WebP con lazy loading
- Dynamic imports para componentes no críticos
- Wrapping de componentes cliente en `Suspense` con fallback

---

## Convenciones de Nomenclatura

| Elemento | Convención |
|---|---|
| Componentes | `PascalCase` — `CheckInForm.tsx` |
| Custom hooks | `camelCase` con `use` — `useCheckIn.ts` |
| Directorios | `kebab-case` — `checkin-flow/` |
| Servicios / utils | `camelCase` — `priorityService.ts` |
| Interfaces | `PascalCase` — `CheckInFormProps` |
| Constantes | `UPPER_SNAKE_CASE` |

---

## Referencias

- [docs/07-Iteracion01-UX-Foundations/frontend-architecture.md](../../docs/07-Iteracion01-UX-Foundations/frontend-architecture.md)
- [docs/07-Iteracion01-UX-Foundations/frontend-folder-structure.md](../../docs/07-Iteracion01-UX-Foundations/frontend-folder-structure.md)
- [docs/07-Iteracion01-UX-Foundations/tanstack-query-strategy.md](../../docs/07-Iteracion01-UX-Foundations/tanstack-query-strategy.md)
- [docs/07-Iteracion01-UX-Foundations/state-management.md](../../docs/07-Iteracion01-UX-Foundations/state-management.md)
- [docs/02-arquitectura/ADR/ADR-007-Frontend-Technology-Stack-Enterprise-Final.md](../../docs/02-arquitectura/ADR/ADR-007-Frontend-Technology-Stack-Enterprise-Final.md)
