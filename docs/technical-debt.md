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
| **Estado** | `open` |
| **Prioridad** | P1 |
| **Módulo** | `priorities` (frontend) |
| **Origen** | US-001 `feature/001-weekly-checkin-creation` |
| **Descripción** | La página `/employee/checkin` tiene un array `MOCK_PHASES` hardcodeado con un solo UUID de fase. El `PriorityForm` necesita consumir un endpoint real que liste proyectos y fases disponibles para el usuario. |
| **Causa raíz** | El módulo `projects` no tiene endpoints de lectura implementados aún. Se usó un mock para no bloquear la entrega de US-001. |
| **Criterio de cierre** | Implementar `GET /api/v1/projects` y `GET /api/v1/projects/{id}/phases` (o un endpoint combinado), crear hook `useAvailablePhases()`, y reemplazar `MOCK_PHASES` por datos reales. |
| **Cuándo cerrar** | En la primera US que implemente el módulo `projects` o antes del primer deploy a staging. |

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

## Deuda Cerrada

| ID | Descripción | Cerrada en | PR |
|---|---|---|---|
| — | — | — | — |

---

## Historial de Cambios

| Fecha | Acción | US |
|---|---|---|
| 2025-06-23 | Registro: TD-005, TD-006, TD-007, TD-008 | US-001 |
| 2026-06-23 | Registro inicial: TD-001, TD-002, TD-003, TD-004 | US-002 |
