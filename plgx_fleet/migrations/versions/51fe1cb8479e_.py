"""empty message

Revision ID: 51fe1cb8479e
Revises: ccf480d35642
Create Date: 2018-10-08 16:28:07.456565

"""

# revision identifiers, used by Alembic.
revision = '51fe1cb8479e'
down_revision = 'ccf480d35642'

from alembic import op
import sqlalchemy as sa
import polylogyx.database
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('distributed_query_task', sa.Column('priority', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():

    op.drop_column('distributed_query_task', 'priority')
