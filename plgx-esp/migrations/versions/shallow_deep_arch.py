"""empty message

Revision ID: 4b6de2085d8c
Revises: j8emsbzxcq1k
Create Date: 2020-01-30 12:15:16.178291

"""

# revision identifiers, used by Alembic.
revision = "4b6de2085d8c"
down_revision = "j8emsbzxcq1k"

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql



def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "config",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("platform", sa.String(), nullable=True),
        sa.Column("arch", sa.String(), nullable=True),
        sa.Column("type", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column(
        "default_filters", sa.Column("config_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(None, "default_filters", "config", ["config_id"], ["id"])
    op.add_column("default_query", sa.Column("config_id", sa.Integer(), nullable=True))

    op.create_foreign_key(None, "default_query", "config", ["config_id"], ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_constraint(None, "default_query", type_="foreignkey")

    op.drop_column("default_query", "config_id")
    op.drop_constraint(None, "default_filters", type_="foreignkey")

    op.drop_column("default_filters", "config_id")

    op.drop_table("config")
    # ### end Alembic commands ###
