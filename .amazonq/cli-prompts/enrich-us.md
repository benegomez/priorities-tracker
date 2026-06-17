---
description: Analiza y enriquece una user story produciendo una especificación lista para implementación siguiendo el flujo Spec-Driven de Priorities Tracker.
---

Por favor analiza y enriquece la user story: $ARGUMENTS

## Contexto del Proyecto

Lee primero:
- `AmazonQ.md` — visión general, módulos, stack
- `.amazonq/rules/base.md` — lenguaje ubicuo y principios
- `.amazonq/rules/domain-standards.md` — entidades, BRs, state machines
- `.amazonq/rules/api-standards.md` — ciclo contract-first
- `docs/01-product-definition/requirements-non-functional.md` — NFR-001..NFR-015
- `docs/01-product-definition/success-metrics.md` — métricas del producto

---

## Paso 1 — Encontrar la User Story

- Busca en `docs/user-stories/` o en la carpeta indicada una historia que coincida con `$ARGUMENTS`.
- Lee el contenido completo del archivo encontrado.
- Si no hay match, lista las historias disponibles y pide clarificación.

---

## Paso 2 — Analizar y Mapear

Identifica y documenta los siguientes elementos antes de escribir el `[enhanced]`:

**Dominio:**
- FR de referencia (FR-001..FR-035)
- Bounded context: Organization / Commitment / Execution / Reliability
- Módulo(s) backend involucrado(s)
- Entidades de dominio afectadas con atributos y validaciones
- Business Rules aplicables (BR-XXX)
- Transiciones de estado involucradas

**Negocio:**
- Usuario principal (rol: administrator / manager / employee)
- Objetivo principal del usuario en esta historia
- Flujo principal de interacción (pasos en orden)
- Problema concreto que resuelve
- Beneficio esperado medible
- Prioridad de negocio: Critical / High / Medium / Low
- NFRs aplicables (NFR-001..NFR-015)
- Métricas de éxito relevantes de `success-metrics.md`
- Dependencias técnicas (otros módulos, tickets) y funcionales (otras US)

**Técnico:**
- Endpoints API necesarios: método, path, descripción
- Contrato API preliminar: request/response shape

---

## Paso 3 — Evaluar Completitud

Una user story lista para implementación debe incluir:
- [ ] User Journey: usuario, objetivo, flujo principal
- [ ] Business Value: problema + beneficio
- [ ] Prioridad de negocio asignada
- [ ] FR de referencia identificado
- [ ] Bounded context y módulo propietario
- [ ] Entidades y campos de datos (inputs, outputs, estado persistido)
- [ ] Business Rules aplicables (BR-XXX)
- [ ] Transiciones de estado (si aplica)
- [ ] Contrato API preliminar (método, path, request/response shape)
- [ ] Criterios de aceptación en Gherkin — mínimo 5
- [ ] NFRs aplicables referenciados
- [ ] Métricas de éxito (1-2 más relevantes)
- [ ] Dependencias identificadas
- [ ] Nivel de riesgo: Low / Medium / High / Critical
- [ ] Complejidad estimada: XS / S / M / L / XL

---

## Paso 3b — Estimar Complejidad

Analiza los siguientes factores y asigna una clasificación:

| Factor | Preguntas a responder |
|---|---|
| **Capas afectadas** | ¿Cuántas capas involucra? (DB, backend, frontend, todas) |
| **Endpoints** | ¿Cuántos endpoints nuevos o modificados? |
| **Entidades** | ¿Cuántas entidades/tablas nuevas o modificadas? |
| **Business Rules** | ¿Cuántas BRs aplican? ¿Alguna es compleja (CRS, carry-over, multi-tenant)? |
| **Integraciones** | ¿Involucra AI, servicios externos, eventos de dominio? |
| **Tests requeridos** | ¿Nivel Critical o High? ¿Requiere E2E? |
| **UI** | ¿Requiere nuevas páginas, flujos complejos, gráficas? |

### Tabla de Clasificación

| Talla | Criterios orientativos | Ejemplo |
|---|---|---|
| **XS** | 1 capa, 1 endpoint simple, sin nueva entidad, sin BRs complejas, sin UI nueva | Cambiar un campo en un response existente |
| **S** | 1-2 capas, 1-2 endpoints, 1 entidad existente modificada, 1-2 BRs simples | Agregar filtro de búsqueda a listado de prioridades |
| **M** | 2-3 capas, 2-4 endpoints, 1 entidad nueva o 2-3 modificadas, hasta 4 BRs, UI moderada | CRUD completo de un recurso con validaciones y pantalla de gestión |
| **L** | 3 capas, 4+ endpoints, 2+ entidades nuevas, BRs complejas o state machine, tests E2E requeridos | Flujo completo de Check-In con prioridades, tareas y validaciones |
| **XL** | 3 capas, flujo end-to-end crítico, múltiples entidades, cálculos complejos (CRS), integraciones externas (AI), cobertura >95% requerida | Cálculo y persistencia del CRS con historial y tendencias |

---

## Paso 4 — Actualizar el Archivo

Sobreescribe el archivo de la user story con la siguiente estructura:

```markdown
# <Título de la User Story>

## [original]

<contenido original intacto — NO modificar>

## [enhanced]

### User Journey
- **Usuario principal:** <rol: administrator / manager / employee>
- **Objetivo principal:** <qué quiere lograr el usuario>
- **Flujo principal:**
  1. <paso 1>
  2. <paso 2>
  3. <paso N>

### Business Value
- **Problema que resuelve:** <descripción concreta del dolor>
- **Beneficio esperado:** <resultado medible para el usuario o el negocio>

### Priority
**<Critical / High / Medium / Low>**
<justificación de 1 línea>

### FR de Referencia
FR-XXX — <descripción>

### Bounded Context
<contexto> → Módulo: <módulo>

### Entidades Involucradas
- `<Entity>`: <atributos relevantes para esta historia>

### Business Rules Aplicables
- **BR-XXX** — <descripción exacta>

### Transiciones de Estado
<si aplica — entidad: Estado A → Estado B>

### Contrato API Preliminar
**<METHOD> /api/v1/<resource>/**
Request:
```json
{ }
```
Response:
```json
{ }
```

### Acceptance Criteria

> Formato Gherkin. Mínimo 5 criterios.

**Escenario 1 — <nombre del escenario happy path>**
```gherkin
Given <contexto inicial>
When <acción del usuario>
Then <resultado esperado>
```

**Escenario 2 — <nombre del escenario de validación>**
```gherkin
Given <contexto inicial>
When <acción inválida>
Then <resultado de error esperado>
```

**Escenario 3 — <nombre del escenario de autorización>**
```gherkin
Given <usuario sin el rol correcto>
When <intenta realizar la acción>
Then <recibe 403 Forbidden>
```

**Escenario 4 — <nombre del escenario de regla de negocio>**
```gherkin
Given <contexto que activa una BR>
When <acción>
Then <sistema aplica la BR correctamente>
```

**Escenario 5 — <nombre del escenario adicional>**
```gherkin
Given <contexto>
When <acción>
Then <resultado>
```

### Non-Functional Requirements
- **NFR-XXX** — <nombre>: <implicación concreta para esta historia>

### Dependencies
- **Técnicas:** <otros módulos, tickets, migraciones previas requeridas>
- **Funcionales:** <otras user stories que deben estar completas primero>

### Success Metrics
- **<KPI del producto>:** <métrica esperada para esta historia>

### Nivel de Riesgo
**<Low / Medium / High / Critical>**

### Complejidad Estimada
**<XS / S / M / L / XL>**

| Factor | Detalle |
|---|---|
| Capas afectadas | <DB / Backend / Frontend / todas> |
| Endpoints | <número y tipo> |
| Entidades | <nuevas / modificadas> |
| Business Rules | <BR-XXX aplicables> |
| Tests requeridos | <nivel y tipos según matriz> |
| Justificación | <razón principal de la talla asignada> |

### Siguiente Paso
Ejecutar `/create-tickets <story-id>`
```

---

## Paso 5 — Confirmar

Responde con:
- Archivo actualizado y su ruta
- Usuario principal y objetivo identificados
- FR mapeado y bounded context
- BRs aplicables
- NFRs referenciados
- Dependencias identificadas
- Nivel de riesgo y complejidad estimada con justificación
- Siguiente paso: `/create-tickets <story-id>`
