"""update study table with follow_up_info column

Revision ID: a20394e0f900
Revises: d18095fc6bbb
Create Date: 2023-11-03 14:54:36.361317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a20394e0f900'
down_revision = 'd18095fc6bbb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('study', sa.Column('follow_up_info', sa.Text))


def downgrade():
    op.drop_column('study', 'follow_up_info')
