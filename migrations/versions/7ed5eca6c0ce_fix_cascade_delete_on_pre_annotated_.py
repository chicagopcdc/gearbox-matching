"""Fix cascade delete on pre_annotated_criterion_model table.

Revision ID: 7ed5eca6c0ce
Revises: a117ad8d4dda
Create Date: 2025-07-10 14:46:48.359543

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7ed5eca6c0ce'
down_revision = 'a117ad8d4dda'
branch_labels = None
depends_on = None


def upgrade():
	op.drop_constraint('pre_annotated_criterion_model_pre_annotated_criterion_id_fkey', 
        table_name='pre_annotated_criterion_model', 
		type_='foreignkey')

	op.create_foreign_key(
		op.f('pre_annotated_criterion_model_pre_annotated_criterion_id_fkey'),
	        'pre_annotated_criterion_model',
	        'pre_annotated_criterion',
	        ['pre_annotated_criterion_id'],
	        ['id'],
	        ondelete='CASCADE'
	)

def downgrade():
	op.drop_constraint('pre_annotated_criterion_model_pre_annotated_criterion_id_fkey', 
        'pre_annotated_criterion_model', 
		type_='foreignkey')

	op.create_foreign_key(
		op.f('pre_annotated_criterion_model_pre_annotated_criterion_id_fkey'),
	        'pre_annotated_criterion_model',
	        'pre_annotated_criterion',
	        ['pre_annotated_criterion_id'],
	        ['id']
	)