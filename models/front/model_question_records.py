# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/28 10:01 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : model_question_records.py 
#@desc: 用来记录需要的问题， 基于朗读的文本句子，基于语音的文本句子，基于视频的句子
数据格式信息：id 问题类型 问题内容 问题状态 问题创建时间 问题更新时间
            id qestion_type text_content emotion_type  other qestion_status qestion_create_time qestion_update_time
            1  texts_audio       青山不改          积极      用于文本录音      删除            2021-09-28 10:00:00  2021-09-28 10:00:00
            1  texts_video       青山不改          积极            删除            2021-09-28 10:00:00  2021-09-28 10:00:00
            1  questions_video       青山不改          积极            删除            2021-09-28 10:00:00  2021-09-28 10:00:00
            1  questions_audio       青山不改          积极            删除            2021-09-28 10:00:00  2021-09-28 10:00:00

'''
from models import base_model
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, Integer



class Model_Qestion_records(base_model):
    __tablename__ = "model_question_records"
    __table_args__ = ({"comment": "问题记录表"})
    qestion_type=Column(String(20), nullable=True, comment="问题类型")
    text_content = Column(String(200), nullable=True, comment="问题内容")
    emotion_type = Column(String(20), nullable=True, comment="情感类型")
    other = Column(String(200), nullable=True, comment="其他")
    qestion_status = Column(String(200), default="无状态", comment="问题状态")
