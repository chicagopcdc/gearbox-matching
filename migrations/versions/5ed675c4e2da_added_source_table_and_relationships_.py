"""Added source table and relationships, mods to site - removed active added location info.

Revision ID: 5ed675c4e2da
Revises: 0d8f98ceec8d
Create Date: 2024-01-04 13:49:29.675653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ed675c4e2da'
down_revision = '0d8f98ceec8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('source',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('source', sa.String(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('source', name='source_uix')
    )
    op.add_column('site', sa.Column('country', sa.String(), nullable=True))
    op.add_column('site', sa.Column('city', sa.String(), nullable=True))
    op.add_column('site', sa.Column('state', sa.String(), nullable=True))
    op.add_column('site', sa.Column('zip', sa.String(), nullable=True))
    op.add_column('site', sa.Column('source_id', sa.Integer(), nullable=True))
    op.drop_constraint('site_uix', 'site', type_='unique')
    op.create_unique_constraint('site_uix', 'site', ['name', 'zip'])
    op.create_foreign_key('fk_site_source_id', 'site', 'source', ['source_id'], ['id'])
    op.drop_column('site', 'active')
    op.drop_column('site', 'code')
    op.add_column('study', sa.Column('source_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_study_source_id', 'study', 'source', ['source_id'], ['id'])
    op.add_column('study_external_id', sa.Column('create_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_study_source_id', 'study', type_='foreignkey')
    op.drop_column('study', 'source_id')
    op.add_column('site', sa.Column('code', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('site', sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_constraint('fk_site_source_id', 'site', type_='foreignkey')
    op.drop_constraint('site_uix', 'site', type_='unique')
    op.create_unique_constraint('site_uix', 'site', ['name', 'code'])
    op.drop_column('site', 'source_id')
    op.drop_column('site', 'zip')
    op.drop_column('site', 'state')
    op.drop_column('site', 'city')
    op.drop_column('site', 'country')
    op.drop_table('source')
    op.drop_column('study_external_id', 'create_date')
    # ### end Alembic commands ###