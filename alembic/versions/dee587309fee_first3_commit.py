"""first3 commit

Revision ID: dee587309fee
Revises: 0cc0a84cb73f
Create Date: 2023-09-24 17:05:00.095401

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dee587309fee'
down_revision = '0cc0a84cb73f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('front_users', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键ID'))
    op.add_column('front_users', sa.Column('create_user', sa.Integer(), nullable=True, comment='创建人'))
    op.add_column('front_users', sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'))
    op.add_column('front_users', sa.Column('update_user', sa.Integer(), nullable=True, comment='更新人'))
    op.add_column('front_users', sa.Column('is_delete', sa.Integer(), nullable=True, comment='删除标识：0-正常 1-已删除'))
    op.alter_column('front_users', 'update_time',
               existing_type=mysql.DATETIME(),
               comment='更新时间',
               existing_comment='最后一次更新时间',
               existing_nullable=True)
    op.alter_column('front_users', 'username',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False,
               existing_comment='用户名')
    op.drop_index('email', table_name='front_users')
    op.drop_index('ix_front_users_user_id', table_name='front_users')
    op.drop_column('front_users', 'creat_time')
    op.drop_column('front_users', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('front_users', sa.Column('user_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=False, comment='用户id'))
    op.add_column('front_users', sa.Column('creat_time', mysql.DATETIME(), nullable=True, comment='创建时间'))
    op.create_index('ix_front_users_user_id', 'front_users', ['user_id'], unique=False)
    op.create_index('email', 'front_users', ['email'], unique=False)
    op.alter_column('front_users', 'username',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True,
               existing_comment='用户名')
    op.alter_column('front_users', 'update_time',
               existing_type=mysql.DATETIME(),
               comment='最后一次更新时间',
               existing_comment='更新时间',
               existing_nullable=True)
    op.drop_column('front_users', 'is_delete')
    op.drop_column('front_users', 'update_user')
    op.drop_column('front_users', 'create_time')
    op.drop_column('front_users', 'create_user')
    op.drop_column('front_users', 'id')
    # ### end Alembic commands ###
