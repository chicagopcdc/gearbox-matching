"""add study_has_patient table

Revision ID: d18095fc6bbb
Revises: 33779211b25c
Create Date: 2023-08-11 18:28:50.043106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd18095fc6bbb'
down_revision = 'f3c7a489a0c0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'study_has_patient',
        sa.Column('study_id', sa.Integer, nullable=False),
        sa.Column('patient_id', sa.String, nullable=False),
        sa.Column('data', sa.JSON, nullable=False),
        sa.Column('source_id', sa.String, nullable=False),
        sa.ForeignKeyConstraint(['study_id'], ['study.id'], ),
        sa.PrimaryKeyConstraint('study_id', 'patient_id', 'source_id')
    )


def downgrade():
    op.drop_table('study_has_patient')
