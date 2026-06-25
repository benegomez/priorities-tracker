"""
Seed script for authentication data.
Creates 2 organizations and users per role for testing, including cross-tenant isolation.

Usage:
    docker compose exec api python scripts/seed_auth.py
"""
import asyncio
import os

import bcrypt
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://pt_user:changeme_local@postgres:5432/priorities_tracker",
)


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


ORGANIZATIONS = [
    {"id": "00000000-0000-0000-0000-000000000001", "name": "Org Alpha", "code": "org-alpha", "status": "active"},
    {"id": "00000000-0000-0000-0000-000000000002", "name": "Org Beta", "code": "org-beta", "status": "active"},
]

USERS = [
    {
        "id": "00000000-0000-0000-0001-000000000001",
        "organization_id": "00000000-0000-0000-0000-000000000001",
        "email": "admin@org-alpha.com",
        "plain_password": "Admin1234!",
        "role": "administrator",
        "status": "active",
        "first_name": "Admin",
        "last_name": "Alpha",
        "manager_id": None,
    },
    {
        "id": "00000000-0000-0000-0001-000000000002",
        "organization_id": "00000000-0000-0000-0000-000000000001",
        "email": "manager@org-alpha.com",
        "plain_password": "Manager1234!",
        "role": "manager",
        "status": "active",
        "first_name": "Manager",
        "last_name": "Alpha",
        "manager_id": "00000000-0000-0000-0001-000000000001",
    },
    {
        "id": "00000000-0000-0000-0001-000000000003",
        "organization_id": "00000000-0000-0000-0000-000000000001",
        "email": "employee@org-alpha.com",
        "plain_password": "Employee1234!",
        "role": "employee",
        "status": "active",
        "first_name": "Employee",
        "last_name": "Alpha",
        "manager_id": "00000000-0000-0000-0001-000000000002",
    },
    {
        "id": "00000000-0000-0000-0001-000000000004",
        "organization_id": "00000000-0000-0000-0000-000000000001",
        "email": "inactive@org-alpha.com",
        "plain_password": "Inactive1234!",
        "role": "employee",
        "status": "inactive",
        "first_name": "Inactive",
        "last_name": "Alpha",
        "manager_id": "00000000-0000-0000-0001-000000000002",
    },
    {
        "id": "00000000-0000-0000-0002-000000000001",
        "organization_id": "00000000-0000-0000-0000-000000000002",
        "email": "employee@org-beta.com",
        "plain_password": "Employee1234!",
        "role": "employee",
        "status": "active",
        "first_name": "Employee",
        "last_name": "Beta",
        "manager_id": None,
    },
]


async def seed() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        for org in ORGANIZATIONS:
            await session.execute(
                text("""
                    INSERT INTO organizations (id, name, code, status)
                    VALUES (:id, :name, :code, :status)
                    ON CONFLICT (code) DO NOTHING
                """),
                org,
            )

        for user in USERS:
            hashed = hash_password(user["plain_password"])
            await session.execute(
                text("""
                    INSERT INTO users
                        (id, organization_id, manager_id, email, hashed_password,
                         role, status, first_name, last_name)
                    VALUES
                        (:id, :organization_id, :manager_id, :email, :hashed_password,
                         :role, :status, :first_name, :last_name)
                    ON CONFLICT DO NOTHING
                """),
                {
                    "id": user["id"],
                    "organization_id": user["organization_id"],
                    "manager_id": user["manager_id"],
                    "email": user["email"],
                    "hashed_password": hashed,
                    "role": user["role"],
                    "status": user["status"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                },
            )

        await session.commit()

    await engine.dispose()
    print("✅ Seed completed successfully.")
    print("\nTest accounts:")
    for u in USERS:
        print(f"  [{u['role']:13s}] {u['email']:35s}  pw: {u['plain_password']}")


if __name__ == "__main__":
    asyncio.run(seed())
