"""Removed status from site model.

Revision ID: 47852b3ec5fd
Revises: 3a26a8e3543c
Create Date: 2023-12-11 15:29:09.168324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47852b3ec5fd'
down_revision = '3a26a8e3543c'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass