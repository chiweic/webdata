"""adding event

Revision ID: fb821fe1f28f
Revises: 25c7c69661b4
Create Date: 2024-10-17 11:43:25.577535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb821fe1f28f'
down_revision: Union[str, None] = '25c7c69661b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('pk', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('pk')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    # ### end Alembic commands ###
