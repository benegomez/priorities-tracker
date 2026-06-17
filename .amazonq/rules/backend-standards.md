---
description: "Estándares de desarrollo backend para Priorities Tracker. FastAPI + Python 3.13 + SQLAlchemy 2 + Pydantic v2."
globs: apps/backend/**/*
alwaysApply: false
---

# Backend Standards — Priorities Tracker

## Stack Oficial

- Python 3.13+
- FastAPI (async por defecto)
- SQLAlchemy 2.0 (async)
- Alembic (migraciones)
- Pydantic v2 (schemas y validación)
- PostgreSQL (persistencia)

## Herramientas de Calidad

- Ruff (linting)
- Black (formatting)
- MyPy (type checking)
- pytest + pytest-cov
- testcontainers (integración)
- httpx (cliente de test)
- schemathesis (contract testing)
- bandit (seguridad)
- pip-audit (dependencias)

---

## Estructura de Proyecto

```
src/
├── main.py
├── modules/
│   ├── auth/
│   ├── users/
│   ├── teams/
│   ├── projects/
│   ├── priorities/
│   ├── checkin/
│   ├── checkout/
│   ├── crs/
│   ├── reporting/
│   └── ai_insights/
├── shared/
│   ├── config/
│   ├── database/
│   ├── security/
│   ├── logging/
│   ├── ai/
│   └── exceptions/
└── tests/
```

---

## Estructura Interna de Módulo (Clean Architecture)

Cada módulo sigue esta estructura obligatoria:

```
<module>/
├── api/
│   ├── router.py        # Solo routing, sin lógica de negocio
│   ├── schemas.py       # Pydantic Request/Response DTOs
│   └── dependencies.py  # FastAPI dependencies
├── application/
│   ├── commands/        # Casos de uso de escritura
│   ├── queries/         # Casos de uso de lectura
│   ├── services/        # Orquestación de dominio
│   └── dto/             # Objetos de transferencia
├── domain/
│   ├── entities/        # Entidades de dominio
│   ├── value_objects/
│   ├── repositories/    # Interfaces (contratos)
│   └── services/        # Servicios de dominio puro
├── infrastructure/
│   ├── repositories/    # Implementaciones SQLAlchemy
│   ├── mappers/
│   └── adapters/
└── tests/
```

---

## Reglas Obligatorias

### Capas
- Sin lógica de negocio en `router.py`
- Sin acceso directo a ORM desde casos de uso (usar repositorios)
- Un caso de uso por acción de negocio
- Usar `UnitOfWork` para transacciones
- Los módulos no comparten entidades entre sí — comunicación por contratos/interfaces

### FastAPI
- `async def` por defecto en todos los endpoints y servicios I/O
- Dependency injection para recursos compartidos (DB session, auth, etc.)
- `HTTPException` para errores esperados
- Middleware para errores inesperados y logging
- Documentar todos los endpoints con OpenAPI (summary, description, response_model)

### Pydantic v2
- Separar siempre `<Entity>Create`, `<Entity>Update`, `<Entity>Response`
- Validaciones declarativas (no lógica en validators)
- Ejemplos JSON en schemas públicos

### SQLAlchemy 2
- Usar `async` sessions (`AsyncSession`)
- Operaciones I/O siempre asíncronas
- Repository pattern — nunca queries directas desde servicios o casos de uso

### Type Hints
- Obligatorios en todos los parámetros de función y valores de retorno

---

## Jerarquía del Dominio

```
Project
  └── ProjectPhase
        └── Priority
              └── Task
```

Owners:
- `projects` module → Project, ProjectPhase
- `priorities` module → Priority, Task

---

## Seguridad

- JWT para autenticación
- RBAC: roles `administrator`, `manager`, `employee`
- Validación de entrada en todos los endpoints
- Secretos solo en variables de entorno, nunca en código
- Audit logging en operaciones críticas

---

## Testing

Ver [testing-standards.md](./testing-standards.md) para la estrategia completa.

Resumen por módulo:
- Tests de use cases → unit tests con mocks de repositorios
- Tests de repositorios → integration tests con `testcontainers`
- Tests de endpoints → `httpx.AsyncClient` contra `TestClient` de FastAPI
- Flujos críticos (auth, checkin, checkout, crs) → cobertura `>95%`

---

## Referencias

- [docs/03-backend/project-structure.md](../../docs/03-backend/project-structure.md)
- [docs/06-api-implementation/coding-standards.md](../../docs/06-api-implementation/coding-standards.md)
- [docs/06-api-implementation/use-case-conventions.md](../../docs/06-api-implementation/use-case-conventions.md)
- [docs/06-api-implementation/pydantic-conventions.md](../../docs/06-api-implementation/pydantic-conventions.md)
- [docs/02-arquitectura/ADR/ADR-006-Backend-Technology-Stack-Enterprise-Final.md](../../docs/02-arquitectura/ADR/ADR-006-Backend-Technology-Stack-Enterprise-Final.md)
