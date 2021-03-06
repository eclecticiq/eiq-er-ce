"""empty message

Revision ID: 03277ebe1fbf
Revises: 08e477ef430f
Create Date: 2021-07-19 18:36:41.050685

"""

# revision identifiers, used by Alembic.
revision = '03277ebe1fbf'
down_revision = '08e477ef430f'

from alembic import op
import sqlalchemy as sa
import polylogyx.db.database
from sqlalchemy.dialects import postgresql


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('rule', sa.Column('alert_description', sa.Boolean(), nullable=True))
    op.execute("update rule set alert_description=false;")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_column('rule', 'alert_description')

    # ### end Alembic commands ###
