"""Add Addresses table and link it with users

Revision ID: fa05e806059f
Revises: 1efd5f9a6ad6
Create Date: 2017-12-26 14:06:09.146810

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa05e806059f'
down_revision = '1efd5f9a6ad6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'addresses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', sa.String(255), nullable=False, unique=True),
        sa.Column('balance', sa.BigInteger, default=0),
        sa.Column('currency', sa.Enum('bitcoin', 'ethereum', name='currency_types')),
        sa.Column('wallet_type', sa.Enum('orv', 'user', name='wallet_types')),
        sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow()),
        sa.Column('updated_at', sa.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow()),
        sa.Column('password', sa.String(255)),
        # # TODO: Add private key field
        sa.Column('user_id', sa.Integer, index=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )


def downgrade():
    op.drop_table('addresses')
