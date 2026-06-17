---
description: "Estándares de seguridad para Priorities Tracker. JWT, RBAC, multi-tenant, auditoría y principios Security by Design."
globs: "**/security/**/*.py, **/auth/**/*.py, **/middleware/**/*.py"
alwaysApply: false
---

# Security Standards — Priorities Tracker

## Principio Rector

La seguridad se diseña desde el inicio — no se agrega después.

> "Security by Design. Zero Trust. Least Privilege. Defense in Depth." — security-architecture.md

---

## Autenticación — JWT

### Tokens
- **Access Token** — vida corta, incluido en cada request
- **Refresh Token** — vida larga, para renovar el access token

### Payload obligatorio del JWT
```json
{
  "sub": "<user_id>",
  "organization_id": "<org_id>",
  "role": "employee | manager | administrator",
  "exp": "<timestamp>"
}
```

### Reglas
- Todo endpoint protegido valida el JWT antes de ejecutar lógica
- El `organization_id` se extrae **siempre del token**, nunca del body ni query params
- Tokens expirados retornan `401 Unauthorized`
- Tokens con firma inválida retornan `401 Unauthorized`
- El secreto JWT solo existe en variables de entorno — nunca en código

---

## Autorización — RBAC

### Roles y permisos

| Rol | Permisos |
|---|---|
| `administrator` | Gestión completa de la organización: usuarios, equipos, proyectos |
| `manager` | Consultar equipo, consultar CRS del equipo, ver dashboards |
| `employee` | Gestionar sus propias prioridades, check-in, check-out |

### Matriz de acceso por operación

| Operación | employee | manager | administrator |
|---|---|---|---|
| Crear check-in propio | ✅ | ✅ | ✅ |
| Ver check-ins del equipo | ❌ | ✅ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ✅ |
| Ver CRS propio | ✅ | ✅ | ✅ |
| Ver CRS del equipo | ❌ | ✅ | ✅ |
| Crear proyectos | ❌ | ❌ | ✅ |
| Ver reportes de equipo | ❌ | ✅ | ✅ |

### Reglas de implementación
- La verificación de rol se hace en `dependencies.py` de cada módulo, no en el router
- Un `employee` que intenta acceder a recursos de otro usuario recibe `403 Forbidden`
- Un `manager` solo accede a usuarios de su equipo — nunca a otros equipos
- Las verificaciones de RBAC van **antes** de cualquier query a la base de datos

---

## Multi-Tenant (Tenant Isolation)

El aislamiento por organización es una regla de seguridad, no solo de datos.

### Reglas obligatorias
- Todo query incluye `WHERE organization_id = :org_id` — sin excepción
- El repositorio base `OrganizationScopedRepository` aplica este filtro automáticamente
- Ningún endpoint acepta `organization_id` como parámetro de entrada del cliente
- Acceder a datos de otra organización retorna `403 Forbidden` — nunca `404`
- Los tests de seguridad deben verificar aislamiento cross-tenant explícitamente

---

## Validación de Entrada

- Toda entrada pasa por validación Pydantic antes de llegar a la capa de aplicación
- Campos inesperados se rechazan (`model_config = ConfigDict(extra="forbid")` en schemas de creación)
- Tipos incorrectos retornan `400 Bad Request` con detalle del campo
- Longitudes máximas definidas en todos los campos de texto
- UUIDs validados como tipo `UUID`, no como `str`

---

## Gestión de Secretos

Los siguientes valores **nunca** van en código fuente ni en el repositorio GitHub:

```
DATABASE_URL
JWT_SECRET
JWT_REFRESH_SECRET
OPENAI_API_KEY
SMTP_PASSWORD
DOCKER_REGISTRY_TOKEN
```

- Se gestionan como variables de entorno
- En producción: GitLab CI/CD Variables (masked + protected)
- En desarrollo local: archivo `.env` excluido del repositorio vía `.gitignore`
- El archivo `.env.example` documenta las variables requeridas sin valores reales

---

## Eventos de Auditoría

Los siguientes eventos deben generar un registro de auditoría con `user_id`, `organization_id`, `timestamp`, y detalle de la acción:

| Evento | Criticidad |
|---|---|
| Login exitoso | Alta |
| Login fallido | Alta |
| Logout | Media |
| Cambio de rol de usuario | Alta |
| Check-In creado | Media |
| Check-In enviado | Media |
| Check-Out enviado | Media |
| CRS recalculado | Alta |
| Uso de IA | Media |

### Formato de log estructurado (JSON)
```json
{
  "event": "checkin.submitted",
  "user_id": "<uuid>",
  "organization_id": "<uuid>",
  "correlation_id": "<uuid>",
  "timestamp": "2025-01-06T10:00:00Z",
  "metadata": {}
}
```

---

## Seguridad en la API

- HTTPS obligatorio en todos los ambientes excepto desarrollo local
- Header `X-Correlation-ID` propagado en todos los requests para trazabilidad
- Rate limiting aplicado en endpoints de autenticación (`/auth/login`, `/auth/refresh`)
- Nunca exponer stack traces en responses de producción
- Nunca incluir información de infraestructura en mensajes de error al cliente

---

## Seguridad en Contenedores

- Imágenes Docker construidas desde base images oficiales y versionadas
- Escaneo de vulnerabilidades con `trivy` en cada build del pipeline
- Cero vulnerabilidades críticas como condición de deploy
- Variables de entorno inyectadas en runtime — nunca en el `Dockerfile`

---

## Reglas Obligatorias

- Todo endpoint que no sea público requiere `Depends(get_current_user)`
- Los tests de seguridad son obligatorios para flujos críticos (ver [testing-standards.md](./testing-standards.md))
- Un endpoint que devuelve `200` sin credenciales válidas en un recurso protegido es un bug crítico
- Las dependencias Python se auditan con `pip-audit` en cada PR
- `bandit` debe pasar sin findings de severidad alta o crítica

---

## Referencias

- [docs/02-arquitectura/security-architecture.md](../../docs/02-arquitectura/security-architecture.md)
- [docs/06-api-implementation/security-implementation.md](../../docs/06-api-implementation/security-implementation.md)
- [docs/06-api-implementation/authorization-matrix.md](../../docs/06-api-implementation/authorization-matrix.md)
- [docs/06-api-implementation/multi-tenant-design.md](../../docs/06-api-implementation/multi-tenant-design.md)
- [docs/02-arquitectura/principles/architecture-principles-v1.0-FINAL.md](../../docs/02-arquitectura/principles/architecture-principles-v1.0-FINAL.md)
