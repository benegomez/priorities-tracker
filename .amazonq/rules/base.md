---
description: Reglas y lineamientos generales del proyecto Priorities Tracker. Aplica a todos los agentes de IA y desarrolladores.
alwaysApply: true
---

## 1. Contexto del Proyecto

**Sistema:** Priorities Tracker — Plataforma SaaS para gestión de compromisos semanales, visibilidad de ejecución y medición de confiabilidad (CRS).  
**Stack principal:** FastAPI (Python 3.13+) + PostgreSQL + Next.js 15 + TypeScript + Docker Compose.  
**Arquitectura:** Modular Monolith con Domain-Driven Design (DDD).  
**Entrada de contexto:** Leer siempre `docs/` antes de cualquier tarea. Navegar a la sección correspondiente según el área de trabajo.

## 2. Dominios del Sistema

El backend se organiza en módulos alineados con los bounded contexts del negocio:

| Módulo | Responsabilidad |
|---|---|
| `auth` | Autenticación y tokens |
| `users` | Gestión de usuarios |
| `teams` | Gestión de equipos |
| `projects` | Proyectos y fases |
| `priorities` | Prioridades y tareas semanales |
| `checkin` | Planificación semanal |
| `checkout` | Cierre semanal |
| `crs` | Commitment Reliability Score |
| `reporting` | Reportes individuales, de equipo y proyecto |
| `ai_insights` | Resúmenes y análisis IA |

## 3. Lenguaje Ubicuo (Ubiquitous Language)

Usar siempre estos términos en código, comentarios y documentación:

- **Prioridad** — Compromiso semanal asumido por un colaborador
- **Tarea** — Unidad mínima de trabajo asociada a una prioridad
- **Check-In** — Proceso de planificación semanal
- **Check-Out** — Proceso de cierre semanal
- **CRS** — Commitment Reliability Score
- **Manager** — Responsable del seguimiento del equipo
- **Empleado / Employee** — Persona que define y ejecuta compromisos
- **Planning Cycle** — Ciclo semanal completo (check-in + ejecución + check-out)

## 4. Principios Fundamentales

- **Cambios incrementales:** Un cambio a la vez. Verificar antes de continuar.
- **Leer antes de escribir:** Examinar el código existente antes de modificarlo.
- **Respetar patrones establecidos:** Clean Architecture por módulo, sin saltarse capas.
- **Soft deletes:** Registros funcionales nunca se eliminan físicamente (`deleted_at`, `deleted_by`).
- **No tocar lo que no se pidió:** No refactorizar código fuera del alcance de la tarea.
- **Sin lógica de negocio en routers:** Toda lógica va en casos de uso o servicios de dominio.
- **Sin acceso directo a ORM desde casos de uso:** Usar repositorios.

## 5. Convenciones de Código

| Ámbito | Convención | Ejemplos |
|---|---|---|
| Tablas y columnas BD | `snake_case` plural | `users`, `project_phases`, `planning_cycles` |
| Archivos Python | `snake_case` | `create_checkin.py`, `crs_engine.py` |
| Funciones y variables Python | `snake_case` | `calculate_crs()`, `is_active` |
| Clases Python / Pydantic | `PascalCase` | `CheckInCreate`, `PriorityResponse` |
| Constantes Python/TS | `UPPER_SNAKE_CASE` | `MAX_PRIORITIES_PER_WEEK` |
| Componentes React | `PascalCase` | `CheckInForm`, `CRSDashboard` |
| Custom hooks Next.js | `camelCase` con prefijo `use` | `useCheckIn`, `useCRSHistory` |
| Directorios frontend | `kebab-case` | `checkin-flow/`, `crs-dashboard/` |
| Commits Git | Inglés, descriptivo | `feat: add crs calculation endpoint` |

## 6. Puertos y URLs

| Servicio | Puerto Host | Puerto Interno |
|---|---|---|
| API FastAPI | 8089 | 8000 |
| PostgreSQL | 5633 | 5432 |
| Frontend Next.js | 8901 | 3000 |
| Frontend dev URL | http://localhost:8901 | — |
| API health check | http://localhost:8089/health | — |

## 7. Definition of Done

Un ticket está completo cuando:
- Código implementado y alineado con los estándares
- Tests aprobados (según nivel de riesgo del flujo)
- Revisión de código aprobada
- Seguridad validada
- Pipeline CI exitoso

## 8. Niveles de Riesgo para Testing

| Nivel | Flujos | Tests Requeridos |
|---|---|---|
| Crítico | auth, check-in, check-out, CRS, planning cycle | Unit + Integration + Contract + E2E |
| Core | priorities, tasks, projects, teams | Unit + Integration |
| Soporte | reporting, ai_insights | Unit |

## 9. Referencias

Para lineamientos detallados, consultar:
- [backend-standards.md](./backend-standards.md)
- [frontend-standards.md](./frontend-standards.md)
- [database-standards.md](./database-standards.md)
- [docs/01-product-definition/](../docs/01-product-definition/)
- [docs/04-domain/ubiquitous-language.md](../docs/04-domain/ubiquitous-language.md)
- [docs/08-Engineering-Delivery/development-standards.md](../docs/08–Engineering-Delivery/development-standards.md)
