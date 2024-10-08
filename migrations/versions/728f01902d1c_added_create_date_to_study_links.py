"""Added create_date to study_links.

Revision ID: 728f01902d1c
Revises: 60a3569ba935
Create Date: 2023-11-16 13:11:11.520748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '728f01902d1c'
down_revision = '60a3569ba935'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('study', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('study', 'code',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('study_links', sa.Column('create_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('study_links', 'create_date')
    op.alter_column('study', 'code',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('study', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
