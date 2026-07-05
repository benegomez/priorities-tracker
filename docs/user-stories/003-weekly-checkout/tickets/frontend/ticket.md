---
status: done
type: frontend
story: docs/user-stories/003-weekly-checkout/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Critical
complexity: L
---

# [FE] US-003 — Weekly Check-Out UI

## Objetivo

Implementar el flujo de UI que permite al colaborador cerrar su semana: ver sus prioridades y tareas, marcar las completadas, agregar notas/aprendizajes, y enviar el Check-Out. El flujo debe ser completable en menos de 5 minutos (NFR-010).

## Scope

Next.js App Router, features/checkouts, TanStack Query, Zod, shadcn/ui + design system existente.

## Dependencia

Endpoints backend disponibles y respondiendo correctamente (ticket BE mergeado).

---

## Contrato API Consumido

| Método | Endpoint | Propósito |
|---|---|---|
| `GET` | `/api/v1/checkouts/current` | Obtener checkout activo (o 404) |
| `POST` | `/api/v1/checkouts` | Crear checkout (carga prioridades del checkin) |
| `PATCH` | `/api/v1/checkouts/{id}/priorities/{pid}` | Marcar prioridad completada |
| `PATCH` | `/api/v1/checkouts/{id}/tasks/{tid}` | Marcar tarea completada |
| `POST` | `/api/v1/checkouts/{id}/submit` | Enviar checkout |

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  app/(authenticated)/employee/checkout/
    page.tsx                              - CREATE (página principal)
    loading.tsx                           - CREATE
    error.tsx                             - CREATE

  features/checkouts/
    components/
      CheckOutForm.tsx                    - CREATE (botón crear checkout)
      CheckOutStatus.tsx                  - CREATE (badge draft/submitted)
      CheckOutPriorityCard.tsx            - CREATE (card con checkbox + tasks)
      CheckOutTaskItem.tsx                - CREATE (checkbox inline)
      CheckOutNotes.tsx                   - CREATE (textarea notas + aprendizajes)
      CheckOutSummary.tsx                 - CREATE (resumen post-submit)
      SubmitCheckOutButton.tsx            - CREATE (confirmación modal)
    hooks/
      useCurrentCheckOut.ts               - CREATE (useQuery)
      useCreateCheckOut.ts                - CREATE (useMutation)
      useMarkPriority.ts                  - CREATE (useMutation)
      useMarkTask.ts                      - CREATE (useMutation)
      useSubmitCheckOut.ts                - CREATE (useMutation)
    schemas/
      checkout-schema.ts                  - CREATE (Zod)
    services/
      checkout-service.ts                 - CREATE (API client)

  config/navigation.ts                    - MODIFY (agregar Check-Out al menú employee)
```

---

## Flujo de UI

```
/employee/checkout
    ↓ useCurrentCheckOut()
    ├── 404 (no existe) → CheckOutForm
    │     → Verifica si hay checkin submitted
    │     → POST /api/v1/checkouts (con checkin_id)
    │     → Invalidar query → re-render con checkout en draft
    │
    └── 200 (existe, status=draft) → Vista de cierre
          ├── Lista de CheckOutPriorityCards
          │     ├── Checkbox para marcar prioridad completada
          │     │     → PATCH /api/v1/checkouts/{id}/priorities/{pid}
          │     └── CheckOutTaskItems con checkboxes
          │           → PATCH /api/v1/checkouts/{id}/tasks/{tid}
          │
          ├── CheckOutNotes (textarea notas + lessons_learned)
          │
          └── SubmitCheckOutButton
                → AlertDialog confirmación
                → POST /api/v1/checkouts/{id}/submit
                → Mostrar CheckOutSummary
                → Redirect a /employee/dashboard

    └── 200 (existe, status=submitted) → Vista read-only con CheckOutSummary
```

---

## Componentes UI

| Componente | Elementos | Comportamiento |
|---|---|---|
| `CheckOutForm` | Button | Crea checkout si hay checkin submitted |
| `CheckOutStatus` | Badge | draft / submitted |
| `CheckOutPriorityCard` | Card, Checkbox, Badge, TaskList | Prioridad con toggle completada + tareas anidadas con checkboxes ✅ |
| `CheckOutTaskItem` | Checkbox, text | Toggle tarea completada inline (PATCH /tasks/{id}) ✅ |
| `CheckOutNotes` | Textarea × 2 | Notas generales + lecciones aprendidas |
| `CheckOutSummary` | Card con stats | priorities completed/carried, tasks completed (calculado desde datos) ✅ |
| `SubmitCheckOutButton` | Button, AlertDialog | Confirmación modal |

---

## Manejo de Errores

| Error API | Comportamiento UI |
|---|---|
| `409` crear checkout (BR-002) | Toast: "Ya tienes un Check-Out para esta semana" |
| `409` crear checkout (checkin not submitted) | Toast: "Primero debes enviar tu Check-In" |
| `409` submit (already submitted) | Toast: "El Check-Out ya fue enviado" |
| `403` | Toast: "No tienes permisos" |
| `401` | Redirect a `/auth/login` |

---

## Navegación

Agregar al menú employee en `config/navigation.ts`:

```typescript
// En el grupo "Mi Semana":
{ label: "Check-Out", href: "/employee/checkout", icon: CheckSquare }
```

---

## Tests Requeridos

### Component Tests (vitest + @testing-library/react)

- [ ] `test_CheckOutForm_renders_create_button`
- [ ] `test_CheckOutForm_shows_error_when_no_checkin`
- [ ] `test_CheckOutPriorityCard_renders_with_checkbox`
- [ ] `test_CheckOutPriorityCard_toggles_completed`
- [ ] `test_CheckOutPriorityCard_renders_tasks_with_checkboxes`
- [ ] `test_CheckOutTaskItem_renders_checkbox_and_title`
- [ ] `test_CheckOutTaskItem_toggles_completed`
- [ ] `test_CheckOutNotes_renders_textareas`
- [ ] `test_CheckOutSummary_renders_stats_with_tasks`
- [ ] `test_SubmitCheckOutButton_shows_confirmation`
- [ ] `test_checkout_page_shows_readonly_when_submitted`

### Schema Tests

- [ ] `test_checkout_schema_validates_checkin_id`
- [ ] `test_submit_schema_accepts_null_notes`

---

## Accesibilidad (WCAG 2.1 AA)

- [ ] Checkboxes con labels asociados
- [ ] Estados completado/pendiente visualmente distintos
- [ ] AlertDialog navegable por teclado
- [ ] `aria-live` en estados loading/error/success
- [ ] Focus management en formularios

---

## Git Branch

`feature/003-weekly-checkout`
