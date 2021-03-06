"""empty message

Revision ID: 53d372cb535a
Revises: 658de397b180
Create Date: 2019-07-26 14:26:19.489445

"""

# revision identifiers, used by Alembic.
revision = "53d372cb535a"
down_revision = "658de397b180"

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column("alerts", sa.Column("status", sa.String(), nullable=True))
    op.add_column('rule', sa.Column('tactics', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('rule', sa.Column('technique_id', sa.String(), nullable=True))
    op.add_column('rule', sa.Column('type', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_column("rule", "type")
    op.drop_column("rule", "technique_id")
    op.drop_column("rule", "tactics")
    op.drop_column("alerts", "status")

    # ### end Alembic commands ###
