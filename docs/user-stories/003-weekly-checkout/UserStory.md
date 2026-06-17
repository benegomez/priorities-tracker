---
id: 003-weekly-checkout
persona: Colaborador Individual
fr: FR-022, FR-023, FR-024
bounded-context: Execution
status: draft
created: 2025-01-06
---

# US-003: Weekly Check-Out

## [original]

**Como** colaborador individual,
**quiero** registrar los resultados de mi semana marcando qué prioridades y tareas completé,
**para** cerrar el ciclo semanal de compromisos y dar a mi manager visibilidad real de lo que logré entregar.

### Contexto

Al final de cada semana, el colaborador necesita cerrar su ciclo de compromisos. Tiene prioridades que completó, otras que no pudo terminar y que deben continuar la próxima semana, y aprendizajes que vale la pena registrar. El manager necesita saber qué se cumplió realmente — no lo que se planeó — para tener una imagen objetiva del desempeño. Este cierre semanal es el insumo principal para calcular el CRS y para que los dashboards del manager muestren datos reales de cumplimiento.

### Notas iniciales
- Solo puede existir un Check-Out por empleado por semana (BR-002)
- Requiere un Check-In previo para la misma semana como prerequisito
- Las prioridades no completadas pueden continuar (carry-over) a la siguiente semana (BR-006)
- Las tareas completadas no se copian en carry-over (BR-007)
- El Check-Out alimenta directamente el cálculo del CRS (BR-009, BR-012)
- El Check-Out inicia en `draft` y se envía explícitamente (`submitted`)

---

## [enhanced]

### User Journey

- **Usuario principal:** Colaborador Individual (employee)
- **Objetivo principal:** Cerrar la semana en menos de 5 minutos registrando qué logró completar, qué continúa y qué aprendió, para que su manager tenga visibilidad real de resultados sin necesidad de una reunión de status
- **Flujo principal:**
  1. El colaborador accede al flujo de Check-Out al cierre de la semana
  2. El sistema carga las prioridades y tareas del Check-In de la semana actual
  3. El colaborador marca cada prioridad como `completed` o la deja sin marcar (pendiente)
  4. Marca las tareas completadas de cada prioridad
  5. Registra comentarios y lecciones aprendidas opcionales
  6. Revisa las prioridades no completadas y confirma cuáles pasan a carry-over
  7. Envía el Check-Out — queda en estado `submitted`
  8. El sistema dispara automáticamente el cálculo del CRS
  9. El manager visualiza los resultados reales del equipo en su dashboard

---

### Business Value

- **Problema que resuelve:** Sin cierre semanal, el manager no sabe qué se completó realmente versus lo que se planeó. Los compromisos quedan en el aire, el CRS no puede calcularse y la visibilidad de ejecución se pierde. El colaborador tampoco tiene un mecanismo para comunicar sus logros sin una reunión.
- **Beneficio esperado:** El colaborador comunica resultados reales en minutos. El manager obtiene la respuesta objetiva a "¿qué completó cada persona esta semana?". El CRS se calcula automáticamente, convirtiendo el cierre semanal en el motor de la métrica diferenciadora del producto.

---

### Priority

**Critical**
Es el segundo paso crítico de la cadena de valor. Sin Check-Out no hay datos de cumplimiento, sin cumplimiento no hay CRS, sin CRS no hay el diferenciador principal del producto ni el dashboard del manager tiene valor real.

---

### FR de Referencia

- **FR-022** — Check-Out Creation: Employees shall be able to complete weekly Check-Outs
- **FR-023** — Completion Tracking: Employees shall be able to mark priorities and tasks as completed
- **FR-024** — Continuity Management: The system shall support carry-over of unfinished priorities and tasks

---

### Bounded Context

Execution → Módulos: `checkout`, `priorities` (actualización de estado)

---

### Entidades Involucradas

- **WeeklyCheckOut:** `id`, `employee_id`, `organization_id`, `checkin_id`, `week_start`, `status` (`draft` → `submitted` → `closed`), `submitted_at`, `notes`, `lessons_learned`
- **Priority:** estado se actualiza a `completed` o `carried_over` al hacer submit del Check-Out
- **Task:** estado se actualiza a `completed` o `cancelled` (las no completadas no se arrastran — BR-007)
- **WeeklyCheckIn:** debe existir en estado `submitted` para la misma `week_start` — invariante de dominio

---

### Business Rules Aplicables

- **BR-002** — Un empleado solo puede tener un Check-Out por semana → `409 Conflict`
- **BR-006** — Una prioridad puede continuar (carry-over) a la siguiente semana con estado `carried_over`
- **BR-007** — Las tareas completadas no se copian automáticamente en carry-over; solo se arrastran las tareas pendientes
- **BR-008** — No puede cerrarse una prioridad inexistente
- **BR-009** — El CRS se calcula automáticamente al hacer submit del Check-Out
- **BR-012** — El CRS se recalcula siempre que existe un Check-Out
- **BR-013** — Un empleado solo ve y modifica sus propias prioridades
- **BR-016** — Ningún usuario puede acceder a datos de otra organización
- **BR-017** — Todos los agregados pertenecen a una organización

---

### Transiciones de Estado

```
WeeklyCheckOut:  (nuevo) → Draft → Submitted

Priority al submit del Check-Out:
  InProgress/Planned + marcada completada  → Completed
  InProgress/Planned + NO marcada          → CarriedOver

Task al submit del Check-Out:
  Pending/InProgress + marcada completada  → Completed
  Pending/InProgress + NO marcada          → Cancelled (BR-007: no se arrastra)
```

**Invariante:** No puede existir un Check-Out sin un Check-In `submitted` para la misma semana y empleado.

---

### Contrato API Preliminar

**POST /api/v1/checkouts**
Crea un Check-Out en estado `draft` cargando las prioridades del Check-In activo.

```
Request:
{
  "checkin_id": "uuid"
}

Response 201:
{
  "id":         "uuid",
  "checkin_id": "uuid",
  "employee_id":     "uuid",
  "organization_id": "uuid",
  "week_start":  "2025-01-06",
  "status":      "draft",
  "priorities":  [
    {
      "id":       "uuid",
      "title":    "string",
      "status":   "planned",
      "completed": false,
      "tasks": [
        { "id": "uuid", "title": "string", "completed": false }
      ]
    }
  ],
  "created_at": "..."
}

Errors:
  401, 403,
  404 — checkin_id no encontrado
  409 — BR-002: ya existe check-out para esta semana
  409 — Check-In no está en estado submitted
```

---

**PATCH /api/v1/checkouts/{id}/priorities/{priority_id}**
Marca o desmarca una prioridad como completada durante el flujo de Check-Out.

```
Request:
{
  "completed": true
}

Response 200:
{
  "priority_id": "uuid",
  "completed":   true
}

Errors: 401, 403, 404, 409 (checkout ya submitted)
```

---

**PATCH /api/v1/checkouts/{id}/tasks/{task_id}**
Marca o desmarca una tarea como completada durante el flujo de Check-Out.

```
Request:
{
  "completed": true
}

Response 200:
{
  "task_id":   "uuid",
  "completed": true
}

Errors: 401, 403, 404, 409 (checkout ya submitted)
```

---

**POST /api/v1/checkouts/{id}/submit**
Envía el Check-Out. Actualiza estados de prioridades y tareas. Dispara cálculo de CRS.

```
Request:
{
  "notes":            "string | null",
  "lessons_learned":  "string | null"
}

Response 200:
{
  "id":           "uuid",
  "status":       "submitted",
  "submitted_at": "2025-01-10T18:00:00Z",
  "summary": {
    "priorities_total":     3,
    "priorities_completed": 2,
    "priorities_carried":   1,
    "tasks_total":          5,
    "tasks_completed":      4
  }
}

Errors:
  401, 403,
  404 — checkout no encontrado
  409 — ya fue submitted previamente
```

---

### Acceptance Criteria

**Escenario 1 — Colaborador crea un Check-Out exitosamente**
```gherkin
Given un empleado con un Check-In en estado "submitted" para la semana actual
  And no tiene Check-Out creado para esa semana
When envía POST /api/v1/checkouts con el checkin_id correspondiente
Then el sistema retorna 201 con el Check-Out en estado "draft"
  And el response incluye la lista de prioridades y tareas del Check-In
  And el Check-Out queda asociado al organization_id del token
```

**Escenario 2 — No se permite Check-Out sin Check-In previo**
```gherkin
Given un empleado sin Check-In submitted para la semana actual
When intenta crear un Check-Out
Then el sistema retorna 409 Conflict
  And el mensaje indica que se requiere un Check-In submitted previamente
```

**Escenario 3 — No se permite duplicar Check-Out (BR-002)**
```gherkin
Given un empleado con un Check-Out ya existente para la semana del 2025-01-06
When intenta crear un segundo Check-Out para la misma semana
Then el sistema retorna 409 Conflict
  And el mensaje de error referencia BR-002
```

**Escenario 4 — Prioridades no completadas van a carry-over (BR-006)**
```gherkin
Given un Check-Out en draft con 3 prioridades
  And el colaborador marca 2 como completadas y deja 1 sin marcar
When envía POST /api/v1/checkouts/{id}/submit
Then las 2 prioridades marcadas quedan en estado "completed"
  And la prioridad sin marcar queda en estado "carried_over"
  And el summary retorna priorities_completed=2, priorities_carried=1
```

**Escenario 5 — Tareas no completadas se cancelan, no se arrastran (BR-007)**
```gherkin
Given una prioridad con 3 tareas: 2 completadas y 1 pendiente
  And el colaborador envía el Check-Out
When el sistema procesa el submit
Then las 2 tareas completadas quedan en estado "completed"
  And la tarea pendiente queda en estado "cancelled"
  And NO se crea una tarea nueva en el siguiente ciclo automáticamente
```

**Escenario 6 — Submit dispara cálculo de CRS (BR-009, BR-012)**
```gherkin
Given un Check-Out con resultados de cumplimiento registrados
When el colaborador envía POST /api/v1/checkouts/{id}/submit exitosamente
Then el sistema calcula automáticamente el CRS del empleado para esa semana
  And el CRS queda persistido con formula_version="v1.0"
  And el CRS NO puede ser modificado manualmente
```

**Escenario 7 — Empleado solo puede hacer Check-Out de sus propios datos (BR-013)**
```gherkin
Given el empleado B intenta crear un Check-Out usando el checkin_id del empleado A
When envía POST /api/v1/checkouts con ese checkin_id
Then el sistema retorna 403 Forbidden
  And no se crea ningún registro
```

---

### Non-Functional Requirements

- **NFR-001 — Authentication:** Todo endpoint de Check-Out requiere Bearer JWT válido
- **NFR-002 — Authorization:** Solo el empleado dueño del Check-In puede crear su Check-Out; validado desde el token
- **NFR-004 — Response Time:** Creación y submit del Check-Out deben responder en < 800ms (incluye disparo de cálculo CRS)
- **NFR-008 — Data Integrity:** Las transiciones de estado de prioridades y tareas deben ejecutarse en una única transacción atómica; si el cálculo del CRS falla, el submit del Check-Out no debe revertirse
- **NFR-009 — Auditability:** El evento `checkout.submitted` debe registrarse en el audit log con `user_id`, `organization_id`, `week_start`, `priorities_completed`, `priorities_carried` y `timestamp`
- **NFR-010 — Simplicity:** El flujo completo de Check-Out debe ser completable en menos de 5 minutos

---

### Dependencies

- **Técnicas:**
  - US-002 (Auth) — JWT válido con `employee_id`, `organization_id` y `role`
  - US-001 (Check-In) — Tablas `check_ins`, `priorities`, `tasks` deben existir con datos
  - Módulo `crs` — `SubmitCheckOutUseCase` dispara el cálculo del CRS mediante evento de dominio o llamada directa al servicio
  - Tabla `check_outs` debe existir (nueva migración Alembic)
- **Funcionales:**
  - El empleado debe tener un Check-In en estado `submitted` para la semana actual antes de poder crear el Check-Out
  - US-004 (CRS Calculation) se beneficia directamente de esta historia — el submit del Check-Out es su trigger

---

### Success Metrics

- **Check-Out Completion Rate:** Porcentaje de empleados que envían su Check-Out cada semana → target > 85%
- **North Star — Commitment Completion Rate:** El Check-Out es quien produce el dato real de `priorities_completed / priorities_committed` que alimenta esta métrica
- **CRS promedio del equipo:** Esta historia habilita el cálculo automático del CRS, sin el cual la métrica no puede existir

---

### Nivel de Riesgo

**Critical**
Módulo `checkout` es siempre Critical por definición (testing-standards.md). Es el trigger del CRS, el dato de cumplimiento real y el cierre del ciclo semanal completo.

---

### Complejidad Estimada

**L**

| Factor | Detalle |
|---|---|
| Capas afectadas | DB + Backend + Frontend (3 capas completas) |
| Endpoints | 4 endpoints (POST checkout, PATCH priority, PATCH task, POST submit) |
| Entidades | 1 nueva (WeeklyCheckOut) + actualización de estado en Priority y Task |
| Business Rules | BR-002, BR-006, BR-007, BR-008, BR-009, BR-012, BR-013, BR-016, BR-017 (9 reglas) |
| Tests requeridos | Critical: Unit + Integration + Contract + E2E + Security, cobertura >95% |
| Justificación | Transacción atómica compleja (actualiza estado de múltiples entidades + dispara CRS), wizard de UI multi-paso, 9 BRs, E2E obligatorio, y es el trigger del CRS |

---

### Siguiente Paso

Ejecutar `/create-tickets 003-weekly-checkout`
