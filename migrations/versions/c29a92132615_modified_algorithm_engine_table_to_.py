"""Modified algorithm_engine table to store JSONB match conditions, other required fields.

Revision ID: c29a92132615
Revises: f5121de7f85f
Create Date: 2023-01-23 16:35:47.239959

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c29a92132615'
down_revision = 'f5121de7f85f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('algorithm_engine', sa.Column('algorithm_engine_version', sa.Integer(), nullable=True))
    op.add_column('algorithm_engine', sa.Column('algorithm_logic', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('algorithm_engine', sa.Column('active', sa.Boolean(), nullable=True))
    op.drop_constraint('algorithm_engine_el_criteria_has_criterion_id_fkey', 'algorithm_engine', type_='foreignkey')
    op.drop_column('algorithm_engine', 'path')
    op.drop_column('algorithm_engine', 'sequence')
    op.drop_column('algorithm_engine', 'el_criteria_has_criterion_id')
    op.create_unique_constraint('criterion_code_uix', 'criterion', ['code'])
    op.create_unique_constraint('criterion_display_name_uix', 'criterion', ['display_name'])
    op.create_unique_constraint('ontology_code_uix', 'ontology_code', ['name', 'code', 'version'])
    op.alter_column('value', 'code',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('value_code_unit_uix', 'value', type_='unique')
    op.create_unique_constraint('value_code_unit_uix', 'value', ['type', 'unit', 'value_string', 'operator'])
    op.create_unique_constraint('value_code_uix', 'value', ['code'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('value_code_uix', 'value', type_='unique')
    op.drop_constraint('value_code_unit_uix', 'value', type_='unique')
    op.create_unique_constraint('value_code_unit_uix', 'value', ['code', 'type', 'unit', 'value_string', 'operator'])
    op.alter_column('value', 'code',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint('ontology_code_uix', 'ontology_code', type_='unique')
    op.drop_constraint('criterion_display_name_uix', 'criterion', type_='unique')
    op.drop_constraint('criterion_code_uix', 'criterion', type_='unique')
    op.add_column('algorithm_engine', sa.Column('el_criteria_has_criterion_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('algorithm_engine', sa.Column('sequence', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('algorithm_engine', sa.Column('path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key('algorithm_engine_el_criteria_has_criterion_id_fkey', 'algorithm_engine', 'el_criteria_has_criterion', ['el_criteria_has_criterion_id'], ['id'])
    op.drop_column('algorithm_engine', 'active')
    op.drop_column('algorithm_engine', 'algorithm_logic')
    op.drop_column('algorithm_engine', 'algorithm_engine_version')
    # ### end Alembic commands ###