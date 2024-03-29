"""empty message

Revision ID: 649e2b29fb4c
Revises: 92f0c1bf2232
Create Date: 2018-09-28 13:27:10.655162

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '649e2b29fb4c'
down_revision = '92f0c1bf2232'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resources',
                    sa.Column('id', sa.String(length=36), nullable=False),
                    sa.Column('name', sa.String(length=60), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True),
                    sa.Column('created_by', sa.String(), nullable=True),
                    sa.Column('updated_by', sa.String(), nullable=True),
                    sa.Column('deleted_by', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'resource_access_levels',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('deleted', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('deleted_by', sa.String(), nullable=True),
        sa.Column('role_id', sa.String(), nullable=False),
        sa.Column('resource_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['resource_id'],
            ['resources.id'],
        ), sa.ForeignKeyConstraint(
            ['role_id'],
            ['roles.id'],
        ), sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'resource_permissions',
        sa.Column('resource_access_level_id', sa.String(), nullable=False),
        sa.Column('permission_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['permission_id'],
            ['permissions.id'],
        ),
        sa.ForeignKeyConstraint(
            ['resource_access_level_id'],
            ['resource_access_levels.id'],
        ), sa.PrimaryKeyConstraint('resource_access_level_id',
                                   'permission_id'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resource_permissions')
    op.drop_table('resource_access_levels')
    op.drop_table('resources')
    # ### end Alembic commands ###
