"""empty message

Revision ID: 582eee64cf54
Revises: 1cb6cb3b4bda
Create Date: 2019-07-11 11:47:26.878069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '582eee64cf54'
down_revision = 'fb1cd924081f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('asset_notes',
                    sa.Column('id', sa.String(length=36), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True),
                    sa.Column('created_by', sa.String(), nullable=True),
                    sa.Column('updated_by', sa.String(), nullable=True),
                    sa.Column('deleted_by', sa.String(), nullable=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('body', sa.Text(), nullable=False),
                    sa.Column('asset_id', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['asset_id'], ['asset.id'], name=op.f('asset_notes_asset_id_fkey')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_asset_notes'))
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('asset_notes')
    # ### end Alembic commands ###
