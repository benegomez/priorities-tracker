---
description: "Estándares de testing para Priorities Tracker. Risk-Based Testing Strategy según ADR-005."
globs: "**/tests/**/*.py, **/*.test.ts, **/*.spec.ts, **/*.test.tsx, **/*.spec.tsx"
alwaysApply: false
---

# Testing Standards — Priorities Tracker

## Principio Rector

Testing es una inversión proporcional al riesgo.

No se busca cobertura uniforme — se busca máxima confianza en los flujos críticos con mínimo costo de mantenimiento.

> "Coverage is an indicator, not a goal." — development-standards.md

---

## Clasificación de Riesgo

Cada cambio debe clasificarse antes de determinar qué tests son obligatorios.

| Nivel | Ejemplos | Tests Requeridos |
|---|---|---|
| **Low** | Docs, UI text, refactoring menor | Code Review + Unit Tests |
| **Medium** | Nuevas features, mejoras de API, reporting | Unit + Integration |
| **High** | Cambios de schema, integraciones, infraestructura | Unit + Integration + Contract + Security |
| **Critical** | Auth, Check-In, Check-Out, CRS, Planning Cycle | Unit + Integration + Contract + E2E + Security |

**Regla por módulo:** independientemente del nivel de riesgo de la US, los módulos `auth`, `checkin`, `checkout` y `crs` son siempre **Critical**.

---

## Matriz de Decisión: Riesgo × Complejidad

Cuando se crea un ticket, cruzar el **nivel de riesgo** de la US con su **complejidad estimada** para determinar qué tests son obligatorios y el umbral de cobertura:

| Nivel de Riesgo | Complejidad | Unit | Integration | Contract | E2E | Security | Cobertura mínima |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| Low | XS / S | ✅ | ❌ | ❌ | ❌ | ❌ | >60% |
| Medium | S / M | ✅ | ✅ | ❌ | ❌ | ❌ | >80% |
| High | M / L | ✅ | ✅ | ✅ | ❌ | ✅ | >80% |
| Critical | L / XL | ✅ | ✅ | ✅ | ✅ | ✅ | >95% |

### Cómo aplicar la matriz
1. Leer el `nivel de riesgo` y la `complejidad estimada` de la sección `[enhanced]` de la US
2. Localizar la fila correspondiente en la matriz
3. Incluir únicamente los tipos de test marcados con ✅ en el ticket
4. Aplicar el umbral de cobertura como condición de merge en el PR gate

---

## Pirámide de Tests

### Unit Tests
- Validan reglas de negocio en aislamiento
- Sin I/O real (mocks para repositorios y servicios externos)
- Feedback rápido — deben ejecutarse en segundos

**Cobertura mínima:**
- Lógica de negocio general: `>80%`
- Flujos críticos (auth, check-in, check-out, CRS): `>95%`

### Integration Tests
- Validan interacción entre capas reales: repositorios + PostgreSQL
- Usan `testcontainers` para levantar PostgreSQL en el test
- Validan comportamiento de `UnitOfWork` (commit y rollback)
- Validan queries ORM contra esquema real

### Contract Tests
- Validan que la API cumple el contrato OpenAPI
- Herramienta: `schemathesis`
- Obligatorios para flujos High y Critical
- Se ejecutan contra el servidor real o TestClient de FastAPI

### End-to-End Tests
- Validan flujos completos desde el navegador
- Herramienta: `Playwright`
- Solo para flujos Critical — no se escriben E2E para todo
- Flujos obligatorios en MVP: Check-In, Check-Out, CRS, Auth

---

## Stack de Testing Oficial

### Backend

| Herramienta | Propósito |
|---|---|
| `pytest` | Runner principal |
| `pytest-cov` | Cobertura |
| `pytest-asyncio` | Tests async (FastAPI + SQLAlchemy async) |
| `httpx` + `AsyncClient` | Tests de endpoints FastAPI |
| `testcontainers` | PostgreSQL real en integration tests |
| `factory_boy` | Fixtures y datos de prueba |
| `schemathesis` | Contract testing contra OpenAPI |
| `bandit` | SAST — análisis de seguridad estático |
| `pip-audit` | Vulnerabilidades en dependencias |

### Frontend

| Herramienta | Propósito |
|---|---|
| `vitest` | Runner + unit tests |
| `@testing-library/react` | Tests de componentes |
| `Playwright` | E2E tests |

### Platform

| Herramienta | Propósito |
|---|---|
| `k6` | Performance smoke tests |
| `trivy` | Scan de imágenes Docker |

---

## Estructura de Tests por Módulo (Backend)

Los tests viven dentro del módulo al que pertenecen:

```
src/modules/<module>/tests/
├── unit/
│   ├── test_<entity>_entity.py
│   ├── test_<usecase>_command.py
│   └── test_<service>_domain.py
├── integration/
│   ├── test_<entity>_repository.py
│   └── test_<module>_uow.py
└── contract/
    └── test_<module>_api_contract.py
```

Tests E2E viven en la raíz del proyecto:

```
src/tests/
├── unit/
├── integration/
└── e2e/
    ├── test_checkin_flow.py
    ├── test_checkout_flow.py
    └── test_crs_flow.py
```

---

## Convenciones de Nomenclatura

| Elemento | Convención | Ejemplo |
|---|---|---|
| Archivos de test | `test_<subject>.py` | `test_create_checkin.py` |
| Clases de test | `Test<Subject>` | `TestCreateCheckIn` |
| Funciones de test | `test_<scenario>_<expected_result>` | `test_create_checkin_returns_draft_status` |
| Fixtures | `snake_case` descriptivo | `checkin_repository`, `mock_crs_service` |

---

## Patrones Obligatorios

### Tests de Use Cases (Unit)

```python
# Arrange
mock_repo = Mock(spec=CheckInRepository)
mock_uow = Mock(spec=UnitOfWork)
command = CreateCheckInCommand(user_id=..., week_start=...)

# Act
result = await CreateCheckInUseCase(mock_uow).execute(command)

# Assert
assert result.status == PlanningCycleStatus.DRAFT
mock_uow.commit.assert_called_once()
```

### Tests de Repositorios (Integration)

```python
@pytest.mark.integration
async def test_checkin_repository_saves_and_retrieves(db_session):
    repo = CheckInRepository(db_session)
    checkin = CheckInFactory.build()
    await repo.save(checkin)
    result = await repo.get_by_id(checkin.id)
    assert result.id == checkin.id
```

### Tests de UnitOfWork (Integration)

- Verificar que `commit()` persiste los cambios
- Verificar que `rollback()` revierte los cambios
- Verificar que el scope de sesión no filtra entre tests

### Tests de Endpoints (Integration vía httpx)

```python
async def test_post_checkin_returns_201(async_client: AsyncClient, auth_headers):
    response = await async_client.post("/api/v1/checkins", json={...}, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["status"] == "draft"
```

---

## Fixtures y Datos de Prueba

- Usar `factory_boy` para generar entidades de prueba — nunca hardcodear UUIDs ni datos reales
- Fixtures de base de datos deben usar transacciones revertidas entre tests (`rollback` al teardown)
- No compartir estado mutable entre tests
- Fixtures de autenticación deben cubrir los tres roles: `administrator`, `manager`, `employee`

```python
# conftest.py
@pytest.fixture
def admin_headers(test_user_admin):
    return {"Authorization": f"Bearer {generate_test_token(test_user_admin)}"}

@pytest.fixture
def manager_headers(test_user_manager):
    return {"Authorization": f"Bearer {generate_test_token(test_user_manager)}"}
```

---

## Módulos Críticos — Tests Obligatorios

Los siguientes módulos requieren el nivel máximo de cobertura:

| Módulo | Flujos Críticos a Testear |
|---|---|
| `auth` | Login, refresh token, token expirado, acceso no autorizado |
| `checkin` | Crear, enviar, validar duplicado por semana, RBAC |
| `checkout` | Cerrar ciclo, carry-over de prioridades, RBAC |
| `crs` | Cálculo del score, histórico, edge cases (0 prioridades, todas completadas) |
| `priorities` | CRUD, cambio de estado, asociación a proyecto/fase |

---

## Reglas Obligatorias

- No mockear la base de datos en integration tests — usar `testcontainers`
- No escribir tests que dependan del orden de ejecución
- Todo test de endpoint debe validar el status code **y** el schema de respuesta
- Los tests de seguridad deben verificar que endpoints protegidos retornan `401`/`403` sin credenciales válidas
- No usar `time.sleep()` en tests — usar mocks de tiempo o fixtures de fecha
- Marcar explícitamente los tests lentos con `@pytest.mark.slow` para poder excluirlos en el PR gate

---

## Quality Gates (resumen ejecutable)

| Gate | Condición de falla |
|---|---|
| PR Gate | Unit tests fallan, coverage <80%, bandit findings críticos |
| Release Gate | Integration tests fallan, contract tests fallan, E2E críticos fallan |
| Producción | 0 vulnerabilidades críticas en imagen (trivy) |

---

## Trazabilidad

Todo test crítico debe poder trazarse a un requerimiento funcional:

```
FR-014 Check-In Creation
    → test_create_checkin_returns_draft_status
    → test_create_checkin_rejects_duplicate_week
    → test_create_checkin_requires_authentication
```

---

## Referencias

- [docs/02-arquitectura/ADR/ADR-005-Risk-Based-Testing-Strategy.md](../../docs/02-arquitectura/ADR/ADR-005-Risk-Based-Testing-Strategy.md)
- [docs/03-backend/testing-strategy.md](../../docs/03-backend/testing-strategy.md)
- [docs/06-api-implementation/testing-strategy.md](../../docs/06-api-implementation/testing-strategy.md)
- [docs/06-api-implementation/repository-pattern.md](../../docs/06-api-implementation/repository-pattern.md)
- [docs/06-api-implementation/unit-of-work.md](../../docs/06-api-implementation/unit-of-work.md)
- [docs/08-Engineering-Delivery/development-standards.md](../../docs/08–Engineering-Delivery/development-standards.md)
