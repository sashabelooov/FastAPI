"""add role to users

Revision ID: 9695533b9499
Revises: e8eb88bbc7b5
Create Date: 2026-05-08 11:56:07.000829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9695533b9499'
down_revision: Union[str, Sequence[str], None] = 'e8eb88bbc7b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    userrole = sa.Enum('USER', 'ADMIN', name='userrole')
    userrole.create(op.get_bind(), checkfirst=True)
    op.add_column('users', sa.Column('role', userrole, nullable=False, server_default='USER'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
    sa.Enum(name='userrole').drop(op.get_bind(), checkfirst=True)
