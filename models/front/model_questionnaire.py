# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/28 11:37 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : model_questionnaire.py
#@desc: 问卷表的模型。用于存储问卷的基本信息
问卷的id,问卷的名称，问卷的描述，问卷的状态，问卷的创建时间，问卷的更新时间

'''

from models import base_model
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, Integer, ForeignKey


class Model_questionnaire(base_model):
    __tablename__ = "model_questionaire"
    __table_args__ = ({"comment": "问卷管理"})

    questionnaire_name = Column(String(200), nullable=True, comment="问卷名称")#SDS
    questionnaire_type = Column(String(200), nullable=True, comment="问卷类型")#心理测量
    questionnaire_beizhu = Column(String(200), nullable=True, comment="文件类型")#问卷类型，抑郁检测
    questionnaire_path = Column(String(200), nullable=True, comment="问卷路径")#问卷保存的路径
    questionnaire_file_name = Column(String(200), nullable=True, comment="问卷保存名称")#问卷保存的路径
    questionnaire_status = Column(String(200), default="无状态", comment="问卷状态")#问卷状态
    other = Column(String(200), nullable=True, comment="其他")
