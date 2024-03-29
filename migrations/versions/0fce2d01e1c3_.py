"""empty message

Revision ID: 0fce2d01e1c3
Revises: fbd06aa0496e
Create Date: 2019-02-28 19:17:27.353201

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0fce2d01e1c3'
down_revision = 'fbd06aa0496e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "ALTER TABLE ASSET RENAME CONSTRAINT asset_tag_key TO uq_asset_tag")
    op.execute(
        "ALTER TABLE USERS RENAME CONSTRAINT unique_token_id TO uq_users_token_id"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "ALTER TABLE USERS RENAME CONSTRAINT uq_users_token_id TO unique_token_id"
    )
    op.execute(
        "ALTER TABLE ASSET RENAME CONSTRAINT uq_asset_tag TO asset_tag_key")
    # ### end Alembic commands ###
