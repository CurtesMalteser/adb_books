"""Remove 'shelf' from BookDto

Revision ID: 525c7d8f2035
Revises: 630f290377a0
Create Date: 2024-09-15 14:53:41.310610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '525c7d8f2035'
down_revision = '630f290377a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_column('shelf')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shelf', sa.VARCHAR(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
