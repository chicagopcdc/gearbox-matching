"""Added comments to study_version model.

Revision ID: eb4f4e85f0e4
Revises: 93c15139a439
Create Date: 2024-08-05 12:56:16.590313

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eb4f4e85f0e4'
down_revision = '93c15139a439'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('study_algorithm_engine', 'algorithm_version')
    op.add_column('study_version', sa.Column('comments', sa.String(), nullable=True))
    op.alter_column('study_version', 'status',
               existing_type=postgresql.ENUM('NEW', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='study_version_status'),
               type_=postgresql.ENUM('NEW', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='study_version_status'),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('study_version', 'status',
               existing_type=postgresql.ENUM('NEW', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='study_version_status'),
               type_=postgresql.ENUM('NEW', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='study_version_status'),
               existing_nullable=True)
    op.drop_column('study_version', 'comments')
    op.add_column('study_algorithm_engine', sa.Column('algorithm_version', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
