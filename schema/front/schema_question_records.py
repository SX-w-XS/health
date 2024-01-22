# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/28 10:11 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : schema_question_records.py 
#@desc: 
'''
from pydantic import BaseModel
from datetime import datetime

"""
    qestion_type=Column(String(20), nullable=False, comment="问题类型")
    text_content = Column(String(200), nullable=False, comment="问题内容")
    emotion_type = Column(String(20), nullable=False, comment="情感类型")
    other = Column(String(200), nullable=False, comment="其他")
    qestion_status = Column(String(200), default="无状态", comment="问题状态")
"""


class Create_model(BaseModel):
    """
    单条记录schema
    """
    qestion_type: str
    text_content: str
    emotion_type: str
    other: str
    qestion_status: str


class Update_model(Create_model):
    """
    创建记录schema
    """
    is_delete: int = 0


class mdoel_Base(Update_model):
    id: int
    # is_delete: int
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True
