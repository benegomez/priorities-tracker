---
id: US-005
title: Check-In Detail View & Edit
status: draft
priority: high
risk_level: High
complexity: M
created: 2026-07-05
---

# US-005 — Check-In Detail View & Edit

## [original]

**Como** colaborador individual,
**quiero** ver el detalle completo de mi Check-In semanal y poder agregar nuevas prioridades y tareas después de haberlo enviado,
**para** reflejar compromisos adicionales que surjan durante la semana sin necesidad de crear un nuevo Check-In.

### Contexto

Actualmente, una vez que el Check-In se envía (`submitted`), la vista es read-only y no permite modificaciones. En la práctica, durante la semana surgen nuevos compromisos que el colaborador necesita registrar. Esta US permite agregar nuevas prioridades y tareas al Check-In ya enviado, manteniendo la integridad de los compromisos originales (no se pueden eliminar ni modificar los existentes).

### Notas iniciales
- En estado `draft`: edición completa (agregar prioridades y tareas, enviar)
- En estado `submitted`: solo agregar nuevas prioridades y nuevas tareas a prioridades existentes
- Si ya existe un Check-Out para la semana, el Check-In se bloquea completamente (read-only)
- Las nuevas prioridades agregadas post-submit quedan en `draft` hasta que el usuario haga "re-submit"
- El re-submit transiciona las nuevas prioridades a `planned`

---

## [enhanced]

### User Journey

- **Usuario principal:** Colaborador Individual (employee)
- **Objetivo principal:** Ver el estado completo de su Check-In y poder agregar compromisos adicionales durante la semana
- **Flujo principal:**
  1. El colaborador accede a `/employee/checkin`
  2. El sistema carga el Check-In de la semana actual
  3. **Si no existe:** muestra botón "Crear Check-In" (flujo existente)
  4. **Si existe en `draft`:** muestra vista de construcción con formularios para agregar prioridades/tareas + botón enviar (flujo existente)
  5. **Si existe en `submitted`:**
     - Muestra detalle completo: prioridades con tareas, niveles, fecha de envío
     - Si NO existe Check-Out → muestra botón "Agregar Prioridades"
     - Si existe Check-Out → vista 100% read-only (badge "Bloqueado por Check-Out")
  6. Al click en "Agregar Prioridades" → se expande el formulario de agregar (inline, misma página)
  7. El colaborador agrega nuevas prioridades y/o tareas
  8. Click "Actualizar Check-In" → re-submit: nuevas prioridades pasan a `planned`
  9. Vista vuelve a read-only con los datos actualizados

---

### Business Value

- **Problema que resuelve:** Los compromisos semanales no son estáticos. Durante la semana surgen nuevas prioridades que el colaborador necesita registrar para mantener visibilidad con su manager. Sin esta funcionalidad, el Check-In queda desactualizado y el manager no tiene la imagen completa.
- **Beneficio esperado:** El colaborador mantiene su Check-In actualizado durante toda la semana. El manager siempre ve la lista completa de compromisos. El CRS al final de la semana refleja todos los compromisos reales, no solo los del lunes.

---

### Priority

**High** — Mejora significativa de usabilidad del flujo core. No es Critical porque el flujo básico ya funciona.

---

### Bounded Context

Commitment → Módulos: `checkin`, `priorities`

---

### Business Rules Aplicables

- **BR-001** — Un empleado solo puede tener un Check-In por semana (no cambia)
- **BR-003** — Una prioridad debe pertenecer a una fase
- **BR-004** — Una fase debe pertenecer a un proyecto activo
- **BR-005** — Una tarea debe pertenecer a una prioridad
- **BR-013** — Un empleado solo ve sus propias prioridades
- **BR-016** — Aislamiento multi-tenant
- **NUEVA** — No se pueden eliminar ni modificar prioridades/tareas existentes en un Check-In submitted
- **NUEVA** — No se puede editar un Check-In si ya existe un Check-Out para la misma semana

---

### Transiciones de Estado

```
Check-In submitted + nuevas prioridades agregadas:
  Nuevas prioridades: draft (mientras se edita)
  Al re-submit: nuevas prioridades → planned

Check-In con Check-Out existente:
  → Completamente bloqueado (read-only)
```

---

### Contrato API

**GET /api/v1/checkins/current** (ya existe)
- Debe retornar prioridades con tareas anidadas para la vista de detalle
- Debe incluir `priorities_count` actualizado

**POST /api/v1/checkins/{id}/submit** (ya existe)
- Re-submit: transiciona nuevas prioridades (status=draft) a `planned`
- No afecta prioridades ya en `planned` o estados posteriores

**POST /api/v1/priorities** (ya existe)
- Funciona igual, pero ahora se permite cuando check-in está en `submitted`
- Nuevas prioridades se crean con status `draft`

**POST /api/v1/priorities/{id}/tasks** (ya existe)
- Funciona igual para agregar tareas a prioridades existentes o nuevas

**GET /api/v1/checkouts/current** (ya existe)
- Se usa para determinar si el Check-In está bloqueado

**Cambios requeridos en backend:**
- `POST /priorities`: relajar validación — permitir agregar a check-in en `submitted` (no solo `draft`)
- `POST /checkins/{id}/submit`: permitir re-submit (transicionar solo prioridades en `draft`)
- `GET /checkins/current`: retornar prioridades con tareas anidadas

---

### Diseño de UX — Vista de Detalle (submitted)

```
┌─────────────────────────────────────────────────────┐
│ Check-In Semanal                    Badge: Enviado  │
│ Semana del 2026-07-05                               │
│ Enviado el 5 jul 2026                               │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ┌─ Prioridad 1 ──────────────────── [high] ──────┐ │
│ │ Implementar login                               │ │
│ │   ○ Crear endpoint                              │ │
│ │   ○ Agregar tests                               │ │
│ │   [+ Agregar tarea]  ← solo si editable         │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ┌─ Prioridad 2 ──────────────────── [medium] ────┐ │
│ │ Diseñar dashboard                               │ │
│ │   ○ Wireframes                                  │ │
│ │   [+ Agregar tarea]  ← solo si editable         │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ [+ Agregar Prioridad]  ← expande formulario     │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ─────────────────────────────────────────────────── │
│                          [Actualizar Check-In]      │
│                          ↑ solo visible si hay      │
│                            nuevas prioridades/tareas│
└─────────────────────────────────────────────────────┘
```

**Cuando está bloqueado por Check-Out:**
```
┌─────────────────────────────────────────────────────┐
│ Check-In Semanal          Badge: Bloqueado 🔒       │
│ Semana del 2026-07-05                               │
│ Enviado el 5 jul 2026                               │
│                                                     │
│ ⚠️ Este Check-In no puede editarse porque ya        │
│    existe un Check-Out para esta semana.            │
│                                                     │
│ [Prioridades en read-only sin botones de agregar]   │
└─────────────────────────────────────────────────────┘
```

**Principios de UX:**
- Inline editing (no navegar a otra página)
- El formulario de agregar prioridad se expande/colapsa con un click
- Agregar tarea es inline dentro de cada card (como ya funciona)
- Botón "Actualizar Check-In" solo aparece si hay cambios pendientes (nuevas prioridades en draft)
- Feedback inmediato: cada prioridad/tarea se muestra al crearla
- Sin confirmación modal para agregar (solo para el re-submit)

---

### Acceptance Criteria

**Escenario 1 — Vista de detalle muestra información completa**
```gherkin
Given un empleado con un Check-In submitted para la semana actual
When accede a /employee/checkin
Then ve el título "Check-In Semanal" con badge "Enviado"
  And ve la fecha de envío
  And ve todas las prioridades con sus tareas, niveles y estados
```

**Escenario 2 — Agregar prioridad a Check-In submitted**
```gherkin
Given un Check-In en estado submitted sin Check-Out existente
When el colaborador agrega una nueva prioridad
Then la prioridad se crea con status "draft"
  And aparece en la lista con indicador visual de "nueva"
  And el botón "Actualizar Check-In" se hace visible
```

**Escenario 3 — Agregar tarea a prioridad existente**
```gherkin
Given un Check-In submitted con prioridades existentes
When el colaborador agrega una tarea a una prioridad existente
Then la tarea se crea con status "pending"
  And aparece en la lista de tareas de esa prioridad
```

**Escenario 4 — Re-submit transiciona nuevas prioridades**
```gherkin
Given un Check-In submitted con 2 nuevas prioridades en draft
When el colaborador hace click en "Actualizar Check-In"
Then las 2 nuevas prioridades pasan a status "planned"
  And el submitted_at se actualiza
  And el botón "Actualizar Check-In" desaparece
```

**Escenario 5 — Check-In bloqueado por Check-Out**
```gherkin
Given un Check-In submitted Y un Check-Out existente para la misma semana
When el colaborador accede a /employee/checkin
Then ve la vista read-only con badge "Bloqueado 🔒"
  And NO ve botones de agregar prioridad ni tarea
  And ve un mensaje indicando que el Check-Out bloquea la edición
```

**Escenario 6 — No se pueden eliminar prioridades existentes**
```gherkin
Given un Check-In submitted con prioridades
When el colaborador está en modo edición
Then NO hay opción de eliminar ni modificar prioridades existentes
  And solo puede agregar nuevas prioridades y tareas
```

---

### Non-Functional Requirements

- **NFR-010 — Simplicity:** Agregar una prioridad adicional debe tomar menos de 1 minuto
- **NFR-011 — Accessibility:** Formularios inline accesibles por teclado

---

### Dependencies

- **Técnicas:**
  - US-001 (Check-In) — Endpoints existentes que se modifican
  - US-003 (Check-Out) — Para determinar si el Check-In está bloqueado
- **Funcionales:**
  - El backend debe permitir `POST /priorities` cuando check-in está en `submitted`
  - El backend debe permitir re-submit (solo transiciona prioridades en `draft`)
  - `GET /checkins/current` debe retornar prioridades con tareas

---

### Nivel de Riesgo

**High** — Modifica comportamiento de endpoints existentes (checkin submit, priorities create). Requiere Unit + Integration tests.

---

### Complejidad Estimada

**M**

| Factor | Detalle |
|---|---|
| Capas afectadas | Backend (modificar 2 use cases) + Frontend (refactor página checkin) |
| Endpoints | 0 nuevos, 3 modificados |
| Entidades | 0 nuevas |
| Business Rules | 2 nuevas restricciones + relajar 1 existente |
| Tests requeridos | Unit + Integration, cobertura >80% |

---

### Siguiente Paso

Ejecutar `/create-tickets 005-checkin-detail-edit`
