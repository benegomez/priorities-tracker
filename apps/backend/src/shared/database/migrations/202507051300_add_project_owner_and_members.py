"""projects: add owner_id to projects and create project_members table

Revision ID: 202507051300
Revises: 202507051200
Create Date: 2026-07-05 13:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "202507051300"
down_revision = "202507051200"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── ALTER projects: add owner_id ──────────────────────────────────────
    op.add_column(
        "projects",
        sa.Column("owner_id", UUID(as_uuid=True), sa.ForeignKey("users.id", name="fk_projects_owner"), nullable=True),
    )
    op.create_index("idx_projects_owner_id", "projects", ["owner_id"])

    # ── project_members ───────────────────────────────────────────────────
    op.create_table(
        "project_members",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", UUID(as_uuid=True), sa.ForeignKey("organizations.id", name="fk_project_members_organizations"), nullable=False),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", name="fk_project_members_projects"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", name="fk_project_members_users"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_by", UUID(as_uuid=True), nullable=True),
    )

    # ── índices project_members ───────────────────────────────────────────
    op.create_index(
        "uq_project_members_project_user", "project_members", ["project_id", "user_id"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index("idx_project_members_organization_id", "project_members", ["organization_id"])
    op.create_index("idx_project_members_project_id", "project_members", ["project_id"])
    op.create_index("idx_project_members_user_id", "project_members", ["user_id"])


def downgrade() -> None:
    # índices project_members
    op.drop_index("idx_project_members_user_id", table_name="project_members")
    op.drop_index("idx_project_members_project_id", table_name="project_members")
    op.drop_index("idx_project_members_organization_id", table_name="project_members")
    op.drop_index("uq_project_members_project_user", table_name="project_members")

    # tabla
    op.drop_table("project_members")

    # ALTER projects
    op.drop_index("idx_projects_owner_id", table_name="projects")
    op.drop_column("projects", "owner_id")
