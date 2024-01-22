# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/28 11:11 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : schema_file_records.py 
#@desc:
'''
from pydantic import BaseModel
from datetime import datetime

'''
    __tablename__ = "model_file_records"
    __table_args__ = ({"comment": "文件存取记录表"})

    file_name = Column(String(200), nullable=True, comment="文件名称")
    file_type = Column(String(200), nullable=True, comment="文件类型")
    file_time = Column(String(200), nullable=True, comment="文件时长")
    file_url = Column(String(200), nullable=True, comment="文件url")
    file_path = Column(String(200), nullable=True, comment="文件保存路径")
    file_path_name = Column(String(200), nullable=True, comment="文件名称")
    file_status = Column(String(200), default="无状态", comment="文件状态")
    other = Column(String(200), nullable=True, comment="其他")
    # 外键
    model_front_users_id=Column(Integer,ForeignKey('model_front_users.id'), comment="前端用户id")
    model_question_records_id=Column(Integer,ForeignKey('model_question_records.id'), comment="对应的问题id")
    questionnaire_id=Column(Integer,ForeignKey('model_questionaire.id'), comment="对应的问卷id")
'''

class Create_model(BaseModel):
    """
    单条记录schema
    """
    file_name: str=None
    file_type: str=None
    file_time: str=None
    file_url: str=None
    file_path: str=None
    file_path_name: str=None
    file_status: str=None
    other:str=None
    model_front_users_id: int=None
    model_question_records_id: int=None
    questionnaire_id: int=None


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
