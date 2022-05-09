"""empty message

Revision ID: 0c39eb9a5b6a
Revises: c78975eaf294
Create Date: 2021-10-18 16:42:47.061445

"""

# revision identifiers, used by Alembic.
revision = '0c39eb9a5b6a'
down_revision = 'c78975eaf294'

from alembic import op
import sqlalchemy as sa
import polylogyx.db.database
from sqlalchemy.dialects import postgresql
import flask_authorize


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###

    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('restrictions', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('access_level', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('allowances', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_level'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_group',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.execute(
        "drop table if exists user_role"
    )
    op.create_table('user_role',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.add_column('user', sa.Column('reset_password', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('reset_email', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('status', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('enable_sso', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('updated_at', sa.DateTime(), nullable=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###

    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'enable_sso')
    op.drop_column('user', 'status')
    op.drop_column('user', 'reset_email')
    op.drop_column('user', 'reset_password')

    op.drop_table('user_role')
    op.drop_table('user_group')
    op.drop_table('roles')
    op.drop_table('groups')

    ### end Alembic commands ###