---
status: todo
type: frontend
story: docs/user-stories/005-checkin-detail-edit/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: High
complexity: M
---

# [FE] US-005 — Check-In Detail View & Edit

## Objetivo

Refactorizar la página `/employee/checkin` para mostrar el detalle completo del Check-In cuando está submitted, permitir agregar nuevas prioridades/tareas inline, y bloquear edición cuando existe un Check-Out.

## Scope

Refactor de la página existente + nuevos componentes. Sin nuevos endpoints (usa los existentes modificados).

## Dependencia

Ticket BE completado — endpoints modificados disponibles.

---

## Flujo de UI

```
/employee/checkin
    ↓ useCurrentCheckIn() + useCurrentCheckOut()
    │
    ├── 404 (no existe) → CheckInForm (crear) [sin cambios]
    │
    ├── status=draft → Vista de construcción [sin cambios]
    │
    ├── status=submitted + NO checkout →
    │     Vista detalle con edición inline:
    │     ├── Header: título + badge "Enviado" + fecha envío
    │     ├── Lista de prioridades existentes (read-only cards)
    │     │     └── Cada card tiene [+ Agregar tarea] inline
    │     ├── [+ Agregar Prioridad] → expande PriorityForm
    │     ├── Nuevas prioridades (cards con indicador "Nueva")
    │     └── [Actualizar Check-In] → re-submit (solo si hay nuevas)
    │
    └── status=submitted + checkout existe →
          Vista read-only bloqueada:
          ├── Header: título + badge "Bloqueado 🔒"
          ├── Mensaje: "No se puede editar, Check-Out existente"
          └── Lista de prioridades/tareas sin botones de agregar
```

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  app/(authenticated)/employee/checkin/
    page.tsx                              - REFACTOR (lógica condicional expandida)

  features/checkins/
    components/
      CheckInDetail.tsx                   - CREATE (vista detalle submitted)
      CheckInPriorityCard.tsx             - CREATE (card read-only con tareas + agregar tarea)
      CheckInLockedBanner.tsx             - CREATE (banner de bloqueo por checkout)
      ResubmitButton.tsx                  - CREATE (botón "Actualizar Check-In")
    hooks/
      useResubmitCheckIn.ts              - CREATE (useMutation para re-submit)
```

---

## Componentes

### CheckInDetail

Vista principal cuando check-in está en `submitted`:
- Header con badge "Enviado" y fecha de envío
- Lista de `CheckInPriorityCard` para prioridades existentes
- Sección de nuevas prioridades (si hay en draft)
- `PriorityForm` expandible para agregar nuevas
- `ResubmitButton` (visible solo si hay prioridades en draft)

### CheckInPriorityCard

Card individual de prioridad en la vista de detalle:
- Título, nivel (badge), estado (badge)
- Lista de tareas con status icon
- `TaskForm` inline para agregar tareas (solo si editable)
- Indicador visual "Nueva" para prioridades en `draft`

### CheckInLockedBanner

Banner informativo cuando el Check-In está bloqueado:
- Icono 🔒
- Mensaje: "Este Check-In no puede editarse porque ya existe un Check-Out para esta semana."
- Estilo: bg-orange-50, border-orange, text-orange

### ResubmitButton

Botón "Actualizar Check-In":
- Solo visible cuando hay prioridades nuevas (status=draft)
- AlertDialog de confirmación: "¿Actualizar tu Check-In con X nueva(s) prioridad(es)?"
- Al confirmar: llama `POST /checkins/{id}/submit`
- On success: invalidar queries, mostrar toast éxito

---

## Hook: useResubmitCheckIn

```typescript
// Reutiliza el endpoint existente POST /checkins/{id}/submit
// Invalida ["checkins", "current"] on success
```

---

## Lógica de la Página (refactor)

```typescript
export default function CheckInPage() {
  const { data: checkin } = useCurrentCheckIn();
  const { data: checkout } = useCurrentCheckOut(); // para detectar bloqueo

  // No existe → CheckInForm
  // Draft → vista construcción (existente)
  // Submitted + no checkout → CheckInDetail (editable)
  // Submitted + checkout existe → CheckInDetail (locked)
}
```

**Prop `editable`:** se pasa a `CheckInDetail` basado en la ausencia de checkout.

---

## Manejo de Errores

| Error API | Comportamiento UI |
|---|---|
| `409` en crear prioridad (checkout exists) | Toast: "No se puede agregar, ya existe un Check-Out" |
| `409` en re-submit | Toast: "Error al actualizar el Check-In" |
| `403` | Toast: "No tienes permisos" |

---

## Tests Requeridos

### Component Tests (vitest + @testing-library/react)

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

---

## Accesibilidad

- [ ] Formularios inline accesibles por teclado
- [ ] Badge "Nueva" con `aria-label`
- [ ] Banner de bloqueo con `role="alert"`
- [ ] `ResubmitButton` AlertDialog con `aria-modal`

---

## Criterios de Aceptación

- [ ] Vista detalle muestra todas las prioridades con tareas anidadas
- [ ] Vista detalle muestra fecha de envío
- [ ] Se puede agregar nueva prioridad a check-in submitted
- [ ] Se puede agregar tarea a prioridad existente
- [ ] Nuevas prioridades muestran indicador visual "Nueva"
- [ ] Botón "Actualizar Check-In" solo visible con prioridades en draft
- [ ] Re-submit transiciona nuevas prioridades a planned
- [ ] Vista bloqueada cuando existe Check-Out (sin botones de agregar)
- [ ] Banner de bloqueo visible con mensaje explicativo
- [ ] Responsive: funciona en mobile y desktop

---

## Git Branch

`feature/005-checkin-detail-edit`
