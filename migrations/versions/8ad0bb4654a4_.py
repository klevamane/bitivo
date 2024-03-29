"""empty message

Revision ID: 8ad0bb4654a4
Revises: 7f4942d6b052
Create Date: 2018-08-15 14:33:14.222261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ad0bb4654a4'
down_revision = '7f4942d6b052'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('description', sa.String(length=250), nullable=False, server_default='this is a temporary value'))
    op.drop_constraint('roles_title_key', 'roles', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('roles_title_key', 'roles', ['title'])
    op.drop_column('roles', 'description')
    # ### end Alembic commands ###
