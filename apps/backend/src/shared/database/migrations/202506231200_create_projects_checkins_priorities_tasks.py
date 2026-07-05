"""checkin: create projects, project_phases, check_ins, priorities, tasks tables

Revision ID: 202506231200
Revises: 202606231109
Create Date: 2025-06-23 12:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "202506231200"
down_revision = "202606231109"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── projects ──────────────────────────────────────────────────────────────
    op.create_table(
        "projects",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", UUID(as_uuid=True), sa.ForeignKey("organizations.id", name="fk_projects_organizations"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_by", UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint("status IN ('draft', 'active', 'on_hold', 'completed', 'archived')", name="ck_projects_status"),
    )

    # ── project_phases ────────────────────────────────────────────────────────
    op.create_table(
        "project_phases",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", UUID(as_uuid=True), sa.ForeignKey("organizations.id", name="fk_project_phases_organizations"), nullable=False),
        sa.Column("project_id", UUID(as_uuid=True), sa.ForeignKey("projects.id", name="fk_project_phases_projects"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="planned"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_by", UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint("status IN ('planned', 'active', 'completed', 'cancelled')", name="ck_project_phases_status"),
    )

    # ── check_ins ─────────────────────────────────────────────────────────────
    op.create_table(
        "check_ins",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", UUID(as_uuid=True), sa.ForeignKey("organizations.id", name="fk_check_ins_organizations"), nullable=False),
        sa.Column("employee_id", UUID(as_uuid=True), sa.ForeignKey("users.id", name="fk_check_ins_users"), nullable=False),
        sa.Column("week_start", sa.Date, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("submitted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_by", UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint("status IN ('draft', 'submitted', 'closed')", name="ck_check_ins_status"),
    )

    # ── priorities ────────────────────────────────────────────────────────────
    op.create_table(
        "priorities",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", UUID(as_uuid=True), sa.ForeignKey("organizations.id", name="fk_priorities_organizations"), nullable=False),
        sa.Column("checkin_id", UUID(as_uuid=True), sa.ForeignKey("check_ins.id", name="fk_priorities_check_ins"), nullable=False),
        sa.Column("phase_id", UUID(as_uuid=True), sa.ForeignKey("project_phases.id", name="fk_priorities_project_phases"), nullable=False),
        sa.Column("owner_id", UUID(as_uuid=True), sa.ForeignKey("users.id", name="fk_priorities_users"), nullable=False),
        sa.Column("week_start", sa.Date, nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("priority_level", sa.String(10), nullable=False, server_default="medium"),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_by", UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint("priority_level IN ('low', 'medium', 'high')", name="ck_priorities_level"),
        sa.CheckConstraint("status IN ('draft', 'planned', 'in_progress', 'completed', 'carried_over')", name="ck_priorities_status"),
    )

    # ── tasks ─────────────────────────────────────────────────────────────────
    op.create_table(
        "tasks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", UUID(as_uuid=True), sa.ForeignKey("organizations.id", name="fk_tasks_organizations"), nullable=False),
        sa.Column("priority_id", UUID(as_uuid=True), sa.ForeignKey("priorities.id", name="fk_tasks_priorities"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_by", UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint("status IN ('pending', 'in_progress', 'completed', 'cancelled')", name="ck_tasks_status"),
    )

    # ── índices ───────────────────────────────────────────────────────────────

    # projects
    op.create_index("idx_projects_organization_id", "projects", ["organization_id"])
    op.create_index(
        "idx_projects_status", "projects", ["status"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )

    # project_phases
    op.create_index("idx_project_phases_organization_id", "project_phases", ["organization_id"])
    op.create_index("idx_project_phases_project_id", "project_phases", ["project_id"])

    # check_ins
    op.create_index(
        "uq_check_ins_employee_week", "check_ins", ["employee_id", "week_start"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index("idx_check_ins_organization_id", "check_ins", ["organization_id"])
    op.create_index("idx_check_ins_employee_id", "check_ins", ["employee_id"])
    op.create_index("idx_check_ins_week_start", "check_ins", ["week_start"])

    # priorities
    op.create_index("idx_priorities_organization_id", "priorities", ["organization_id"])
    op.create_index("idx_priorities_checkin_id", "priorities", ["checkin_id"])
    op.create_index("idx_priorities_phase_id", "priorities", ["phase_id"])
    op.create_index("idx_priorities_owner_id", "priorities", ["owner_id"])
    op.create_index("idx_priorities_week_start", "priorities", ["week_start"])
    op.create_index(
        "idx_priorities_status", "priorities", ["status"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )

    # tasks
    op.create_index("idx_tasks_organization_id", "tasks", ["organization_id"])
    op.create_index("idx_tasks_priority_id", "tasks", ["priority_id"])
    op.create_index(
        "idx_tasks_status", "tasks", ["status"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )


def downgrade() -> None:
    # índices (orden inverso)
    op.drop_index("idx_tasks_status", table_name="tasks")
    op.drop_index("idx_tasks_priority_id", table_name="tasks")
    op.drop_index("idx_tasks_organization_id", table_name="tasks")

    op.drop_index("idx_priorities_status", table_name="priorities")
    op.drop_index("idx_priorities_week_start", table_name="priorities")
    op.drop_index("idx_priorities_owner_id", table_name="priorities")
    op.drop_index("idx_priorities_phase_id", table_name="priorities")
    op.drop_index("idx_priorities_checkin_id", table_name="priorities")
    op.drop_index("idx_priorities_organization_id", table_name="priorities")

    op.drop_index("idx_check_ins_week_start", table_name="check_ins")
    op.drop_index("idx_check_ins_employee_id", table_name="check_ins")
    op.drop_index("idx_check_ins_organization_id", table_name="check_ins")
    op.drop_index("uq_check_ins_employee_week", table_name="check_ins")

    op.drop_index("idx_project_phases_project_id", table_name="project_phases")
    op.drop_index("idx_project_phases_organization_id", table_name="project_phases")

    op.drop_index("idx_projects_status", table_name="projects")
    op.drop_index("idx_projects_organization_id", table_name="projects")

    # tablas (orden inverso por FKs)
    op.drop_table("tasks")
    op.drop_table("priorities")
    op.drop_table("check_ins")
    op.drop_table("project_phases")
    op.drop_table("projects")
