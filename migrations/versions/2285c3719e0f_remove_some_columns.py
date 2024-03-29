"""remove some columns

Revision ID: 2285c3719e0f
Revises: 7d5c3da146a1
Create Date: 2023-04-24 00:40:03.522578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2285c3719e0f'
down_revision = '7d5c3da146a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))
        batch_op.drop_column('short_description')
        batch_op.drop_column('long_description')


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.add_column(sa.Column('long_description', sa.VARCHAR(), nullable=False))
        batch_op.add_column(sa.Column('short_description', sa.VARCHAR(length=255), nullable=False))
        batch_op.drop_column('description')

    # ### end Alembic commands ###
