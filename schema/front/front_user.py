# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/24 0:04 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : front_user.py 
#@desc:
'''
from __future__ import annotations

from pydantic import BaseModel
from datetime import datetime


class Create_Front_User(BaseModel):
    """
    单条记录schema
    """
    username: str
    gender: str
    age: str
    location: str
    level: str
    email: str
    # creat_time: datetime=datetime.now()
    # 取消验证
    # class Config:
    #     arbitrary_types_allowed = False


class Update_Front_User(Create_Front_User):
    """
    创建记录schema
    """
    is_active: str = "未完成"
    is_person_questionare: str = "未完成"
    is_mental_questionare: str = "未完成"
    is_read_audio: str = "未完成"
    is_read_video: str = "未完成"
    is_interview_audio: str = "未完成"
    is_interview_video: str = "未完成"
    is_send_mail: str = "未完成"
    mental_status: str = "无"
    is_delete: int = 0


class Front_User_Base(Update_Front_User):
    id: int
    # is_delete: int
    create_time: datetime
    update_time: datetime
    class Config:
        orm_mode = True
