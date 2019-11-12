"""Add indexes to improve various sql query performance

Revision ID: c107fa0468ff
Revises: 236318ee3d3e
Create Date: 2017-08-22 15:33:13.706301

"""

# revision identifiers, used by Alembic.
revision = 'c107fa0468ff'
down_revision = '236318ee3d3e'

from alembic import op
import sqlalchemy as sa
import polylogyx.database


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_distributed_query_task_node_id_status', 'distributed_query_task', ['node_id', 'status'], unique=False)
    op.create_index(op.f('ix_file_path_tags_file_path.id'), 'file_path_tags', ['file_path.id'], unique=False)
    op.create_index(op.f('ix_node_tags_node.id'), 'node_tags', ['node.id'], unique=False)
    op.create_index(op.f('ix_pack_tags_pack.id'), 'pack_tags', ['pack.id'], unique=False)
    op.create_index(op.f('ix_query_tags_query.id'), 'query_tags', ['query.id'], unique=False)
    op.create_index('idx_result_log_node_id_timestamp_desc', 'result_log', ['node_id', sa.text(u'timestamp DESC')], unique=False)
    op.create_index('idx_status_log_node_id_created_desc', 'status_log', ['node_id', sa.text(u'created DESC')], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_status_log_node_id_created_desc', table_name='status_log')
    op.drop_index('idx_result_log_node_id_timestamp_desc', table_name='result_log')
    op.drop_index(op.f('ix_query_tags_query.id'), table_name='query_tags')
    op.drop_index(op.f('ix_pack_tags_pack.id'), table_name='pack_tags')
    op.drop_index(op.f('ix_node_tags_node.id'), table_name='node_tags')
    op.drop_index(op.f('ix_file_path_tags_file_path.id'), table_name='file_path_tags')
    op.drop_index('idx_distributed_query_task_node_id_status', table_name='distributed_query_task')
    ### end Alembic commands ###
