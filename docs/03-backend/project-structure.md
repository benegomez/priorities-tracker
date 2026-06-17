# Project Structure

## Objetivo

Definir la estructura física oficial del repositorio backend de Priorities Tracker.

## Principios

- Modular Monolith.
- Clean Architecture por módulo.
- Bajo acoplamiento.
- Alta cohesión.
- Evolución futura a microservicios si fuera necesario.

---

## Estructura General

```text
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
│
├── shared/
│   ├── config/
│   ├── database/
│   ├── security/
│   ├── logging/
│   ├── ai/
│   └── exceptions/
│
└── tests/
```

---

## Jerarquía de Dominio Obligatoria

```text
Proyecto
    ↓
Fase Proyecto
    ↓
Prioridad
    ↓
Tarea
```

### Ownership

Projects Module:
- Project
- ProjectPhase

Priorities Module:
- Priority
- Task

---

## Estructura Interna de un Módulo

Ejemplo: priorities/

```text
priorities/
├── api/
│   ├── router.py
│   ├── schemas.py
│   └── dependencies.py
│
├── application/
│   ├── commands/
│   ├── queries/
│   ├── services/
│   └── dto/
│
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── repositories/
│   └── services/
│
├── infrastructure/
│   ├── repositories/
│   ├── mappers/
│   └── adapters/
│
└── tests/
```

---

## Shared Layer

### database/

- SQLAlchemy setup
- Session management
- Base models

### security/

- JWT
- RBAC
- Password hashing

### logging/

- Structured logging
- Correlation IDs

### ai/

- AI Gateway
- Provider adapters

### config/

- Settings
- Environment management

---

## Testing Structure

```text
tests/
├── unit/
├── integration/
└── e2e/
```

## Convenciones

- Un módulo por dominio.
- No compartir entidades entre módulos.
- Comunicación mediante contratos e interfaces.
