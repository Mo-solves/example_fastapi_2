"""add last few columns in post table

Revision ID: d05d80e39158
Revises: 8a52c61ad526
Create Date: 2025-09-28 11:51:49.549367

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d05d80e39158"
down_revision: Union[str, Sequence[str], None] = "8a52c61ad526"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts_2",
        sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts_2",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts_2", "published")
    op.drop_column("posts_2", "created_at")
