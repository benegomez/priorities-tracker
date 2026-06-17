---
description: Actualiza la documentación del proyecto tras cambios en código, BD, API o configuración. Aplica a AmazonQ.md, docs/ y .amazonq/rules/.
---

Por favor actualiza la documentación tras los siguientes cambios: $ARGUMENTS

## Paso 1 — Identificar Tipo de Cambio

A partir de `$ARGUMENTS`, identifica qué documentos deben actualizarse:

| Tipo de cambio | Documentos a actualizar |
|---|---|
| Nuevo endpoint API | `docs/06-api-implementation/<module>-api.md`, `AmazonQ.md` sección 6 |
| Nueva migración / tabla | `docs/05-database/full-ddl-specification.md`, `docs/05-database/table-definitions.md` |
| Nuevo módulo backend | `docs/03-backend/project-structure.md`, `docs/03-backend/modules/<module>.md`, `AmazonQ.md` sección 6 |
| Nueva entidad de dominio | `docs/04-domain/entities.md`, `docs/04-domain/domain-model.md` |
| Nueva business rule | `docs/04-domain/business-rules.md`, `.amazonq/rules/domain-standards.md` |
| Cambio de state machine | `docs/04-domain/state-machines.md`, `.amazonq/rules/domain-standards.md` |
| Nuevo componente frontend | `docs/07-Iteracion01-UX-Foundations/feature-components.md` |
| Cambio de stack / versión | `AmazonQ.md` sección 2, `docs/02-arquitectura/ADR/<nuevo-ADR>.md` si aplica |
| Cambio de estándares | `.amazonq/rules/<rule-afectado>.md` |
| Nueva decisión arquitectónica | `docs/02-arquitectura/ADR/ADR-XXX-<titulo>.md`, `AmazonQ.md` sección 7 |

## Paso 2 — Tomar Contexto Actual

Antes de editar, lee:
- `AmazonQ.md` — siempre
- El documento específico identificado en el paso 1

## Paso 3 — Aplicar Actualizaciones

### Reglas Generales
- No duplicar información — si ya existe una sección similar, actualizarla
- Mantener consistencia entre `AmazonQ.md` y `docs/`
- Usar el lenguaje ubicuo del proyecto (Prioridad, Check-In, Check-Out, CRS, etc.)
- Referencias entre documentos con paths relativos

### Actualizar AmazonQ.md
- Sección 2 (Stack): si cambió tecnología o versión
- Sección 4 (Estructura): si cambió la organización de carpetas
- Sección 5 (Pointers): si se creó documentación nueva relevante
- Sección 6 (Dominios): si cambió la asignación de módulos a contextos
- Sección 7 (ADRs): si se tomó una nueva decisión arquitectónica
- Sección 8 (Rules): si se creó o modificó un rule
- Sección 10 (Notas): si hay nueva regla crítica para el agente

### Actualizar docs/
- Editar solo la sección relevante — no reescribir documentos completos
- Si es un documento de API, seguir la estructura existente del módulo
- Si es una nueva entidad, agregar con todos sus atributos y validaciones

### Actualizar .amazonq/rules/ (si aplica)
- Solo si el cambio afecta directamente una regla de desarrollo
- Mantener el formato frontmatter del rule existente

## Paso 4 — Verificar Consistencia

- [ ] `AmazonQ.md` no contradice ningún documento en `docs/`
- [ ] Los paths referenciados en `AmazonQ.md` sección 5 existen
- [ ] Los enums en `domain-standards.md` coinciden con `docs/04-domain/`
- [ ] Los endpoints en `api-standards.md` coinciden con `docs/06-api-implementation/`
- [ ] No hay información duplicada entre rules y docs

## Paso 5 — Confirmar

Responde con:
- Lista de archivos actualizados con su ruta
- Resumen de qué cambió en cada uno
- Si algún documento quedó desactualizado y requiere atención futura, advertirlo explícitamente
