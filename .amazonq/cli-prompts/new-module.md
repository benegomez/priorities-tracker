---
description: Crea el scaffold completo de un nuevo módulo backend siguiendo Clean Architecture y los estándares del proyecto.
---

Por favor crea el scaffold del módulo: $ARGUMENTS

## Parseo de Argumentos

`$ARGUMENTS` = nombre del módulo en snake_case (ej. `priorities`, `checkin`, `ai_insights`)

## Paso 1 — Verificar que No Existe

Confirma que `apps/backend/src/modules/<module>/` no existe. Si existe, detente y advierte al usuario.

Verifica que el módulo esté en la lista aprobada de `AmazonQ.md`:
`auth`, `users`, `teams`, `projects`, `priorities`, `checkin`, `checkout`, `crs`, `reporting`, `ai_insights`

Si no está en la lista, solicitar confirmación antes de continuar.

## Paso 2 — Crear Estructura de Directorios

```
apps/backend/src/modules/<module>/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── router.py
│   ├── schemas.py
│   └── dependencies.py
├── application/
│   ├── __init__.py
│   ├── commands/
│   │   └── __init__.py
│   ├── queries/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── dto/
│       └── __init__.py
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   └── __init__.py
│   ├── value_objects/
│   │   └── __init__.py
│   ├── repositories/
│   │   └── __init__.py
│   └── services/
│       └── __init__.py
├── infrastructure/
│   ├── __init__.py
│   ├── repositories/
│   │   └── __init__.py
│   ├── mappers/
│   │   └── __init__.py
│   └── adapters/
│       └── __init__.py
└── tests/
    ├── __init__.py
    ├── unit/
    │   └── __init__.py
    ├── integration/
    │   └── __init__.py
    └── contract/
        └── __init__.py
```

## Paso 3 — Archivos Base a Generar

### `api/router.py`
```python
from fastapi import APIRouter, Depends
from src.shared.security.dependencies import get_current_user
from src.modules.<module>.api.schemas import (
    <Entity>Create,
    <Entity>Response,
)

router = APIRouter(prefix="/<resource>", tags=["<module>"])


@router.get(
    "/",
    response_model=list[<Entity>Response],
    summary="List <entities>",
    description="Returns a paginated list of <entities> for the current organization.",
    operation_id="list_<entities>",
)
async def list_<entities>(
    current_user=Depends(get_current_user),
):
    raise NotImplementedError
```

### `api/schemas.py`
```python
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class <Entity>Create(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # campos requeridos


class <Entity>Update(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # campos opcionales (todos Optional)


class <Entity>Response(BaseModel):
    id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime
    # campos del response
```

### `domain/entities/<entity>.py`
```python
from uuid import UUID
from dataclasses import dataclass
from src.shared.exceptions import BusinessRuleViolation


@dataclass
class <Entity>:
    id: UUID
    organization_id: UUID
    # atributos de la entidad

    def validate(self) -> None:
        """Validar invariantes de dominio."""
        if not self.organization_id:
            raise BusinessRuleViolation("BR-017: organization_id is required")
```

### `domain/repositories/<entity>_repository.py`
```python
from abc import ABC, abstractmethod
from uuid import UUID
from src.modules.<module>.domain.entities.<entity> import <Entity>


class <Entity>Repository(ABC):

    @abstractmethod
    async def get_by_id(self, id: UUID, organization_id: UUID) -> <Entity> | None:
        ...

    @abstractmethod
    async def save(self, entity: <Entity>) -> <Entity>:
        ...
```

### `infrastructure/repositories/<entity>_repository_impl.py`
```python
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.modules.<module>.domain.entities.<entity> import <Entity>
from src.modules.<module>.domain.repositories.<entity>_repository import <Entity>Repository


class SQLAlchemy<Entity>Repository(<Entity>Repository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: UUID, organization_id: UUID) -> <Entity> | None:
        # Siempre filtrar por organization_id y deleted_at IS NULL
        stmt = (
            select(...)
            .where(...id == id)
            .where(...organization_id == organization_id)
            .where(...deleted_at.is_(None))
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return self._to_entity(row) if row else None

    async def save(self, entity: <Entity>) -> <Entity>:
        raise NotImplementedError

    def _to_entity(self, row) -> <Entity>:
        raise NotImplementedError
```

### `api/dependencies.py`
```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.database.session import get_session
from src.modules.<module>.infrastructure.repositories.<entity>_repository_impl import (
    SQLAlchemy<Entity>Repository,
)


def get_<entity>_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemy<Entity>Repository:
    return SQLAlchemy<Entity>Repository(session)
```

### `tests/unit/__init__.py` y `tests/integration/__init__.py`
Vacíos — `pytest` los detecta automáticamente.

## Paso 4 — Registrar Router en main.py

Agregar en `apps/backend/src/main.py`:
```python
from src.modules.<module>.api.router import router as <module>_router

app.include_router(<module>_router, prefix="/api/v1")
```

## Paso 5 — Confirmar

```
Módulo creado: <module>

Estructura generada:
  apps/backend/src/modules/<module>/   (<N> archivos)

Archivos base con scaffolding:
  api/router.py
  api/schemas.py
  api/dependencies.py
  domain/entities/<entity>.py
  domain/repositories/<entity>_repository.py
  infrastructure/repositories/<entity>_repository_impl.py

Registrado en:
  apps/backend/src/main.py

Siguiente paso:
  1. Definir el contrato OpenAPI completo en api/schemas.py
  2. Implementar la entidad de dominio con sus BRs
  3. Crear la migración Alembic: /create-tickets <story-id> db
```
