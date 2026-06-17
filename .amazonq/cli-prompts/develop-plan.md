---
description: Implementa el código de un ticket ejecutando su plan.md fase por fase, siguiendo las convenciones de Priorities Tracker.
---

Por favor implementa el plan de desarrollo: $ARGUMENTS

## Parseo de Argumentos

`$ARGUMENTS` debe incluir story-id y capa:

| Formato | Ejemplo |
|---|---|
| `<story-id> <capa>` | `checkin-flow backend` |
| `<story-id> <alias>` | `checkin-flow db`, `checkin-flow be`, `checkin-flow fe` |

Capas aceptadas: `database` / `db`, `backend` / `be`, `frontend` / `fe`.

## Paso 1 — Cargar Contexto

1. Lee `AmazonQ.md`
2. Lee `tickets/<capa>/plan.md` — checklist ordenada
3. Lee `tickets/<capa>/ticket.md` — especificación completa
4. Lee el rule correspondiente a la capa:
   - database → `.amazonq/rules/database-standards.md`
   - backend → `.amazonq/rules/backend-standards.md` + `domain-standards.md` + `api-standards.md`
   - frontend → `.amazonq/rules/frontend-standards.md`
5. Escanea el código existente antes de crear o modificar archivos
6. Guard clause: si `plan.md` no tiene tareas sin marcar (`- [ ]`), reporta que el plan está completo y detente

## Paso 2 — Reglas de Trabajo por Capa

### Database
- Migraciones Alembic en `apps/backend/src/shared/database/migrations/`
- Timestamp de archivo: `YYYYMMDDHHMI_descripcion.py`
- Siempre implementar `upgrade()` y `downgrade()`
- `organization_id UUID NOT NULL` en toda entidad de negocio
- Columnas de auditoría obligatorias: `created_at`, `updated_at`, `deleted_at`, `deleted_by`
- Tipos: `TIMESTAMPTZ` (nunca `TIMESTAMP`), `UUID` para PKs públicas
- Índices: `CREATE INDEX CONCURRENTLY` para FK columns
- Probar rollback antes de reportar completado

### Backend
- Estructura obligatoria por capa: `router → use case → repository → ORM`
- Sin lógica de negocio en `router.py` — todo va en casos de uso o dominio
- `async def` en todos los endpoints y servicios I/O
- `organization_id` extraído del JWT — nunca del body
- Todo query filtra `WHERE deleted_at IS NULL` y `WHERE organization_id = :org_id`
- `SELECT` con columnas explícitas — sin `SELECT *`
- Toda violación de BR lanza `BusinessRuleViolation("BR-XXX: ...")`
- Validar transición de estado antes de persistir
- Contrato OpenAPI documentado en el router antes de implementar lógica

### Frontend
- Componentes con `function` keyword y named export
- Lógica de negocio en `features/` — nunca en `components/`
- TanStack Query para todo estado del servidor
- Zustand solo para estado UI local (modales, filtros)
- Minimizar `use client` — solo cuando necesario
- Wrapping de componentes cliente en `Suspense` con fallback
- Errores del servidor como valores de retorno — no `try/catch` en Server Actions

## Paso 3 — Ejecutar el Plan Fase por Fase

Para cada fase del `plan.md`:
1. Lee la siguiente tarea sin marcar (`- [ ]`)
2. Impleméntala completamente
3. Actualiza `plan.md` marcando las tareas completadas (`- [x]`) y el `progress` en el frontmatter — en un solo edit al terminar cada fase
4. No avances a la siguiente fase hasta completar todas las tareas de la actual

## Paso 4 — Verificación Final

### Database
- [ ] `docker compose exec api alembic upgrade head` — sin errores
- [ ] `docker compose exec api alembic downgrade -1` y re-upgrade — sin errores

### Backend
- [ ] `docker compose exec api python -m pytest modules/<module>/tests/ -v --cov`
- [ ] `docker compose exec api ruff check src/modules/<module>/`
- [ ] `docker compose exec api mypy src/modules/<module>/`
- [ ] API levanta sin errores: `docker compose up api`
- [ ] Probar endpoint manualmente con curl o el cliente HTTP

### Frontend
- [ ] `npm run build` — sin errores TypeScript
- [ ] `npm run lint` — sin warnings ESLint
- [ ] Revisar en navegador: loading, error y success states

## Paso 5 — Entrega (NO merge automático)

Después de verificación:
1. `git add -A`
2. `git commit -m "<type>(<scope>): <descripción en inglés>"`
   - Tipos: `feat`, `fix`, `refactor`, `test`, `docs`
   - Scope: nombre del módulo (ej. `checkin`, `crs`, `priorities`)
3. `git push origin <branch-name>`
4. **NO hacer merge** — informar al usuario que el branch está listo para validación local

El merge a `main` solo ocurre después de que el usuario valide localmente y apruebe el PR.

## Paso 6 — Reporte de Completitud

```
Plan completo: [<CAPA>] <Feature Name>

  plan.md progress: <N> / <N> tareas completadas

Archivos creados:
  <lista de archivos nuevos>

Archivos modificados:
  <lista de archivos editados y qué cambió>

Branch pusheado: <nombre del branch>

Siguiente paso:
  Validar localmente → aprobar PR → /develop-plan <story-id> <siguiente-capa>
```
