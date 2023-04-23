"""empty message

Revision ID: 5251c6f56d9b
Revises: 
Create Date: 2023-04-23 22:22:18.932462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5251c6f56d9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('long_description', sa.String(), nullable=False),
    sa.Column('short_description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_course_id'), ['id'], unique=False)

    op.create_table('module',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('long_description', sa.String(), nullable=False),
    sa.Column('short_description', sa.String(length=255), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_module_id'), ['id'], unique=False)

    op.create_table('lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_lesson_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_lesson_id'))

    op.drop_table('lesson')
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_module_id'))

    op.drop_table('module')
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_course_id'))

    op.drop_table('course')
    # ### end Alembic commands ###
