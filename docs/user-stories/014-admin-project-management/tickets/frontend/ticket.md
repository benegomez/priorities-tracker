---
status: pending
type: frontend
story: docs/user-stories/014-admin-project-management/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Medium
complexity: S
---

# [FE] US-014 — Admin Project Management Tests

## Objetivo

Agregar tests de componentes para el módulo de proyectos. Las páginas y componentes ya existen — este ticket cubre únicamente la cobertura de tests faltante.

## Contexto

El frontend de proyectos tiene:
- `/admin/projects/page.tsx` — lista de proyectos con formulario de creación
- `/admin/projects/[id]/page.tsx` — detalle con fases, miembros y transiciones de estado
- `features/projects/` — hooks, servicios y componente `UserSelect`
- **0 tests** de componentes para proyectos

## Scope

Solo crear `src/tests/project-management.test.tsx`. No modificar código existente.

---

## Archivo a Crear

```
apps/frontend/src/tests/
  project-management.test.tsx
```

---

## Tests Requeridos (8 tests)

### UserSelect component
- `UserSelect renders placeholder when no value` — muestra placeholder inicial
- `UserSelect renders user options` — lista usuarios en el select
- `UserSelect calls onChange when user selected` — dispara callback con user_id

### ProjectsPage (lista)
- `ProjectsPage shows empty state when no projects` — mensaje sin proyectos
- `ProjectsPage renders project list with status badge` — nombre y badge de estado

### ProjectDetailPage (detalle)
- `ProjectDetailPage renders project name and status` — encabezado correcto
- `ProjectDetailPage renders phases list` — lista de fases
- `ProjectDetailPage renders members list` — lista de participantes

---

## Patrón de Tests

Mismo patrón que `user-management.test.tsx` y `team-management.test.tsx`:
- `render` + `screen` de `@testing-library/react`
- Mocks con `vi.fn()`
- Sin TanStack Query wrapper — testear componentes puros con props directas

---

## Criterios de Aceptación

- [ ] 8 tests pasando
- [ ] 87+ tests totales frontend siguen pasando
- [ ] Build exitoso
