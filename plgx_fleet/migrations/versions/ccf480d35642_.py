"""empty message

Revision ID: ccf480d35642
Revises: fcf6cc75ebd2
Create Date: 2018-10-01 14:55:13.226549

"""

# revision identifiers, used by Alembic.
revision = 'ccf480d35642'
down_revision = 'fcf6cc75ebd2'

from alembic import op
import sqlalchemy as sa
import polylogyx.database
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('node_recon_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('columns', postgresql.JSONB(), nullable=False),
    sa.Column('node_data_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['node_data_id'], ['node_data.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        'index_node_recon_data_on_columns', 'node_recon_data', ['columns'],
        unique=False,
        postgresql_ops={'columns': ''},
        postgresql_using='gin')

    op.create_index(
        'index_node_recon_data_on_columns_path', 'node_recon_data', ['columns'],
        unique=False,
        postgresql_ops={"columns->'path'": ''},
        postgresql_using='gin')

    op.create_index(
        'index_result_log_on_columns', 'result_log', ['columns'],
        unique=False,
        postgresql_ops={'columns': ''},
        postgresql_using='gin')

    op.create_index(
        'index_result_log_on_columns_path', 'result_log', ['columns'],
        unique=False,
        postgresql_ops={"columns->'path'": ''},
        postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_index('index_result_log_on_columns_path')
    op.drop_index('index_node_recon_data_on_columns_path')
    op.drop_index('index_result_log_on_columns')
    op.drop_index('index_node_recon_data_on_columns')
    op.drop_table('node_recon_data')
    # ### end Alembic commands ###
