"""checkout: create check_outs, crs_scores tables and add completed_in_checkout columns

Revision ID: 202507051200
Revises: 202506231200
Create Date: 2026-07-05 12:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "202507051200"
down_revision = "202506231200"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── check_outs ────────────────────────────────────────────────────────────
    op.create_table(
        "check_outs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", UUID(as_uuid=True), sa.ForeignKey("organizations.id", name="fk_check_outs_organizations"), nullable=False),
        sa.Column("employee_id", UUID(as_uuid=True), sa.ForeignKey("users.id", name="fk_check_outs_users"), nullable=False),
        sa.Column("checkin_id", UUID(as_uuid=True), sa.ForeignKey("check_ins.id", name="fk_check_outs_check_ins"), nullable=False),
        sa.Column("week_start", sa.Date, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("submitted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("lessons_learned", sa.Text, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_by", UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint("status IN ('draft', 'submitted', 'closed')", name="ck_check_outs_status"),
    )

    # ── crs_scores ────────────────────────────────────────────────────────────
    op.create_table(
        "crs_scores",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("organization_id", UUID(as_uuid=True), sa.ForeignKey("organizations.id", name="fk_crs_scores_organizations"), nullable=False),
        sa.Column("employee_id", UUID(as_uuid=True), sa.ForeignKey("users.id", name="fk_crs_scores_users"), nullable=False),
        sa.Column("checkout_id", UUID(as_uuid=True), sa.ForeignKey("check_outs.id", name="fk_crs_scores_check_outs"), nullable=False),
        sa.Column("week_start", sa.Date, nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=False),
        sa.Column("trend", sa.String(20), nullable=False, server_default="stable"),
        sa.Column("risk_level", sa.String(20), nullable=False, server_default="low"),
        sa.Column("formula_version", sa.String(10), nullable=False, server_default="v1.0"),
        sa.Column("priorities_total", sa.Integer, nullable=False, server_default="0"),
        sa.Column("priorities_completed", sa.Integer, nullable=False, server_default="0"),
        sa.Column("tasks_total", sa.Integer, nullable=False, server_default="0"),
        sa.Column("tasks_completed", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_by", UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint("trend IN ('improving', 'stable', 'declining')", name="ck_crs_scores_trend"),
        sa.CheckConstraint("risk_level IN ('low', 'moderate', 'high')", name="ck_crs_scores_risk_level"),
    )

    # ── ALTER priorities: add completed_in_checkout ───────────────────────────
    op.add_column(
        "priorities",
        sa.Column("completed_in_checkout", UUID(as_uuid=True), sa.ForeignKey("check_outs.id", name="fk_priorities_check_outs"), nullable=True),
    )

    # ── ALTER tasks: add completed_in_checkout ────────────────────────────────
    op.add_column(
        "tasks",
        sa.Column("completed_in_checkout", UUID(as_uuid=True), sa.ForeignKey("check_outs.id", name="fk_tasks_check_outs"), nullable=True),
    )

    # ── índices check_outs ────────────────────────────────────────────────────
    op.create_index(
        "uq_check_outs_employee_week", "check_outs", ["employee_id", "week_start"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index("idx_check_outs_organization_id", "check_outs", ["organization_id"])
    op.create_index("idx_check_outs_employee_id", "check_outs", ["employee_id"])
    op.create_index("idx_check_outs_checkin_id", "check_outs", ["checkin_id"])
    op.create_index("idx_check_outs_week_start", "check_outs", ["week_start"])

    # ── índices crs_scores ────────────────────────────────────────────────────
    op.create_index(
        "uq_crs_scores_employee_week", "crs_scores", ["employee_id", "week_start"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index("idx_crs_scores_organization_id", "crs_scores", ["organization_id"])
    op.create_index("idx_crs_scores_employee_id", "crs_scores", ["employee_id"])
    op.create_index("idx_crs_scores_checkout_id", "crs_scores", ["checkout_id"])
    op.create_index("idx_crs_scores_week_start", "crs_scores", ["week_start"])


def downgrade() -> None:
    # índices crs_scores
    op.drop_index("idx_crs_scores_week_start", table_name="crs_scores")
    op.drop_index("idx_crs_scores_checkout_id", table_name="crs_scores")
    op.drop_index("idx_crs_scores_employee_id", table_name="crs_scores")
    op.drop_index("idx_crs_scores_organization_id", table_name="crs_scores")
    op.drop_index("uq_crs_scores_employee_week", table_name="crs_scores")

    # índices check_outs
    op.drop_index("idx_check_outs_week_start", table_name="check_outs")
    op.drop_index("idx_check_outs_checkin_id", table_name="check_outs")
    op.drop_index("idx_check_outs_employee_id", table_name="check_outs")
    op.drop_index("idx_check_outs_organization_id", table_name="check_outs")
    op.drop_index("uq_check_outs_employee_week", table_name="check_outs")

    # ALTER: drop columns
    op.drop_column("tasks", "completed_in_checkout")
    op.drop_column("priorities", "completed_in_checkout")

    # tablas (orden inverso por FKs)
    op.drop_table("crs_scores")
    op.drop_table("check_outs")
