---
description: "Estándares de diseño y gobernanza de APIs para Priorities Tracker. API First + OpenAPI Contract First según ADR-008 y ADR-009."
globs: "**/api/**/*.py, **/schemas/**/*.py, contracts/**/*.yaml, contracts/**/*.yml"
alwaysApply: false
---

# API Standards — Priorities Tracker

## Principio Rector

El contrato precede a la implementación. La especificación OpenAPI es la fuente de verdad — no el código.

> "Contract before code." — ADR-009

---

## Ciclo de Vida Obligatorio

Todo endpoint nuevo sigue este orden sin excepción:

```
Requerimiento funcional (FR-XXX)
    ↓
Diseño del contrato OpenAPI
    ↓
Revisión y aprobación del contrato
    ↓
Implementación en FastAPI
    ↓
Validación con schemathesis
    ↓
Release
```

Nunca implementar un endpoint sin contrato aprobado primero.

---

## Estructura de Recursos REST

### Prefijo base obligatorio
```
/api/v1/
```

### Recursos del MVP

| Recurso | Path |
|---|---|
| Auth | `/api/v1/auth` |
| Users | `/api/v1/users` |
| Teams | `/api/v1/teams` |
| Projects | `/api/v1/projects` |
| Project Phases | `/api/v1/projects/{id}/phases` |
| Priorities | `/api/v1/priorities` |
| Tasks | `/api/v1/priorities/{id}/tasks` |
| Check-Ins | `/api/v1/checkins` |
| Check-Outs | `/api/v1/checkouts` |
| CRS | `/api/v1/crs` |
| Reports | `/api/v1/reports` |
| Planning Cycles | `/api/v1/planning-cycles` |

### Convenciones de naming
- Recursos en `kebab-case` plural: `/project-phases`, `/planning-cycles`
- IDs siempre como path parameter: `/{id}`
- Acciones como sub-recursos: `/checkins/{id}/submit`
- Sin verbos en paths: ~~`/createCheckin`~~

---

## Estándares HTTP

| Operación | Método | Status exitoso |
|---|---|---|
| Crear | `POST` | `201 Created` |
| Leer uno | `GET` | `200 OK` |
| Leer lista | `GET` | `200 OK` |
| Actualizar parcial | `PATCH` | `200 OK` |
| Actualizar completo | `PUT` | `200 OK` |
| Eliminar (soft) | `DELETE` | `204 No Content` |
| Acción | `POST` | `200 OK` |

---

## Versionado

- Versión actual: `v1`
- Cambios breaking → nueva versión: `v2`
- Cambios no-breaking → misma versión
- Nunca eliminar campos de response en la misma versión

---

## Estructura de Errores (Obligatoria)

Todos los errores deben seguir este schema:

```json
{
  "error_code": "PRIORITY_NOT_FOUND",
  "message": "Priority with id X was not found",
  "correlation_id": "uuid-v4",
  "details": {}
}
```

### Códigos HTTP de error estándar

| Situación | Status |
|---|---|
| Recurso no encontrado | `404 Not Found` |
| Acción no autorizada | `403 Forbidden` |
| No autenticado | `401 Unauthorized` |
| Validación de entrada | `400 Bad Request` |
| Conflicto de negocio (ej. duplicate check-in) | `409 Conflict` |
| Error interno | `500 Internal Server Error` |

### Excepciones de dominio → HTTP

| Excepción | Status |
|---|---|
| `DomainException` | `400` |
| `ValidationException` | `400` |
| `AuthorizationException` | `403` |
| `BusinessRuleViolation` | `409` |

---

## Estándares OpenAPI

### Cada endpoint debe documentar:
- `summary` — una línea descriptiva
- `description` — comportamiento, reglas de negocio relevantes
- `response_model` — schema Pydantic tipado
- `responses` — todos los status codes posibles (200/201, 400, 401, 403, 404, 409)
- `tags` — alineado con el módulo (`checkin`, `priorities`, etc.)
- `operation_id` — único, en snake_case

### Ejemplo de anotación FastAPI:
```python
@router.post(
    "/",
    response_model=CheckInResponse,
    status_code=201,
    summary="Create a weekly check-in",
    description="Creates a new check-in for the current week. Only one check-in per employee per week is allowed (BR-001).",
    responses={
        409: {"description": "Check-in already exists for this week"},
        403: {"description": "Insufficient permissions"},
    },
    tags=["checkin"],
    operation_id="create_checkin",
)
```

---

## Schemas Pydantic (Convenciones)

### Separación obligatoria por operación:
- `<Entity>Create` — campos requeridos para crear
- `<Entity>Update` — campos opcionales para actualizar (todos `Optional`)
- `<Entity>Response` — campos retornados al cliente
- `<Entity>ListResponse` — wrapper paginado

### Schemas compartidos (usar siempre):
- `UUIDResponse` — para respuestas con solo ID
- `PaginationRequest` — para parámetros de paginación
- `PaginationResponse` — para listas paginadas
- `ErrorResponse` — para errores estándar
- `AuditFieldsResponse` — `created_at`, `updated_at`

### Ejemplo de schema:
```python
class CheckInCreate(BaseModel):
    week_start: date
    notes: str | None = None

    model_config = ConfigDict(json_schema_extra={
        "example": {"week_start": "2025-01-06", "notes": "Planning week 2"}
    })

class CheckInResponse(AuditFieldsResponse):
    id: UUID
    employee_id: UUID
    week_start: date
    status: CheckInStatus
```

---

## Paginación

Todas las listas deben soportar paginación:

```
GET /api/v1/priorities?page=1&page_size=20
```

Response wrapper obligatorio:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

---

## Health y Observabilidad

Endpoints obligatorios:
- `GET /health` — liveness check, retorna `{"status": "ok"}`
- `GET /health/ready` — readiness check con validación de DB

Todos los requests deben incluir en los logs:
- `correlation_id` (header `X-Correlation-ID` o generado automáticamente)
- `request_id`
- método HTTP, path, status code, duración

---

## Reglas Obligatorias

- Nunca exponer stack traces en respuestas de error en producción
- Nunca retornar campos de contraseña o secretos en ningún response
- Todo endpoint que modifica datos requiere autenticación JWT
- Todo endpoint debe validar `organization_id` del token (multi-tenant)
- Los IDs expuestos en la API siempre son `UUID` — nunca IDs internos secuenciales
- `SELECT *` nunca en queries que alimentan responses de API

---

## Referencias

- [docs/02-arquitectura/ADR/ADR-008-API-First-Strategy-Enterprise-Final.md](../../docs/02-arquitectura/ADR/ADR-008-API-First-Strategy-Enterprise-Final.md)
- [docs/02-arquitectura/ADR/ADR-009-OpenAPI-Contract-First-Enterprise-Final.md](../../docs/02-arquitectura/ADR/ADR-009-OpenAPI-Contract-First-Enterprise-Final.md)
- [docs/06-api-implementation/api-overview.md](../../docs/06-api-implementation/api-overview.md)
- [docs/06-api-implementation/shared-schemas.md](../../docs/06-api-implementation/shared-schemas.md)
- [docs/06-api-implementation/application-errors.md](../../docs/06-api-implementation/application-errors.md)
- [docs/06-api-implementation/pydantic-conventions.md](../../docs/06-api-implementation/pydantic-conventions.md)
