"""create contracts table

Revision ID: 4f2e5d25f93e
Revises: fa05e806059f
Create Date: 2017-12-29 16:07:32.766799

"""
import datetime
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4f2e5d25f93e'
down_revision = 'fa05e806059f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'contracts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('address', sa.String(255), nullable=False),
        sa.Column('abi', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow()),
        sa.Column('updated_at', sa.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow()),
    )


def downgrade():
    op.drop_table('contracts')
