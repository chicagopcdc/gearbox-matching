"""Added study_version to study_version table.

Revision ID: 1aa0e74815e7
Revises: 41d465e25870
Create Date: 2023-02-14 20:09:12.644114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aa0e74815e7'
down_revision = '41d465e25870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('study_code_uix', 'study', ['code'])
    op.add_column('study_version', sa.Column('study_version', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('study_version', 'study_version')
    op.drop_constraint('study_code_uix', 'study', type_='unique')
    # ### end Alembic commands ###