---
story: 011-ai-weekly-summary
status: done
branch: feature/011-ai-weekly-summary
risk_level: Medium
complexity: L
created: 2026-07-08
---

# Plan de Implementación — US-011: AI Weekly Team Summary (with Cache)

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Backend | Módulo `ai_insights` + tabla `ai_summaries` + OpenAI client + cache + fallback + tests |
| 2 | Frontend | Página `/manager/ai-summary` + badges de origen + regenerar + tests |

**Branch único:** `feature/011-ai-weekly-summary`

---

## Fase 1 — Backend ✅

### 1.1 Dependencia + env

- [x] Agregar `openai>=1.30.0` a `requirements.txt`
- [x] Descomentar `OPENAI_API_KEY` y `OPENAI_MODEL` en `.env.example`
- [x] Rebuild container: `docker compose build api`

### 1.2 Tabla `ai_summaries`

- [x] Tabla creada con unique constraint `(manager_id, week_start, organization_id)`

### 1.3 Módulo `ai_insights` — Estructura

- [x] Directorios y `__init__.py` creados

### 1.4 Infrastructure — `openai_client.py`

- [x] `OpenAIClient` con `is_configured`, `model_name`, `generate()`
- [x] Timeout 10s, max_tokens 500, temperature 0.3
- [x] Any exception → None + log warning
- [x] Log tokens on success

### 1.5 Infrastructure — `ai_summary_repository.py`

- [x] `get_cached()`, `save()`, `delete()`
- [x] CAST(:snapshot AS jsonb) para evitar conflicto con SQLAlchemy params

### 1.6 Application — `generate_team_summary.py`

- [x] `GenerateTeamSummaryUseCase` con flujo completo:
  - [x] Cache check → team data → prompt → OpenAI → persist/fallback
  - [x] `_get_crs_with_counts()` para obtener priorities/tasks totals
  - [x] `_build_user_prompt()` con datos estructurados
  - [x] `_build_fallback_summary()` sin IA
  - [x] Decimal → float casting para JSON serialization

### 1.7 API — Schemas

- [x] `TeamSummaryRequest`, `DataSnapshot`, `TeamSummaryResponse`

### 1.8 API — Router

- [x] `POST /ai/team-summary` con `require_roles("manager", "administrator")`

### 1.9 Registrar router en main.py

- [x] `ai_router` registrado con prefix `/api/v1/ai`

### 1.10 Tests — Unit (9 passing)

- [x] `test_generate_summary_calls_openai_when_no_cache`
- [x] `test_generate_summary_returns_cached_when_exists`
- [x] `test_generate_summary_regenerate_deletes_cache`
- [x] `test_generate_summary_fallback_when_openai_fails`
- [x] `test_generate_summary_fallback_when_no_api_key`
- [x] `test_fallback_not_persisted_in_cache`
- [x] `test_generate_summary_empty_team`
- [x] `test_data_snapshot_calculated_correctly`
- [x] `test_prompt_contains_team_data`

### 1.11 Verificación Backend

- [x] 9/9 tests pasan
- [x] `POST /ai/team-summary` → 200 con resumen (primera vez: `cached=false`)
- [x] `POST /ai/team-summary` → 200 con cache (segunda vez: `cached=true`)
- [x] `POST /ai/team-summary` con `regenerate=true` → 200 nuevo (`cached=false`)
- [x] Token de employee → 403
- [x] OpenAI genera resumen real con datos del equipo

---

## Fase 2 — Frontend ✅

### 2.1 Feature module `ai`

- [x] Directorios creados: `features/ai/{services,hooks,components}`

### 2.2 Service — `ai-service.ts`

- [x] Types + `generateTeamSummary(regenerate)`

### 2.3 Hook — `useTeamSummary.ts`

- [x] `useMutation` on-demand

### 2.4 Componentes

- [x] `AISummaryCard.tsx` — resumen + badges (IA/cache/fallback) + métricas + regenerar
- [x] `AISummaryEmptyState.tsx` — icono Sparkles + botón "Generar Resumen"

### 2.5 Página

- [x] `app/(authenticated)/manager/ai-summary/page.tsx` — empty → loading → resultado
- [x] `app/(authenticated)/manager/ai-summary/loading.tsx` — skeleton

### 2.6 Navegación

- [x] `config/navigation.ts` — "Resumen IA" con icono Sparkles en sección "Mi Equipo"

### 2.7 Badge `info` variant

- [x] `components/ui/badge.tsx` — agregado variant `info` (azul) para cache badge

### 2.8 Tests (8 passing)

- [x] `test_AISummaryCard_renders_summary_text`
- [x] `test_AISummaryCard_shows_ai_badge_when_fresh`
- [x] `test_AISummaryCard_shows_cache_badge`
- [x] `test_AISummaryCard_shows_fallback_badge`
- [x] `test_AISummaryCard_shows_metrics`
- [x] `test_AISummaryCard_shows_regenerate_button`
- [x] `test_empty_state_shows_generate_button`
- [x] `test_empty_state_shows_loading_state`

### 2.9 Verificación Frontend

- [x] `npx next build --no-lint` sin errores (17 páginas)
- [x] `npm test` — 66/66 tests pasan
- [x] `/manager/ai-summary` muestra botón "Generar Resumen"
- [x] Badge correcto según origen (IA/cache/fallback)
- [x] Botón "Regenerar" funciona
- [x] Link "Resumen IA" en sidebar para managers

---

## Gate Final — PR

- [x] Backend: 9 unit tests pasan
- [x] Frontend: 8 component tests pasan
- [x] Build sin errores (BE + FE)
- [x] Cache funciona (primera vez genera, segunda retorna cache)
- [x] Regenerar invalida cache y genera nuevo
- [x] Fallback funciona sin API key
- [x] Badges correctos en UI
- [x] 403 para employee
- [ ] PR creado con resumen, nivel de riesgo Medium
