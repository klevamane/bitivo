"""empty message

Revision ID: 038599261f2a
Revises: 0a59db9e93be
Create Date: 2019-02-08 17:27:19.186649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '038599261f2a'
down_revision = '0a59db9e93be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('maintenance_categories',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('title', sa.String(length=60), nullable=False),
    sa.Column('asset_category_id', sa.String(), nullable=False),
    sa.Column('center_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['asset_category_id'],['asset_categories.id'],), 
    sa.ForeignKeyConstraint(['center_id'],['centers.id'],), 
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('schedules', 'assignee_id', 
                existing_type=sa.VARCHAR(),
                nullable=False)
    op.add_column('work_orders',sa.Column('maintenance_category_id', sa.String(), nullable=True))
    op.drop_constraint('work_orders_asset_category_id_fkey','work_orders', type_='foreignkey')
    op.create_foreign_key('work_orders_maintenance_category_id_fkey','work_orders', 'maintenance_categories',['maintenance_category_id'], ['id'])
    op.drop_column('work_orders', 'asset_category_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('work_orders',sa.Column('asset_category_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint('work_orders_maintenance_category_id_fkey', 'work_orders', type_='foreignkey')
    op.create_foreign_key('work_orders_asset_category_id_fkey', 'work_orders', 'asset_categories', ['asset_category_id'], ['id'])
    op.drop_column('work_orders', 'maintenance_category_id')
    op.alter_column('schedules', 'assignee_id',
                existing_type=sa.VARCHAR(),
                nullable=True)
    op.drop_table('maintenance_categories')
    # ### end Alembic commands ###
