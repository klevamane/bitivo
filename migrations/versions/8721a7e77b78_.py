"""empty message

Revision ID: 8721a7e77b78
Revises: 8f6b3f05ade9
Create Date: 2019-05-22 10:56:41.168155

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8721a7e77b78'
down_revision = '8f6b3f05ade9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asset_categories', sa.Column('image', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('asset_categories', 'image')
    # ### end Alembic commands ###