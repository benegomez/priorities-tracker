"""
Seed 4 weeks of check-in/check-out/CRS data for multiple employees.
Creates 3 new employees under manager@org-alpha.com and generates
realistic weekly data for team visibility and AI features.

Usage:
    docker compose exec api python scripts/seed_multi_week.py
"""
import asyncio
import os
import random
from datetime import date, timedelta
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://pt_user:changeme_local@postgres:5432/priorities_tracker",
)

ORG_ID = UUID("00000000-0000-0000-0000-000000000001")
MANAGER_ID = UUID("00000000-0000-0000-0001-000000000002")
EXISTING_EMPLOYEE_ID = UUID("00000000-0000-0000-0001-000000000003")

# New employees to create
NEW_EMPLOYEES = [
    {"id": UUID("00000000-0000-0000-0001-000000000005"), "email": "carlos@org-alpha.com", "first_name": "Carlos", "last_name": "Rivera"},
    {"id": UUID("00000000-0000-0000-0001-000000000006"), "email": "maria@org-alpha.com", "first_name": "María", "last_name": "González"},
    {"id": UUID("00000000-0000-0000-0001-000000000007"), "email": "andres@org-alpha.com", "first_name": "Andrés", "last_name": "López"},
]

# All employees (existing + new)
ALL_EMPLOYEES = [
    {"id": EXISTING_EMPLOYEE_ID, "name": "Employee Alpha"},
    {"id": UUID("00000000-0000-0000-0001-000000000005"), "name": "Carlos Rivera"},
    {"id": UUID("00000000-0000-0000-0001-000000000006"), "name": "María González"},
    {"id": UUID("00000000-0000-0000-0001-000000000007"), "name": "Andrés López"},
]

# Phases to use
PHASES = [
    UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"),  # Desarrollo
    UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),  # Descubrimiento
    UUID("dddddddd-dddd-dddd-dddd-dddddddddddd"),  # Pruebas
]

# Priority titles pool (realistic)
PRIORITY_TITLES = [
    "Implementar endpoint de reportes",
    "Refactorizar servicio de autenticación",
    "Diseñar mockups del dashboard",
    "Configurar pipeline CI/CD",
    "Escribir documentación de API",
    "Optimizar queries de base de datos",
    "Implementar notificaciones por email",
    "Crear componentes de formulario",
    "Migrar datos legacy",
    "Implementar filtros de búsqueda",
    "Agregar validaciones de entrada",
    "Configurar monitoreo de errores",
    "Diseñar modelo de datos para reportes",
    "Implementar exportación a CSV",
    "Crear tests de integración",
    "Optimizar carga de imágenes",
    "Implementar paginación en listados",
    "Configurar caché de respuestas",
    "Diseñar flujo de onboarding",
    "Implementar sistema de permisos",
]

TASK_TITLES = [
    "Crear endpoint", "Agregar tests", "Implementar UI", "Revisar PR",
    "Actualizar documentación", "Configurar variables", "Agregar validaciones",
    "Crear migración", "Implementar servicio", "Agregar logging",
    "Crear componente", "Agregar estilos", "Implementar hook",
    "Configurar build", "Agregar error handling",
]

# Employee performance profiles (determines completion rates)
PROFILES = {
    EXISTING_EMPLOYEE_ID: {"completion_rate": 0.70, "task_rate": 0.75, "carry_rate": 0.20},  # Moderate
    UUID("00000000-0000-0000-0001-000000000005"): {"completion_rate": 0.90, "task_rate": 0.95, "carry_rate": 0.05},  # Excellent
    UUID("00000000-0000-0000-0001-000000000006"): {"completion_rate": 0.80, "task_rate": 0.85, "carry_rate": 0.10},  # Good
    UUID("00000000-0000-0000-0001-000000000007"): {"completion_rate": 0.55, "task_rate": 0.60, "carry_rate": 0.30},  # Needs attention
}


def get_week_starts(num_weeks: int) -> list[date]:
    """Get Monday dates for the last N weeks including current."""
    today = date.today()
    # Current week start (use today for dev, like the app does)
    weeks = [today]
    for i in range(1, num_weeks):
        weeks.append(today - timedelta(days=7 * i))
    return sorted(weeks)  # oldest first


def calculate_crs(priorities_completed: int, priorities_total: int,
                  tasks_completed: int, tasks_total: int,
                  priorities_carried: int, history_scores: list[float]) -> dict:
    """Calculate CRS using v1.0 formula."""
    # Component 1: Priority completion (40%)
    comp_priorities = (priorities_completed / priorities_total * 100) if priorities_total > 0 else 100

    # Component 2: Task completion (30%)
    comp_tasks = (tasks_completed / tasks_total * 100) if tasks_total > 0 else 100

    # Component 4: Carry-over factor (10%)
    comp_carry = ((1 - priorities_carried / priorities_total) * 100) if priorities_total > 0 else 100

    # Component 3: Historical consistency (20%)
    if len(history_scores) == 0:
        # First week: re-weight
        score = 0.50 * comp_priorities + 0.375 * comp_tasks + 0.125 * comp_carry
    else:
        comp_history = sum(history_scores) / len(history_scores)
        score = 0.40 * comp_priorities + 0.30 * comp_tasks + 0.20 * comp_history + 0.10 * comp_carry

    score = round(min(100, max(0, score)), 2)

    # Trend
    if len(history_scores) >= 1:
        avg = sum(history_scores) / len(history_scores)
        if score > avg + 5:
            trend = "improving"
        elif score < avg - 5:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "stable"

    # Risk level
    if score >= 75:
        risk_level = "low"
    elif score >= 60:
        risk_level = "moderate"
    else:
        risk_level = "high"

    return {"score": score, "trend": trend, "risk_level": risk_level}


async def seed() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # ── Clean existing data ──
        print("🧹 Cleaning existing check-in/check-out/CRS data...")
        await session.execute(text("DELETE FROM tasks WHERE organization_id = :org"), {"org": ORG_ID})
        await session.execute(text("DELETE FROM crs_scores WHERE organization_id = :org"), {"org": ORG_ID})
        await session.execute(text("DELETE FROM priorities WHERE organization_id = :org"), {"org": ORG_ID})
        await session.execute(text("DELETE FROM check_outs WHERE organization_id = :org"), {"org": ORG_ID})
        await session.execute(text("DELETE FROM check_ins WHERE organization_id = :org"), {"org": ORG_ID})

        # ── Create new employees ──
        print("👥 Creating new employees...")
        for emp in NEW_EMPLOYEES:
            # Check if exists
            result = await session.execute(
                text("SELECT id FROM users WHERE id = :id"), {"id": emp["id"]}
            )
            if result.first() is None:
                await session.execute(
                    text("""
                        INSERT INTO users (id, organization_id, email, first_name, last_name, hashed_password, role, status, manager_id)
                        VALUES (:id, :org, :email, :first, :last, :pw, 'employee', 'active', :mgr)
                    """),
                    {
                        "id": emp["id"], "org": ORG_ID, "email": emp["email"],
                        "first": emp["first_name"], "last": emp["last_name"],
                        "pw": "$2b$12$LQv3c1yqBo9SkvXS7QTJPOoGz3Fz.5VQz5z5z5z5z5z5z5z5z5z5z",
                        "mgr": MANAGER_ID,
                    },
                )
                print(f"  ✅ Created {emp['email']}")
            else:
                # Update manager_id in case it's missing
                await session.execute(
                    text("UPDATE users SET manager_id = :mgr, status = 'active' WHERE id = :id"),
                    {"mgr": MANAGER_ID, "id": emp["id"]},
                )
                print(f"  ⏭️  {emp['email']} already exists (updated manager)")

        # ── Generate 4 weeks of data ──
        weeks = get_week_starts(4)
        print(f"\n📅 Generating data for {len(weeks)} weeks: {[str(w) for w in weeks]}")

        random.seed(42)  # Reproducible results
        title_idx = 0

        for emp in ALL_EMPLOYEES:
            emp_id = emp["id"]
            profile = PROFILES[emp_id]
            history_scores: list[float] = []

            print(f"\n👤 {emp['name']} (completion: {profile['completion_rate']:.0%})")

            for week_start in weeks:
                # ── Check-In ──
                checkin_id = uuid4()
                await session.execute(
                    text("""
                        INSERT INTO check_ins (id, organization_id, employee_id, week_start, status, submitted_at)
                        VALUES (:id, :org, :emp, :ws, 'submitted', now())
                    """),
                    {"id": checkin_id, "org": ORG_ID, "emp": emp_id, "ws": week_start},
                )

                # ── Priorities (2-4 per week) ──
                num_priorities = random.randint(2, 4)
                priority_ids = []
                for _ in range(num_priorities):
                    pid = uuid4()
                    priority_ids.append(pid)
                    title = PRIORITY_TITLES[title_idx % len(PRIORITY_TITLES)]
                    title_idx += 1
                    phase = random.choice(PHASES)
                    level = random.choice(["high", "medium", "low"])
                    await session.execute(
                        text("""
                            INSERT INTO priorities (id, organization_id, checkin_id, phase_id, owner_id, week_start, title, description, priority_level, status)
                            VALUES (:id, :org, :checkin, :phase, :owner, :ws, :title, :desc, :level, 'planned')
                        """),
                        {
                            "id": pid, "org": ORG_ID, "checkin": checkin_id, "phase": phase,
                            "owner": emp_id, "ws": week_start, "title": title,
                            "desc": f"Trabajo planificado para semana {week_start}",
                            "level": level,
                        },
                    )

                # ── Tasks (2-3 per priority) ──
                all_task_ids = []
                for pid in priority_ids:
                    num_tasks = random.randint(2, 3)
                    for _ in range(num_tasks):
                        tid = uuid4()
                        all_task_ids.append((tid, pid))
                        task_title = random.choice(TASK_TITLES)
                        await session.execute(
                            text("""
                                INSERT INTO tasks (id, organization_id, priority_id, title, status)
                                VALUES (:id, :org, :pid, :title, 'pending')
                            """),
                            {"id": tid, "org": ORG_ID, "pid": pid, "title": task_title},
                        )

                # ── Check-Out ──
                checkout_id = uuid4()
                await session.execute(
                    text("""
                        INSERT INTO check_outs (id, organization_id, employee_id, checkin_id, week_start, status, submitted_at, notes)
                        VALUES (:id, :org, :emp, :checkin, :ws, 'submitted', now(), :notes)
                    """),
                    {
                        "id": checkout_id, "org": ORG_ID, "emp": emp_id,
                        "checkin": checkin_id, "ws": week_start,
                        "notes": f"Cierre de semana {week_start}. {'Buena semana.' if profile['completion_rate'] > 0.7 else 'Semana complicada con bloqueadores.'}",
                    },
                )

                # ── Mark priorities completed/carried based on profile ──
                priorities_completed = 0
                priorities_carried = 0
                for pid in priority_ids:
                    r = random.random()
                    if r < profile["completion_rate"]:
                        await session.execute(
                            text("UPDATE priorities SET status = 'completed', completed_in_checkout = :co WHERE id = :id"),
                            {"co": checkout_id, "id": pid},
                        )
                        priorities_completed += 1
                    elif r < profile["completion_rate"] + profile["carry_rate"]:
                        await session.execute(
                            text("UPDATE priorities SET status = 'carried_over' WHERE id = :id"),
                            {"id": pid},
                        )
                        priorities_carried += 1
                    else:
                        # Left as planned (incomplete)
                        await session.execute(
                            text("UPDATE priorities SET status = 'in_progress' WHERE id = :id"),
                            {"id": pid},
                        )

                # ── Mark tasks completed based on profile ──
                tasks_completed = 0
                for tid, pid in all_task_ids:
                    if random.random() < profile["task_rate"]:
                        await session.execute(
                            text("UPDATE tasks SET status = 'completed', completed_in_checkout = :co WHERE id = :id"),
                            {"co": checkout_id, "id": tid},
                        )
                        tasks_completed += 1
                    else:
                        status = random.choice(["in_progress", "cancelled"])
                        await session.execute(
                            text("UPDATE tasks SET status = :s WHERE id = :id"),
                            {"s": status, "id": tid},
                        )

                # ── Calculate CRS ──
                crs_data = calculate_crs(
                    priorities_completed=priorities_completed,
                    priorities_total=num_priorities,
                    tasks_completed=tasks_completed,
                    tasks_total=len(all_task_ids),
                    priorities_carried=priorities_carried,
                    history_scores=history_scores[-4:],  # Last 4 weeks
                )

                crs_id = uuid4()
                await session.execute(
                    text("""
                        INSERT INTO crs_scores (id, organization_id, employee_id, checkout_id, week_start,
                            score, trend, risk_level, formula_version, priorities_total, priorities_completed, tasks_total, tasks_completed)
                        VALUES (:id, :org, :emp, :co, :ws, :score, :trend, :risk, 'v1.0', :pt, :pc, :tt, :tc)
                    """),
                    {
                        "id": crs_id, "org": ORG_ID, "emp": emp_id, "co": checkout_id,
                        "ws": week_start, "score": crs_data["score"],
                        "trend": crs_data["trend"], "risk": crs_data["risk_level"],
                        "pt": num_priorities, "pc": priorities_completed,
                        "tt": len(all_task_ids), "tc": tasks_completed,
                    },
                )

                history_scores.append(crs_data["score"])
                print(f"  📊 Week {week_start}: CRS={crs_data['score']:.1f} ({crs_data['trend']}, {crs_data['risk_level']}) | P:{priorities_completed}/{num_priorities} T:{tasks_completed}/{len(all_task_ids)}")

        await session.commit()

    await engine.dispose()
    print("\n🎉 Seed complete!")
    print("   4 employees × 4 weeks = 16 check-ins, 16 check-outs, 16 CRS scores")
    print("   Ready for: Team Visibility, Weekly View, AI features")


if __name__ == "__main__":
    asyncio.run(seed())
