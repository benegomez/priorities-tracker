
# CRS Module

## Estado: ✅ Implementado (US-007)

## Objetivo

Implementar el Commitment Reliability Score (CRS) — principal diferenciador estratégico de Priorities Tracker.

Mide la confiabilidad de una persona para cumplir los compromisos que ella misma definió.

---

## Fórmula v1.0 (Implementada)

```
CRS = (0.40 × priority_completion_rate)
    + (0.30 × task_completion_rate)
    + (0.20 × historical_consistency)
    + (0.10 × carryover_penalty)
```

Sin historial previo, se re-pondera:
- 50% prioridades, 37.5% tareas, 12.5% carry-over

### Escala

| Rango | Nivel | Risk Level |
|---|---|---|
| 75–100 | Confiable/Excelente | `low` |
| 60–74 | Riesgo moderado | `moderate` |
| 0–59 | Riesgo alto | `high` |

### Tendencia

- `improving` — score > promedio histórico + 5
- `declining` — score < promedio histórico - 5
- `stable` — dentro de ±5 del promedio

---

## Endpoints Implementados

| Método | Path | Descripción |
|---|---|---|
| GET | `/api/v1/crs/current` | Score actual del empleado autenticado |
| GET | `/api/v1/crs/history` | Historial de scores (últimas N semanas) |

---

## Trigger de Cálculo

El CRS se calcula automáticamente al ejecutar `SubmitCheckOutUseCase`. Es best-effort: si falla el cálculo, el checkout permanece submitted (no se revierte).

---

## Estructura del Módulo

```
modules/crs/
├── api/
│   ├── router.py
│   └── schemas.py
├── application/
│   └── services/
│       └── crs_calculator.py
├── domain/
│   └── entities.py
├── infrastructure/
│   └── repository.py
└── tests/
    └── unit/
        └── test_crs_calculator.py  (17 tests)
```

---

## Reglas de Negocio

- **BR-009** — CRS se calcula automáticamente al hacer Check-Out
- **BR-010** — CRS no puede modificarse manualmente
- **BR-011** — Toda ejecución de CRS debe ser auditable (`formula_version` almacenado)
- **BR-012** — CRS se recalcula cuando existe Check-Out

---

## Evolución Futura

- Team CRS aggregation (GenerateTeamCRSUseCase)
- Project/Phase CRS
- Predicción de riesgo
- Benchmarks organizacionales
