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

## Deuda Cerrada

| ID | Descripción | Cerrada en | PR |
|---|---|---|---|
| — | — | — | — |

---

## Historial de Cambios

| Fecha | Acción | US |
|---|---|---|
| 2026-06-23 | Registro inicial: TD-001, TD-002, TD-003, TD-004 | US-002 |
