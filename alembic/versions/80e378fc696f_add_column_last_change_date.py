"""add column last_change_date

Revision ID: 80e378fc696f
Revises: bafb3bd350a6
Create Date: 2022-11-10 21:26:57.842968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80e378fc696f'
down_revision = 'bafb3bd350a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('last_change_date', sa.DateTime))


def downgrade() -> None:
    op.drop_column('users', 'last_change_date')
