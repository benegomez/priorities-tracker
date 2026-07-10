# Technical Debt — Priorities Tracker

> Este archivo es la fuente de verdad de la deuda técnica del proyecto.
> Se actualiza en cada US cuando se registra nueva deuda o se cierra una existente.
> Revisarlo al inicio de cada sprint como parte del backlog.

---

## Cómo usar este archivo

- **Al registrar deuda nueva:** agregar un ítem con estado `open`, origen y criterio de cierre claro.
- **Al cerrar deuda:** cambiar estado a `closed`, agregar fecha y PR de cierre.
- **Al planificar un sprint:** evaluar si algún ítem `open` debe priorizarse junto a las nuevas US.
- **Regla Boy Scout:** si trabajas en un módulo con deuda `open`, paga al menos un ítem antes de cerrar el PR.

---

## Prioridades

| Prioridad | Descripción |
|---|---|
| `P1` | Bloquea calidad o seguridad — resolver antes del siguiente deploy a producción |
| `P2` | Afecta cobertura de tests en flujos críticos — resolver en la próxima US del mismo módulo |
| `P3` | Mejora de calidad no urgente — resolver cuando se toque el módulo |

---

## Deuda Activa

### TD-001 — Rate limit test aislado

| Campo | Valor |
|---|---|
| **ID** | TD-001 |
| **Estado** | `open` |
| **Prioridad** | P3 |
| **Módulo** | `auth` |
| **Origen** | US-002 `feature/002-user-authentication` |
| **Descripción** | `test_endpoint_login_returns_429_after_5_failed_attempts` no puede ejecutarse en el mismo run que los demás integration tests porque comparte la IP del contenedor y agota el rate limit. Está marcado `@slow` y se salta automáticamente. |
| **Causa raíz** | `RATELIMIT_ENABLED=false` en `.env` para desarrollo. El test necesita un ambiente aislado con rate limiting activo. |
| **Criterio de cierre** | Configurar en CI (GitHub Actions) un job separado que ejecute con `RATELIMIT_ENABLED=true` exclusivamente para este test. |
| **Cuándo cerrar** | Al configurar el pipeline de GitHub Actions para el módulo `auth`. |

---

### TD-002 — Contract tests (schemathesis) para auth

| Campo | Valor |
|---|---|
| **ID** | TD-002 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `auth` |
| **Origen** | US-002 `feature/002-user-authentication` |
| **Descripción** | Los 4 endpoints de auth no tienen contract tests con `schemathesis` que validen que la implementación cumple el contrato OpenAPI. El contrato está verificado implícitamente por los integration tests, pero no de forma formal. |
| **Causa raíz** | `schemathesis` no estaba instalado al momento de implementar. Se difirió por bajo riesgo inmediato. |
| **Criterio de cierre** | Agregar `schemathesis` a `requirements.txt`, crear `tests/contract/test_auth_contract.py` con al menos los 4 endpoints y ejecutarlo en el pipeline. |
| **Cuándo cerrar** | Antes del primer deploy a staging o al tocar el módulo `auth` nuevamente. |

---

### TD-003 — Component render tests para LoginForm

| Campo | Valor |
|---|---|
| **ID** | TD-003 |
| **Estado** | `open` |
| **Prioridad** | P3 |
| **Módulo** | `auth` (frontend) |
| **Origen** | US-002 `feature/002-user-authentication` |
| **Descripción** | `LoginForm.tsx` no tiene tests de renderizado que verifiquen los estados loading, error 401, error 403 y error 429. Los tests de Zod schema y Zustand store sí están cubiertos. |
| **Causa raíz** | Requiere mocking de `useLogin` hook con TanStack Query — complejidad media de setup que se difirió. |
| **Criterio de cierre** | Crear `src/tests/LoginForm.test.tsx` con los 5 casos de render usando `@testing-library/react` y mocking de `useMutation`. |
| **Cuándo cerrar** | En la primera US que modifique `LoginForm` o en la iteración de UX/estilos. |

---

### TD-004 — E2E tests (Playwright) para flujo de autenticación

| Campo | Valor |
|---|---|
| **ID** | TD-004 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `auth` (frontend + backend) |
| **Origen** | US-002 `feature/002-user-authentication` |
| **Descripción** | Los 9 escenarios E2E del flujo de login/logout/redirección por rol no están automatizados con Playwright. |
| **Causa raíz** | Playwright requiere UI con estilos estables. Con el frontend en fase de scaffolding, los selectores serían frágiles y habría que reescribirlos. |
| **Criterio de cierre** | Configurar Playwright, crear `tests/e2e/test_auth_flow.spec.ts` con los 9 escenarios del ticket frontend. Se puede usar `data-testid` para hacer los selectores estables desde ahora. |
| **Cuándo cerrar** | Al completar la iteración de UX/estilos del módulo auth. Agregar `data-testid` a los elementos del `LoginForm` como preparación desde ahora. |

---

### TD-005 — Contract tests (schemathesis) para checkin y priorities

| Campo | Valor |
|---|---|
| **ID** | TD-005 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `checkin`, `priorities` |
| **Origen** | US-001 `feature/001-weekly-checkin-creation` |
| **Descripción** | Los 5 endpoints de checkin/priorities no tienen contract tests con `schemathesis`. La validación del contrato se hace implícitamente por los integration tests pero no de forma formal contra el spec OpenAPI. |
| **Causa raíz** | `schemathesis` no está instalado ni configurado en el proyecto. Se difirió junto con TD-002. |
| **Criterio de cierre** | Agregar `schemathesis` a `requirements.txt`, crear `tests/contract/test_checkin_contract.py` y `test_priorities_contract.py` con los 5 endpoints. |
| **Cuándo cerrar** | Al resolver TD-002 (mismo esfuerzo — configurar schemathesis una vez cubre ambos). |

---

### TD-006 — E2E tests (Playwright) para flujo de Check-In

| Campo | Valor |
|---|---|
| **ID** | TD-006 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `checkin` (frontend + backend) |
| **Origen** | US-001 `feature/001-weekly-checkin-creation` |
| **Descripción** | Los 3 escenarios E2E del flujo de check-in (happy path, unauthenticated redirect, submitted read-only) no están automatizados. |
| **Causa raíz** | Playwright no está configurado en el proyecto. Misma causa que TD-004. |
| **Criterio de cierre** | Configurar Playwright, crear `tests/e2e/test_checkin_flow.spec.ts` con los 3 escenarios. Agregar `data-testid` a los componentes del flujo. |
| **Cuándo cerrar** | Al resolver TD-004 (configurar Playwright una vez cubre ambos flujos). |

---

### TD-007 — PriorityForm usa fases hardcodeadas (mock)

| Campo | Valor |
|---|---|
| **ID** | TD-007 |
| **Estado** | `closed` |
| **Prioridad** | P1 |
| **Módulo** | `priorities` (frontend) |
| **Origen** | US-001 `feature/001-weekly-checkin-creation` |
| **Descripción** | ~~La página `/employee/checkin` tiene un array `MOCK_PHASES` hardcodeado.~~ Resuelto: PriorityForm ahora consume `GET /api/v1/projects/phases/available` via `useAvailablePhases()` hook. |
| **Cerrado en** | 2026-07-05 — US-006 |
| **PR** | feature/006-project-phase-management |

---

### TD-008 — Security tests pendientes para checkin/priorities

| Campo | Valor |
|---|---|
| **ID** | TD-008 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `checkin`, `priorities` |
| **Origen** | US-001 `feature/001-weekly-checkin-creation` |
| **Descripción** | Faltan tests explícitos de seguridad: cross-tenant access (fase de otra org), acceso a checkin de otro empleado, y validación de 401 sin token en todos los endpoints. La lógica está implementada pero no tiene tests dedicados. |
| **Causa raíz** | Se priorizó la cobertura funcional (24 tests BE) sobre los tests de seguridad dedicados. |
| **Criterio de cierre** | Crear `tests/security/test_checkin_security.py` con al menos: `test_cross_tenant_phase_returns_403`, `test_other_employee_checkin_returns_403`, `test_all_endpoints_return_401_without_token`. |
| **Cuándo cerrar** | Antes del primer deploy a staging o en la próxima US que toque `checkin`/`priorities`. |

---

### TD-009 — Contract tests (schemathesis) para checkout

| Campo | Valor |
|---|---|
| **ID** | TD-009 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `checkout` |
| **Origen** | US-003 `feature/003-weekly-checkout` |
| **Descripción** | Los 5 endpoints del módulo checkout no tienen contract tests con `schemathesis`. La validación se hace implícitamente por los unit tests y verificación funcional via curl. |
| **Causa raíz** | `schemathesis` no está configurado en el proyecto. Misma causa que TD-002/TD-005. |
| **Criterio de cierre** | Crear `tests/contract/test_checkout_contract.py` con los 5 endpoints. |
| **Cuándo cerrar** | Al resolver TD-002 (configurar schemathesis una vez cubre todos los módulos). |

---

### TD-010 — E2E tests (Playwright) para flujo de Check-Out

| Campo | Valor |
|---|---|
| **ID** | TD-010 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `checkout` (frontend + backend) |
| **Origen** | US-003 `feature/003-weekly-checkout` |
| **Descripción** | El flujo completo de Check-Out (crear → marcar prioridades/tareas → submit → summary) no tiene tests E2E automatizados. |
| **Causa raíz** | Playwright no está configurado. Misma causa que TD-004/TD-006. |
| **Criterio de cierre** | Crear `tests/e2e/test_checkout_flow.spec.ts` con happy path + edge cases. |
| **Cuándo cerrar** | Al resolver TD-004 (configurar Playwright una vez). |

---

### TD-011 — Security tests pendientes para checkout

| Campo | Valor |
|---|---|
| **ID** | TD-011 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `checkout` |
| **Origen** | US-003 `feature/003-weekly-checkout` |
| **Descripción** | Faltan tests explícitos de seguridad para checkout: cross-tenant, acceso a checkout de otro empleado, 401 sin token. La lógica está implementada pero sin tests dedicados. |
| **Causa raíz** | Se priorizó la cobertura funcional sobre tests de seguridad dedicados. |
| **Criterio de cierre** | Crear `tests/security/test_checkout_security.py` con al menos 3 tests de aislamiento. |
| **Cuándo cerrar** | Antes del primer deploy a staging. |

---

### TD-012 — CRS calculation no implementado (solo placeholder)

| Campo | Valor |
|---|---|
| **ID** | TD-012 |
| **Estado** | `closed` |
| **Prioridad** | P1 |
| **Módulo** | `crs`, `checkout` |
| **Origen** | US-003 `feature/003-weekly-checkout` |
| **Descripción** | ~~El submit del Check-Out tenía un `TODO: invoke CRS module`.~~ Resuelto: CRSCalculationService implementado con fórmula v1.0 (4 componentes), persistencia en `crs_scores`, y 17 unit tests. |
| **Cerrado en** | 2026-07-05 — US-007 |
| **PR** | feature/007-crs-calculation |

---

### TD-013 — Integration tests para checkout endpoints

| Campo | Valor |
|---|---|
| **ID** | TD-013 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `checkout` |
| **Origen** | US-003 `feature/003-weekly-checkout` |
| **Descripción** | El módulo checkout solo tiene 7 unit tests. Faltan integration tests que validen los endpoints contra la base de datos real (similar a los de checkin). |
| **Causa raíz** | Se verificó funcionalmente via curl pero no se automatizaron los integration tests. |
| **Criterio de cierre** | Crear `tests/integration/test_checkout_endpoints.py` con al menos 8 tests (POST 201, POST 409, GET 200, GET 404, PATCH priority, PATCH task, submit 200, submit 409). |
| **Cuándo cerrar** | En la próxima US que toque el módulo `checkout`. |

---

### TD-014 — Component tests para CheckIn detail y CheckOut flow

| Campo | Valor |
|---|---|
| **ID** | TD-014 |
| **Estado** | `open` |
| **Prioridad** | P3 |
| **Módulo** | `checkin`, `checkout` (frontend) |
| **Origen** | US-003, US-005 |
| **Descripción** | Los nuevos componentes de US-003 (CheckOutForm, CheckOutPriorityCard, CheckOutTaskItem, etc.) y US-005 (CheckInDetail, CheckInPriorityCard, ResubmitButton, CheckInLockedBanner) no tienen component tests dedicados. |
| **Causa raíz** | Se priorizó la entrega funcional. Los tests existentes (47) cubren los componentes originales pero no los nuevos. |
| **Criterio de cierre** | Crear `tests/checkout-flow.test.tsx` y `tests/checkin-detail.test.tsx` con al menos 12 tests cada uno (según lo definido en los tickets). |
| **Cuándo cerrar** | En la próxima iteración de calidad o al tocar estos módulos. |

---

### TD-015 — Monday validation skipped en desarrollo

| Campo | Valor |
|---|---|
| **ID** | TD-015 |
| **Estado** | `open` |
| **Prioridad** | P3 |
| **Módulo** | `checkin` |
| **Origen** | US-004 (fix durante testing) |
| **Descripción** | La validación de que `week_start` sea lunes está deshabilitada en `ENVIRONMENT=development`. El test correspondiente se salta con `pytest.skip`. Esto es intencional para facilitar testing, pero el test no valida la lógica en CI. |
| **Causa raíz** | Se necesitaba probar cualquier día de la semana durante desarrollo. |
| **Criterio de cierre** | En CI (GitHub Actions), ejecutar con `ENVIRONMENT=production` para que el test de Monday validation se ejecute. O crear un test que force el environment a production via monkeypatch. |
| **Cuándo cerrar** | Al configurar GitHub Actions CI pipeline. |

---

### TD-016 — Component tests para módulo projects (frontend)

| Campo | Valor |
|---|---|
| **ID** | TD-016 |
| **Estado** | `open` |
| **Prioridad** | P3 |
| **Módulo** | `projects` (frontend) |
| **Origen** | US-006 `feature/006-project-phase-management` |
| **Descripción** | Los componentes de gestión de proyectos (ProjectList, ProjectDetail, UserSelect, PhaseList, MemberList) no tienen component tests dedicados. La funcionalidad se verificó manualmente y via build. |
| **Causa raíz** | Se priorizó la entrega funcional sobre tests de componentes. |
| **Criterio de cierre** | Crear `tests/projects.test.tsx` con al menos 10 tests: UserSelect renders, ProjectForm validates, MemberAddForm filters, etc. |
| **Cuándo cerrar** | En la próxima iteración de calidad o al tocar el módulo projects. |

---

### TD-017 — Integration tests para projects endpoints

| Campo | Valor |
|---|---|
| **ID** | TD-017 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `projects` (backend) |
| **Origen** | US-006 `feature/006-project-phase-management` |
| **Descripción** | El módulo projects tiene 13 unit tests (state machines) pero no tiene integration tests que validen los endpoints contra la base de datos real. Se verificó via curl pero no está automatizado. |
| **Causa raíz** | Se priorizó la entrega funcional. |
| **Criterio de cierre** | Crear `tests/integration/test_project_endpoints.py` con al menos 10 tests (GET list, POST create, GET detail, PATCH status, POST phase, PATCH phase, POST member, DELETE member, GET available, GET org-members, 403 for employee). |
| **Cuándo cerrar** | En la próxima US que toque el módulo `projects`. |

---

### TD-018 — Duplicación de páginas admin/manager projects

| Campo | Valor |
|---|---|
| **ID** | TD-018 |
| **Estado** | `open` |
| **Prioridad** | P3 |
| **Módulo** | `projects` (frontend) |
| **Origen** | US-006 `feature/006-project-phase-management` |
| **Descripción** | Las páginas `/admin/projects` y `/manager/projects` (lista + detalle) son prácticamente idénticas — código duplicado. Deberían extraerse a componentes compartidos y las páginas solo ser wrappers con la ruta correcta. |
| **Causa raíz** | Se creó rápido para que ambos roles tuvieran acceso. |
| **Criterio de cierre** | Extraer `ProjectListView` y `ProjectDetailView` como componentes en `features/projects/components/`, y que las páginas de admin y manager solo importen y rendericen esos componentes. |
| **Cuándo cerrar** | En la próxima iteración de refactoring o al agregar funcionalidad diferenciada por rol. |

---

### TD-019 — Sidebar flash en carga inicial (hydration delay)

| Campo | Valor |
|---|---|
| **ID** | TD-019 |
| **Estado** | `open` |
| **Prioridad** | P3 |
| **Módulo** | layout (frontend) |
| **Origen** | US-006 (fix hydration) |
| **Descripción** | El sidebar muestra brevemente el menú de `employee` antes de cambiar al menú correcto del rol. Esto ocurre porque el rol se lee de la cookie en `useEffect` (post-mount) para evitar hydration mismatch. |
| **Causa raíz** | Server render no tiene acceso a cookies del browser. El `useEffect` lee la cookie después del mount, causando un re-render visible. |
| **Criterio de cierre** | Usar middleware de Next.js para inyectar el rol como header o usar Server Components con `cookies()` de Next.js para leer el rol en el servidor. Alternativa: mostrar skeleton del sidebar hasta que el rol esté disponible. |
| **Cuándo cerrar** | En la próxima iteración de UX polish. |

---

### TD-020 — Component tests para CRS dashboard

| Campo | Valor |
|---|---|
| **ID** | TD-020 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `crs` (frontend) |
| **Origen** | US-007 `feature/007-crs-calculation` |
| **Descripción** | Los componentes del dashboard CRS (CRSScoreCard, CRSTrendIndicator, CRSHistoryChart, CRSEmptyState) no tienen component tests dedicados. La funcionalidad se verificó manualmente. |
| **Causa raíz** | Se priorizó la entrega funcional. |
| **Criterio de cierre** | Crear `tests/crs-dashboard.test.tsx` con al menos 8 tests según lo definido en el ticket FE. |
| **Cuándo cerrar** | En la próxima iteración de calidad. |

---

### TD-021 — Cascading checkbox logic es client-side only

| Campo | Valor |
|---|---|
| **ID** | TD-021 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `checkout` (frontend + backend) |
| **Origen** | US-007 (fix durante testing) |
| **Descripción** | La lógica de cascading (marcar prioridad → marca tareas, todas tareas marcadas → marca prioridad) se ejecuta solo en el frontend. Si el usuario usa la API directamente, puede tener datos inconsistentes. Idealmente el backend también debería enforcar esta lógica en el submit. |
| **Causa raíz** | Se implementó como fix de UX rápido en el frontend. |
| **Criterio de cierre** | En `SubmitCheckOutUseCase`, antes de transicionar estados, verificar: si todas las tareas de una prioridad están marcadas como completed, marcar la prioridad también. Esto garantiza consistencia independientemente del cliente. |
| **Cuándo cerrar** | En la próxima US que toque el módulo checkout. |

---

### TD-022 — Integration + security tests para teams endpoints

| Campo | Valor |
|---|---|
| **ID** | TD-022 |
| **Estado** | `open` |
| **Prioridad** | P2 |
| **Módulo** | `teams` (backend) |
| **Origen** | US-008 `feature/008-manager-team-visibility` |
| **Descripción** | Los 3 endpoints del módulo teams tienen 10 unit tests pero no tienen integration tests automatizados ni security tests dedicados. La seguridad (403 para employee, cross-manager, cross-org, 401 sin token) se verificó manualmente via curl pero no está automatizada. |
| **Causa raíz** | Se priorizó la entrega funcional. La verificación manual cubre los escenarios pero no es repetible en CI. |
| **Criterio de cierre** | Crear `tests/integration/test_team_endpoints.py` con al menos 8 tests y `tests/security/test_team_security.py` con al menos 4 tests (401, 403 employee, cross-manager, cross-org). |
| **Cuándo cerrar** | Antes del primer deploy a staging o en la próxima US que toque `teams`. |

---

### TD-023 — Component tests para team dashboard (frontend)

| Campo | Valor |
|---|---|
| **ID** | TD-023 |
| **Estado** | `open` |
| **Prioridad** | P3 |
| **Módulo** | `teams` (frontend) |
| **Origen** | US-008 `feature/008-manager-team-visibility` |
| **Descripción** | Los componentes del team dashboard (TeamTable, TeamCRSBadge, TeamWeekStatusBadge, TeamEmptyState, MemberCRSHistory, MemberCheckInView) no tienen component tests dedicados. La funcionalidad se verificó via build y manualmente. |
| **Causa raíz** | Se priorizó la entrega funcional. |
| **Criterio de cierre** | Crear `tests/team-dashboard.test.tsx` con al menos 10 tests según lo definido en el ticket FE. |
| **Cuándo cerrar** | En la próxima iteración de calidad. |

---

## Deuda Cerrada

| ID | Descripción | Cerrada en | PR |
|---|---|---|---|
| TD-007 | PriorityForm usa fases hardcodeadas (mock) | 2026-07-05 | PR #6 (US-006) |
| TD-012 | CRS calculation no implementado (solo placeholder) | 2026-07-05 | PR #7 (US-007) |

---

## Historial de Cambios

| Fecha | Acción | US |
|---|---|---|
| 2026-07-08 | Sin deuda nueva. US-011 con 9 BE + 8 FE tests. Cache semanal implementado | US-011 |
| 2026-07-07 | Sin deuda nueva. US-010 conecta UI con hook existente | US-010 |
| 2026-07-07 | Sin deuda nueva. US-009 100% frontend con tests completos | US-009 |
| 2026-07-06 | Registro: TD-022, TD-023 | US-008 |
| 2026-07-05 | Registro: TD-020, TD-021. Cierre: TD-012 | US-007 |
| 2026-07-05 | Registro: TD-016 a TD-019. Cierre: TD-007 | US-006 |
| 2026-07-05 | Registro: TD-009 a TD-015 | US-003, US-004, US-005 |
| 2025-06-23 | Registro: TD-005, TD-006, TD-007, TD-008 | US-001 |
| 2026-06-23 | Registro inicial: TD-001, TD-002, TD-003, TD-004 | US-002 |
