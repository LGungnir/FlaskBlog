"""empty message

Revision ID: e3c1bb86ea09
Revises: fb63957c468b
Create Date: 2019-07-02 19:44:51.434512

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e3c1bb86ea09'
down_revision = 'fb63957c468b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('atimed', sa.DateTime(), nullable=True))
    op.drop_column('article', 'atime')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('atime', mysql.DATETIME(), nullable=True))
    op.drop_column('article', 'atimed')
    # ### end Alembic commands ###