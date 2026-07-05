---
id: US-007
title: CRS Calculation & Dashboard
status: enriched
priority: critical
risk_level: Critical
complexity: L
created: 2026-07-05
---

# US-007 — CRS Calculation & Dashboard

## [original]

**Como** colaborador individual,
**quiero** que mi Commitment Reliability Score se calcule automáticamente al enviar mi Check-Out semanal y poder ver mi score, tendencia e historial,
**para** entender qué tan confiable soy cumpliendo mis compromisos y mejorar mi desempeño a lo largo del tiempo.

### Contexto

El CRS es el diferenciador principal del producto. Actualmente el submit del Check-Out tiene un placeholder (`TODO: invoke CRS module`) y la tabla `crs_scores` existe pero está vacía. Esta US implementa el cálculo real de la fórmula v1.0, persiste el resultado, y muestra un dashboard con score actual, tendencia e historial.

### Notas iniciales
- Tabla `crs_scores` ya existe con todos los campos necesarios
- El trigger point ya existe en `SubmitCheckOutUseCase`
- BR-009: CRS se calcula automáticamente al submit del Check-Out
- BR-010: CRS no puede modificarse manualmente
- BR-011: Toda ejecución CRS debe ser auditable
- BR-012: CRS se recalcula cuando existe Check-Out

---

## [enhanced]

### User Journey

- **Usuario principal:** Colaborador Individual (employee)
- **Usuarios secundarios:** Manager (ve CRS del equipo)
- **Flujo:**
  1. Empleado envía su Check-Out semanal
  2. El sistema calcula el CRS automáticamente (best-effort post-commit)
  3. El score se persiste en `crs_scores` con todos los datos de auditoría
  4. El empleado accede a `/employee/crs` y ve:
     - Score actual con indicador visual (gauge o número grande)
     - Nivel de riesgo (badge de color)
     - Tendencia (improving/stable/declining con flecha)
     - Historial de las últimas semanas (gráfico o tabla)

---

### Business Value

- **Problema que resuelve:** Sin CRS, la plataforma es solo un tracker de tareas. El CRS convierte datos de cumplimiento en una métrica accionable de confiabilidad que diferencia al producto de cualquier herramienta de gestión de proyectos.
- **Beneficio esperado:** El colaborador tiene visibilidad objetiva de su confiabilidad. El manager puede identificar patrones sin microgestión. La organización tiene datos para evaluaciones de desempeño basadas en evidencia.

---

### FR de Referencia

- **FR-032** — CRS Calculation
- **FR-033** — CRS History

---

### Bounded Context

Reliability → Módulo: `crs`

---

### Fórmula CRS v1.0

```
CRS = (0.40 × cumplimiento_prioridades)
    + (0.30 × cumplimiento_tareas)
    + (0.20 × consistencia_historica)
    + (0.10 × factor_arrastre)
```

#### Componente 1: Cumplimiento de Prioridades (40%)

```
cumplimiento_prioridades = (priorities_completed / priorities_total) × 100
```

- Si `priorities_total = 0` → componente = 100 (no penalizar por no tener prioridades)

#### Componente 2: Cumplimiento de Tareas (30%)

```
cumplimiento_tareas = (tasks_completed / tasks_total) × 100
```

- Si `tasks_total = 0` → componente = 100

#### Componente 3: Consistencia Histórica (20%)

```
consistencia_historica = promedio de scores de las últimas 4 semanas
```

- Si no hay historia (primera semana) → re-ponderar los otros 3 componentes:
  - Prioridades: 50%, Tareas: 37.5%, Arrastre: 12.5%
- Si hay menos de 4 semanas → promediar las que existan

#### Componente 4: Factor Arrastre (10%)

```
factor_arrastre = (1 - (priorities_carried / priorities_total)) × 100
```

- Si `priorities_total = 0` → componente = 100
- Penaliza por prioridades que no se completaron ni se arrastraron... wait, carried_over ES arrastre.
- Corrección: penaliza proporcionalmente al arrastre. 0 arrastres = 100, todo arrastrado = 0.

#### Escala de Interpretación

| Rango | Nivel | Risk Level |
|---|---|---|
| 90–100 | Excelente | `low` |
| 75–89 | Confiable | `low` |
| 60–74 | Riesgo moderado | `moderate` |
| 0–59 | Riesgo alto | `high` |

#### Tendencia

Comparar score actual vs promedio de las últimas 4 semanas:
- `improving`: score actual > promedio + 5 puntos
- `declining`: score actual < promedio - 5 puntos
- `stable`: dentro de ±5 puntos del promedio
- Si primera semana → `stable`

---

### Business Rules

- **BR-009** — CRS se calcula automáticamente al submit del Check-Out
- **BR-010** — CRS no puede modificarse manualmente (no hay endpoint PATCH/PUT)
- **BR-011** — Toda ejecución CRS debe ser auditable (formula_version + totals almacenados)
- **BR-012** — CRS se recalcula cuando existe Check-Out
- **BR-013** — Empleado solo ve su propio CRS
- **BR-016** — Multi-tenant

---

### Contrato API

**GET /api/v1/crs/current**
Score actual del empleado autenticado.

```
Response 200:
{
  "score": 85.50,
  "trend": "improving",
  "risk_level": "low",
  "week_start": "2026-07-05",
  "formula_version": "v1.0",
  "priorities_total": 3,
  "priorities_completed": 2,
  "tasks_total": 5,
  "tasks_completed": 4
}

Response 404: No CRS calculated yet
```

---

**GET /api/v1/crs/history**
Historial de scores del empleado.

```
Query params: ?weeks=8 (default 8, max 52)

Response 200:
{
  "items": [
    {
      "week_start": "2026-07-05",
      "score": 85.50,
      "trend": "improving",
      "risk_level": "low"
    },
    {
      "week_start": "2026-06-28",
      "score": 78.00,
      "trend": "stable",
      "risk_level": "low"
    }
  ]
}
```

---

### Acceptance Criteria

**Escenario 1 — CRS se calcula al submit del Check-Out**
```gherkin
Given un empleado que envía su Check-Out con 3 prioridades (2 completadas, 1 carried)
  And 5 tareas (4 completadas, 1 cancelada)
When el submit se procesa exitosamente
Then se crea un registro en crs_scores con:
  - score calculado según fórmula v1.0
  - formula_version = "v1.0"
  - priorities_total = 3, priorities_completed = 2
  - tasks_total = 5, tasks_completed = 4
  - trend y risk_level calculados
```

**Escenario 2 — Primera semana (sin historia)**
```gherkin
Given un empleado sin CRS previo
When se calcula su primer CRS
Then consistencia_historica se omite
  And los pesos se re-ponderan: prioridades 50%, tareas 37.5%, arrastre 12.5%
  And trend = "stable"
```

**Escenario 3 — Tendencia improving**
```gherkin
Given un empleado con promedio histórico de 70
When su score actual es 80
Then trend = "improving" (diferencia > 5)
```

**Escenario 4 — Dashboard muestra score actual**
```gherkin
Given un empleado con CRS calculado
When accede a /employee/crs
Then ve su score numérico, badge de risk_level, indicador de tendencia
  And ve historial de semanas anteriores
```

**Escenario 5 — CRS no se puede modificar manualmente**
```gherkin
Given un CRS calculado
When se intenta modificar via API
Then no existe endpoint para hacerlo (BR-010)
```

---

### Non-Functional Requirements

- **NFR-004** — CRS calculation < 500ms
- **NFR-008** — Datos de cálculo almacenados para auditoría (BR-011)
- **NFR-009** — Evento `crs.calculated` registrado en logs

---

### Dependencies

- **Técnicas:**
  - Tabla `crs_scores` ya existe
  - `SubmitCheckOutUseCase` tiene el trigger point
  - Datos de summary ya disponibles post-submit
- **Funcionales:**
  - Requiere al menos un Check-Out submitted para calcular

---

### Nivel de Riesgo

**Critical** — Módulo `crs` es siempre Critical. Es el diferenciador del producto.

---

### Complejidad Estimada

**L**

| Factor | Detalle |
|---|---|
| Capas afectadas | Backend (nuevo módulo crs) + Frontend (dashboard) |
| Endpoints | 2 nuevos (GET /current, GET /history) |
| Lógica | Fórmula con 4 componentes + queries históricos + edge cases |
| Tests | Critical: >95% cobertura, edge cases extensivos |
| UI | 1 página nueva (dashboard CRS) |

---

### Siguiente Paso

Ejecutar `/create-tickets 007-crs-calculation`
