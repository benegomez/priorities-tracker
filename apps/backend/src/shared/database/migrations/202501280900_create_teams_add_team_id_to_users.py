"""teams: create teams table and add team_id to users

Revision ID: 202501280900
Revises: 202507051300
Create Date: 2025-01-28 09:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "202501280900"
down_revision = "202507051300"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── CREATE TABLE teams ────────────────────────────────────────────────
    op.create_table(
        "teams",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", UUID(as_uuid=True), sa.ForeignKey("organizations.id", name="fk_teams_organizations"), nullable=False),
        sa.Column("manager_id", UUID(as_uuid=True), sa.ForeignKey("users.id", name="fk_teams_manager"), nullable=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_by", UUID(as_uuid=True), nullable=True),
    )
    op.create_index("idx_teams_organization_id", "teams", ["organization_id"])
    op.create_index("idx_teams_manager_id", "teams", ["manager_id"])
    op.create_index(
        "uq_teams_org_name", "teams", ["organization_id", "name"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )

    # ── ALTER TABLE users: add team_id ────────────────────────────────────
    op.add_column(
        "users",
        sa.Column("team_id", UUID(as_uuid=True), sa.ForeignKey("teams.id", name="fk_users_team"), nullable=True),
    )
    op.create_index("idx_users_team_id", "users", ["team_id"])


def downgrade() -> None:
    # ── ALTER TABLE users: drop team_id ───────────────────────────────────
    op.drop_index("idx_users_team_id", table_name="users")
    op.drop_column("users", "team_id")

    # ── DROP TABLE teams ──────────────────────────────────────────────────
    op.drop_index("uq_teams_org_name", table_name="teams")
    op.drop_index("idx_teams_manager_id", table_name="teams")
    op.drop_index("idx_teams_organization_id", table_name="teams")
    op.drop_table("teams")
