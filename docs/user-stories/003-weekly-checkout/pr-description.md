# Pull Request — US-003 Weekly Check-Out

**URL:** https://github.com/benegomez/priorities-tracker/pull/new/feature/003-weekly-checkout

**Base:** `main`
**Branch:** `feature/003-weekly-checkout`

---

## Título

```
feat: US-003 Weekly Check-Out
```

## Resumen

Implementación completa del flujo de cierre semanal (Check-Out). Permite al colaborador marcar prioridades y tareas como completadas, agregar notas/aprendizajes, y enviar el cierre. El submit transiciona estados atómicamente y prepara el terreno para el cálculo del CRS.

## Cambios

### Fase 1 — Database
- Tabla `check_outs` con partial unique index (BR-002)
- Tabla `crs_scores` (lista para módulo CRS futuro)
- ALTER `priorities` y `tasks`: columna `completed_in_checkout`

### Fase 2 — Backend
- Módulo `checkout` con 5 endpoints y 5 use cases
- Submit atómico: prioridades → completed/carried_over, tareas → completed/cancelled
- CRS best-effort (log + TODO)
- Prioridades retornan tareas anidadas con flag `completed`
- 7 unit tests passing

### Fase 3 — Frontend
- Flujo completo: crear checkout → marcar prioridades/tareas → notas → submit → summary
- Componentes: CheckOutForm, CheckOutPriorityCard (con tareas), CheckOutTaskItem, CheckOutNotes, CheckOutSummary, SubmitCheckOutButton
- Check-Out agregado al menú de navegación employee
- Summary calcula correctamente tasks_total/tasks_completed

### Fixes incluidos
- LoginForm: previene submit nativo (credenciales ya no aparecen en URL)
- useLogin: usa window.location.href para redirect correcto con cookies
- apiPatch helper agregado al API client

## Nivel de Riesgo

**Critical** — Módulo checkout es trigger del CRS y cierre del ciclo semanal

## Business Rules Validadas

| BR | Descripción | Validación |
|---|---|---|
| BR-002 | Un checkout por semana por empleado | Partial unique index + use case |
| BR-006 | Prioridades no completadas → carried_over | Submit use case |
| BR-007 | Tareas no completadas → cancelled | Submit use case |
| BR-008 | No puede cerrarse prioridad inexistente | Validation in mark_priority |
| BR-009 | CRS se calcula al submit | Best-effort post-commit |
| BR-013 | Empleado solo accede a sus datos | Ownership check |
| BR-016 | Aislamiento multi-tenant | organization_id from JWT |

## Evidencia de Tests

- Backend: 63 passed, 2 skipped (all modules)
- Frontend: 47/47 tests passing
- Build: `npm run build` sin errores
- Functional: flujo completo verificado via curl y UI
