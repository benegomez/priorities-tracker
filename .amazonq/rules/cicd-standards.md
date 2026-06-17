---
description: "Estándares de CI/CD para Priorities Tracker. GitHub (código fuente) + GitLab CI/CD (deployment)."
globs: .gitlab-ci.yml, .github/**/*,  infrastructure/**/*,  docker/**/*,  docker-compose*.yml
alwaysApply: false
---

# CI/CD Standards — Priorities Tracker

## Modelo de Repositorios

El proyecto usa dos repositorios con responsabilidades separadas:

| Repositorio | Plataforma | Propósito |
|---|---|---|
| `priorities-tracker` | GitHub | Código fuente, documentación, contratos, tests |
| `priorities-tracker-deploy` | GitLab | Pipelines de CI/CD, deployment automation, infraestructura |

### Repositorio GitHub — Fuente de Verdad del Código

Contiene todo lo que define el producto:
- `apps/backend/` — FastAPI
- `apps/frontend/` — Next.js
- `docs/` — ADRs, arquitectura, especificaciones
- `contracts/` — OpenAPI specs
- `tests/` — Tests de todos los niveles

### Repositorio GitLab — Fuente de Verdad del Despliegue

Contiene todo lo que opera el producto:
- Pipelines `.gitlab-ci.yml`
- Docker Compose y Dockerfiles de producción
- Variables de entorno por ambiente
- Scripts de migración y seed
- Runbooks de operación

---

## Estrategia de Branching (GitHub)

Modelo: **Trunk-Based Development**

| Branch | Propósito | Restricciones |
|---|---|---|
| `main` | Producción — siempre deployable | Commits directos prohibidos. PR obligatorio |
| `feature/*` | Desarrollo de nuevas capacidades | Desde `main`, merge via PR |
| `release/*` | Estabilización de release | Desde `main`, merge via PR con aprobación |
| `hotfix/*` | Corrección de producción urgente | Merge directo a `main` con aprobación |

Ejemplos de nombres de branch:
```
feature/checkin-flow
feature/crs-calculation
hotfix/auth-token-expiry
release/v1.0.0
```

---

## Pull Request — Requisitos

Todo PR debe incluir:
- **Resumen:** qué cambia y por qué
- **ADR de referencia:** si aplica (ej. `ADR-006`)
- **Nivel de riesgo:** Low / Medium / High / Critical
- **Evidencia de validación:** tests corridos, resultados
- **Impacto en documentación:** si requiere actualizar docs

### Aprobaciones requeridas según riesgo

| Nivel | Ejemplos | Aprobaciones |
|---|---|---|
| Low | Docs, refactoring menor | 1 reviewer |
| Medium | Nuevas APIs, cambios de UI | 1 Engineering Lead |
| High | Cambios de schema, infra | 2 reviewers + Platform |
| Critical | Auth, CRS, Planning Cycle | Engineering Lead + Architecture |

---

## Quality Gates

### PR Gate (GitHub Actions → notifica a GitLab)

Debe pasar antes de merge a `main`:

| Check | Herramienta | Condición de falla |
|---|---|---|
| Unit Tests | pytest / vitest | Cualquier falla |
| Linting | Ruff + ESLint | Errores de lint |
| Type Check | MyPy + tsc | Errores de tipos |
| Security Scan | bandit + trivy | Findings críticos/altos |
| Dependency Audit | pip-audit | Vulnerabilidades conocidas |
| OpenAPI Validation | schemathesis | Contrato inválido |
| Coverage Backend | pytest-cov | <80% lógica de negocio / <95% flujos críticos |

### Release Gate (GitLab Pipeline)

Debe pasar antes de deploy a producción:

| Check | Condición |
|---|---|
| Integration Tests | PASS |
| Contract Tests (schemathesis) | PASS |
| E2E Tests críticos (Playwright) | PASS |
| Performance Smoke (k6) | PASS |
| Secret Detection | 0 secrets expuestos |
| Image Scan (trivy) | 0 vulnerabilidades críticas en imagen |

---

## Flujo de Entrega

```
GitHub (feature branch)
    ↓ Pull Request
GitHub Actions (PR Gate)
    ↓ Merge a main
GitLab Pipeline (CI)
    ↓ Build + Tests + Scan
Docker Registry (imagen versionada)
    ↓ Deploy via Docker Compose
Ambiente objetivo (staging / production)
    ↓ Post-deploy validation
Health Check + Smoke Tests
```

---

## Pipelines GitLab — Estructura de Stages

```yaml
stages:
  - build
  - test
  - scan
  - package
  - deploy
  - validate
```

| Stage | Qué hace |
|---|---|
| `build` | Compila imágenes Docker, valida sintaxis |
| `test` | Integration tests, contract tests |
| `scan` | trivy, bandit, pip-audit, secret detection |
| `package` | Tag y push de imágenes al registry |
| `deploy` | Docker Compose up en ambiente objetivo |
| `validate` | Health checks, smoke tests, validación de conectividad |

---

## Versionado de Imágenes Docker

Formato: `<servicio>:<versión>`

```
priorities-tracker-api:v1.0.0
priorities-tracker-frontend:v1.0.0
```

- Versión unificada para backend y frontend
- Nunca usar `latest` en producción
- Tags semánticos: `v<MAJOR>.<MINOR>.<PATCH>`

---

## Variables de Entorno y Secretos

- **Nunca** en código fuente ni en el repositorio GitHub
- Gestionadas en GitLab CI/CD Variables (masked + protected)
- Por ambiente: `dev`, `staging`, `production`

Variables obligatorias por ambiente:

```
DATABASE_URL
JWT_SECRET
OPENAI_API_KEY
SMTP_PASSWORD
DOCKER_REGISTRY_TOKEN
```

---

## CODEOWNERS (GitHub)

```
/apps/backend/       @backend-team
/apps/frontend/      @frontend-team
/contracts/          @architecture-board
/docs/               @architecture-board
/infrastructure/     @platform-team
```

---

## Reglas Obligatorias

- Commits directos a `main` están prohibidos
- Todo deploy a producción requiere pipeline verde en GitLab
- Rollback disponible: imagen anterior en registry + `docker compose up` previo
- Los Dockerfiles de producción viven en el repo GitLab, no en GitHub
- Las migraciones de Alembic se ejecutan como step separado en el pipeline, antes del deploy de la app
- Los health checks deben responder antes de marcar el deploy como exitoso

---

## Referencias

- [docs/02-arquitectura/ADR/ADR-001-Monorepo-Strategy.md](../../docs/02-arquitectura/ADR/ADR-001-Monorepo-Strategy.md)
- [docs/02-arquitectura/ADR/ADR-002-Repository-Strategy.md](../../docs/02-arquitectura/ADR/ADR-002-Repository-Strategy.md)
- [docs/02-arquitectura/ADR/ADR-005-Risk-Based-Testing-Strategy.md](../../docs/02-arquitectura/ADR/ADR-005-Risk-Based-Testing-Strategy.md)
- [docs/08-Engineering-Delivery/development-standards.md](../../docs/08–Engineering-Delivery/development-standards.md)
- [testing-standards.md](./testing-standards.md)
