"""使用basemode

Revision ID: 0c512f467a01
Revises: 85ebfb24ed1a
Create Date: 2023-09-24 17:12:42.624329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c512f467a01'
down_revision = '85ebfb24ed1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('front_users', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键ID'))
    op.add_column('front_users', sa.Column('create_user', sa.Integer(), nullable=True, comment='创建人'))
    op.add_column('front_users', sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'))
    op.add_column('front_users', sa.Column('update_user', sa.Integer(), nullable=True, comment='更新人'))
    op.add_column('front_users', sa.Column('update_time', sa.DateTime(), nullable=True, comment='更新时间'))
    op.add_column('front_users', sa.Column('is_delete', sa.Integer(), nullable=True, comment='删除标识：0-正常 1-已删除'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('front_users', 'is_delete')
    op.drop_column('front_users', 'update_time')
    op.drop_column('front_users', 'update_user')
    op.drop_column('front_users', 'create_time')
    op.drop_column('front_users', 'create_user')
    op.drop_column('front_users', 'id')
    # ### end Alembic commands ###
