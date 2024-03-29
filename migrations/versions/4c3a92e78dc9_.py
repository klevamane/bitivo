"""empty message

Revision ID: 4c3a92e78dc9
Revises: 18ed7b1b42e4
Create Date: 2019-07-23 15:54:10.001838

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4c3a92e78dc9'
down_revision = '18ed7b1b42e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asset_repair_logs',
                  sa.Column('date_reported', sa.DateTime(), nullable=True))
    op.add_column('asset_repair_logs',
                  sa.Column('defect_type', sa.String(), nullable=True))
    op.add_column('asset_repair_logs',
                  sa.Column('repairer', sa.String(), nullable=True))
    op.drop_constraint(
        'asset_repair_logs_assignee_id_fkey',
        'asset_repair_logs',
        type_='foreignkey')
    op.drop_constraint(
        'asset_repair_logs_complainant_id_fkey',
        'asset_repair_logs',
        type_='foreignkey')
    op.drop_column('asset_repair_logs', 'complainant_id')
    op.drop_column('asset_repair_logs', 'assignee_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'asset_repair_logs',
        sa.Column(
            'assignee_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column(
        'asset_repair_logs',
        sa.Column(
            'complainant_id',
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False))
    op.create_foreign_key('asset_repair_logs_complainant_id_fkey',
                          'asset_repair_logs', 'users', ['complainant_id'],
                          ['token_id'])
    op.create_foreign_key('asset_repair_logs_assignee_id_fkey',
                          'asset_repair_logs', 'users', ['assignee_id'],
                          ['token_id'])
    op.drop_column('asset_repair_logs', 'repairer')
    op.drop_column('asset_repair_logs', 'defect_type')
    op.drop_column('asset_repair_logs', 'date_reported')
    # ### end Alembic commands ###
