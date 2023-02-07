"""empty message

Revision ID: 9308d94fb9c9
Revises: 3abfbc2d035b
Create Date: 2023-02-03 13:48:51.919609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9308d94fb9c9'
down_revision = '3abfbc2d035b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('votes', sa.Column('dir', sa.Integer(), nullable=False))
    op.drop_column('votes', 'like')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('votes', sa.Column('like', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('votes', 'dir')
    # ### end Alembic commands ###