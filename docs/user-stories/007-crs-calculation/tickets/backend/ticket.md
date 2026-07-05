---
status: done
type: backend
story: docs/user-stories/007-crs-calculation/UserStory.md
depends-on: null
risk_level: Critical
complexity: L
---

# [BE] US-007 — CRS Calculation & API

## Objetivo

Implementar el servicio de cálculo del CRS (fórmula v1.0), integrarlo con el submit del Check-Out, y exponer 2 endpoints para consultar el score actual e historial.

## Scope

Nuevo módulo `crs` con servicio de cálculo + 2 endpoints. Modificar `SubmitCheckOutUseCase` para invocar el cálculo. Sin cambios de schema (tabla ya existe).

---

## Fórmula CRS v1.0

```
CRS = (0.40 × cumplimiento_prioridades)
    + (0.30 × cumplimiento_tareas)
    + (0.20 × consistencia_historica)
    + (0.10 × factor_arrastre)
```

### Componentes

| # | Componente | Cálculo | Edge case |
|---|---|---|---|
| 1 | Prioridades | `(completed / total) × 100` | total=0 → 100 |
| 2 | Tareas | `(completed / total) × 100` | total=0 → 100 |
| 3 | Consistencia | Promedio scores últimas 4 semanas | Sin historia → re-ponderar |
| 4 | Arrastre | `(1 - carried / total) × 100` | total=0 → 100 |

### Re-ponderación (primera semana sin historia)

Cuando no hay scores previos, se omite consistencia y se re-ponderan:
- Prioridades: 50% (0.40 / 0.80)
- Tareas: 37.5% (0.30 / 0.80)
- Arrastre: 12.5% (0.10 / 0.80)

### Tendencia

```
diff = score_actual - promedio_ultimas_4_semanas
if diff > 5: "improving"
elif diff < -5: "declining"
else: "stable"
```

Primera semana → `"stable"`

### Risk Level

```
if score >= 75: "low"
elif score >= 60: "moderate"
else: "high"
```

---

## Archivos a Crear / Modificar

```
apps/backend/src/modules/crs/
  __init__.py
  api/
    __init__.py
    router.py               - GET /crs/current, GET /crs/history
    schemas.py              - CRSCurrentResponse, CRSHistoryItem, CRSHistoryResponse
  application/
    __init__.py
    services/
      __init__.py
      crs_calculator.py     - CRSCalculationService (fórmula + persistencia)
    queries/
      __init__.py
      get_current_crs.py
      get_crs_history.py
  infrastructure/
    __init__.py
    repositories/
      __init__.py
      crs_repository_impl.py
  tests/
    __init__.py
    unit/
      __init__.py
      test_crs_calculator.py

apps/backend/src/modules/checkout/application/commands/submit_checkout.py
  - MODIFY: reemplazar TODO con invocación real a CRSCalculationService

apps/backend/src/main.py
  - MODIFY: registrar crs_router
```

---

## Endpoints

### GET /api/v1/crs/current

| Campo | Valor |
|---|---|
| Auth | Bearer JWT (any role) |
| operation_id | `get_current_crs` |
| Response 200 | CRSCurrentResponse |
| Response 404 | No CRS calculated yet |

### GET /api/v1/crs/history

| Campo | Valor |
|---|---|
| Auth | Bearer JWT (any role) |
| operation_id | `get_crs_history` |
| Query params | `weeks` (default 8, max 52) |
| Response 200 | CRSHistoryResponse |

---

## CRSCalculationService

```python
class CRSCalculationService:
    async def calculate(
        self,
        employee_id: UUID,
        organization_id: UUID,
        checkout_id: UUID,
        week_start: date,
        priorities_total: int,
        priorities_completed: int,
        priorities_carried: int,
        tasks_total: int,
        tasks_completed: int,
    ) -> CRSScore:
        # 1. Calculate components
        # 2. Get historical scores (last 4 weeks)
        # 3. Determine weights (with/without history)
        # 4. Calculate final score
        # 5. Determine trend and risk_level
        # 6. Persist to crs_scores
        # 7. Return result
```

---

## Integración con SubmitCheckOutUseCase

Reemplazar:
```python
# TODO: invoke CRS module when implemented
```

Con:
```python
crs_service = CRSCalculationService(session)
await crs_service.calculate(
    employee_id=command.employee_id,
    organization_id=command.organization_id,
    checkout_id=checkout.id,
    week_start=checkout.week_start,
    priorities_total=summary.priorities_total,
    priorities_completed=summary.priorities_completed,
    priorities_carried=summary.priorities_carried,
    tasks_total=summary.tasks_total,
    tasks_completed=summary.tasks_completed,
)
```

> Mantener try/except para best-effort (no revertir checkout si CRS falla).

---

## Tests Requeridos

> Nivel de riesgo: Critical → cobertura >95%

### Unit Tests — CRS Calculator

- [ ] `test_calculate_all_completed_returns_100`
- [ ] `test_calculate_none_completed_returns_low_score`
- [ ] `test_calculate_zero_priorities_uses_100_for_component`
- [ ] `test_calculate_zero_tasks_uses_100_for_component`
- [ ] `test_calculate_first_week_reponders_without_history`
- [ ] `test_calculate_with_4_weeks_history_uses_average`
- [ ] `test_calculate_with_2_weeks_history_averages_available`
- [ ] `test_calculate_carried_over_penalizes_score`
- [ ] `test_calculate_all_carried_gives_zero_arrastre_component`
- [ ] `test_trend_improving_when_above_average_plus_5`
- [ ] `test_trend_declining_when_below_average_minus_5`
- [ ] `test_trend_stable_within_5_points`
- [ ] `test_trend_stable_on_first_week`
- [ ] `test_risk_level_low_above_75`
- [ ] `test_risk_level_moderate_between_60_and_74`
- [ ] `test_risk_level_high_below_60`
- [ ] `test_formula_version_stored_as_v1_0`

### Integration Tests

- [ ] `test_submit_checkout_calculates_and_persists_crs`
- [ ] `test_endpoint_get_current_crs_returns_200`
- [ ] `test_endpoint_get_current_crs_returns_404_no_data`
- [ ] `test_endpoint_get_history_returns_list`
- [ ] `test_endpoint_get_history_respects_weeks_param`

---

## Criterios de Aceptación

- [ ] CRS se calcula automáticamente al submit del Check-Out
- [ ] Score persiste en `crs_scores` con formula_version="v1.0"
- [ ] Fórmula correcta con 4 componentes y pesos
- [ ] Primera semana: re-ponderación sin consistencia histórica
- [ ] Tendencia calculada correctamente (±5 puntos vs promedio)
- [ ] Risk level derivado del score
- [ ] GET /crs/current retorna score actual
- [ ] GET /crs/history retorna historial
- [ ] CRS no modificable manualmente (no hay PATCH/PUT)
- [ ] Best-effort: fallo en CRS no revierte el checkout
- [ ] Tests >95% cobertura en el calculador

---

## Git Branch

`feature/007-crs-calculation`
