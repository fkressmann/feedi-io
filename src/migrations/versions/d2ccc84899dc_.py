"""empty message

Revision ID: d2ccc84899dc
Revises: 52e6bab21a26
Create Date: 2021-05-30 03:31:18.360484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2ccc84899dc'
down_revision = '52e6bab21a26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_pkey', 'users', type_='primary')
    op.add_column('users', sa.Column('id', sa.Integer(), primary_key=True))
    op.create_primary_key('users_pkey', 'users', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_id_key', 'users', type_='unique')
    op.drop_constraint('users_pkey', 'users', type_='primary')
    op.create_primary_key('users_pkey', 'users', ['email'])
    op.drop_column('users', 'id')
    # ### end Alembic commands ###