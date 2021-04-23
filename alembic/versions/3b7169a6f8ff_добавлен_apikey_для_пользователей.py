"""добавлен apikey для пользователей

Revision ID: 3b7169a6f8ff
Revises: 
Create Date: 2021-04-22 20:28:36.847101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b7169a6f8ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('apikey', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['apikey'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'apikey')
    # ### end Alembic commands ###
