---
description: Selecciona y crea la siguiente User Story de mayor valor para el MVP de Priorities Tracker, usando las personas definidas y el criterio de valor de negocio sobre simplicidad técnica.
---

Por favor selecciona y crea la siguiente user story del MVP: $ARGUMENTS

## Contexto del Proyecto

Lee primero:
- `AmazonQ.md` — módulos, stack, bounded contexts
- `docs/01-product-definition/mvp-definition.md` — scope del MVP
- `docs/01-product-definition/personas.md` — las 3 personas del producto
- `docs/01-product-definition/requirements-functional.md` — FR-001..FR-035
- `docs/01-product-definition/value-proposition.md` — propuesta de valor por persona
- `docs/01-product-definition/success-metrics.md` — métricas del producto
- `.amazonq/rules/domain-standards.md` — bounded contexts y módulos

---

## Parseo de Argumentos

`$ARGUMENTS` puede ser:

| Formato | Comportamiento |
|---|---|
| *(vacío)* | El agente propone y justifica la siguiente historia de mayor valor |
| `<tema o feature>` | Crea una historia sobre ese tema específico (ej. `checkin`, `crs`, `auth`) |
| `list` | Lista las historias candidatas ordenadas por valor, sin crear ninguna |

---

## Paso 1 — Revisar Historias Existentes

- Escanea `docs/user-stories/` para identificar qué historias ya existen.
- Lista las historias ya creadas con su estado (`[original]` only vs. `[enhanced]`).
- Identifica el **gap**: qué capacidades del MVP aún no tienen user story.

---

## Paso 2 — Evaluar Candidatas por Valor

Para cada capacidad sin historia, evalúa su valor usando estos cuatro criterios:

### Criterio 1 — Valor para el Usuario (peso: 40%)

Usa las **3 personas** del producto:

| Persona | Pregunta clave |
|---|---|
| **Manager de Equipo Pequeño** | ¿Le da visibilidad de su equipo en < 5 minutos? ¿Reduce reuniones de status? |
| **Colaborador Individual** | ¿Le permite registrar compromisos en minutos? ¿Reduce interrupciones? |
| **Líder de Área** | ¿Le da visibilidad consolidada sin revisar cada proyecto? |

Puntúa 1-3 según cuántas personas se benefician directamente.

### Criterio 2 — Posición en la Cadena de Valor (peso: 30%)

El MVP tiene una cadena de valor central:

```
Estructura organizacional (users, teams, projects)
        ↓  habilita
Check-In semanal (compromisos)
        ↓  genera
Check-Out semanal (resultados)
        ↓  alimenta
CRS (confiabilidad)
        ↓  visualiza
Dashboards y Reportes (visibilidad)
        ↓  amplifica
AI Insights (inteligencia)
```

Una historia que habilita pasos posteriores de la cadena tiene más valor que una que solo agrega detalle a un paso existente.

Puntúa:
- `3` — Es un paso de la cadena principal sin el que pasos posteriores no funcionan
- `2` — Enriquece un paso existente de la cadena
- `1` — Es complementaria o de soporte

### Criterio 3 — Impacto en Métricas de Éxito (peso: 20%)

Consulta `success-metrics.md`. ¿Esta historia impacta directamente alguna métrica clave?

- North Star: Commitment Completion Rate
- Check-In Completion Rate > 90%
- Check-Out Completion Rate > 85%
- CRS promedio del equipo
- Team Visibility Time < 5 minutos

Puntúa 1-3 según el número de métricas que impacta.

### Criterio 4 — Deuda de Dependencias (peso: 10%)

¿Cuántas otras historias del backlog dependen de esta para poder implementarse?

- `3` — 3 o más historias la necesitan como prerequisito
- `2` — 1-2 historias dependen de ella
- `1` — No tiene dependientes directos

### Scoring Final

```
Score = (Valor usuario × 0.40) + (Cadena de valor × 0.30) + (Métricas × 0.20) + (Dependencias × 0.10)
```

Ordena las candidatas de mayor a menor score. La de mayor score es la siguiente historia a crear.

---

## Paso 3 — Justificar la Selección

Antes de crear la historia, presenta al usuario:

```
Historia seleccionada: <título>
Persona principal: <persona>

Scoring:
  Valor para el usuario:      <score>/3 — <justificación breve>
  Posición en cadena valor:   <score>/3 — <justificación breve>
  Impacto en métricas:        <score>/3 — <justificación breve>
  Deuda de dependencias:      <score>/3 — <justificación breve>
  Score total:                <X.XX>/3

Por qué esta y no otra:
  <2-3 líneas explicando por qué esta historia entrega más valor al producto ahora>

¿Procedemos con esta historia? (sí / elegir otra candidata)
```

Si el usuario responde con otra opción, crear esa historia en su lugar.

---

## Paso 4 — Crear la User Story

Una vez confirmada la historia, crea el archivo en:

```
docs/user-stories/<story-id>/UserStory.md
```

El `story-id` sigue el formato: `<NNN>-<kebab-case-titulo>`
Ejemplo: `001-weekly-checkin-creation`

Estructura del archivo:

```markdown
---
id: <story-id>
persona: <Manager de Equipo Pequeño / Colaborador Individual / Líder de Área>
fr: FR-XXX
bounded-context: <Organization / Commitment / Execution / Reliability>
status: draft
created: <fecha actual>
---

# <Título de la User Story>

## [original]

**Como** <rol específico de la persona>,
**quiero** <acción concreta>,
**para** <beneficio de negocio medible>.

### Contexto
<2-3 líneas describiendo la situación de la persona antes de esta historia — el dolor o necesidad que motiva la historia>

### Notas iniciales
- <observación relevante 1>
- <observación relevante 2>
- <restricción conocida si aplica>
```

---

## Paso 5 — Confirmar

Responde con:

```
✅ User Story creada: docs/user-stories/<story-id>/UserStory.md

Persona:         <nombre de la persona>
FR de referencia: FR-XXX
Bounded Context: <contexto> → Módulo: <módulo>
Score de valor:  <X.XX>/3

Siguiente paso:  /enrich-us <story-id>
```
