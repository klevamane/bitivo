"""cater for asset sub-categories by extending AssetCategories model to have description and parent_id fields

Revision ID: 18ed7b1b42e4
Revises: 84a254f3a1e4
Create Date: 2019-07-17 18:42:17.407252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18ed7b1b42e4'
down_revision = '84a254f3a1e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asset_categories', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('asset_categories', sa.Column('parent_id', sa.String(length=60), nullable=True))
    op.create_foreign_key(op.f('asset_categories_parent_id_fkey'), 'asset_categories', 'asset_categories', ['parent_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('asset_categories_parent_id_fkey'), 'asset_categories', type_='foreignkey')
    op.drop_column('asset_categories', 'parent_id')
    op.drop_column('asset_categories', 'description')
    # ### end Alembic commands ###