# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/28 10:00 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : model_file_records.py
#@desc: 记录用户传递的数据
记录文件的位置
id 用户id 问题id    文件名称 文件类型 文件时长 文件url 文件状态
id model_front_users_id model_question_records_id file_name file_type file_time file_url file_status

'''
from models import base_model
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, Integer, ForeignKey


class Model_file_records(base_model):
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
