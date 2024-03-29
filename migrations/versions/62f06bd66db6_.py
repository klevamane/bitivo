"""empty message

Revision ID: 62f06bd66db6
Revises: 52e5a61c032c
Create Date: 2019-01-11 12:30:18.080994

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '62f06bd66db6'
down_revision = '52e5a61c032c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('work_orders', 'end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('work_orders', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('work_orders', 'end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('work_orders', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###
