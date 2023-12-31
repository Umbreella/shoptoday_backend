"""Rename balance field in Transactions

Revision ID: b49f363a7ee9
Revises: 4f3dbf6d08fc
Create Date: 2023-06-20 11:41:40.128686

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b49f363a7ee9'
down_revision = '4f3dbf6d08fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'balance', new_column_name='amount')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'amount', new_column_name='balance')
    # ### end Alembic commands ###
