"""rename_lombaryers_fields

Revision ID: dbb1fd4a959d
Revises: 267aaf26546c
Create Date: 2022-10-17 10:04:04.927086

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'dbb1fd4a959d'
down_revision = '267aaf26546c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requests', sa.Column('sum_lombaryers', sa.Integer(), nullable=True))
    op.drop_column('requests', 'lombaryers_sum')
    op.add_column('users', sa.Column('sum_lombaryers', sa.Integer(), nullable=True))
    op.drop_column('users', 'lombaryers_sum')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lombaryers_sum', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('users', 'sum_lombaryers')
    op.add_column('requests', sa.Column('lombaryers_sum', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('requests', 'sum_lombaryers')
    # ### end Alembic commands ###
