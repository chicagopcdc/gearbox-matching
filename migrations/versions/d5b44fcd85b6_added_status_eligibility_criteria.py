"""Added status eligibility_criteria.

Revision ID: d5b44fcd85b6
Revises: 1b17bb764a3f
Create Date: 2024-07-03 13:49:18.476673

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd5b44fcd85b6'
down_revision = '1b17bb764a3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    eligibilityCriteriaStatus = postgresql.ENUM('NEW','ACTIVE','IN_PROCESS','INACTIVE','CRITERIA_ADJUDICATION','ECHC_ADJUDICATION',name='eligibilityCriteriaStatus')
    eligibilityCriteriaStatus.create(op.get_bind())
    op.add_column('eligibility_criteria', sa.Column('status', postgresql.ENUM('NEW', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', 'CRITERIA_ADJUDICATION', 'ECHC_ADJUDICATION',name='eligibilityCriteriaStatus'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('eligibility_criteria', 'status')
    # ### end Alembic commands ###
