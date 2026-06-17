# Coding Standards

## Python

- Python 3.13+
- Type Hints obligatorios
- Ruff
- Black
- MyPy

## FastAPI

- Async por defecto
- Dependency Injection
- Pydantic v2

## Convenciones

snake_case:
- variables
- funciones

PascalCase:
- clases

UPPER_CASE:
- constantes

## Reglas

- Sin lógica de negocio en routers.
- Sin acceso directo a DB desde casos de uso.
