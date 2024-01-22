# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/28 11:43 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : schema_questionnaire.py 
#@desc:
'''
from datetime import datetime

from pydantic import BaseModel

'''
    __tablename__ = "model_questionaire"
    __table_args__ = ({"comment": "问卷管理"})

    questionnaire_name = Column(String(200), nullable=True, comment="问卷名称")#SDS
    questionnaire_type = Column(String(200), nullable=True, comment="问卷类型")#心理测量
    questionnaire_beizhu = Column(String(200), nullable=True, comment="文件类型")#问卷类型，抑郁检测
    questionnaire_path = Column(String(200), nullable=True, comment="问卷路径")#问卷保存的路径
    questionnaire_status = Column(String(200), default="无状态", comment="问卷状态")#问卷状态
    other = Column(String(200), nullable=True, comment="其他")
'''


class Create_model(BaseModel):
    """
    单条记录schema
    """
    questionnaire_name: str
    questionnaire_type: str
    questionnaire_beizhu: str
    questionnaire_status: str
    questionnaire_path: str
    questionnaire_file_name: str=""
    other: str = ""


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
