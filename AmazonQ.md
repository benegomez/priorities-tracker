# AmazonQ.md — Contexto del Proyecto: Priorities Tracker

---

## 1. Overview

Priorities Tracker es una plataforma SaaS de gestión de compromisos semanales que ayuda a managers a obtener visibilidad sobre las prioridades, ejecución y confiabilidad de sus equipos sin microgestión. Los colaboradores registran sus compromisos mediante Check-Ins semanales y cierran la semana con Check-Outs. La plataforma calcula el **Commitment Reliability Score (CRS)**, un indicador objetivo de confiabilidad de ejecución por persona. El stack es FastAPI + PostgreSQL en backend y Next.js 15 + TypeScript en frontend, desplegado con Docker Compose. La arquitectura es un **Modular Monolith con DDD**, organizado en módulos por bounded context.

---

## 2. Stack Tecnológico

| Capa | Tecnología | Versión | Ubicación |
|---|---|---|---|
| Backend | FastAPI (Python, async/await) | Python 3.13+ | `apps/backend/` |
| ORM | SQLAlchemy async + Alembic | 2.0 | `apps/backend/` |
| Base de Datos | PostgreSQL | — | `docker-compose.yml` |
| Frontend | Next.js (App Router) | 15 | `apps/frontend/` |
| Lenguaje Frontend | TypeScript | — | `apps/frontend/` |
| UI Components | shadcn/ui + TailwindCSS | — | `apps/frontend/src/components/` |
| State (server) | TanStack Query | — | `apps/frontend/` |
| State (local) | Zustand | — | `apps/frontend/src/store/` |
| Validación forms | Zod | — | `apps/frontend/src/features/` |
| Infraestructura | Docker Compose | — | `docker-compose.yml` |
| CI (código) | GitHub Actions | — | `.github/` |
| CD (deploy) | GitLab CI/CD | — | repo separado `priorities-tracker-deploy` |

---

## 3. Puertos Locales

| Servicio | URL |
|---|---|
| API FastAPI | http://localhost:8089 |
| Frontend Next.js | http://localhost:8901 |
| PostgreSQL | localhost:5633 |
| Health check | http://localhost:8089/health |

---

## 4. Estructura de Directorios

```
prioritiestraccker/
├── apps/
│   ├── backend/
│   │   └── src/
│   │       ├── main.py
│   │       ├── modules/          # Un directorio por módulo de negocio
│   │       │   ├── auth/
│   │       │   ├── users/
│   │       │   ├── teams/
│   │       │   ├── projects/
│   │       │   ├── priorities/
│   │       │   ├── checkin/
│   │       │   ├── checkout/
│   │       │   ├── crs/
│   │       │   ├── reporting/
│   │       │   └── ai_insights/
│   │       ├── shared/           # Config, DB, security, logging, AI, exceptions
│   │       └── tests/            # E2E y tests transversales
│   └── frontend/
│       └── src/
│           ├── app/              # Next.js App Router (auth/, employee/, manager/, admin/)
│           ├── features/         # Módulos por dominio (checkins/, priorities/, crs/, etc.)
│           ├── components/       # UI reutilizable (ui/, layout/, forms/, tables/, charts/)
│           ├── services/         # Clientes API
│           ├── store/            # Zustand stores
│           └── hooks/            # Custom hooks globales
├── docs/                         # Documentación completa del proyecto
├── contracts/                    # OpenAPI specs (fuente de verdad de APIs)
├── infrastructure/               # Docker, ambientes, deployments
├── scripts/                      # Migraciones, seeds, utilidades
├── tests/                        # Tests de integración y E2E cross-module
├── docker-compose.yml
└── .amazonq/rules/               # Reglas y estándares para Amazon Q
```

### Estructura interna de cada módulo backend
```
<module>/
├── api/            # router.py, schemas.py, dependencies.py
├── application/    # commands/, queries/, services/, dto/
├── domain/         # entities/, value_objects/, repositories/, services/
├── infrastructure/ # repositories/ (SQLAlchemy), mappers/, adapters/
└── tests/          # unit/, integration/, contract/
```

---

## 5. Dónde Encontrar Documentación Detallada

**Regla de oro:** Todo lo detallado está en `docs/`. Este archivo es solo el mapa.

| Tema | Archivo | Qué contiene |
|---|---|---|
| Visión del producto | `docs/01-product-definition/product-summary.md` | Propuesta de valor, personas, principios |
| MVP scope | `docs/01-product-definition/mvp-definition.md` | Funcionalidades incluidas y excluidas |
| Requerimientos funcionales | `docs/01-product-definition/requirements-functional.md` | FR-001 a FR-035 |
| Arquitectura general | `docs/02-arquitectura/resumen-arquitectura.md` | Visión general, componentes |
| Principios arquitectónicos | `docs/02-arquitectura/principles/architecture-principles-v1.0-FINAL.md` | 12 principios guía |
| ADRs | `docs/02-arquitectura/ADR/` | Todas las decisiones arquitectónicas |
| Modelo de dominio | `docs/04-domain/domain-model.md` | Aggregates, entidades, jerarquía |
| Business Rules | `docs/04-domain/business-rules.md` | BR-001 a BR-017 |
| State Machines | `docs/04-domain/state-machines.md` | Transiciones de estado por entidad |
| CRS Formula | `docs/04-domain/crs-formula.md` | Fórmula, pesos, escala, tendencias |
| Estructura backend | `docs/03-backend/project-structure.md` | Módulos, capas, convenciones |
| Módulos backend | `docs/03-backend/modules/` | Detalle de cada módulo |
| API overview | `docs/06-api-implementation/api-overview.md` | Recursos REST, prefijos, conceptos |
| Contratos API por módulo | `docs/06-api-implementation/<module>-api.md` | Endpoints, schemas, reglas |
| Schemas compartidos | `docs/06-api-implementation/shared-schemas.md` | UUIDResponse, Pagination, Error, Audit |
| DDL completo | `docs/05-database/full-ddl-specification.md` | Schema físico PostgreSQL |
| Naming conventions BD | `docs/05-database/postgres-naming-conventions.md` | Tablas, PKs, FKs, índices |
| Frontend architecture | `docs/07-Iteracion01-UX-Foundations/frontend-architecture.md` | Capas, stack, objetivos |
| Frontend folder structure | `docs/07-Iteracion01-UX-Foundations/frontend-folder-structure.md` | Organización de carpetas |
| Seguridad | `docs/02-arquitectura/security-architecture.md` | JWT, RBAC, audit, evolución |
| Observabilidad | `docs/02-arquitectura/observability-architecture.md` | Logging, correlation IDs, métricas |
| Standards de desarrollo | `docs/08-Engineering-Delivery/development-standards.md` | DoD, quality gates, ciclo de vida |

---

## 6. Dominios y Módulos Clave

| Bounded Context | Módulos backend | Responsabilidad principal |
|---|---|---|
| Organization | `users`, `teams` | Estructura organizacional, roles, asignaciones |
| Commitment | `projects`, `priorities`, `checkin` | Proyectos, fases, compromisos semanales |
| Execution | `checkout`, `priorities` (estado) | Resultados, carry-over, avance |
| Reliability | `crs`, `reporting` | CRS, métricas, reportes de confiabilidad |

---

## 7. Decisiones Arquitectónicas Clave

| ADR | Decisión | Impacto |
|---|---|---|
| ADR-001 | Monorepo en GitHub | Todo el código en un solo repositorio |
| ADR-002 | Repository Governance | Trunk-based development, CODEOWNERS, PR obligatorio |
| ADR-003 | Modular Monolith | No microservicios en v1 |
| ADR-005 | Risk-Based Testing | Cobertura proporcional al riesgo del flujo |
| ADR-006 | FastAPI + Python 3.13 | Stack oficial backend |
| ADR-007 | Next.js 15 + TypeScript | Stack oficial frontend |
| ADR-008 | API First | APIs diseñadas antes de implementar |
| ADR-009 | OpenAPI Contract First | Contrato es la fuente de verdad, no el código |
| ADR-010 | DDD | Bounded contexts como unidad organizadora |

---

## 8. Reglas del Agente (.amazonq/rules/)

Antes de generar código, el agente debe considerar el rule correspondiente al área de trabajo:

| Rule | Aplica a |
|---|---|
| `base.md` | Todo el proyecto — siempre activo |
| `api-standards.md` | Endpoints, schemas, contratos OpenAPI |
| `backend-standards.md` | Código Python, FastAPI, módulos, casos de uso |
| `database-standards.md` | Modelos SQLAlchemy, migraciones Alembic, queries |
| `domain-standards.md` | Entidades, reglas de negocio, state machines, CRS |
| `frontend-standards.md` | Componentes React, features, hooks, servicios |
| `security-standards.md` | JWT, RBAC, multi-tenant, auditoría |
| `testing-standards.md` | Estrategia de tests por nivel de riesgo |
| `cicd-standards.md` | GitHub Actions, GitLab pipelines, branching |

---

## 9. Flujo de Trabajo Spec-Driven (Obligatorio)

Para cualquier nueva funcionalidad, seguir este orden:

```
1. Leer FR correspondiente en docs/01-product-definition/requirements-functional.md
2. Revisar domain-standards.md — ¿qué entidades y BRs aplican?
3. Revisar api-standards.md — diseñar contrato OpenAPI primero
4. Implementar en backend respetando Clean Architecture por módulo
5. Escribir tests según nivel de riesgo (testing-standards.md)
6. Implementar en frontend consumiendo el contrato
```

---

## 10. Notas para el Agente

- **Nunca implementar un endpoint sin contrato OpenAPI aprobado primero** (ADR-009)
- **El `organization_id` siempre viene del JWT** — nunca del body del request
- **Las business rules (BR-001 a BR-017) se validan en dominio/aplicación**, nunca solo en el router
- **Soft delete obligatorio** — nunca `DELETE` físico en entidades de negocio (`deleted_at`, `deleted_by`)
- **Un módulo no importa entidades de otro módulo** — comunicación solo por interfaces
- **El CRS nunca se modifica manualmente** — siempre calculado automáticamente al hacer Check-Out
- Flujos críticos (auth, checkin, checkout, crs) requieren cobertura de tests `>95%`
- Commits directos a `main` están prohibidos — siempre mediante PR

---

*Documentación completa en `docs/`. Este archivo es el mapa de orientación rápida. Para detalles, seguir los pointers a `docs/` y `.amazonq/rules/`.*
