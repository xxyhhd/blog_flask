"""empty message

Revision ID: 3b0da06c44ab
Revises: f99d6848c811
Create Date: 2019-03-03 13:49:50.622417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b0da06c44ab'
down_revision = 'f99d6848c811'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('timestamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'timestamp')
    # ### end Alembic commands ###
