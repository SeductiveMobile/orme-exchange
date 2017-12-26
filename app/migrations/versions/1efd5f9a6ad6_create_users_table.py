"""Create users table

Revision ID: 1efd5f9a6ad6
Revises: 
Create Date: 2017-12-26 13:44:01.451352

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1efd5f9a6ad6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False)
    )


def downgrade():
    op.drop_table('users')
