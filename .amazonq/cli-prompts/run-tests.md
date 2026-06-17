---
description: Ejecuta tests del proyecto por nivel de riesgo, módulo o tipo. Sigue la Risk-Based Testing Strategy (ADR-005).
---

Por favor ejecuta los tests: $ARGUMENTS

## Opciones Disponibles

| Formato | Ejemplo | Qué ejecuta |
|---|---|---|
| `unit` | `unit` | Todos los unit tests del backend |
| `unit <module>` | `unit checkin` | Unit tests de un módulo específico |
| `integration <module>` | `integration crs` | Integration tests de un módulo |
| `contract <module>` | `contract checkin` | Contract tests con schemathesis |
| `e2e` | `e2e` | E2E tests críticos con Playwright |
| `critical` | `critical` | Suite completa de flujos críticos |
| `frontend` | `frontend` | Tests frontend con vitest |
| `security` | `security` | bandit + pip-audit |
| `coverage` | `coverage` | Reporte de cobertura completo |
| `all` | `all` | Suite completa (PR gate) |

---

## Unit Tests

```bash
# Todos los unit tests
docker compose exec api python -m pytest src/ -m "not integration and not e2e" -v

# Módulo específico
docker compose exec api python -m pytest src/modules/<module>/tests/unit/ -v

# Con cobertura del módulo
docker compose exec api python -m pytest src/modules/<module>/tests/unit/ -v \
  --cov=src/modules/<module> --cov-report=term-missing
```

Umbral mínimo: `>80%` general, `>95%` para módulos críticos (auth, checkin, checkout, crs)

---

## Integration Tests

Requieren PostgreSQL corriendo via testcontainers.

```bash
# Módulo específico
docker compose exec api python -m pytest src/modules/<module>/tests/integration/ \
  -v -m integration

# Todos los integration tests
docker compose exec api python -m pytest src/ -m integration -v
```

---

## Contract Tests (schemathesis)

Valida que la implementación cumple el contrato OpenAPI.

```bash
# Módulo específico — levantar API primero
docker compose up api -d

schemathesis run http://localhost:8089/openapi.json \
  --validate-schema=true \
  --checks all \
  --base-url http://localhost:8089 \
  --tag <module>

# Todos los contratos
schemathesis run http://localhost:8089/openapi.json --checks all
```

---

## E2E Tests (Playwright)

Solo flujos críticos del MVP.

```bash
# Todos los E2E críticos
npx playwright test

# Flujo específico
npx playwright test tests/e2e/test_checkin_flow.py
npx playwright test tests/e2e/test_checkout_flow.py
npx playwright test tests/e2e/test_crs_flow.py
npx playwright test tests/e2e/test_auth_flow.py

# Con UI para debugging
npx playwright test --ui
```

---

## Suite Crítica Completa

Para flujos de nivel Critical (auth, checkin, checkout, crs):

```bash
# Backend crítico
docker compose exec api python -m pytest \
  src/modules/auth/tests/ \
  src/modules/checkin/tests/ \
  src/modules/checkout/tests/ \
  src/modules/crs/tests/ \
  -v --cov --cov-fail-under=95

# E2E crítico
npx playwright test tests/e2e/
```

---

## Tests Frontend

```bash
cd apps/frontend

# Unit + component tests
npm run test

# Con cobertura
npm run test -- --coverage

# Watch mode
npm run test -- --watch

# Un archivo específico
npm run test -- src/features/checkins/
```

---

## Security Scan

```bash
# SAST con bandit
docker compose exec api bandit -r src/ -ll

# Vulnerabilidades en dependencias
docker compose exec api pip-audit

# Scan de imagen Docker
trivy image priorities-tracker-api:latest
```

---

## Cobertura Completa

```bash
# Reporte completo
docker compose exec api python -m pytest src/ \
  --cov=src \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-fail-under=80

# Ver reporte HTML
open apps/backend/htmlcov/index.html
```

---

## PR Gate (ejecutar antes de cada PR)

```bash
# 1. Unit tests + cobertura
docker compose exec api python -m pytest src/ -m "not integration and not e2e" \
  --cov=src --cov-fail-under=80 -q

# 2. Linting
docker compose exec api ruff check src/

# 3. Type check
docker compose exec api mypy src/

# 4. Security
docker compose exec api bandit -r src/ -ll
docker compose exec api pip-audit

# 5. Frontend
cd apps/frontend && npm run build && npm run lint
```

Todos deben pasar antes de abrir un PR. El pipeline de GitHub Actions los ejecuta automáticamente al crear el PR.

---

## Interpretar Resultados

| Resultado | Acción |
|---|---|
| Tests pasan, cobertura OK | ✅ Listo para PR |
| Tests fallan | Corregir antes de continuar |
| Cobertura <80% en módulo general | Agregar tests faltantes |
| Cobertura <95% en módulo crítico | Obligatorio completar antes de merge |
| bandit findings HIGH/CRITICAL | Corregir antes de PR |
| pip-audit vulnerabilidades | Evaluar y actualizar dependencias |
