# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/23 23:44 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : models.py 
#@desc:
'''
import uuid

from models.abstract_base import base_model
from models.base import Base
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, Integer
from datetime import datetime
from utils.snow_flake import generate_id


class Front_User(base_model):

    """
    前端用户表
    """
    __tablename__ = "model_front_users"
    __table_args__ = ({"comment": "前端用户表"})
    # user_id = Column(Integer(),default=generate_id(),comment="用户id")
    # user_id = Column(String(50), primary_key=True, default=str(generate_id()), index=True, comment="用户id")
    username = Column(String(20),nullable=True, comment="用户名")
    gender = Column(String(20), nullable=True, comment="性别")
    age = Column(String(4), nullable=True, comment="年龄")
    location = Column(String(200), nullable=True, comment="位置")
    level = Column(String(20), nullable=True, comment="学业水平")
    email = Column(String(200), nullable=False, comment="邮箱")

    is_active = Column(String(20), default="未完成", comment="参与状态")
    is_person_questionare = Column(String(20), default="未完成", comment="是否完成问卷")
    is_mental_questionare = Column(String(20), default="未完成", comment="是否完成问卷")
    is_read_audio = Column(String(20), default="未完成", comment="是否语音录制")
    is_read_video = Column(String(20), default="未完成", comment="是否视频录制")
    is_interview_audio = Column(String(20), default="未完成", comment="是否语音面试录制")
    is_interview_video = Column(String(20), default="未完成", comment="是否视频面试录制")

    mental_status = Column(String(20), default="无", comment="心理状态")

    is_send_mail = Column(String(20), default="未完成", comment="是否发送邮件")
    # is_delete = Column(Integer, default=0, comment="删除标识：0-正常 1-已删除")
    # creat_time = Column(DateTime, default=datetime.now, comment="创建时间")
    # update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="最后一次更新时间")

    def __repr__(self):
        return f"<Front_User(username={self.username},email={self.email})>"