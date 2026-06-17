---
status: todo
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

Next.js 15 App Router, features/, TanStack Query, Zod, shadcn/ui. Sin schema SQL, sin lógica de API directa.

## Dependencia

Endpoints backend disponibles y respondiendo correctamente.

---

## Contrato API Consumido

```
POST /api/v1/checkins                     → crear check-in
POST /api/v1/priorities                   → agregar prioridad
POST /api/v1/priorities/{id}/tasks        → agregar tarea
POST /api/v1/checkins/{id}/submit         → enviar check-in
GET  /api/v1/checkins/current             → obtener check-in activo (si existe)
```

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
      useCreateCheckIn.ts                 - CREATE (mutation)
      useCurrentCheckIn.ts               - CREATE (query check-in activo)
      useSubmitCheckIn.ts                 - CREATE (mutation submit)
    schemas/
      checkin-schema.ts                   - CREATE (Zod)
    services/
      checkin-service.ts                  - CREATE

  features/priorities/
    components/
      PriorityList.tsx                    - CREATE (lista de prioridades del check-in)
      PriorityForm.tsx                    - CREATE (form agregar prioridad)
      PriorityCard.tsx                    - CREATE (card individual con tasks)
      TaskForm.tsx                        - CREATE (form agregar tarea inline)
      TaskList.tsx                        - CREATE (lista de tasks de una prioridad)
    hooks/
      useCreatePriority.ts                - CREATE (mutation)
      useCreateTask.ts                    - CREATE (mutation)
    schemas/
      priority-schema.ts                  - CREATE (Zod)
      task-schema.ts                      - CREATE (Zod)
    services/
      priority-service.ts                 - CREATE
```

---

## Schemas de Validación (Zod)

### `checkin-schema.ts`
```typescript
const createCheckInSchema = z.object({
  week_start: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Formato YYYY-MM-DD requerido"),
})
```

### `priority-schema.ts`
```typescript
const createPrioritySchema = z.object({
  checkin_id:     z.string().uuid(),
  phase_id:       z.string().uuid("Selecciona una fase"),
  title:          z.string().min(1, "El título es requerido").max(255),
  description:    z.string().max(1000).optional(),
  priority_level: z.enum(["low", "medium", "high", "critical"]),
})
```

### `task-schema.ts`
```typescript
const createTaskSchema = z.object({
  title: z.string().min(1, "El título es requerido").max(255),
  description: z.string().max(500).optional(),
})
```

---

## Gestión de Estado

- `useCurrentCheckIn` — `useQuery` para obtener check-in activo de la semana (si existe)
- `useCreateCheckIn` — `useMutation` con `onSuccess`: invalidar `["checkin", "current"]`
- `useCreatePriority` — `useMutation` con `onSuccess`: invalidar `["checkin", checkinId, "priorities"]`
- `useCreateTask` — `useMutation` con `onSuccess`: invalidar `["priorities", priorityId, "tasks"]`
- `useSubmitCheckIn` — `useMutation` con `onSuccess`: invalidar `["checkin", "current"]` + redirigir a dashboard

---

## Flujo de UI

```
/employee/checkin
    ↓ (si no hay check-in activo)
  Botón "Iniciar Check-In de la semana"
    → CreateCheckInForm (selecciona week_start automáticamente al lunes actual)
    → POST /api/v1/checkins
    ↓ (check-in en draft)
  Vista de Check-In en construcción
    → PriorityForm (selecciona proyecto → fase → título → nivel)
    → POST /api/v1/priorities
    → PriorityCard aparece en PriorityList
    → TaskForm inline en cada PriorityCard
    → POST /api/v1/priorities/{id}/tasks
    → TaskList actualiza debajo de la prioridad
    ↓ (al menos 1 prioridad)
  SubmitCheckInButton habilitado
    → Modal de confirmación: "¿Estás listo para enviar tu Check-In?"
    → POST /api/v1/checkins/{id}/submit
    → Redirección a /employee/dashboard con mensaje de éxito
```

---

## Componentes UI (shadcn/ui)

- `CheckInForm` — `Form`, `DatePicker` (semana actual pre-seleccionada), `Button`
- `PriorityForm` — `Form`, `Select` (proyecto), `Select` (fase), `Input` (título), `Textarea` (descripción), `Select` (nivel), `Button`
- `PriorityCard` — `Card`, `Badge` (estado), `Badge` (nivel), botón inline "Agregar tarea"
- `TaskForm` — `Input` inline + `Button` (agregar), diseño minimalista
- `SubmitCheckInButton` — `Button` (disabled si 0 prioridades), `AlertDialog` para confirmación

---

## Tests Requeridos

> Nivel de riesgo: Critical | Complejidad: L → cobertura mínima >95%

### Unit / Component Tests ✅
Herramienta: `vitest` + `@testing-library/react`

- [ ] `test_CheckInForm_renders_with_current_week_preselected`
- [ ] `test_CheckInForm_shows_validation_error_on_empty_submit`
- [ ] `test_PriorityForm_renders_without_errors`
- [ ] `test_PriorityForm_disables_phase_select_until_project_selected`
- [ ] `test_PriorityForm_shows_validation_error_on_empty_title`
- [ ] `test_PriorityCard_renders_title_level_and_status`
- [ ] `test_TaskForm_adds_task_inline_on_submit`
- [ ] `test_SubmitCheckInButton_disabled_when_no_priorities`
- [ ] `test_SubmitCheckInButton_enabled_when_at_least_one_priority`
- [ ] `test_SubmitCheckInButton_shows_confirmation_dialog`
- [ ] `test_checkin_schema_rejects_invalid_date_format`
- [ ] `test_priority_schema_rejects_empty_title`

### E2E Tests ✅
Herramienta: `Playwright`

- [ ] `test_checkin_flow_complete_happy_path`
  - Navegar a /employee/checkin
  - Crear check-in de la semana
  - Agregar 2 prioridades con sus fases
  - Agregar 1 tarea a cada prioridad
  - Enviar check-in
  - Verificar redirección a dashboard con estado submitted
- [ ] `test_checkin_flow_unauthenticated_redirects_to_login`

---

## Accesibilidad (NFR-011)

- [ ] Todos los `Select` tienen `<label>` asociado
- [ ] Todos los `Input` tienen `aria-label` o `<label>`
- [ ] Estados loading/error/success visualmente distintos
- [ ] `SubmitCheckInButton` tiene `aria-disabled` cuando está deshabilitado
- [ ] Confirmación dialog navegable por teclado

---

## Git Branch

`feature/001-weekly-checkin-creation-frontend`
