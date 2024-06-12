"""add foreign keys to posts table

Revision ID: 10aab06800d3
Revises: 181f72494bff
Create Date: 2024-06-12 10:46:54.790431

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "10aab06800d3"
down_revision: Union[str, None] = "181f72494bff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        'post_users_fk', "posts", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', "posts", type_="foreignkey")
    op.drop_column("posts", "user_id")
    pass
