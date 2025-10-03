"""add content column to post table

Revision ID: 7868270c5fba
Revises: 97a395624251
Create Date: 2025-09-28 11:36:33.141006

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7868270c5fba"
down_revision: Union[str, Sequence[str], None] = "97a395624251"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts_2", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts_2", "content")
