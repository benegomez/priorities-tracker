---
story: 005-checkin-detail-edit
status: done
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

- [x] Crear `CheckInTaskItem` schema en `modules/checkin/api/schemas.py`
- [x] Crear `CheckInPriorityItem` schema con `phase_name`, `project_name`, `tasks`
- [x] Modificar `CheckInResponse`: agregar `priorities: list[CheckInPriorityItem]`

### 1.2 Router — GET /checkins/current con prioridades y tareas

- [x] Crear helper `_load_priorities_with_tasks` con JOIN a project_phases y projects
- [x] Modificar endpoint `get_current_checkin`: retorna prioridades con tareas anidadas

### 1.3 Use Case — Permitir agregar prioridades a checkin submitted

- [x] Modificar `create_priority.py`: permitir `status in ("draft", "submitted")`
- [x] Agregar validación: verificar que NO existe checkout para la semana
- [x] Si existe checkout → `BusinessRuleViolation("Check-In is locked...")`

### 1.4 Use Case — Permitir re-submit

- [x] Modificar `checkin.py` entity: `submit()` permite desde `draft` o `submitted`
- [x] `transition_to_planned` ya filtra por `status = 'draft'` (sin cambios necesarios)
- [x] Re-submit actualiza `submitted_at`

### 1.5 Tests

- [x] `test_create_priority_allows_submitted_checkin`
- [x] `test_create_priority_raises_409_when_checkout_exists`
- [x] `test_create_priority_raises_when_checkin_closed`
- [x] `test_submit_checkin_resubmit_from_submitted`
- [x] `test_submit_checkin_raises_409_when_closed`
- [x] Todos los tests existentes siguen pasando (66 passed, 2 skipped)

### 1.6 Verificación

- [x] `POST /priorities` funciona con checkin en submitted
- [x] `POST /priorities` retorna 409 si existe checkout
- [x] `POST /checkins/{id}/submit` re-submit funciona
- [x] `GET /checkins/current` retorna prioridades con tareas, phase_name, project_name

---

## Fase 2 — Frontend ✅

### 2.1 Hook — useResubmitCheckIn

- [x] Crear `features/checkins/hooks/useResubmitCheckIn.ts`

### 2.2 Componente — CheckInLockedBanner

- [x] Crear `features/checkins/components/CheckInLockedBanner.tsx`

### 2.3 Componente — CheckInPriorityCard

- [x] Crear `features/checkins/components/CheckInPriorityCard.tsx`:
  - [x] Título + badge nivel + badge estado
  - [x] Proyecto → Fase (text-xs text-secondary)
  - [x] Descripción
  - [x] Lista de tareas con status icon
  - [x] TaskForm inline (solo si editable)
  - [x] Badge "Nueva" si status === "draft"

### 2.4 Componente — ResubmitButton

- [x] Crear `features/checkins/components/ResubmitButton.tsx`:
  - [x] Solo visible si newPrioritiesCount > 0
  - [x] AlertDialog confirmación
  - [x] Usa useResubmitCheckIn (sin redirect)

### 2.5 Refactor — Página /employee/checkin

- [x] Agregar `useCurrentCheckOut()` para detectar bloqueo
- [x] Draft → vista construcción con CheckInPriorityCard + PriorityForm + SubmitButton
- [x] Submitted + no checkout → detalle editable + "+ Agregar Prioridad" + ResubmitButton
- [x] Submitted + checkout → read-only con CheckInLockedBanner
- [x] Eliminado state local de prioridades (usa refetch del backend exclusivamente)
- [x] Fix: prioridades ya no aparecen duplicadas

### 2.6 Service types

- [x] `CheckInPriorityItem` con `phase_name`, `project_name`, `tasks[]`
- [x] `CheckInTaskItem` con `id`, `title`, `status`

### 2.7 Verificación

- [x] `npm run build` sin errores
- [x] `npm test` — 47/47 passing
- [x] Vista detalle muestra prioridades con fase/proyecto/descripción/tareas
- [x] Agregar prioridad a submitted funciona (sin duplicados)
- [x] Re-submit funciona
- [x] Vista bloqueada cuando existe checkout

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
