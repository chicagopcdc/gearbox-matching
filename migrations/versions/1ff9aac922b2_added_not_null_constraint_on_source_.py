"""Added not null constraint on source.priority.

Revision ID: 1ff9aac922b2
Revises: e2dafa86eee0
Create Date: 2024-01-16 16:37:38.502297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ff9aac922b2'
down_revision = 'e2dafa86eee0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('source', 'priority',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('source', 'priority',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###