"""Removed eligibility_criteria_info table and relationships.

Revision ID: 93c15139a439
Revises: 0efe88d98640
Create Date: 2024-07-28 16:52:07.871525

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '93c15139a439'
down_revision = '0efe88d98640'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eligibility_criteria_info')
    op.alter_column('criterion_staging', 'criterion_adjudication_status',
               existing_type=postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='adjudication_status'),
               type_=postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='adjudication_status'),
               existing_nullable=False)
    op.alter_column('criterion_staging', 'echc_adjudication_status',
               existing_type=postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='echc_adjudication_status'),
               type_=postgresql.ENUM('NEW', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='echc_adjudication_status'),
               existing_nullable=False)

    study_version_status = postgresql.ENUM('NEW','ACTIVE', 'IN_PROCESS', 'INACTIVE', name='study_version_status')
    study_version_status.create(op.get_bind())

    op.add_column('study_version', sa.Column('status', postgresql.ENUM('NEW','ACTIVE', 'IN_PROCESS', 'INACTIVE', name='study_version_status'), nullable=True))
    op.add_column('study_version', sa.Column('eligibility_criteria_id', sa.Integer(), nullable=True))
    op.add_column('study_version', sa.Column('study_algorithm_engine_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_study_algorithm_engine_id', 'study_version', 'study_algorithm_engine', ['study_algorithm_engine_id'], ['id'])
    op.create_foreign_key('fk_eligibility_criteria_id', 'study_version', 'eligibility_criteria', ['eligibility_criteria_id'], ['id'])
    op.drop_column('study_version', 'active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('study_version', sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_constraint('fk_eligibility_criteria_id', 'study_version', type_='foreignkey')
    op.drop_constraint('fk_study_algorithm_engine_id', 'study_version', type_='foreignkey')
    op.drop_column('study_version', 'study_algorithm_engine_id')
    op.drop_column('study_version', 'eligibility_criteria_id')
    op.drop_column('study_version', 'status')
    op.alter_column('criterion_staging', 'echc_adjudication_status',
               existing_type=postgresql.ENUM('NEW', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='echc_adjudication_status'),
               type_=postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='echc_adjudication_status'),
               existing_nullable=False)
    op.alter_column('criterion_staging', 'criterion_adjudication_status',
               existing_type=postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='adjudication_status'),
               type_=postgresql.ENUM('NEW', 'EXISTING', 'ACTIVE', 'IN_PROCESS', 'INACTIVE', name='adjudication_status'),
               existing_nullable=False)
    op.create_table('eligibility_criteria_info',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('create_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('study_version_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('study_algorithm_engine_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('eligibility_criteria_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['eligibility_criteria_id'], ['eligibility_criteria.id'], name='fk_eligibility_criteria_id'),
    sa.ForeignKeyConstraint(['study_algorithm_engine_id'], ['study_algorithm_engine.id'], name='fk_study_algorithm_engine_id'),
    sa.ForeignKeyConstraint(['study_version_id'], ['study_version.id'], name='fk_study_version_id'),
    sa.PrimaryKeyConstraint('id', name='eligibility_criteria_info_pkey'),
    )
    sa.Enum('NEW','ACTIVE', 'IN_PROCESS', 'INACTIVE',name='study_version_status').drop(op.get_bind())
    op.add_column('eligibility_criteria_info', sa.Column('status', postgresql.ENUM('ACTIVE', 'IN_PROCESS', 'INACTIVE', name='eligibilityCriteriaInfoStatus'), nullable=False))
    # ### end Alembic commands ###
