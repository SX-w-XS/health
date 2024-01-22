"""生成其他表

Revision ID: 50ac5ccbe564
Revises: 10695c426dbc
Create Date: 2023-09-28 11:51:54.544302

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '50ac5ccbe564'
down_revision = '10695c426dbc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('model_front_users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('create_user', sa.BigInteger(), nullable=True, comment='创建人'),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_user', sa.Integer(), nullable=True, comment='更新人'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.Column('is_delete', sa.Integer(), nullable=True, comment='删除标识：0-正常 1-已删除'),
    sa.Column('username', sa.String(length=20), nullable=True, comment='用户名'),
    sa.Column('gender', sa.String(length=20), nullable=True, comment='性别'),
    sa.Column('age', sa.String(length=4), nullable=True, comment='年龄'),
    sa.Column('location', sa.String(length=200), nullable=True, comment='位置'),
    sa.Column('level', sa.String(length=20), nullable=True, comment='学业水平'),
    sa.Column('email', sa.String(length=200), nullable=False, comment='邮箱'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='参与状态'),
    sa.Column('is_person_questionare', sa.Boolean(), nullable=True, comment='是否完成问卷'),
    sa.Column('is_mental_questionare', sa.Boolean(), nullable=True, comment='是否完成问卷'),
    sa.Column('is_read_audio', sa.Boolean(), nullable=True, comment='是否语音录制'),
    sa.Column('is_read_video', sa.Boolean(), nullable=True, comment='是否视频录制'),
    sa.Column('is_interview_audio', sa.Boolean(), nullable=True, comment='是否语音面试录制'),
    sa.Column('is_interview_video', sa.Boolean(), nullable=True, comment='是否视频面试录制'),
    sa.Column('mental_status', sa.String(length=20), nullable=True, comment='心理状态'),
    sa.Column('is_send_mail', sa.Boolean(), nullable=True, comment='是否发送邮件'),
    sa.PrimaryKeyConstraint('id'),
    comment='前端用户表'
    )
    op.create_table('model_question_records',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('create_user', sa.BigInteger(), nullable=True, comment='创建人'),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_user', sa.Integer(), nullable=True, comment='更新人'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.Column('is_delete', sa.Integer(), nullable=True, comment='删除标识：0-正常 1-已删除'),
    sa.Column('qestion_type', sa.String(length=20), nullable=True, comment='问题类型'),
    sa.Column('text_content', sa.String(length=200), nullable=True, comment='问题内容'),
    sa.Column('emotion_type', sa.String(length=20), nullable=True, comment='情感类型'),
    sa.Column('other', sa.String(length=200), nullable=True, comment='其他'),
    sa.Column('qestion_status', sa.String(length=200), nullable=True, comment='问题状态'),
    sa.PrimaryKeyConstraint('id'),
    comment='问题记录表'
    )
    op.create_table('model_questionaire',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('create_user', sa.BigInteger(), nullable=True, comment='创建人'),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_user', sa.Integer(), nullable=True, comment='更新人'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.Column('is_delete', sa.Integer(), nullable=True, comment='删除标识：0-正常 1-已删除'),
    sa.Column('questionnaire_name', sa.String(length=200), nullable=True, comment='问卷名称'),
    sa.Column('questionnaire_type', sa.String(length=200), nullable=True, comment='问卷类型'),
    sa.Column('questionnaire_beizhu', sa.String(length=200), nullable=True, comment='文件类型'),
    sa.Column('questionnaire_path', sa.String(length=200), nullable=True, comment='问卷路径'),
    sa.Column('questionnaire_status', sa.String(length=200), nullable=True, comment='问卷状态'),
    sa.Column('other', sa.String(length=200), nullable=True, comment='其他'),
    sa.PrimaryKeyConstraint('id'),
    comment='问卷管理'
    )
    op.create_table('model_file_records',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('create_user', sa.BigInteger(), nullable=True, comment='创建人'),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_user', sa.Integer(), nullable=True, comment='更新人'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.Column('is_delete', sa.Integer(), nullable=True, comment='删除标识：0-正常 1-已删除'),
    sa.Column('file_name', sa.String(length=200), nullable=True, comment='文件名称'),
    sa.Column('file_type', sa.String(length=200), nullable=True, comment='文件类型'),
    sa.Column('file_time', sa.String(length=200), nullable=True, comment='文件时长'),
    sa.Column('file_url', sa.String(length=200), nullable=True, comment='文件url'),
    sa.Column('file_status', sa.String(length=200), nullable=True, comment='文件状态'),
    sa.Column('other', sa.String(length=200), nullable=True, comment='其他'),
    sa.Column('model_front_users_id', sa.Integer(), nullable=True, comment='前端用户id'),
    sa.Column('model_question_records_id', sa.Integer(), nullable=True, comment='对应的问题id'),
    sa.ForeignKeyConstraint(['model_front_users_id'], ['model_front_users.id'], ),
    sa.ForeignKeyConstraint(['model_question_records_id'], ['model_question_records.id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='文件存取记录表'
    )
    op.drop_table('front_users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('front_users',
    sa.Column('username', mysql.VARCHAR(length=20), nullable=False, comment='用户名'),
    sa.Column('gender', mysql.VARCHAR(length=20), nullable=True, comment='性别'),
    sa.Column('age', mysql.VARCHAR(length=11), nullable=True, comment='年龄'),
    sa.Column('location', mysql.VARCHAR(length=200), nullable=True, comment='位置'),
    sa.Column('level', mysql.VARCHAR(length=20), nullable=True, comment='学业水平'),
    sa.Column('email', mysql.VARCHAR(length=200), nullable=False, comment='邮箱'),
    sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='参与状态'),
    sa.Column('is_person_questionare', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否完成问卷'),
    sa.Column('is_mental_questionare', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否完成问卷'),
    sa.Column('is_read_audio', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否语音录制'),
    sa.Column('is_read_video', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否视频录制'),
    sa.Column('is_interview_audio', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否语音面试录制'),
    sa.Column('is_interview_video', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否视频面试录制'),
    sa.Column('mental_status', mysql.VARCHAR(length=20), nullable=True, comment='心理状态'),
    sa.Column('is_send_mail', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否发送邮件'),
    sa.Column('id', mysql.BIGINT(display_width=11), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('create_user', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True, comment='创建人'),
    sa.Column('create_time', mysql.DATETIME(), nullable=True, comment='创建时间'),
    sa.Column('update_user', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True, comment='更新人'),
    sa.Column('update_time', mysql.DATETIME(), nullable=True, comment='更新时间'),
    sa.Column('is_delete', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True, comment='删除标识：0-正常 1-已删除'),
    sa.PrimaryKeyConstraint('id'),
    comment='前端用户表',
    mysql_comment='前端用户表',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('model_file_records')
    op.drop_table('model_questionaire')
    op.drop_table('model_question_records')
    op.drop_table('model_front_users')
    # ### end Alembic commands ###
