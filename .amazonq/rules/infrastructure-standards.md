---
description: "Estándares de infraestructura local de desarrollo para Priorities Tracker. Docker Compose First según ADR-004."
globs: "docker-compose*.yml, **/Dockerfile*, .env.example, infrastructure/**/*"
alwaysApply: false
---

# Infrastructure Standards — Priorities Tracker

## Principio Rector

La infraestructura de desarrollo debe ser simple, reproducible y Kubernetes-compatible desde el primer día.

> "Docker Compose First → Operational Maturity → Kubernetes." — ADR-004

---

## Separación de Ambientes

| Artefacto | Repositorio | Responsable |
|---|---|---|
| `docker-compose.yml` (desarrollo) | GitHub `priorities-tracker` | Este proyecto |
| `docker-compose.yml` (producción) | GitLab `priorities-tracker-deploy` | Repo de deploy |
| Dockerfiles de desarrollo | GitHub | Este proyecto |
| Dockerfiles de producción | GitLab | Repo de deploy |
| Variables reales por ambiente | GitLab CI/CD Variables | Repo de deploy |
| `.env.example` | GitHub | Este proyecto |

**Nunca** poner valores reales de producción en el repositorio GitHub.

---

## Servicios del Stack de Desarrollo (MVP)

| Servicio | Imagen | Puerto host | Puerto interno | Red interna |
|---|---|---|---|---|
| `api` | build local | `8089` | `8000` | `priorities-net` |
| `frontend` | build local | `8901` | `3000` | `priorities-net` |
| `postgres` | `postgres:16-alpine` | `5633` | `5432` | `priorities-net` |

Servicios futuros (cuando una US los requiera):
- `redis` — cache y rate limiting
- `ai-gateway` — proxy de LLM

---

## Convenciones de Nomenclatura

```yaml
# Nombre del proyecto Docker Compose
name: priorities-tracker

# Nombres de servicios: kebab-case, singular
services:
  api:
  frontend:
  postgres:
  redis:          # cuando se agregue

# Nombres de volúmenes: <proyecto>_<dato>
volumes:
  priorities-tracker_postgres-data:

# Nombre de red interna
networks:
  priorities-net:
    driver: bridge
```

---

## Estándares de Dockerfile (Desarrollo)

### Backend (`apps/backend/Dockerfile.dev`)
```dockerfile
FROM python:3.13-slim

# Un proceso por contenedor
# Imagen mínima (slim)
# Sin secretos en el Dockerfile
# WORKDIR explícito
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Health check obligatorio
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Frontend (`apps/frontend/Dockerfile.dev`)
```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget -q -O /dev/null http://localhost:3000 || exit 1

CMD ["npm", "run", "dev"]
```

---

## Estándares de Variables de Entorno

### Reglas
- **Nunca** valores reales en código fuente o en el repo
- `.env` en `.gitignore` — nunca commiteado
- `.env.example` commiteado — documenta todas las variables sin valores reales
- Cada variable tiene un comentario explicativo en `.env.example`

### Formato de `.env.example`
```bash
# ── Base de Datos ──────────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/priorities_tracker
POSTGRES_DB=priorities_tracker
POSTGRES_USER=pt_user
POSTGRES_PASSWORD=changeme_local

# ── JWT ────────────────────────────────────────────────────
# Generar con: openssl rand -hex 32
JWT_SECRET=changeme_generate_with_openssl
JWT_REFRESH_SECRET=changeme_generate_with_openssl
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# ── Backend ────────────────────────────────────────────────
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# ── Frontend ───────────────────────────────────────────────
NEXT_PUBLIC_API_URL=http://localhost:8089

# ── IA (agregar cuando se implemente ai_insights) ──────────
# OPENAI_API_KEY=sk-...
```

### Cuándo actualizar `.env.example`
Cada vez que un ticket backend introduce una nueva variable de entorno, **el ticket debe incluir** la actualización de `.env.example` como criterio de aceptación.

---

## Health Checks Obligatorios

Todo servicio debe exponer un health check:

| Servicio | Endpoint | Respuesta esperada |
|---|---|---|
| `api` | `GET /health` | `{"status": "ok"}` — 200 |
| `api` | `GET /health/ready` | `{"status": "ok", "db": "ok"}` — 200 |
| `frontend` | `GET /` | HTTP 200 |
| `postgres` | `pg_isready` | exit 0 |

El health check de `api` debe verificar conectividad con PostgreSQL antes de retornar `ready`.

---

## Compatibilidad Kubernetes (Obligatorio desde día 1)

Siguiendo ADR-004, cada contenedor debe cumplir:

- ✅ **Stateless** — sin estado en el filesystem del contenedor
- ✅ **Configuración externalizada** — toda config via env vars
- ✅ **Health checks** — readiness y liveness
- ✅ **Un proceso por contenedor**
- ✅ **Imagen reproducible** — build determinístico desde source control
- ✅ **Sin secretos en la imagen**

---

## Cuándo Agregar un Nuevo Servicio al Compose

Un nuevo servicio se agrega al `docker-compose.yml` cuando:
1. Una US declara en su `[enhanced]` una nueva dependencia técnica de infraestructura
2. Se crea un ticket `infra/ticket.md` específico para ese servicio
3. El ticket incluye: imagen, puertos, variables de entorno necesarias, health check

**No agregar servicios "por si acaso"** — solo cuando una US los requiere.

---

## Referencias

- [docs/02-arquitectura/ADR/ADR-004-Kubernetes-Migration-Path.md](../../docs/02-arquitectura/ADR/ADR-004–Kubernetes-Migration-Path.md)
- [docs/02-arquitectura/contenedores.md](../../docs/02-arquitectura/contenedores.md)
- [.amazonq/rules/cicd-standards.md](./cicd-standards.md)
- [.amazonq/rules/security-standards.md](./security-standards.md)
