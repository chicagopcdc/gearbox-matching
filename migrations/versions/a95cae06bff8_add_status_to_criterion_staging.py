"""Add status to criterion_staging.

Revision ID: a95cae06bff8
Revises: 3f15449b3069
Create Date: 2024-07-15 12:43:55.565941

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a95cae06bff8'
down_revision = '3f15449b3069'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    criterionstagingstatus = postgresql.ENUM('NEW','EXISTING','ACTIVE','IN_PROCESS','INACTIVE',name='criterionstagingstatus')
    criterionstagingstatus.create(op.get_bind())
    op.add_column('criterion_staging', sa.Column('status', postgresql.ENUM('NEW', 'EXISTING','ACTIVE', 'IN_PROCESS', 'INACTIVE', name='criterionstagingstatus'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('criterion_staging', 'status')
    # ### end Alembic commands ###
