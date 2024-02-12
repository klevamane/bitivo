"""empty message

Revision ID: 0177171a0a19
Revises: 7b7d87c75ac2
Create Date: 2018-11-09 14:14:03.496564

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0177171a0a19'
down_revision = '7b7d87c75ac2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("COMMIT")
    op.execute("ALTER TYPE assignee_type ADD VALUE 'store'")


def downgrade():
    update_to_space = "UPDATE asset SET assignee_type = 'space' WHERE assignee_type = 'store'"
    op.execute(update_to_space)
    get_store_enum = \
    """SELECT t.typname,
       e.enumlabel,
       e.enumsortorder,
       e.enumtypid
       FROM pg_type t
       JOIN pg_enum e ON e.enumtypid = t.oid
       WHERE t.typname = 'assignee_type'
       AND e.enumlabel = 'store'
       ORDER BY 1, enumsortorder;
    """
    conn = op.get_bind()
    result = conn.execute(get_store_enum).fetchall()[0]

    remove_store_enum = f"""DELETE FROM pg_enum WHERE enumtypid = {result[-1]} AND enumlabel = 'store'"""
    conn.execute(remove_store_enum)
