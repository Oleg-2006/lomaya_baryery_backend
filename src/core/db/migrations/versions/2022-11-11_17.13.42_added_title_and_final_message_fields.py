"""Added title and final_message fields

Revision ID: 04de55017d8d
Revises: 415099a58080
Create Date: 2022-11-11 17:13:42.360168

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '04de55017d8d'
down_revision = '415099a58080'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shifts', sa.Column('title', sa.String(length=100), server_default='', nullable=False))
    op.add_column('shifts', sa.Column('final_message', sa.String(length=150), server_default='', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shifts', 'final_message')
    op.drop_column('shifts', 'title')
    # ### end Alembic commands ###
