---
description: Crea tickets de implementación (database, backend, frontend) a partir de una user story enriquecida de Priorities Tracker.
---

Por favor crea los tickets de implementación de la user story: $ARGUMENTS

## Contexto del Proyecto

Lee primero:
- `AmazonQ.md` — estructura de módulos y stack
- `.amazonq/rules/domain-standards.md` — entidades, BRs, enums
- `.amazonq/rules/api-standards.md` — contrato OpenAPI, schemas Pydantic
- `.amazonq/rules/database-standards.md` — naming, soft delete, audit columns

## Paso 1 — Encontrar la User Story Enriquecida

- Busca el archivo de la user story que coincida con `$ARGUMENTS`.
- Verifica que contenga la sección `## [enhanced]`. Si no existe, detente y pide ejecutar `/enrich-us` primero.

## Paso 2 — Determinar Estrategia de Tests

Antes de crear los tickets, lee de la sección `[enhanced]` de la US:
- **Nivel de riesgo:** Low / Medium / High / Critical
- **Complejidad estimada:** XS / S / M / L / XL

Con esos dos valores, aplica esta matriz para determinar qué tests son obligatorios en cada ticket:

| Nivel de Riesgo | Complejidad | Unit | Integration | Contract | E2E | Security | Cobertura mínima |
|---|---|---|---|---|---|---|---|
| Low | XS / S | ✅ | ❌ | ❌ | ❌ | ❌ | >60% |
| Medium | S / M | ✅ | ✅ | ❌ | ❌ | ❌ | >80% |
| High | M / L | ✅ | ✅ | ✅ | ❌ | ✅ | >80% |
| Critical | L / XL | ✅ | ✅ | ✅ | ✅ | ✅ | >95% |

**Regla adicional por módulo:** independientemente del nivel de riesgo de la US, los módulos `auth`, `checkin`, `checkout` y `crs` siempre requieren nivel Critical.

Guarda mentalmente esta decisión — la usarás para poblar la sección `## Tests Requeridos` de cada ticket.

## Paso 2b — Crear Estructura de Tickets

Dentro de la carpeta de la user story, crea:

```
<story-folder>/
  tickets/
    database/ticket.md
    backend/ticket.md
    frontend/ticket.md
```

## Paso 3 — Ticket Database

> La capa database no tiene tests unitarios propios. Sus criterios de aceptación actúan como tests de verificación manual/migration.

Plantilla para `tickets/database/ticket.md`:

```markdown
---
status: todo
type: database
story: <ruta al UserStory.md>
---

# [DB] <Feature Name>

## Objetivo
<qué persiste esta capa — tablas, columnas, índices>

## Scope
Solo schema PostgreSQL + migraciones Alembic. Sin endpoints, sin lógica de negocio.

## Cambios al Schema

### Tablas nuevas
<nombre_tabla (snake_case plural)>
  - id UUID PK
  - organization_id UUID FK NOT NULL  ← obligatorio en toda entidad
  - <campo> <tipo> <restricciones>
  - created_at TIMESTAMPTZ NOT NULL DEFAULT now()
  - updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
  - deleted_at TIMESTAMPTZ NULL
  - deleted_by UUID NULL

### Columnas nuevas en tablas existentes
<ALTER TABLE ... ADD COLUMN IF NOT EXISTS ...>

### Índices
<CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_<tabla>_<columna>>

## Migración Alembic
Archivo: `apps/backend/src/shared/database/migrations/<YYYYMMDDHHMI>_<descripcion>.py`

## Criterios de Aceptación
- [ ] Tablas/columnas creadas con tipos y restricciones correctas
- [ ] organization_id presente en toda entidad de negocio
- [ ] Columnas de auditoría presentes (created_at, updated_at, deleted_at, deleted_by)
- [ ] Índices creados para todas las FKs
- [ ] Migración ejecuta sin errores
- [ ] downgrade() implementado y probado

## Dependencias
Ninguna. Debe completarse antes del ticket backend.
```

## Paso 4 — Ticket Backend

Plantilla para `tickets/backend/ticket.md`:

```markdown
---
status: todo
type: backend
story: <ruta al UserStory.md>
depends-on: tickets/database/ticket.md
---

# [BE] <Feature Name>

## Objetivo
<lógica de negocio, casos de uso y endpoints a implementar>

## Scope
FastAPI router, Pydantic schemas, casos de uso, repositorios SQLAlchemy. Sin schema SQL, sin UI.

## Dependencia
Ticket database mergeado y migración aplicada.

## FR de Referencia
FR-XXX — <descripción>

## Business Rules Aplicables
- BR-XXX — <descripción>

## Contrato OpenAPI (diseñar ANTES de implementar — ADR-009)

### Endpoint 1
**Método y path:** POST /api/v1/<resource>/
**Tags:** [<módulo>]
**operation_id:** <snake_case_único>
**Auth:** Bearer JWT requerido

Request body:
\`\`\`json
{ }
\`\`\`

Response 201:
\`\`\`json
{ }
\`\`\`

Responses de error: 400, 401, 403, 404, 409

## Archivos a Crear / Modificar

```
apps/backend/src/modules/<module>/
  api/
    router.py          - MODIFY (agregar endpoint)
    schemas.py         - MODIFY (agregar <Entity>Create, <Entity>Response)
    dependencies.py    - MODIFY (si nueva dependency)
  application/
    commands/<action>_command.py    - CREATE
    queries/<query>_query.py        - CREATE (si lectura)
  domain/
    entities/<entity>.py            - CREATE/MODIFY
    repositories/<entity>_repo.py   - MODIFY (agregar método)
  infrastructure/
    repositories/<entity>_repo_impl.py - MODIFY
```

## Casos de Uso a Implementar
- `<ActionNameUseCase>` — descripción

## Validaciones de Dominio
<lista de validaciones que van en dominio/aplicación, NO en el router>

## Tests Requeridos

> Generado automáticamente desde: Nivel de riesgo = <nivel> | Complejidad = <talla>

### Unit Tests — `tests/unit/` ✅ siempre requeridos
Herramienta: `pytest` con mocks de repositorios
Cobertura mínima: <% según matriz>

Casos obligatorios por cada caso de uso:
- [ ] `test_<usecase>_<happy_path>_returns_expected_result`
- [ ] `test_<usecase>_<br_violation>_raises_business_rule_violation` *(uno por cada BR-XXX aplicable)*
- [ ] `test_<usecase>_missing_required_field_raises_validation_error`
- [ ] `test_<usecase>_wrong_organization_raises_authorization_error` *(BR-016)*

### Integration Tests — `tests/integration/` <✅ si Medium/High/Critical | ❌ si Low>
Herramienta: `pytest` + `testcontainers`

- [ ] `test_<entity>_repository_save_and_retrieve`
- [ ] `test_<entity>_repository_filters_by_organization_id`
- [ ] `test_<entity>_repository_excludes_soft_deleted`
- [ ] `test_uow_commit_persists_changes`
- [ ] `test_uow_rollback_reverts_changes`
- [ ] `test_endpoint_<method>_returns_<status>` *(httpx.AsyncClient)*
- [ ] `test_endpoint_without_auth_returns_401`
- [ ] `test_endpoint_wrong_role_returns_403`

### Contract Tests — `tests/contract/` <✅ si High/Critical | ❌ si Low/Medium>
Herramienta: `schemathesis`

- [ ] `test_<module>_openapi_schema_is_valid`
- [ ] `test_<endpoint>_response_matches_contract`

### E2E Tests — `tests/e2e/` <✅ si Critical | ❌ si Low/Medium/High>
Herramienta: `Playwright`

- [ ] `test_<flow>_complete_happy_path`
- [ ] `test_<flow>_handles_error_state`

### Security Tests <✅ si High/Critical | ❌ si Low/Medium>
- [ ] `bandit` sin findings HIGH/CRITICAL
- [ ] `pip-audit` sin vulnerabilidades conocidas
- [ ] `test_cross_tenant_access_returns_403`

## Git Branch
`feature/<feature-name>-backend`
```

## Paso 5 — Ticket Frontend

Plantilla para `tickets/frontend/ticket.md`:

```markdown
---
status: todo
type: frontend
story: <ruta al UserStory.md>
depends-on: tickets/backend/ticket.md
---

# [FE] <Feature Name>

## Objetivo
<UI, flujo de usuario y componentes a implementar>

## Scope
Next.js 15 App Router, features/, components/, TanStack Query, Zod. Sin schema SQL, sin lógica de API.

## Dependencia
Endpoint backend disponible y contrato OpenAPI aprobado.

## Contrato API Consumido
**Endpoint:** <METHOD> /api/v1/<resource>/
<copiar del ticket backend>

## Archivos a Crear / Modificar

```
apps/frontend/src/
  app/<role>/<route>/
    page.tsx             - CREATE
    loading.tsx          - CREATE (si aplica)
    error.tsx            - CREATE (si aplica)
  features/<module>/
    components/
      <FeatureComponent>.tsx   - CREATE
    hooks/
      use<Feature>.ts          - CREATE
    schemas/
      <feature>-schema.ts      - CREATE (Zod)
    services/
      <feature>-service.ts     - CREATE/MODIFY
```

## Componentes UI
- <ComponentName> — descripción, props, comportamiento

## Gestión de Estado
- TanStack Query: `useQuery` para <recurso>, `useMutation` para <acción>
- Zustand: solo si hay estado UI local (modales, filtros)

## Validación de Formulario (Zod)
```typescript
const <feature>Schema = z.object({
  // campos con tipos y validaciones
})
```

## Tests Requeridos

> Generado automáticamente desde: Nivel de riesgo = <nivel> | Complejidad = <talla>

### Unit / Component Tests — `tests/` ✅ siempre requeridos
Herramienta: `vitest` + `@testing-library/react`

- [ ] `test_<Component>_renders_without_errors`
- [ ] `test_<Component>_shows_loading_state`
- [ ] `test_<Component>_shows_error_state`
- [ ] `test_<Component>_shows_success_state_with_data`
- [ ] `test_<form>_zod_validation_rejects_invalid_input` *(si hay formulario)*
- [ ] `test_<form>_zod_validation_accepts_valid_input` *(si hay formulario)*

### E2E Tests <✅ si Critical | ❌ si Low/Medium/High>
Herramienta: `Playwright`

- [ ] `test_<flow>_complete_user_journey`
- [ ] `test_<flow>_unauthenticated_redirects_to_login`

## Accesibilidad
- [ ] HTML semántico
- [ ] aria-labels en inputs
- [ ] Navegación por teclado

## Git Branch
`feature/<feature-name>-frontend`
```

## Paso 6 — Confirmar

Responde con la lista de tickets creados y sus rutas. Siguiente paso sugerido: `/create-plan <story-id>`
