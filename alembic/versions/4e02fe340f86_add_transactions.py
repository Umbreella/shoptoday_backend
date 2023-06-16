"""Add Transactions

Revision ID: 4e02fe340f86
Revises: 23962cf7f4a1
Create Date: 2023-06-16 16:48:03.327969

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4e02fe340f86'
down_revision = '23962cf7f4a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('balance', sa.DECIMAL(), nullable=False),
    sa.Column('bank_account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bank_account_id'], ['bank_accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    # ### end Alembic commands ###
