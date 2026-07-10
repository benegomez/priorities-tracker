---
status: done
type: backend
story: docs/user-stories/011-ai-weekly-summary/UserStory.md
depends-on: null
risk_level: Medium
complexity: L
---

# [BE] US-011 — AI Weekly Team Summary API (with Cache)

## Objetivo

Implementar el módulo `ai_insights` con un endpoint `POST /api/v1/ai/team-summary` que:
1. Verifica si existe un resumen cacheado para esta semana
2. Si existe y `regenerate=false` → retorna el cache
3. Si no existe o `regenerate=true` → recopila datos, llama a OpenAI, persiste y retorna
4. Si OpenAI falla → retorna fallback calculado (sin cachear)

## Scope

Módulo nuevo `ai_insights`, dependencia `openai`, tabla `ai_summaries`, 1 endpoint POST, OpenAI client wrapper, cache semanal, fallback, unit tests.

---

## FR de Referencia

- FR-034 — Weekly Summary Generation

## Business Rules Aplicables

- **BR-014** — Manager solo ve datos de sus reportes directos
- **BR-016** — Multi-tenant (`organization_id` del JWT)
- **NUEVA** — IA nunca bloquea la operación (fallback obligatorio)
- **NUEVA** — Solo roles manager/administrator
- **NUEVA** — Cache semanal: 1 resumen por manager por semana
- **NUEVA** — Fallback no se cachea

---

## Contrato API

### POST /api/v1/ai/team-summary

| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: manager, administrator) |
| operation_id | `generate_team_summary` |
| Request body | `{ "regenerate": false }` |
| Response 200 | TeamSummaryResponse |
| Response 403 | Insufficient permissions (employee role) |

### Request Schema

```python
class TeamSummaryRequest(BaseModel):
    regenerate: bool = False
```

### Response Schema

```python
class DataSnapshot(BaseModel):
    team_size: int
    week_start: date
    avg_crs: float
    total_priorities: int
    completed_priorities: int
    completion_rate: float

class TeamSummaryResponse(BaseModel):
    summary: str
    generated_at: datetime
    model: str | None
    data_snapshot: DataSnapshot
    fallback: bool
    cached: bool
```

---

## Tabla `ai_summaries` (migración Alembic)

```sql
CREATE TABLE ai_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    manager_id UUID NOT NULL,
    week_start DATE NOT NULL,
    summary TEXT NOT NULL,
    model VARCHAR(50),
    data_snapshot JSONB NOT NULL,
    fallback BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_ai_summaries_manager_week UNIQUE (manager_id, week_start, organization_id)
);

CREATE INDEX idx_ai_summaries_manager_week ON ai_summaries (manager_id, week_start);
```

---

## Archivos a Crear / Modificar

```
apps/backend/src/modules/ai_insights/
  __init__.py
  api/
    __init__.py
    router.py                        - POST /ai/team-summary
    schemas.py                       - TeamSummaryRequest, TeamSummaryResponse, DataSnapshot
  application/
    __init__.py
    commands/
      __init__.py
      generate_team_summary.py       - GenerateTeamSummaryUseCase
  infrastructure/
    __init__.py
    openai_client.py                 - OpenAI wrapper
    ai_summary_repository.py         - CRUD ai_summaries table
  tests/
    __init__.py
    unit/
      __init__.py
      test_team_summary.py

apps/backend/src/main.py             - MODIFY (registrar ai_router)
apps/backend/requirements.txt        - MODIFY (agregar openai>=1.30.0)
.env.example                         - MODIFY (descomentar OPENAI vars)
```

**Nota sobre migración:** Dado que el proyecto usa scripts SQL directos (no Alembic migrations automatizadas en dev), la tabla se crea via script SQL o directamente en el seed. Incluir el DDL en el script de setup.

---

## Implementación

### Flujo del Use Case

```
POST /ai/team-summary { regenerate: false }
    │
    ├── Check cache: SELECT FROM ai_summaries WHERE manager_id AND week_start AND org_id
    │   ├── Found + regenerate=false → return cached (cached=true)
    │   └── Not found OR regenerate=true
    │       │
    │       ├── Delete existing cache (if regenerate=true)
    │       ├── Get team data (TeamRepositoryImpl)
    │       ├── Calculate DataSnapshot
    │       ├── Build prompt
    │       ├── Call OpenAI
    │       │   ├── Success → persist in ai_summaries, return (cached=false, fallback=false)
    │       │   └── Failure → return fallback (cached=false, fallback=true, NOT persisted)
    │       └── Empty team → return fixed message (not persisted)
```

### `openai_client.py`

```python
class OpenAIClient:
    def __init__(self):
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self._client = AsyncOpenAI(api_key=self._api_key, timeout=10.0) if self._api_key else None

    @property
    def is_configured(self) -> bool:
        return self._client is not None

    @property
    def model_name(self) -> str:
        return self._model

    async def generate(self, system_prompt: str, user_prompt: str) -> str | None:
        """Returns generated text or None on any failure."""
        if not self.is_configured:
            return None
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"ai.openai_error: {e}")
            return None
```

### `ai_summary_repository.py`

```python
class AISummaryRepository:
    async def get_cached(self, manager_id, week_start, organization_id) -> Row | None
    async def save(self, manager_id, week_start, organization_id, summary, model, data_snapshot) -> None
    async def delete(self, manager_id, week_start, organization_id) -> None
```

### Prompts

**System:**
```
Eres un asistente de gestión de equipos. Tu rol es generar resúmenes ejecutivos semanales para managers.
Responde siempre en español. Sé conciso (máximo 200 palabras). Estructura tu respuesta en:
1. Resumen general (1-2 oraciones)
2. Logros destacados
3. Puntos de atención
4. Recomendaciones (si aplica)
No inventes datos. Solo usa la información proporcionada.
```

**User (template):**
```
Genera un resumen ejecutivo semanal para el equipo con los siguientes datos:

Semana: {week_start}
Tamaño del equipo: {team_size} personas

Datos por miembro:
- {name}: CRS {score} ({trend}), {pc}/{pt} prioridades completadas, {tc}/{tt} tareas

Métricas agregadas:
- CRS promedio: {avg_crs}
- Tasa de cumplimiento: {completion_rate}%
- Miembros en riesgo alto: {high_risk_count}
- Miembros con tendencia declining: {declining_count}
```

---

## Reutilización de Código Existente

| Componente | Ubicación | Uso |
|---|---|---|
| `TeamRepositoryImpl.get_direct_reports()` | `modules/teams/infrastructure/` | Lista de miembros |
| `TeamRepositoryImpl.get_latest_crs_batch()` | `modules/teams/infrastructure/` | CRS actual batch |
| `TeamRepositoryImpl.get_week_checkins_batch()` | `modules/teams/infrastructure/` | Estado check-in |
| `TeamRepositoryImpl.get_week_checkouts_batch()` | `modules/teams/infrastructure/` | Estado check-out |
| `require_roles()` | `modules/auth/api/dependencies.py` | Auth |

---

## Tests Requeridos

### Unit Tests (mock OpenAI + mock repository)

- [ ] `test_generate_summary_returns_cached_when_exists`
- [ ] `test_generate_summary_calls_openai_when_no_cache`
- [ ] `test_generate_summary_regenerate_deletes_cache_and_calls_openai`
- [ ] `test_generate_summary_fallback_when_openai_fails`
- [ ] `test_generate_summary_fallback_when_no_api_key`
- [ ] `test_fallback_not_persisted_in_cache`
- [ ] `test_generate_summary_empty_team`
- [ ] `test_data_snapshot_calculated_correctly`
- [ ] `test_prompt_contains_team_data`
- [ ] `test_endpoint_returns_403_for_employee`

---

## Criterios de Aceptación

- [ ] `POST /ai/team-summary` retorna resumen con datos del equipo
- [ ] Primera llamada: genera y cachea (`cached=false`)
- [ ] Segunda llamada: retorna cache (`cached=true`, sin llamar OpenAI)
- [ ] `regenerate=true`: borra cache, genera nuevo
- [ ] Si OpenAI funciona: `fallback=false`, `model="gpt-4o-mini"`
- [ ] Si OpenAI falla: `fallback=true`, `model=null`, NO se cachea
- [ ] Si no hay API key: fallback directo sin error
- [ ] Solo roles manager/administrator (403 para employee)
- [ ] Multi-tenant enforced (BR-016)
- [ ] Manager solo ve datos de sus reportes (BR-014)
- [ ] `data_snapshot` contiene métricas reales
- [ ] Tabla `ai_summaries` creada
- [ ] Tests pasan
- [ ] `openai` agregado a requirements.txt

---

## Git Branch

`feature/011-ai-weekly-summary`
