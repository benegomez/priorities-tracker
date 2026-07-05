---
story: 005-checkin-detail-edit
status: pending
branch: feature/005-checkin-detail-edit
risk_level: High
complexity: M
created: 2026-07-05
---

# Plan de Implementación — US-005: Check-In Detail View & Edit

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Backend | Modificar 3 use cases + schemas para soportar edición post-submit |
| 2 | Frontend | Refactor página checkin + 4 nuevos componentes |

**Branch único:** `feature/005-checkin-detail-edit`
**Commits:** secuenciales por fase (`feat(checkin):`, `feat(fe):`)

---

## Fase 1 — Backend ✅

### 1.1 Schemas — Agregar prioridades con tareas al response

- [ ] Crear `CheckInTaskItem` schema en `modules/checkin/api/schemas.py`:
  - [ ] Campos: `id`, `title`, `status`
- [ ] Crear `CheckInPriorityItem` schema:
  - [ ] Campos: `id`, `title`, `description`, `priority_level`, `status`, `tasks: list[CheckInTaskItem]`
- [ ] Modificar `CheckInResponse`:
  - [ ] Agregar `priorities: list[CheckInPriorityItem] = []`

### 1.2 Router — GET /checkins/current con prioridades y tareas

- [ ] Crear helper `_load_priorities_for_checkin(session, checkin_id, organization_id)`:
  - [ ] Query prioridades del checkin
  - [ ] Query tareas agrupadas por prioridad (un solo query con ANY)
  - [ ] Retornar lista de `CheckInPriorityItem` con tareas anidadas
- [ ] Modificar endpoint `get_current_checkin`:
  - [ ] Llamar helper y agregar `priorities` al response

### 1.3 Use Case — Permitir agregar prioridades a checkin submitted

- [ ] Modificar `modules/priorities/application/commands/create_priority.py`:
  - [ ] Cambiar validación: permitir `status in ("draft", "submitted")` (no solo `draft`)
  - [ ] Agregar validación: verificar que NO existe checkout para la misma semana/empleado
  - [ ] Si existe checkout → `BusinessRuleViolation("Check-In is locked by an existing Check-Out")`

### 1.4 Use Case — Permitir re-submit

- [ ] Modificar `modules/checkin/domain/entities/checkin.py`:
  - [ ] Método `submit()`: permitir desde `draft` o `submitted`
- [ ] Modificar `modules/checkin/application/commands/submit_checkin.py`:
  - [ ] Si status actual es `submitted` (re-submit):
    - [ ] Solo transicionar prioridades con `status = 'draft'` a `planned`
    - [ ] No afectar prioridades ya en `planned` o posteriores
  - [ ] Si status actual es `draft` (primer submit):
    - [ ] Comportamiento existente (transicionar todas a `planned`)
  - [ ] Actualizar `submitted_at` en ambos casos

### 1.5 Tests — Unit

- [ ] `test_create_priority_allows_submitted_checkin`
- [ ] `test_create_priority_raises_409_when_checkout_exists`
- [ ] `test_submit_checkin_resubmit_transitions_only_draft_priorities`
- [ ] `test_submit_checkin_resubmit_updates_submitted_at`
- [ ] `test_submit_checkin_resubmit_does_not_affect_planned_priorities`

### 1.6 Tests — Integration

- [ ] `test_endpoint_post_priority_returns_201_on_submitted_checkin`
- [ ] `test_endpoint_post_priority_returns_409_when_checkout_exists`
- [ ] `test_endpoint_submit_resubmit_returns_200`
- [ ] `test_endpoint_get_current_returns_priorities_with_tasks`

### 1.7 Verificación Backend

- [ ] Todos los tests existentes siguen pasando
- [ ] Nuevos tests pasan
- [ ] `POST /priorities` funciona con checkin en submitted
- [ ] `POST /priorities` retorna 409 si existe checkout
- [ ] `POST /checkins/{id}/submit` re-submit funciona
- [ ] `GET /checkins/current` retorna prioridades con tareas

### 1.8 Commit

```
feat(checkin): allow adding priorities to submitted check-in and re-submit

- create_priority: accept submitted check-in, block if checkout exists
- submit_checkin: allow re-submit, only transition draft priorities
- GET /current: return priorities with nested tasks
```

---

## Fase 2 — Frontend ✅

### 2.1 Hook — useResubmitCheckIn

- [ ] Crear `features/checkins/hooks/useResubmitCheckIn.ts`:
  - [ ] Reutiliza `submitCheckIn(id)` del service existente
  - [ ] Invalida `["checkins", "current"]` on success

### 2.2 Componente — CheckInLockedBanner

- [ ] Crear `features/checkins/components/CheckInLockedBanner.tsx`:
  - [ ] Icono 🔒 + mensaje de bloqueo
  - [ ] Estilo: `bg-orange-50 border-orange text-orange`
  - [ ] `role="alert"`

### 2.3 Componente — CheckInPriorityCard

- [ ] Crear `features/checkins/components/CheckInPriorityCard.tsx`:
  - [ ] Título + badge nivel + badge estado
  - [ ] Lista de tareas con status icon
  - [ ] `TaskForm` inline (solo si `editable` prop es true)
  - [ ] Badge "Nueva" si `priority.status === "draft"`

### 2.4 Componente — ResubmitButton

- [ ] Crear `features/checkins/components/ResubmitButton.tsx`:
  - [ ] Solo visible si `newPrioritiesCount > 0`
  - [ ] AlertDialog: "¿Actualizar tu Check-In con X nueva(s) prioridad(es)?"
  - [ ] Llama `useResubmitCheckIn` on confirm
  - [ ] Toast éxito on success

### 2.5 Componente — CheckInDetail

- [ ] Crear `features/checkins/components/CheckInDetail.tsx`:
  - [ ] Props: `checkin`, `editable`, `onPriorityCreated`, `onTaskCreated`
  - [ ] Header: título + badge (Enviado / Bloqueado 🔒) + fecha envío
  - [ ] Si locked: `CheckInLockedBanner`
  - [ ] Lista de `CheckInPriorityCard` para cada prioridad
  - [ ] Si editable: `PriorityForm` expandible (toggle show/hide)
  - [ ] Si editable + hay prioridades draft: `ResubmitButton`

### 2.6 Refactor — Página /employee/checkin

- [ ] Modificar `app/(authenticated)/employee/checkin/page.tsx`:
  - [ ] Agregar `useCurrentCheckOut()` para detectar bloqueo
  - [ ] Cuando `submitted + no checkout` → renderizar `CheckInDetail` con `editable=true`
  - [ ] Cuando `submitted + checkout existe` → renderizar `CheckInDetail` con `editable=false`
  - [ ] Cuando `draft` → mantener vista de construcción existente
  - [ ] Cuando no existe → mantener `CheckInForm` existente
  - [ ] Tracking de nuevas prioridades/tareas via state local (patrón existente)

### 2.7 Tests — Component

- [ ] `test_CheckInDetail_renders_priorities_with_tasks`
- [ ] `test_CheckInDetail_shows_submitted_date`
- [ ] `test_CheckInDetail_shows_add_priority_button_when_editable`
- [ ] `test_CheckInDetail_hides_add_buttons_when_locked`
- [ ] `test_CheckInPriorityCard_renders_title_level_status`
- [ ] `test_CheckInPriorityCard_shows_task_form_when_editable`
- [ ] `test_CheckInPriorityCard_shows_new_badge_for_draft`
- [ ] `test_CheckInLockedBanner_renders_message`
- [ ] `test_ResubmitButton_visible_when_new_priorities_exist`
- [ ] `test_ResubmitButton_hidden_when_no_new_priorities`
- [ ] `test_ResubmitButton_shows_confirmation_dialog`
- [ ] `test_page_shows_locked_view_when_checkout_exists`

### 2.8 Verificación Frontend

- [ ] `npm run build` sin errores
- [ ] `npm test` — todos los tests pasan
- [ ] Vista detalle muestra prioridades con tareas
- [ ] Se puede agregar prioridad a checkin submitted
- [ ] Se puede agregar tarea a prioridad existente
- [ ] Re-submit funciona y actualiza la vista
- [ ] Vista bloqueada cuando existe checkout
- [ ] Responsive verificado

### 2.9 Commits

```
feat(checkin): add CheckInDetail, CheckInPriorityCard, ResubmitButton components
feat(checkin): refactor checkin page with detail view and edit mode
test(fe): add component tests for checkin detail and edit flow
```

---

## Gate Final — PR

- [ ] Todos los tests pasan (backend + frontend)
- [ ] `npm run build` sin errores
- [ ] Flujo verificado: submitted → agregar prioridad → re-submit → planned
- [ ] Flujo verificado: submitted + checkout → bloqueado
- [ ] No se pueden eliminar/modificar prioridades existentes
- [ ] Tests existentes no se rompen
- [ ] PR creado con resumen y evidencia

---

## Orden de Ejecución

```
/develop-plan be    → Fase 1 (backend modifications)
/develop-plan fe    → Fase 2 (frontend refactor)
/git-flow pr        → PR único con las 2 fases
```
