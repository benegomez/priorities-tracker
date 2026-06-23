---
description: Inicializa el ambiente de desarrollo del proyecto una sola vez. Crea la estructura de carpetas apps/, docker-compose.yml dev, Dockerfiles, .env.example y GitHub Actions PR gate. Ejecutar ANTES del primer /create-tickets.
---

Inicializa el ambiente de desarrollo del proyecto Priorities Tracker.

## Contexto

Lee primero:
- `AmazonQ.md` — stack, puertos, módulos
- `.amazonq/rules/infrastructure-standards.md` — convenciones Docker, env vars, health checks
- `.amazonq/rules/cicd-standards.md` — separación GitHub vs GitLab, PR gate

## Cuándo Ejecutar Este Prompt

**Una sola vez**, al inicio del proyecto, antes del primer `/create-tickets`.

Si el proyecto ya tiene `docker-compose.yml` o `apps/`, este prompt no debe sobreescribir — verificar primero y solo crear lo que falta.

---

## Paso 1 — Verificar Estado Actual

Revisar qué existe en la raíz del proyecto:
- ¿Existe `apps/backend/`? ¿`apps/frontend/`?
- ¿Existe `docker-compose.yml`?
- ¿Existe `.env.example`?
- ¿Existe `.github/workflows/`?

Reportar qué existe y qué se va a crear. Solo crear lo que no existe.

---

## Paso 2 — Estructura de Carpetas

Crear la estructura base del monorepo:

```
apps/
  backend/
    src/
      main.py
      modules/        # vacío — módulos se crean con /new-module
      shared/
        config/
        database/
          migrations/ # vacío — migraciones se crean por US
        security/
        logging/
        exceptions/
    Dockerfile.dev
    requirements.txt  # dependencias base
    pyproject.toml    # config de ruff, mypy, pytest
  frontend/
    src/
      app/
      features/       # vacío — features se crean por US
      components/
        ui/
      services/
      store/
      hooks/
      lib/
      types/
      providers/
      styles/
    Dockerfile.dev
    package.json
    tsconfig.json
    next.config.ts
infrastructure/        # vacío — para futuros scripts de infra
contracts/             # vacío — OpenAPI specs por US
scripts/               # vacío — seeds y utilidades
tests/
  e2e/                 # vacío — E2E tests por US
```

---

## Paso 3 — docker-compose.yml (Desarrollo)

Crear `docker-compose.yml` en la raíz del proyecto:

```yaml
name: priorities-tracker

services:

  api:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile.dev
    container_name: priorities-tracker-api
    ports:
      - "8089:8000"
    volumes:
      - ./apps/backend:/app
    env_file:
      - .env
    environment:
      - ENVIRONMENT=development
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    networks:
      - priorities-net
    restart: unless-stopped

  frontend:
    build:
      context: ./apps/frontend
      dockerfile: Dockerfile.dev
    container_name: priorities-tracker-frontend
    ports:
      - "8901:3000"
    volumes:
      - ./apps/frontend:/app
      - /app/node_modules
    env_file:
      - .env
    depends_on:
      - api
    healthcheck:
      test: ["CMD", "wget", "-q", "-O", "/dev/null", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    networks:
      - priorities-net
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    container_name: priorities-tracker-postgres
    ports:
      - "5633:5432"
    volumes:
      - priorities-tracker_postgres-data:/var/lib/postgresql/data
    env_file:
      - .env
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    networks:
      - priorities-net
    restart: unless-stopped

volumes:
  priorities-tracker_postgres-data:

networks:
  priorities-net:
    driver: bridge
```

---

## Paso 4 — .env.example

Crear `.env.example` en la raíz (nunca `.env` — ese va en `.gitignore`):

```bash
# ── Base de Datos ──────────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://pt_user:changeme_local@postgres:5432/priorities_tracker
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

# ── IA (descomentar cuando se implemente ai_insights) ──────
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4o-mini
```

---

## Paso 5 — Archivos Base del Backend

### `apps/backend/requirements.txt`
```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
alembic>=1.13.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
httpx>=0.27.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
pytest-cov>=5.0.0
ruff>=0.4.0
mypy>=1.10.0
bandit>=1.7.0
```

### `apps/backend/src/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Priorities Tracker API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8901"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
async def health_ready() -> dict:
    # TODO: agregar validación de DB cuando shared/database esté implementado
    return {"status": "ok"}
```

---

## Paso 6 — Archivos Base del Frontend

### `apps/frontend/next.config.ts`
```typescript
import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  output: "standalone",
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
}

export default nextConfig
```

---

## Paso 7 — GitHub Actions PR Gate

Crear `.github/workflows/pr-gate.yml`:

```yaml
name: PR Gate

on:
  pull_request:
    branches: [main]

jobs:
  backend:
    name: Backend Quality Gate
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/backend

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint (ruff)
        run: ruff check src/

      - name: Type check (mypy)
        run: mypy src/ --ignore-missing-imports

      - name: Security scan (bandit)
        run: bandit -r src/ -ll

      - name: Unit tests + coverage
        run: |
          pytest src/ -m "not integration and not e2e" \
            --cov=src --cov-fail-under=80 -q

  frontend:
    name: Frontend Quality Gate
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/frontend

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: apps/frontend/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Type check
        run: npm run type-check

      - name: Lint
        run: npm run lint

      - name: Build
        run: npm run build
```

---

## Paso 8 — Verificación Final

Después de crear todos los archivos, verificar:

```bash
# Levantar el ambiente
cp .env.example .env   # editar con valores locales
docker compose up --build -d

# Verificar servicios
docker compose ps
curl http://localhost:8089/health
curl http://localhost:8901

# Verificar logs
docker compose logs api
docker compose logs frontend
docker compose logs postgres
```

---

## Paso 9 — Commit

```bash
git add -A
git commit -m "chore(infra): setup development environment

- docker-compose.yml with api, frontend, postgres services
- Dockerfile.dev for backend and frontend
- .env.example with all required variables
- apps/ folder structure for backend and frontend
- GitHub Actions PR gate workflow
- Base FastAPI app with health endpoints"

git push origin main
```

---

## Paso 10 — Confirmar

Responde con:

```
✅ Ambiente de desarrollo inicializado

Creado:
  docker-compose.yml          — servicios: api (8089), frontend (8901), postgres (5633)
  .env.example                — N variables documentadas
  apps/backend/               — estructura base FastAPI
  apps/frontend/              — estructura base Next.js
  .github/workflows/pr-gate.yml — backend + frontend quality gates

Siguiente paso:
  1. cp .env.example .env
  2. Editar .env con valores locales
  3. docker compose up --build -d
  4. Verificar: curl http://localhost:8089/health
  5. Continuar con /create-tickets <story-id>
```
