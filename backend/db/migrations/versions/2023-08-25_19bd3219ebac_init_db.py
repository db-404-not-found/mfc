"""Init db

Revision ID: 19bd3219ebac
Revises:
Create Date: 2023-08-25 23:43:35.729077

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "19bd3219ebac"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "task",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("question", sa.String(length=2048), nullable=False),
        sa.Column("result", sa.String(), nullable=True),
        sa.Column("counter", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__task")),
    )


def downgrade() -> None:
    op.drop_table("task")
