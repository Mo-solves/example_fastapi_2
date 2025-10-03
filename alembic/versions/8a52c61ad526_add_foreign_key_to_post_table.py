"""add foreign key to post table

Revision ID: 8a52c61ad526
Revises: 6bd86a2e0258
Create Date: 2025-09-28 11:46:42.322728

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a52c61ad526"
down_revision: Union[str, Sequence[str], None] = "6bd86a2e0258"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts_2", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        "posts_2",
        "users_2",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", "posts_2")
    op.drop_column("posts_2", "owner_id")
