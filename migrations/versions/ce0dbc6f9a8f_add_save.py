"""add_save

Revision ID: ce0dbc6f9a8f
Revises: 
Create Date: 2021-09-30 13:24:43.715584

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'ce0dbc6f9a8f'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        "saved_input",
        sa.Column("id", sa.Integer, nullable=False, autoincrement=True),
        sa.Column("user_id", sa.Integer, nullable=False),   
        sa.Column("patient_id", sa.Integer, nullable=True),
        sa.Column("create_date", sa.DateTime, nullable=False),
        sa.Column("update_date", sa.DateTime, nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("saved_input")


