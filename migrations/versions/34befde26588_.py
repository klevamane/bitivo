"""empty message

Revision ID: 34befde26588
Revises: 582eee64cf54
Create Date: 2019-07-12 08:46:55.348393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34befde26588'
down_revision = '582eee64cf54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('asset_insurances',
                    sa.Column('id', sa.String(length=36), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True),
                    sa.Column('created_by', sa.String(), nullable=True),
                    sa.Column('updated_by', sa.String(), nullable=True),
                    sa.Column('deleted_by', sa.String(), nullable=True),
                    sa.Column('company', sa.String(length=250), nullable=False),
                    sa.Column('start_date', sa.Date(), nullable=False),
                    sa.Column('end_date', sa.Date(), nullable=False),
                    sa.Column('asset_id', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['asset_id'],
                        ['asset.id'],
                        name=op.f('asset_insurances_asset_id_fkey')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_asset_insurances'))
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('asset_insurances')
    # ### end Alembic commands ###