from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.modules.auth.api.router import limiter, router as auth_router
from src.modules.checkin.api.router import router as checkin_router
from src.modules.priorities.api.router import router as priorities_router
from src.modules.checkout.api.router import router as checkout_router
from src.modules.projects.api.router import router as projects_router
from src.modules.crs.api.router import router as crs_router

app = FastAPI(
    title="Priorities Tracker API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8901"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(checkin_router, prefix="/api/v1")
app.include_router(priorities_router, prefix="/api/v1")
app.include_router(checkout_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(crs_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
async def health_ready() -> dict[str, str]:
    return {"status": "ok"}
