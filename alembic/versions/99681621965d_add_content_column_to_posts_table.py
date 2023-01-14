"""add content column to posts table

Revision ID: 99681621965d
Revises: bac664949c35
Create Date: 2023-01-14 10:52:37.069479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99681621965d'
down_revision = 'bac664949c35'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
