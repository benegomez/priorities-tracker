---
story: 007-crs-calculation
status: done
branch: feature/007-crs-calculation
risk_level: Critical
complexity: L
created: 2026-07-05
---

# Plan de Implementación — US-007: CRS Calculation & Dashboard

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Backend | Módulo `crs` con servicio de cálculo + 2 endpoints + integración con checkout |
| 2 | Frontend | Dashboard `/employee/crs` con score, tendencia e historial |

**Branch único:** `feature/007-crs-calculation`
**Commits:** secuenciales por fase (`feat(crs):`, `feat(fe):`)
**Nota:** No hay fase de DB — tabla `crs_scores` ya existe.

---

## Fase 1 — Backend ✅

### 1.1 Módulo `crs` — Estructura

- [ ] Crear directorios y `__init__.py`:
  - [ ] `modules/crs/api/`
  - [ ] `modules/crs/application/services/`
  - [ ] `modules/crs/application/queries/`
  - [ ] `modules/crs/infrastructure/repositories/`
  - [ ] `modules/crs/tests/unit/`

### 1.2 CRS Repository

- [ ] `modules/crs/infrastructure/repositories/crs_repository_impl.py`:
  - [ ] `get_latest_by_employee(employee_id, organization_id)` → CRS más reciente
  - [ ] `get_history(employee_id, organization_id, weeks)` → últimos N scores
  - [ ] `get_last_n_scores(employee_id, organization_id, n)` → para consistencia histórica
  - [ ] `save(crs_score)` → INSERT en crs_scores

### 1.3 CRS Calculation Service

- [ ] `modules/crs/application/services/crs_calculator.py`:
  - [ ] Método `calculate()` con parámetros: employee_id, organization_id, checkout_id, week_start, priorities_total/completed/carried, tasks_total/completed
  - [ ] Componente 1: `cumplimiento_prioridades`
    - [ ] `(completed / total) × 100`, si total=0 → 100
  - [ ] Componente 2: `cumplimiento_tareas`
    - [ ] `(completed / total) × 100`, si total=0 → 100
  - [ ] Componente 3: `consistencia_historica`
    - [ ] Query últimos 4 scores
    - [ ] Si hay historia → promedio de scores
    - [ ] Si no hay historia → None (trigger re-ponderación)
  - [ ] Componente 4: `factor_arrastre`
    - [ ] `(1 - carried / total) × 100`, si total=0 → 100
  - [ ] Pesos normales: 0.40, 0.30, 0.20, 0.10
  - [ ] Pesos sin historia: 0.50, 0.375, 0 (omitido), 0.125
  - [ ] Score final: suma ponderada, clamp 0-100
  - [ ] Tendencia:
    - [ ] Si no hay historia → "stable"
    - [ ] diff = score - promedio_historico
    - [ ] diff > 5 → "improving", diff < -5 → "declining", else → "stable"
  - [ ] Risk level:
    - [ ] score >= 75 → "low"
    - [ ] score >= 60 → "moderate"
    - [ ] else → "high"
  - [ ] Persistir en `crs_scores` con formula_version="v1.0"
  - [ ] Retornar resultado

### 1.4 Integración con SubmitCheckOutUseCase

- [ ] Modificar `modules/checkout/application/commands/submit_checkout.py`:
  - [ ] Importar `CRSCalculationService`
  - [ ] Reemplazar `# TODO: invoke CRS module when implemented` con invocación real
  - [ ] Mantener try/except (best-effort)
  - [ ] Pasar summary data al servicio

### 1.5 API — Endpoints

- [ ] `modules/crs/api/schemas.py`:
  - [ ] `CRSCurrentResponse` — score, trend, risk_level, week_start, formula_version, totals
  - [ ] `CRSHistoryItem` — week_start, score, trend, risk_level
  - [ ] `CRSHistoryResponse` — items[]

- [ ] `modules/crs/api/router.py`:
  - [ ] `GET /crs/current` — score más reciente del empleado
  - [ ] `GET /crs/history?weeks=8` — historial con paginación por semanas
  - [ ] Auth: cualquier rol autenticado
  - [ ] Filtro por employee_id del token + organization_id

### 1.6 Registrar router en main.py

- [ ] Importar y registrar `crs_router` con prefix `/api/v1`

### 1.7 Tests — Unit (CRS Calculator)

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

### 1.8 Tests — Integration

- [ ] `test_submit_checkout_calculates_and_persists_crs`
- [ ] `test_endpoint_get_current_crs_returns_200`
- [ ] `test_endpoint_get_current_crs_returns_404_no_data`
- [ ] `test_endpoint_get_history_returns_list`
- [ ] `test_endpoint_get_history_respects_weeks_param`

### 1.9 Verificación Backend

- [ ] Todos los unit tests pasan (17)
- [ ] Integration tests pasan (5)
- [ ] Submit checkout ahora persiste CRS en la tabla
- [ ] GET /crs/current retorna score calculado
- [ ] GET /crs/history retorna historial
- [ ] Edge cases: primera semana, 0 prioridades, todo completado, nada completado
- [ ] Best-effort: fallo en CRS no revierte checkout

### 1.10 Commits

```
feat(crs): implement CRS calculation service with formula v1.0
feat(crs): add GET /current and GET /history endpoints
feat(crs): integrate calculation with submit_checkout (replaces TODO)
test(crs): add unit tests for calculator and integration tests for endpoints
```

---

## Fase 2 — Frontend ✅

### Implementado:
- [x] Service + hooks (useCurrentCRS, useCRSHistory)
- [x] CRSScoreCard (score grande + color + badge + detalle)
- [x] CRSTrendIndicator (flecha + label)
- [x] CRSHistoryChart (tabla con historial)
- [x] CRSEmptyState (sin datos)
- [x] Página `/employee/crs` con conditional rendering
- [x] Loading skeleton
- [x] `npm run build` sin errores (14 páginas)
- [x] `npm test` — 47/47 passing

### Fixes adicionales incluidos:
- [x] Middleware: manager puede acceder a `/employee/*` routes
- [x] Navegación manager: agregado "Mi Semana" (Check-In, Check-Out, Mi CRS)
- [x] CheckOutPriorityCard: cascading logic (prioridad ↔ tareas)
  - [x] Marcar prioridad → marca todas las tareas
  - [x] Desmarcar prioridad → desmarca todas las tareas
  - [x] Marcar última tarea → marca prioridad automáticamente
  - [x] Desmarcar tarea → desmarca prioridad si estaba marcada
- [x] Test de navegación manager actualizado (4 grupos)

### 2.1 Service + Hooks

- [ ] `features/crs/services/crs-service.ts`:
  - [ ] `getCurrentCRS()` → GET `/api/v1/crs/current`
  - [ ] `getCRSHistory(weeks?)` → GET `/api/v1/crs/history?weeks=N`
- [ ] `features/crs/hooks/useCurrentCRS.ts` — useQuery `["crs", "current"]`
- [ ] `features/crs/hooks/useCRSHistory.ts` — useQuery `["crs", "history"]`

### 2.2 Componentes

- [ ] `features/crs/components/CRSScoreCard.tsx`:
  - [ ] Score numérico grande (text-4xl)
  - [ ] Color por risk_level (green/orange/red)
  - [ ] Badge: "Excelente" / "Confiable" / "Riesgo Moderado" / "Riesgo Alto"
  - [ ] Semana del cálculo
  - [ ] Detalle: prioridades X/Y, tareas X/Y

- [ ] `features/crs/components/CRSTrendIndicator.tsx`:
  - [ ] Flecha: ↑ green, → gray, ↓ red
  - [ ] Label: "Mejorando" / "Estable" / "Declinando"

- [ ] `features/crs/components/CRSHistoryChart.tsx`:
  - [ ] Tabla con columnas: Semana, Score, Tendencia, Riesgo
  - [ ] Últimas 8 semanas
  - [ ] Colores por risk_level en cada fila

- [ ] `features/crs/components/CRSEmptyState.tsx`:
  - [ ] Mensaje: "Aún no tienes un CRS calculado"
  - [ ] Subtexto: "Completa tu primer Check-Out para ver tu score"

### 2.3 Página

- [ ] `app/(authenticated)/employee/crs/page.tsx`:
  - [ ] Si 404 → CRSEmptyState
  - [ ] Si data → CRSScoreCard + CRSTrendIndicator + CRSHistoryChart
- [ ] `app/(authenticated)/employee/crs/loading.tsx` — skeleton

### 2.4 Tests — Component

- [ ] `test_CRSScoreCard_renders_score_and_badge`
- [ ] `test_CRSScoreCard_shows_correct_color_for_risk_level`
- [ ] `test_CRSTrendIndicator_shows_improving_arrow`
- [ ] `test_CRSTrendIndicator_shows_declining_arrow`
- [ ] `test_CRSHistoryChart_renders_rows`
- [ ] `test_CRSEmptyState_renders_message`
- [ ] `test_crs_page_shows_empty_state_when_404`
- [ ] `test_crs_page_shows_score_when_data_exists`

### 2.5 Verificación Frontend

- [ ] `npm run build` sin errores
- [ ] `npm test` — todos los tests pasan
- [ ] Página muestra score con colores correctos
- [ ] Tendencia con flecha correcta
- [ ] Historial con datos
- [ ] Empty state cuando no hay CRS
- [ ] Responsive

### 2.6 Commits

```
feat(crs): add service, hooks, and dashboard components
feat(crs): add CRS dashboard page /employee/crs
test(fe): add component tests for CRS dashboard
```

---

## Gate Final — PR

- [ ] Todos los tests pasan (unit + integration + component)
- [ ] Coverage >95% en CRS calculator
- [ ] `npm run build` sin errores
- [ ] Submit checkout persiste CRS correctamente
- [ ] Dashboard muestra score, tendencia, historial
- [ ] Edge cases verificados (primera semana, 0 prioridades, etc.)
- [ ] Best-effort: checkout no falla si CRS falla
- [ ] TD-012 cerrado
- [ ] PR creado con resumen y evidencia

---

## Orden de Ejecución

```
/develop-plan be    → Fase 1 (cálculo + endpoints + integración)
/develop-plan fe    → Fase 2 (dashboard)
/git-flow pr        → PR único con las 2 fases
```
