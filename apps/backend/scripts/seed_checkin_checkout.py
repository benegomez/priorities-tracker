"""
Seed check-in + checkout data for employee@org-alpha.com to test manager team visibility.

Usage:
    docker compose exec api python scripts/seed_checkin_checkout.py
"""
import asyncio
import os
from datetime import date
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://pt_user:changeme_local@postgres:5432/priorities_tracker",
)

ORG_ID = UUID("00000000-0000-0000-0000-000000000001")
EMPLOYEE_ID = UUID("00000000-0000-0000-0001-000000000003")
PHASE_ID = UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")  # Desarrollo phase

TODAY = date.today()


async def seed() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Clean existing data for today
        await session.execute(text("DELETE FROM tasks WHERE organization_id = :org"), {"org": ORG_ID})
        await session.execute(text("DELETE FROM crs_scores WHERE organization_id = :org"), {"org": ORG_ID})
        await session.execute(text("DELETE FROM priorities WHERE organization_id = :org"), {"org": ORG_ID})
        await session.execute(text("DELETE FROM check_outs WHERE organization_id = :org"), {"org": ORG_ID})
        await session.execute(text("DELETE FROM check_ins WHERE organization_id = :org"), {"org": ORG_ID})

        # Create check-in
        checkin_id = uuid4()
        await session.execute(
            text("""
                INSERT INTO check_ins (id, organization_id, employee_id, week_start, status, submitted_at)
                VALUES (:id, :org, :emp, :ws, 'submitted', now())
            """),
            {"id": checkin_id, "org": ORG_ID, "emp": EMPLOYEE_ID, "ws": TODAY},
        )
        print(f"✅ Check-in created: {checkin_id}")

        # Create 3 priorities
        priority_ids = []
        for i, title in enumerate(["Implementar dashboard de equipo", "Refactorizar módulo auth", "Documentar API de CRS"]):
            pid = uuid4()
            priority_ids.append(pid)
            await session.execute(
                text("""
                    INSERT INTO priorities (id, organization_id, checkin_id, phase_id, owner_id, week_start, title, description, priority_level, status)
                    VALUES (:id, :org, :checkin, :phase, :owner, :ws, :title, :desc, :level, 'planned')
                """),
                {
                    "id": pid, "org": ORG_ID, "checkin": checkin_id, "phase": PHASE_ID,
                    "owner": EMPLOYEE_ID, "ws": TODAY, "title": title,
                    "desc": f"Descripción de la prioridad {i+1}",
                    "level": ["high", "medium", "low"][i],
                },
            )

        # Create tasks for first 2 priorities
        task_ids = []
        tasks_data = [
            (priority_ids[0], "Crear endpoint GET /teams/my-team"),
            (priority_ids[0], "Agregar tests unitarios"),
            (priority_ids[0], "Implementar UI de tabla"),
            (priority_ids[1], "Extraer servicio de tokens"),
            (priority_ids[1], "Agregar rate limiting configurable"),
        ]
        for priority_id, title in tasks_data:
            tid = uuid4()
            task_ids.append(tid)
            await session.execute(
                text("""
                    INSERT INTO tasks (id, organization_id, priority_id, title, status)
                    VALUES (:id, :org, :pid, :title, 'pending')
                """),
                {"id": tid, "org": ORG_ID, "pid": priority_id, "title": title},
            )

        print(f"✅ 3 priorities + 5 tasks created")

        # Create checkout
        checkout_id = uuid4()
        await session.execute(
            text("""
                INSERT INTO check_outs (id, organization_id, employee_id, checkin_id, week_start, status, submitted_at, notes)
                VALUES (:id, :org, :emp, :checkin, :ws, 'submitted', now(), 'Buena semana, completé la mayoría de tareas.')
            """),
            {"id": checkout_id, "org": ORG_ID, "emp": EMPLOYEE_ID, "checkin": checkin_id, "ws": TODAY},
        )
        print(f"✅ Check-out created: {checkout_id}")

        # Mark 2/3 priorities as completed, 1 as carried_over
        await session.execute(
            text("UPDATE priorities SET status = 'completed', completed_in_checkout = :co WHERE id = :id"),
            {"co": checkout_id, "id": priority_ids[0]},
        )
        await session.execute(
            text("UPDATE priorities SET status = 'completed', completed_in_checkout = :co WHERE id = :id"),
            {"co": checkout_id, "id": priority_ids[1]},
        )
        await session.execute(
            text("UPDATE priorities SET status = 'carried_over' WHERE id = :id"),
            {"id": priority_ids[2]},
        )

        # Mark 4/5 tasks as completed, 1 as cancelled
        for tid in task_ids[:4]:
            await session.execute(
                text("UPDATE tasks SET status = 'completed', completed_in_checkout = :co WHERE id = :id"),
                {"co": checkout_id, "id": tid},
            )
        await session.execute(
            text("UPDATE tasks SET status = 'cancelled' WHERE id = :id"),
            {"id": task_ids[4]},
        )
        print("✅ 2/3 priorities completed, 4/5 tasks completed")

        # Calculate and insert CRS
        # Formula: 0.40*(2/3*100) + 0.30*(4/5*100) + 0.20*0(no history) + 0.10*((1-1/3)*100)
        # Without history reponder: 0.50*(66.67) + 0.375*(80) + 0.125*(66.67) = 33.33 + 30 + 8.33 = 71.67
        score = 71.67
        crs_id = uuid4()
        await session.execute(
            text("""
                INSERT INTO crs_scores (id, organization_id, employee_id, checkout_id, week_start,
                    score, trend, risk_level, formula_version, priorities_total, priorities_completed, tasks_total, tasks_completed)
                VALUES (:id, :org, :emp, :co, :ws, :score, 'stable', 'low', 'v1.0', 3, 2, 5, 4)
            """),
            {"id": crs_id, "org": ORG_ID, "emp": EMPLOYEE_ID, "co": checkout_id, "ws": TODAY, "score": score},
        )
        print(f"✅ CRS score: {score} (stable, low risk)")

        await session.commit()

    await engine.dispose()
    print("\n🎉 Seed complete! Manager can now see team data.")


if __name__ == "__main__":
    asyncio.run(seed())
