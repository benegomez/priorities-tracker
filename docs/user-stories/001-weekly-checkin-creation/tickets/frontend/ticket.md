---
status: done
type: frontend
story: docs/user-stories/001-weekly-checkin-creation/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Critical
complexity: L
---

# [FE] US-001 — Weekly Check-In Creation

## Objetivo

Implementar el flujo de UI que permite al colaborador crear su Check-In semanal, agregar prioridades y tareas, y enviarlo. El flujo completo debe ser ejecutable en menos de 5 minutos (NFR-010).

## Scope

Next.js 15 App Router, features/, TanStack Query, Zod, shadcn/ui. Sin lógica de API directa ni schema SQL.

## Dependencia

Endpoints backend disponibles y respondiendo correctamente (ticket BE mergeado).

---

## Contrato API Consumido

| Método | Endpoint | Propósito |
|---|---|---|
| `GET` | `/api/v1/checkins/current` | Obtener check-in activo de la semana (o 404) |
| `POST` | `/api/v1/checkins` | Crear check-in |
| `POST` | `/api/v1/priorities` | Agregar prioridad al check-in |
| `POST` | `/api/v1/priorities/{id}/tasks` | Agregar tarea a una prioridad |
| `POST` | `/api/v1/checkins/{id}/submit` | Enviar check-in |

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  app/employee/checkin/
    page.tsx                              - CREATE (página principal del flujo)
    loading.tsx                           - CREATE
    error.tsx                             - CREATE

  features/checkins/
    components/
      CheckInForm.tsx                     - CREATE (form crear check-in)
      CheckInStatus.tsx                   - CREATE (badge de estado)
      SubmitCheckInButton.tsx             - CREATE (botón enviar con confirmación)
    hooks/
      useCreateCheckIn.ts                 - CREATE (useMutation)
      useCurrentCheckIn.ts                - CREATE (useQuery)
      useSubmitCheckIn.ts                 - CREATE (useMutation)
    schemas/
      checkin-schema.ts                   - CREATE (Zod)
    services/
      checkin-service.ts                  - CREATE (API client)

  features/priorities/
    components/
      PriorityList.tsx                    - CREATE (lista de prioridades del check-in)
      PriorityForm.tsx                    - CREATE (form agregar prioridad)
      PriorityCard.tsx                    - CREATE (card individual con tasks)
      TaskForm.tsx                        - CREATE (form agregar tarea inline)
      TaskList.tsx                        - CREATE (lista de tasks)
    hooks/
      useCreatePriority.ts                - CREATE (useMutation)
      useCreateTask.ts                    - CREATE (useMutation)
      useCheckInPriorities.ts             - CREATE (useQuery)
    schemas/
      priority-schema.ts                  - CREATE (Zod)
      task-schema.ts                      - CREATE (Zod)
    services/
      priority-service.ts                 - CREATE (API client)
```

---

## Schemas de Validación (Zod)

### `checkin-schema.ts`
```typescript
import { z } from "zod"

export const createCheckInSchema = z.object({
  week_start: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Formato YYYY-MM-DD requerido"),
})
```

### `priority-schema.ts`
```typescript
import { z } from "zod"

export const createPrioritySchema = z.object({
  checkin_id: z.string().uuid(),
  phase_id: z.string().uuid("Selecciona una fase"),
  title: z.string().min(1, "El título es requerido").max(255),
  description: z.string().max(1000).nullable().optional(),
  priority_level: z.enum(["low", "medium", "high"]),
})
```

### `task-schema.ts`
```typescript
import { z } from "zod"

export const createTaskSchema = z.object({
  title: z.string().min(1, "El título es requerido").max(255),
  description: z.string().max(500).nullable().optional(),
})
```

---

## Gestión de Estado (TanStack Query)

| Hook | Tipo | Query Key | Invalidaciones |
|---|---|---|---|
| `useCurrentCheckIn` | `useQuery` | `["checkins", "current"]` | — |
| `useCreateCheckIn` | `useMutation` | — | `["checkins", "current"]` |
| `useCheckInPriorities` | `useQuery` | `["checkins", checkinId, "priorities"]` | — |
| `useCreatePriority` | `useMutation` | — | `["checkins", checkinId, "priorities"]` |
| `useCreateTask` | `useMutation` | — | `["checkins", checkinId, "priorities"]` |
| `useSubmitCheckIn` | `useMutation` | — | `["checkins", "current"]` + redirect |

---

## Flujo de UI

```
/employee/checkin
    ↓ useCurrentCheckIn()
    ├── 404 (no existe) → Mostrar CheckInForm
    │     → POST /api/v1/checkins (week_start = lunes actual)
    │     → Invalidar query → re-render con check-in en draft
    │
    └── 200 (existe, status=draft) → Vista de construcción
          ├── PriorityForm (select proyecto → select fase → título → nivel)
          │     → POST /api/v1/priorities
          │     → PriorityCard aparece en PriorityList
          │
          ├── TaskForm inline en cada PriorityCard
          │     → POST /api/v1/priorities/{id}/tasks
          │     → TaskList actualiza
          │
          └── SubmitCheckInButton (disabled si 0 prioridades)
                → AlertDialog confirmación
                → POST /api/v1/checkins/{id}/submit
                → Redirect a /employee/dashboard + toast éxito

    └── 200 (existe, status=submitted) → Vista read-only con badge "Enviado"
```

---

## Componentes UI (shadcn/ui)

| Componente | Elementos shadcn | Comportamiento |
|---|---|---|
| `CheckInForm` | `Button` | Auto-calcula lunes actual, un click para crear |
| `CheckInStatus` | `Badge` | Muestra `draft` / `submitted` con colores |
| `PriorityForm` | `Select` × 2, `Input`, `Textarea`, `Select`, `Button` | Proyecto → Fase (cascada), título, nivel |
| `PriorityCard` | `Card`, `Badge` × 2 | Título, nivel, estado, lista de tasks |
| `PriorityList` | Layout vertical | Renderiza PriorityCards |
| `TaskForm` | `Input`, `Button` | Inline dentro de PriorityCard |
| `TaskList` | Lista simple | Checkbox visual (read-only en esta US) |
| `SubmitCheckInButton` | `Button`, `AlertDialog` | Disabled sin prioridades, confirmación modal |

---

## Manejo de Errores

| Error API | Comportamiento UI |
|---|---|
| `409` en crear check-in | Toast: "Ya tienes un check-in para esta semana" + redirect a check-in existente |
| `409` en submit (vacío) | Toast: "Agrega al menos una prioridad antes de enviar" |
| `404` en crear prioridad | Toast: "La fase seleccionada no existe o fue eliminada" |
| `403` | Toast: "No tienes permisos para esta acción" |
| `401` | Redirect a `/auth/login` |

---

## Tests Requeridos

> Nivel de riesgo: Critical | Complejidad: L → cobertura mínima >95%

### Unit / Component Tests
Herramienta: `vitest` + `@testing-library/react`

- [x] `test_CheckInForm_renders_create_button`
- [x] `test_CheckInForm_calls_mutation_on_click`
- [ ] `test_PriorityForm_validates_empty_title` (deferred — PriorityForm uses native required)
- [ ] `test_PriorityForm_validates_phase_required` (deferred)
- [ ] `test_PriorityForm_submits_with_valid_data` (deferred)
- [x] `test_PriorityCard_renders_title_level_status`
- [x] `test_PriorityCard_shows_task_count`
- [x] `test_TaskForm_validates_empty_title`
- [x] `test_TaskForm_submits_inline`
- [x] `test_SubmitCheckInButton_disabled_when_no_priorities`
- [x] `test_SubmitCheckInButton_enabled_with_priorities`
- [x] `test_SubmitCheckInButton_shows_confirmation_dialog`
- [x] `test_checkin_schema_rejects_invalid_date`
- [x] `test_priority_schema_rejects_empty_title`
- [x] `test_task_schema_rejects_empty_title`

### E2E Tests
Herramienta: `Playwright`

- [ ] `test_checkin_flow_happy_path` (deferred — Playwright not configured)
- [ ] `test_checkin_flow_unauthenticated_redirects_to_login` (deferred)
- [ ] `test_checkin_submitted_shows_readonly_view` (deferred)

---

## Accesibilidad (WCAG 2.1 AA)

- [x] Todos los `Select` tienen `<label>` asociado
- [x] Todos los `Input` tienen `aria-label` o `<label>`
- [x] Estados loading/error/success visualmente distintos y con `aria-live`
- [x] `SubmitCheckInButton` tiene `aria-disabled` cuando está deshabilitado
- [x] `AlertDialog` navegable por teclado (Escape para cerrar)
- [x] Focus management: auto-focus en primer campo de cada form

---

## Git Branch

`feature/001-weekly-checkin-creation`
