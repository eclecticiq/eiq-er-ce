"""Add "node_info" column to capture arbitrary node information on the fly

Revision ID: 54ef3f06612c
Revises: c17f01adbe31
Create Date: 2016-06-15 10:31:13.791641

"""

# revision identifiers, used by Alembic.
revision = "54ef3f06612c"
down_revision = "c17f01adbe31"

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql



def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "node",
        sa.Column("node_info", postgresql.JSONB(), server_default="{}", nullable=False),
    )
    op.drop_index("idx__rule__updated_at", table_name="rule")
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index("idx__rule__updated_at", "rule", ["updated_at"], unique=False)
    op.drop_column("node", "node_info")
    ### end Alembic commands ###
