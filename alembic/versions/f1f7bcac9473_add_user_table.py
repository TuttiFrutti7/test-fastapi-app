"""add user table

Revision ID: f1f7bcac9473
Revises: 99681621965d
Create Date: 2023-01-14 11:13:34.820230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1f7bcac9473'
down_revision = '99681621965d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )
    pass


def downgrade():
    op.drop_table('users')
    pass
