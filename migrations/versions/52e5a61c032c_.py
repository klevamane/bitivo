"""empty message
Revision ID: 52e5a61c032c
Revises: 5d662fe4d804
Create Date: 2019-01-10 06:34:32.851236
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52e5a61c032c'
down_revision = '5d662fe4d804'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('work_orders',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('deleted_by', sa.String(), nullable=True),
    sa.Column('title', sa.String(length=60), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('center_id', sa.String(), nullable=False),
    sa.Column('asset_category_id', sa.String(), nullable=False),
    sa.Column('assignee_id', sa.String(), nullable=True),
    sa.Column('frequency_type',sa.Enum('hours', 'days', 'weeks', 'months', name='frequencytypesenum'), nullable=False),
    sa.Column('frequency_units', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['asset_category_id'], ['asset_categories.id'], name='work_orders_asset_category_id_fkey', ),
    sa.ForeignKeyConstraint(['assignee_id'], ['users.token_id'], ),
    sa.ForeignKeyConstraint(['center_id'], ['centers.id'], name='work_orders_center_id_fkey', ),
    sa.PrimaryKeyConstraint('id'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('work_orders')
    op.execute("DROP TYPE frequencytypesenum")
    # ### end Alembic commands ###
