"""
Seed script for demo data.

Creates a realistic demo scenario for Org Alpha:
  - 1 team: "Equipo de Producto"
  - 1 manager: manager@org-alpha.com (already exists)
  - 5 employees with distinct CRS profiles
  - 3 projects with phases
  - 8 weeks of check-ins, check-outs, priorities, tasks and CRS scores

Profiles:
  Ana Martínez   — CRS excelente (improving)   ~92
  Carlos Ruiz    — CRS sólido (stable)          ~82
  Laura Gómez    — CRS moderado (stable)        ~74
  Diego Torres   — CRS en riesgo (declining)    ~58
  Sofía Herrera  — CRS nuevo (improving)        ~70 (solo 4 semanas)

Usage:
    docker compose exec api python scripts/seed_demo.py
"""

import asyncio
import os
from datetime import date, datetime, timedelta, timezone
from uuid import UUID

import bcrypt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://pt_user:changeme_local@postgres:5432/priorities_tracker",
)

ORG_ID = "00000000-0000-0000-0000-000000000001"
MANAGER_ID = "00000000-0000-0000-0001-000000000002"

# ── IDs fijos para idempotencia ───────────────────────────────────────────────

TEAM_ID = "00000000-0000-0000-0010-000000000001"

EMPLOYEES = [
    {
        "id": "00000000-0000-0000-0020-000000000001",
        "email": "ana.martinez@org-alpha.com",
        "first_name": "Ana",
        "last_name": "Martínez",
        "password": "Demo1234!",
        # CRS profile: excelente, improving — completa casi todo
        "profile": {"completion": 0.95, "task_completion": 0.93, "carry_rate": 0.05},
    },
    {
        "id": "00000000-0000-0000-0020-000000000002",
        "email": "carlos.ruiz@org-alpha.com",
        "first_name": "Carlos",
        "last_name": "Ruiz",
        "password": "Demo1234!",
        # CRS profile: sólido, stable
        "profile": {"completion": 0.83, "task_completion": 0.80, "carry_rate": 0.17},
    },
    {
        "id": "00000000-0000-0000-0020-000000000003",
        "email": "laura.gomez@org-alpha.com",
        "first_name": "Laura",
        "last_name": "Gómez",
        "password": "Demo1234!",
        # CRS profile: moderado, stable
        "profile": {"completion": 0.72, "task_completion": 0.68, "carry_rate": 0.28},
    },
    {
        "id": "00000000-0000-0000-0020-000000000004",
        "email": "diego.torres@org-alpha.com",
        "first_name": "Diego",
        "last_name": "Torres",
        "password": "Demo1234!",
        # CRS profile: riesgo alto, declining
        "profile": {"completion": 0.55, "task_completion": 0.50, "carry_rate": 0.45},
    },
    {
        "id": "00000000-0000-0000-0020-000000000005",
        "email": "sofia.herrera@org-alpha.com",
        "first_name": "Sofía",
        "last_name": "Herrera",
        "password": "Demo1234!",
        # CRS profile: nuevo empleado, improving — solo 4 semanas
        "profile": {"completion": 0.70, "task_completion": 0.65, "carry_rate": 0.30},
        "weeks_active": 4,
    },
]

# ── Proyectos ─────────────────────────────────────────────────────────────────

PROJECTS = [
    {
        "id": "00000000-0000-0000-0030-000000000001",
        "name": "Implementación CRM",
        "description": "Migración e implementación del nuevo sistema CRM corporativo",
        "status": "active",
        "phases": [
            {"id": "00000000-0000-0000-0031-000000000001", "name": "Descubrimiento", "status": "completed"},
            {"id": "00000000-0000-0000-0031-000000000002", "name": "Diseño", "status": "completed"},
            {"id": "00000000-0000-0000-0031-000000000003", "name": "Desarrollo", "status": "active"},
            {"id": "00000000-0000-0000-0031-000000000004", "name": "Pruebas", "status": "planned"},
        ],
    },
    {
        "id": "00000000-0000-0000-0030-000000000002",
        "name": "Portal de Clientes",
        "description": "Desarrollo del portal self-service para clientes externos",
        "status": "active",
        "phases": [
            {"id": "00000000-0000-0000-0032-000000000001", "name": "Requerimientos", "status": "completed"},
            {"id": "00000000-0000-0000-0032-000000000002", "name": "Desarrollo Frontend", "status": "active"},
            {"id": "00000000-0000-0000-0032-000000000003", "name": "Integración API", "status": "active"},
        ],
    },
    {
        "id": "00000000-0000-0000-0030-000000000003",
        "name": "Migración de Infraestructura",
        "description": "Migración de servidores on-premise a cloud",
        "status": "active",
        "phases": [
            {"id": "00000000-0000-0000-0033-000000000001", "name": "Evaluación", "status": "completed"},
            {"id": "00000000-0000-0000-0033-000000000002", "name": "Planificación", "status": "active"},
            {"id": "00000000-0000-0000-0033-000000000003", "name": "Ejecución", "status": "planned"},
        ],
    },
]

# Prioridades por empleado (rotadas entre proyectos/fases)
PRIORITY_TEMPLATES = {
    "00000000-0000-0000-0020-000000000001": [  # Ana — CRM + Portal
        ("Diseñar arquitectura de integración CRM", "high", "00000000-0000-0000-0031-000000000003"),
        ("Implementar módulo de contactos", "high", "00000000-0000-0000-0031-000000000003"),
        ("Revisar requerimientos del portal", "medium", "00000000-0000-0000-0032-000000000001"),
        ("Desarrollar componentes de autenticación", "high", "00000000-0000-0000-0032-000000000002"),
    ],
    "00000000-0000-0000-0020-000000000002": [  # Carlos — CRM + Infra
        ("Configurar entorno de desarrollo CRM", "high", "00000000-0000-0000-0031-000000000003"),
        ("Documentar APIs de integración", "medium", "00000000-0000-0000-0031-000000000003"),
        ("Evaluar proveedores cloud", "high", "00000000-0000-0000-0033-000000000001"),
        ("Preparar plan de migración", "medium", "00000000-0000-0000-0033-000000000002"),
    ],
    "00000000-0000-0000-0020-000000000003": [  # Laura — Portal + Infra
        ("Desarrollar pantallas de dashboard", "high", "00000000-0000-0000-0032-000000000002"),
        ("Integrar API de reportes", "medium", "00000000-0000-0000-0032-000000000003"),
        ("Configurar pipeline CI/CD", "medium", "00000000-0000-0000-0033-000000000002"),
        ("Documentar procedimientos de migración", "low", "00000000-0000-0000-0033-000000000002"),
    ],
    "00000000-0000-0000-0020-000000000004": [  # Diego — CRM + Portal
        ("Implementar módulo de oportunidades CRM", "high", "00000000-0000-0000-0031-000000000003"),
        ("Corregir bugs de integración", "high", "00000000-0000-0000-0031-000000000003"),
        ("Desarrollar API de notificaciones", "medium", "00000000-0000-0000-0032-000000000003"),
        ("Revisar seguridad del portal", "medium", "00000000-0000-0000-0032-000000000003"),
    ],
    "00000000-0000-0000-0020-000000000005": [  # Sofía — Portal + Infra
        ("Diseñar componentes UI del portal", "high", "00000000-0000-0000-0032-000000000002"),
        ("Implementar formularios de registro", "medium", "00000000-0000-0000-0032-000000000002"),
        ("Apoyar en evaluación de infraestructura", "low", "00000000-0000-0000-0033-000000000001"),
        ("Crear documentación técnica", "medium", "00000000-0000-0000-0033-000000000002"),
    ],
}

TASK_TEMPLATES = [
    "Análisis inicial",
    "Implementación",
    "Pruebas unitarias",
    "Code review",
    "Documentación",
]


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def get_monday(weeks_ago: int = 0) -> date:
    """Retorna el lunes de la semana actual menos N semanas."""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return monday - timedelta(weeks=weeks_ago)


def calc_crs(p_total: int, p_completed: int, t_total: int, t_completed: int,
             carry: int, history_scores: list[float]) -> tuple[float, str, str]:
    """Calcula CRS v1.0 y retorna (score, trend, risk_level)."""
    p_rate = p_completed / p_total if p_total > 0 else 0
    t_rate = t_completed / t_total if t_total > 0 else 0
    carry_factor = max(0, 1 - (carry / p_total * 0.5)) if p_total > 0 else 1

    # Consistencia histórica (promedio de últimas 4 semanas o 1.0 si no hay)
    hist = history_scores[-4:] if history_scores else []
    consistency = (sum(h / 100 for h in hist) / len(hist)) if hist else 0.75

    score = round(
        (0.40 * p_rate * 100)
        + (0.30 * t_rate * 100)
        + (0.20 * consistency * 100)
        + (0.10 * carry_factor * 100),
        2,
    )
    score = max(0, min(100, score))

    # Trend
    if len(history_scores) >= 2:
        delta = score - history_scores[-1]
        trend = "improving" if delta > 3 else ("declining" if delta < -3 else "stable")
    else:
        trend = "stable"

    # Risk level
    risk = "low" if score >= 75 else ("moderate" if score >= 60 else "high")

    return score, trend, risk


async def seed() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:

        # ── 1. Team ───────────────────────────────────────────────────────────
        await session.execute(text("""
            INSERT INTO teams (id, organization_id, manager_id, name)
            VALUES (:id, :org_id, :manager_id, :name)
            ON CONFLICT DO NOTHING
        """), {"id": TEAM_ID, "org_id": ORG_ID, "manager_id": MANAGER_ID, "name": "Equipo de Producto"})

        # ── 2. Employees ──────────────────────────────────────────────────────
        for emp in EMPLOYEES:
            hashed = hash_password(emp["password"])
            await session.execute(text("""
                INSERT INTO users
                    (id, organization_id, manager_id, team_id, email, hashed_password,
                     role, status, first_name, last_name)
                VALUES
                    (:id, :org_id, :manager_id, :team_id, :email, :hashed_password,
                     'employee', 'active', :first_name, :last_name)
                ON CONFLICT DO NOTHING
            """), {
                "id": emp["id"], "org_id": ORG_ID, "manager_id": MANAGER_ID,
                "team_id": TEAM_ID, "email": emp["email"],
                "hashed_password": hashed,
                "first_name": emp["first_name"], "last_name": emp["last_name"],
            })

        # ── 3. Projects + Phases ──────────────────────────────────────────────
        for proj in PROJECTS:
            await session.execute(text("""
                INSERT INTO projects (id, organization_id, owner_id, name, description, status)
                VALUES (:id, :org_id, :owner_id, :name, :desc, :status)
                ON CONFLICT DO NOTHING
            """), {
                "id": proj["id"], "org_id": ORG_ID, "owner_id": MANAGER_ID,
                "name": proj["name"], "desc": proj["description"], "status": proj["status"],
            })
            for phase in proj["phases"]:
                await session.execute(text("""
                    INSERT INTO project_phases (id, organization_id, project_id, name, status)
                    VALUES (:id, :org_id, :project_id, :name, :status)
                    ON CONFLICT DO NOTHING
                """), {
                    "id": phase["id"], "org_id": ORG_ID,
                    "project_id": proj["id"], "name": phase["name"], "status": phase["status"],
                })

        # ── 4. Check-ins, priorities, tasks, check-outs, CRS ─────────────────
        total_weeks = 8

        for emp in EMPLOYEES:
            emp_id = emp["id"]
            profile = emp["profile"]
            weeks_active = emp.get("weeks_active", total_weeks)
            history_scores: list[float] = []

            for week_idx in range(weeks_active - 1, -1, -1):  # oldest → newest
                week_start = get_monday(week_idx)
                is_past = week_idx > 0  # semana actual no tiene checkout

                # IDs deterministas por empleado + semana
                base = f"{emp_id[:35]}{week_idx:02d}"
                checkin_id = f"{base[:8]}-{base[8:12]}-{base[12:16]}-ci{week_idx:02d}-{base[16:28]}"
                checkout_id = f"{base[:8]}-{base[8:12]}-{base[12:16]}-co{week_idx:02d}-{base[16:28]}"

                # Normalizar a UUID válido
                import uuid as _uuid
                checkin_id = str(_uuid.uuid5(_uuid.UUID(emp_id), f"checkin-{week_start}"))
                checkout_id = str(_uuid.uuid5(_uuid.UUID(emp_id), f"checkout-{week_start}"))

                # Check-in
                ci_status = "closed" if is_past else "submitted"
                ci_submitted_at = datetime(week_start.year, week_start.month, week_start.day, 9, 0, 0, tzinfo=timezone.utc)
                await session.execute(text("""
                    INSERT INTO check_ins
                        (id, organization_id, employee_id, week_start, status, submitted_at)
                    VALUES
                        (:id, :org_id, :emp_id, :week_start, :status, :submitted_at)
                    ON CONFLICT DO NOTHING
                """), {
                    "id": checkin_id, "org_id": ORG_ID, "emp_id": emp_id,
                    "week_start": week_start, "status": ci_status,
                    "submitted_at": ci_submitted_at,
                })

                # Priorities (3 por semana, rotadas)
                templates = PRIORITY_TEMPLATES[emp_id]
                n_priorities = 3
                p_completed_count = 0
                t_total_count = 0
                t_completed_count = 0
                carry_count = 0
                priority_ids = []

                for p_idx in range(n_priorities):
                    tmpl = templates[(week_idx + p_idx) % len(templates)]
                    title, level, phase_id = tmpl
                    p_id = str(_uuid.uuid5(_uuid.UUID(emp_id), f"priority-{week_start}-{p_idx}"))
                    priority_ids.append(p_id)

                    # Determinar status de la prioridad
                    if is_past:
                        rand_val = (hash(f"{emp_id}{week_start}{p_idx}") % 100) / 100
                        if rand_val < profile["completion"]:
                            p_status = "completed"
                            p_completed_count += 1
                        elif rand_val < profile["completion"] + profile["carry_rate"]:
                            p_status = "carried_over"
                            carry_count += 1
                        else:
                            p_status = "in_progress"
                    else:
                        p_status = "in_progress"

                    await session.execute(text("""
                        INSERT INTO priorities
                            (id, organization_id, checkin_id, phase_id, owner_id,
                             week_start, title, priority_level, status)
                        VALUES
                            (:id, :org_id, :checkin_id, :phase_id, :owner_id,
                             :week_start, :title, :level, :status)
                        ON CONFLICT DO NOTHING
                    """), {
                        "id": p_id, "org_id": ORG_ID, "checkin_id": checkin_id,
                        "phase_id": phase_id, "owner_id": emp_id,
                        "week_start": week_start,
                        "title": f"{title} — S{8 - week_idx}",
                        "level": level, "status": p_status,
                    })

                    # Tasks (2 por prioridad)
                    for t_idx in range(2):
                        t_id = str(_uuid.uuid5(_uuid.UUID(emp_id), f"task-{week_start}-{p_idx}-{t_idx}"))
                        t_total_count += 1

                        if is_past:
                            rand_t = (hash(f"{emp_id}{week_start}{p_idx}{t_idx}task") % 100) / 100
                            if rand_t < profile["task_completion"]:
                                t_status = "completed"
                                t_completed_count += 1
                            else:
                                t_status = "in_progress" if p_status == "in_progress" else "pending"
                        else:
                            t_status = "in_progress" if t_idx == 0 else "pending"

                        await session.execute(text("""
                            INSERT INTO tasks
                                (id, organization_id, priority_id, title, status)
                            VALUES
                                (:id, :org_id, :priority_id, :title, :status)
                            ON CONFLICT DO NOTHING
                        """), {
                            "id": t_id, "org_id": ORG_ID, "priority_id": p_id,
                            "title": TASK_TEMPLATES[t_idx % len(TASK_TEMPLATES)],
                            "status": t_status,
                        })

                # Check-out + CRS (solo semanas pasadas)
                if is_past:
                    co_status = "closed"
                    co_submitted_at = datetime(week_start.year, week_start.month, week_start.day, tzinfo=timezone.utc) + timedelta(days=5, hours=17)
                    await session.execute(text("""
                        INSERT INTO check_outs
                            (id, organization_id, employee_id, checkin_id, week_start,
                             status, submitted_at, notes)
                        VALUES
                            (:id, :org_id, :emp_id, :checkin_id, :week_start,
                             :status, :submitted_at, :notes)
                        ON CONFLICT DO NOTHING
                    """), {
                        "id": checkout_id, "org_id": ORG_ID, "emp_id": emp_id,
                        "checkin_id": checkin_id,
                        "week_start": week_start,
                        "week_start2": week_start,
                        "status": co_status,
                        "submitted_at": co_submitted_at,
                        "notes": f"Semana {8 - week_idx} completada. {p_completed_count}/{n_priorities} prioridades cumplidas.",
                    })

                    # Marcar prioridades completadas con checkout
                    await session.execute(text("""
                        UPDATE priorities
                        SET completed_in_checkout = :checkout_id
                        WHERE checkin_id = :checkin_id
                          AND status = 'completed'
                          AND completed_in_checkout IS NULL
                    """), {"checkout_id": checkout_id, "checkin_id": checkin_id})

                    # CRS
                    score, trend, risk = calc_crs(
                        n_priorities, p_completed_count,
                        t_total_count, t_completed_count,
                        carry_count, history_scores,
                    )
                    history_scores.append(score)

                    crs_id = str(_uuid.uuid5(_uuid.UUID(emp_id), f"crs-{week_start}"))
                    await session.execute(text("""
                        INSERT INTO crs_scores
                            (id, organization_id, employee_id, checkout_id, week_start,
                             score, trend, risk_level, formula_version,
                             priorities_total, priorities_completed,
                             tasks_total, tasks_completed)
                        VALUES
                            (:id, :org_id, :emp_id, :checkout_id, :week_start,
                             :score, :trend, :risk, 'v1.0',
                             :p_total, :p_completed, :t_total, :t_completed)
                        ON CONFLICT DO NOTHING
                    """), {
                        "id": crs_id, "org_id": ORG_ID, "emp_id": emp_id,
                        "checkout_id": checkout_id,
                        "week_start": week_start,
                        "score": score, "trend": trend, "risk": risk,
                        "p_total": n_priorities, "p_completed": p_completed_count,
                        "t_total": t_total_count, "t_completed": t_completed_count,
                    })

        await session.commit()

    await engine.dispose()

    print("✅ Demo seed completed successfully.")
    print("\n── Equipo de Producto ──────────────────────────────────────────")
    print(f"  Manager: manager@org-alpha.com  /  Manager1234!")
    print("\n── Empleados ───────────────────────────────────────────────────")
    for emp in EMPLOYEES:
        weeks = emp.get("weeks_active", 8)
        print(f"  {emp['first_name']:8s} {emp['last_name']:10s}  {emp['email']:35s}  pw: {emp['password']}  ({weeks} semanas)")
    print("\n── Proyectos ───────────────────────────────────────────────────")
    for proj in PROJECTS:
        print(f"  {proj['name']}  ({len(proj['phases'])} fases)")
    print("\n── Semanas generadas ───────────────────────────────────────────")
    for i in range(7, -1, -1):
        w = get_monday(i)
        label = " ← semana actual" if i == 0 else ""
        print(f"  {w.isoformat()}{label}")


if __name__ == "__main__":
    asyncio.run(seed())
