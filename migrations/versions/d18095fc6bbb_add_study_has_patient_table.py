"""add study_has_patient table

Revision ID: d18095fc6bbb
Revises: 33779211b25c
Create Date: 2023-08-11 18:28:50.043106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd18095fc6bbb'
down_revision = '33779211b25c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'study_has_patient',
        sa.Column('study_id', sa.Integer, sa.ForeignKey('study.id'), primary_key=True),
        sa.Column('patient_id', sa.Integer, primary_key=True),
        sa.Column('data', sa.JSON, nullable=False),
    )


def downgrade():
    op.drop_table('study_has_patient')
