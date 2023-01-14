"""add the last fucking collumns to table posts

Revision ID: 722e767c2006
Revises: dc0f3135a60f
Create Date: 2023-01-14 13:18:10.087699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '722e767c2006'
down_revision = 'dc0f3135a60f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
