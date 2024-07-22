"""empty message

Revision ID: 82e08418ffb2
Revises: e66a00534fe2
Create Date: 2024-07-22 15:32:43.974949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82e08418ffb2'
down_revision: Union[str, None] = 'e66a00534fe2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('bio', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'bio')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###