---
id: US-011
title: AI Weekly Team Summary
status: enriched
priority: high
risk_level: Medium
complexity: L
created: 2026-07-08
---

# US-011 — AI Weekly Team Summary

## [original]

**Como** manager de equipo,
**quiero** obtener un resumen ejecutivo semanal generado por IA sobre el estado de mi equipo,
**para** entender rápidamente qué se logró, qué está en riesgo y qué requiere mi atención sin revisar cada check-in individualmente.

### Contexto

El MVP define una única capacidad de IA: "Weekly Summary Generation". Todos los datos necesarios ya existen en la plataforma (check-ins, check-outs, prioridades, tareas, CRS con historial de 4 semanas). Falta el módulo `ai_insights`, la dependencia `openai`, y el endpoint que recopile datos del equipo, construya un prompt y retorne un resumen en lenguaje natural.

### Notas iniciales
- FR-034: Weekly Summary Generation
- Principio: "AI as an Amplifier" — nunca bloquea la operación principal
- Fail-safe: si OpenAI falla, retornar resumen básico calculado sin IA
- El `OPENAI_API_KEY` ya está en `.env.example` (comentado)
- Datos disponibles: 5 empleados × 4 semanas de historial

---

## [enhanced]

### User Journey

- **Usuario principal:** Manager de Equipo
- **Flujo:**
  1. Manager accede a `/manager/ai-summary`
  2. Ve un botón "Generar Resumen"
  3. Hace click en "Generar Resumen"
  4. **Primera vez en la semana:**
     - El sistema recopila datos del equipo de la semana actual
     - Envía los datos como contexto a OpenAI con un prompt estructurado
     - Persiste el resumen en tabla `ai_summaries` (cache semanal)
     - Retorna el resumen generado con `cached=false`
  5. **Siguientes visitas en la misma semana:**
     - El sistema detecta que ya existe un resumen para esta semana
     - Retorna el resumen guardado con `cached=true`
     - No llama a OpenAI
  6. El manager puede hacer click en "Regenerar" para forzar una nueva generación (invalida cache)
  7. Si OpenAI falla → retorna un resumen básico calculado (fallback)

---

### Business Value

- **Problema que resuelve:** El manager tiene que revisar cada empleado individualmente para entender el estado del equipo. Con 4-5 personas es manejable, pero consume tiempo y no genera insights automáticos.
- **Beneficio esperado:** En 10 segundos el manager obtiene un resumen ejecutivo que le dice: qué se logró, quién necesita atención, qué tendencias hay, y qué riesgos existen. Esto prepara mejor los 1:1 y reduce reuniones de status.
- **Métrica de éxito:** Manager puede preparar un 1:1 en <2 minutos usando el resumen.

---

### FR de Referencia

- **FR-034** — Weekly Summary Generation

---

### Bounded Context

Reliability → Módulo: `ai_insights` (nuevo)

---

### Contrato API

#### POST /api/v1/ai/team-summary

Genera (o retorna desde cache) un resumen ejecutivo semanal del equipo del manager autenticado.

```
Auth: Bearer JWT (role: manager, administrator)
operation_id: generate_team_summary

Request body:
{
  "regenerate": false    // true para forzar nueva generación (invalida cache)
}

Response 200:
{
  "summary": "Esta semana el equipo completó el 72% de sus compromisos...",
  "generated_at": "2026-07-08T10:30:00Z",
  "model": "gpt-4o-mini",
  "data_snapshot": {
    "team_size": 4,
    "week_start": "2026-07-08",
    "avg_crs": 66.5,
    "total_priorities": 13,
    "completed_priorities": 9,
    "completion_rate": 69.2
  },
  "fallback": false,
  "cached": false
}

Response 200 (from cache):
{
  "summary": "Esta semana el equipo completó el 72% de sus compromisos...",
  "generated_at": "2026-07-08T10:30:00Z",
  "model": "gpt-4o-mini",
  "data_snapshot": { ... },
  "fallback": false,
  "cached": true
}

Response 200 (fallback — OpenAI failed):
{
  "summary": "Resumen automático: El equipo completó 9 de 13 prioridades (69%). CRS promedio: 66.5. 2 miembros con tendencia declining. 1 miembro en riesgo alto.",
  "generated_at": "2026-07-08T10:30:00Z",
  "model": null,
  "data_snapshot": { ... },
  "fallback": true,
  "cached": false
}

Response 403: Insufficient permissions (employee role)
```

---

### Cache Strategy

- **Tabla:** `ai_summaries`
- **Key:** `manager_id` + `week_start` + `organization_id`
- **TTL:** No expira automáticamente — 1 resumen por semana por manager
- **Invalidación:** `regenerate=true` en el request borra el cache y genera uno nuevo
- **Fallback no se cachea** — solo se cachean resúmenes generados por IA exitosamente

#### Tabla `ai_summaries`

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

### Prompt Strategy

#### System Prompt
```
Eres un asistente de gestión de equipos. Tu rol es generar resúmenes ejecutivos semanales para managers.
Responde siempre en español. Sé conciso (máximo 200 palabras). Estructura tu respuesta en:
1. Resumen general (1-2 oraciones)
2. Logros destacados
3. Puntos de atención
4. Recomendaciones (si aplica)
No inventes datos. Solo usa la información proporcionada.
```

#### User Prompt (template)
```
Genera un resumen ejecutivo semanal para el equipo con los siguientes datos:

Semana: {week_start}
Tamaño del equipo: {team_size} personas

Datos por miembro:
{for each member}
- {name}: CRS {score} ({trend}), {priorities_completed}/{priorities_total} prioridades completadas, {tasks_completed}/{tasks_total} tareas
{end for}

Métricas agregadas:
- CRS promedio: {avg_crs}
- Tasa de cumplimiento: {completion_rate}%
- Miembros en riesgo alto: {high_risk_count}
- Miembros con tendencia declining: {declining_count}
```

---

### Arquitectura del módulo `ai_insights`

```
modules/ai_insights/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── router.py          # POST /ai/team-summary
│   └── schemas.py         # TeamSummaryRequest, TeamSummaryResponse, DataSnapshot
├── application/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── generate_team_summary.py  # GenerateTeamSummaryUseCase
├── infrastructure/
│   ├── __init__.py
│   ├── openai_client.py   # OpenAI wrapper con retry + fallback
│   └── ai_summary_repository.py  # CRUD para ai_summaries table
└── tests/
    ├── __init__.py
    └── unit/
        ├── __init__.py
        └── test_team_summary.py
```

---

### Dependencias nuevas

| Dependencia | Versión | Propósito |
|---|---|---|
| `openai` | `>=1.30.0` | Cliente oficial OpenAI |

---

### Variables de entorno

```bash
# Activar en .env (ya están en .env.example comentadas)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

---

### Business Rules

| BR | Regla | Validación |
|---|---|---|
| BR-014 | Manager solo ve datos de sus reportes directos | Datos recopilados solo de `manager_id = current_user.id` |
| BR-016 | Multi-tenant | `organization_id` del JWT en todas las queries |
| NUEVA | IA nunca bloquea la operación | Si OpenAI falla → fallback calculado |
| NUEVA | Solo roles manager/administrator | `require_roles("manager", "administrator")` |
| NUEVA | Cache semanal | 1 resumen por manager por semana, invalidable con `regenerate=true` |
| NUEVA | Fallback no se cachea | Solo resúmenes exitosos de IA se persisten |

---

### Edge Cases

| Caso | Comportamiento |
|---|---|
| Manager sin reportes directos | Summary: "No tienes miembros en tu equipo", no se cachea |
| Ningún empleado hizo check-in esta semana | Summary indica "Ningún miembro registró check-in" |
| `OPENAI_API_KEY` no configurada | Fallback directo (sin intentar llamar a OpenAI) |
| OpenAI timeout (>10s) | Fallback calculado, no se cachea |
| OpenAI rate limit (429) | Fallback calculado, no se cachea |
| OpenAI error (500) | Fallback calculado, no se cachea |
| Respuesta de OpenAI vacía | Fallback calculado, no se cachea |
| Segunda visita misma semana | Retorna cache, `cached=true` |
| `regenerate=true` | Borra cache existente, genera nuevo |
| Regenerar cuando OpenAI falla | Retorna fallback, cache anterior se borró |

---

### Acceptance Criteria

**Escenario 1 — Resumen generado con IA (primera vez)**
```gherkin
Given un manager con 4 reportes directos con datos de la semana
  And OPENAI_API_KEY configurada
  And no existe resumen cacheado para esta semana
When hace POST /api/v1/ai/team-summary
Then recibe un resumen en español con logros, puntos de atención y recomendaciones
  And "fallback" = false
  And "cached" = false
  And "model" = "gpt-4o-mini"
  And el resumen se persiste en ai_summaries
```

**Escenario 2 — Resumen desde cache (segunda visita)**
```gherkin
Given un manager que ya generó un resumen esta semana
When hace POST /api/v1/ai/team-summary (sin regenerate)
Then recibe el resumen cacheado
  And "cached" = true
  And no se llama a OpenAI
```

**Escenario 3 — Regenerar (invalida cache)**
```gherkin
Given un manager con resumen cacheado
When hace POST /api/v1/ai/team-summary con "regenerate": true
Then se borra el cache anterior
  And se genera un nuevo resumen llamando a OpenAI
  And "cached" = false
  And el nuevo resumen se persiste
```

**Escenario 4 — Fallback cuando OpenAI falla**
```gherkin
Given un manager con reportes directos
  And OpenAI no está disponible
When hace POST /api/v1/ai/team-summary
Then recibe un resumen básico calculado (sin IA)
  And "fallback" = true
  And "cached" = false
  And el fallback NO se persiste en cache
```

**Escenario 5 — Sin API key configurada**
```gherkin
Given OPENAI_API_KEY no está configurada
When un manager hace POST /api/v1/ai/team-summary
Then recibe el fallback directamente
  And "fallback" = true
```

**Escenario 6 — Employee no puede acceder**
```gherkin
Given un usuario con rol employee
When hace POST /api/v1/ai/team-summary
Then recibe 403 Forbidden
```

**Escenario 7 — UI indica origen del resumen**
```gherkin
Given un manager que ve el resumen
Then ve un badge que indica:
  - "Generado por IA" (verde) si fallback=false y cached=false
  - "Desde cache" (azul) si cached=true
  - "Resumen automático" (gris) si fallback=true
```

**Escenario 8 — UI permite regenerar**
```gherkin
Given un manager viendo un resumen cacheado
When hace click en "Regenerar"
Then se genera un nuevo resumen (loading visible)
  And el resultado reemplaza el anterior
```

---

### Non-Functional Requirements

- **NFR-004** — Respuesta < 15s (primera generación con OpenAI)
- **NFR-013** — Respuesta desde cache < 200ms
- **NFR-014** — Fallback < 500ms (sin IA)
- **NFR-015** — Timeout de OpenAI: 10s máximo
- **NFR-016** — Tokens consumidos logueados para control de costos

---

### Dependencies

- **Técnicas:**
  - `TeamRepositoryImpl` con queries batch ✅ US-008
  - `require_roles()` ✅ US-002
  - `.env.example` con `OPENAI_API_KEY` ✅ preparado
  - Datos de equipo (4 semanas × 5 empleados) ✅ seed
- **Funcionales:**
  - Requiere US-008 (team visibility) ✅
  - Requiere US-007 (CRS) ✅
- **Externas:**
  - `OPENAI_API_KEY` válida para generación con IA (sin ella funciona con fallback)

---

### Nivel de Riesgo

**Medium** — Introduce dependencia externa (OpenAI) pero con fallback obligatorio. Módulo nuevo pero reutiliza queries existentes. No modifica datos de negocio (solo tabla propia `ai_summaries`).

---

### Complejidad Estimada

**L**

| Factor | Detalle |
|---|---|
| Capas afectadas | Backend (módulo nuevo + migración) + Frontend (1 página) |
| Endpoints nuevos | 1 (POST /ai/team-summary) |
| Dependencias nuevas | `openai` en requirements.txt |
| DB | 1 tabla nueva (`ai_summaries`) + migración Alembic |
| Lógica | Cache check → datos → prompt → OpenAI → fallback → persist |
| Tests | Medium: unit tests del use case + mock de OpenAI |
| UI | 1 página con botón + resultado + badges + regenerar |

---

### Siguiente Paso

Ejecutar `/create-tickets 011-ai-weekly-summary`
