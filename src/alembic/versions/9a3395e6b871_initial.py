"""initial

Revision ID: 9a3395e6b871
Revises: 
Create Date: 2018-09-29 14:29:44.354345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a3395e6b871'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('batch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('base_currency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['base_currency_id'], ['currency.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date')
    )
    op.create_table('currency_rate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rate', sa.DECIMAL(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('batch_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['batch_id'], ['batch.id'], ),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('currency_id', 'batch_id', name='_currency_batch_uc')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('currency_rate')
    op.drop_table('batch')
    op.drop_table('currency')
    # ### end Alembic commands ###
