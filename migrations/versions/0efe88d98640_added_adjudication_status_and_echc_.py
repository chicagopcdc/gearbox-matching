"""Added adjudication_status and echc_adjudication_status to criterion_staging.

Revision ID: 0efe88d98640
Revises: 8295f20f3a8e
Create Date: 2024-07-26 13:34:52.217355

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0efe88d98640'
down_revision = '8295f20f3a8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    adjudication_status = postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='adjudication_status')
    adjudication_status.create(op.get_bind())

    echc_adjudication_status = postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='echc_adjudication_status')
    echc_adjudication_status.create(op.get_bind())

    op.add_column('criterion_staging', sa.Column('criterion_adjudication_status', postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='adjudication_status'), nullable=False))
    op.add_column('criterion_staging', sa.Column('echc_adjudication_status', postgresql.ENUM('NEW', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='echc_adjudication_status'), nullable=False))
    op.drop_column('criterion_staging', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('criterion_staging', sa.Column('status', postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='criterionstagingstatus'), autoincrement=False, nullable=False))
    op.drop_column('criterion_staging', 'echc_adjudication_status')
    op.drop_column('criterion_staging', 'criterion_adjudication_status')
    # ### end Alembic commands ###
    sa.Enum('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE',name='adjudication_status').drop(op.get_bind())
    sa.Enum('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE',name='echc_adjudication_status').drop(op.get_bind())