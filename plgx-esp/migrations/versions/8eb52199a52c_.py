"""empty message

Revision ID: 8eb52199a52c
Revises: 5bf4802bc92b
Create Date: 2021-09-23 12:15:10.842297

"""

# revision identifiers, used by Alembic.
revision = "8eb52199a52c"
down_revision = "5bf4802bc92b"

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql



def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # New updates for node_query_count table
    op.add_column("node_query_count", sa.Column("event_id", sa.String(), nullable=True))
    op.execute(
        "create index if not exists idx_result_log_scan_on_scan_value on result_log_scan using btree(scan_value);"
    )

    # Dropping tables which are not actually present
    op.drop_table("node_email")
    op.drop_table("virus_total")
    op.drop_table("ibm_force_exchange")

    op.execute(
        """
        CREATE or REPLACE FUNCTION node_query_count() RETURNS trigger
            LANGUAGE plpgsql AS
        $$BEGIN
            IF TG_OP = 'INSERT' and NEW.action != 'removed' THEN
                IF NEW.name != 'windows_events' THEN
                    UPDATE node_query_count SET total_results=total_results+1 WHERE node_id=NEW.node_id and query_name=NEW.name;
                ELSE
                    UPDATE node_query_count SET total_results=total_results+1 WHERE node_id=NEW.node_id and query_name=NEW.name and event_id=NEW.columns->>'eventid';
                END IF;
                IF found THEN
                    RETURN NEW;
                END IF;
                BEGIN
                    IF NEW.name != 'windows_events' THEN
                        INSERT INTO  node_query_count(node_id, query_name, total_results) VALUES (NEW.node_id, NEW.name, 1);
                    ELSE
                        INSERT INTO  node_query_count(node_id, query_name, event_id, total_results) VALUES (NEW.node_id, NEW.name, NEW.columns->>'eventid', 1);
                    END IF;
                    RETURN NEW;
                END;
            ELSIF TG_OP = 'DELETE' and OLD.action != 'removed' THEN
                IF OLD.name != 'windows_events' THEN
                    UPDATE node_query_count SET total_results=total_results-1 WHERE node_id=OLD.node_id and query_name=OLD.name;
                ELSE
                    UPDATE node_query_count SET total_results=total_results-1 WHERE node_id=OLD.node_id and query_name=OLD.name and event_id=OLD.columns->>'eventid';
                END IF;
                DELETE from node_query_count WHERE total_results=0;
                RETURN OLD;
            ELSE
                RETURN NULL;
            END IF;
        END;$$;
        """
    )
    op.execute("DELETE FROM node_query_count where query_name='windows_events';")
    # Counting all windows events
    op.execute(
        """
        INSERT INTO node_query_count(node_id, query_name, event_id, total_results)
        SELECT node_id, name, columns->>'eventid', count(*) FROM result_log WHERE name='windows_events' group by node_id, name, columns->>'eventid';
        """
    )
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_column("node_query_count", "event_id")
    op.drop_index("idx_result_log_scan_on_scan_value", table_name="result_log_scan")

    op.create_table(
        "ibm_force_exchange",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("search_term", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("comment", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("malware_family", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("risk", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="ibm_force_exchange_pkey"),
    )
    op.create_table(
        "virus_total",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("search_term", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("comment", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("response", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "scan_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("detections", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("total", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("permalink", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("avs", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("cves", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="virus_total_pkey"),
    )
    op.create_table(
        "node_email",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("status", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("node_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("email_verified", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column(
            "verification_token", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["node_id"], ["node.id"], name="node_email_node_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="node_email_pkey"),
    )
    # ### end Alembic commands ###
