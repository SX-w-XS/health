# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/23 12:56 
# @Author : PVINCE
# @Project: fastapi
# @Path:
# @Software: PyCharm
# @File : API.py 
#@desc:
'''
import datetime
import json
import os

import pandas as pd
from fastapi import APIRouter, File, Depends, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict

from apis.front_user.utils import save_upload_file, create_folder_if_not_exists, results_to_dict, \
    load_excel_from_results
from core.config import settings
from core.db import get_db
from models import Front_User, Model_Qestion_records, Model_questionnaire, Model_file_records

# 使用路由
# create router
front_router = APIRouter()


@front_router.get('/get_all', summary="获取问卷数据，提问数据，提问数据等等")
async def get_all():
    with open('static/API.json', "r", encoding="utf8") as f:
        data = json.load(f)
    return JSONResponse(content=data)


from sqlalchemy.orm import Session


@front_router.get('/get_all2', summary="建议使用get_all2 该方法从数据库中获取问卷数据，提问数据，提问数据等等")
async def get_all2(db: Session = Depends(get_db)):
    # 从数据库中获取
    db_Model_Qestion_records = db.query(Model_Qestion_records.id, Model_Qestion_records.qestion_type,
                                        Model_Qestion_records.text_content, Model_Qestion_records.emotion_type).filter(
        Model_Qestion_records.qestion_status == '启用', Model_Qestion_records.is_delete == 0)
    texts_audio_list = db_Model_Qestion_records.filter(Model_Qestion_records.qestion_type == 'texts_audio').all()
    texts_video_list = db_Model_Qestion_records.filter(Model_Qestion_records.qestion_type == 'texts_video').all()
    questions_audio_list = db_Model_Qestion_records.filter(
        Model_Qestion_records.qestion_type == 'questions_audio').all()
    questions_video_list = db_Model_Qestion_records.filter(
        Model_Qestion_records.qestion_type == 'questions_video').all()

    Model_questionnaire_list = db.query(Model_questionnaire.id, Model_questionnaire.questionnaire_type,
                                        Model_questionnaire.questionnaire_name, Model_questionnaire.questionnaire_path,
                                        Model_questionnaire.questionnaire_file_name).filter(
        Model_questionnaire.questionnaire_status == '启用', Model_questionnaire.is_delete == 0).all()

    db.close()
    data = {"questionnaires": load_excel_from_results(Model_questionnaire_list),
            'texts_audio': results_to_dict(texts_audio_list),
            'texts_video': results_to_dict(texts_video_list),
            'questions_audio': results_to_dict(questions_audio_list),
            'questions_video': results_to_dict(questions_video_list),
            }
    return JSONResponse(content=data)


from fastapi import FastAPI, UploadFile

app = FastAPI()


class Upload_recording(BaseModel):
    u_id: str
    title_id: str
    filetype: str
    muilt_type: str
    # file: File(...)


@front_router.post("/upload_recording/", summary="保存音视频文件，这是面试回答录音",
                   description="u_id为用户id。title_id为题目id。"
                               "filetype为文件类型:audio为音频video为视频;"
                               "muilt_type为文件类型的子类型：:text,interview为面试题目")
async def save_recording(file: UploadFile = File(...), u_id: str = 0, title_id: str = 0, filetype: str = "audio",
                         muilt_type="text", db: Session = Depends(get_db)):
    '''
    保存音视频文件，这是面试回答录音
    这里需要书写逻辑。将记录存到数据库中  uid,title_id,filetype,muilt_type,file_path
    '''
    file_path = f"{settings.UPLOAD_FILE_PATH}{u_id}/{filetype}_{muilt_type}/"
    prefix_file = "question_"
    file_name = f"{prefix_file}{title_id}"  # question_1
    # ====================================================================================
    # file_path_return= save_upload_file(file_path=file_path,file_name=file_name,file=file)
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    # now = str(datetime.datetime.now().strftime('%M%S'))
    infix_file = today  # 中缀
    create_folder_if_not_exists(file_path)
    file_name = f"{file_name}_{infix_file}{file.filename}"
    with open(f"{file_path}{file_name}", "wb") as f:
        f.write(await file.read())

    # ===============================================================================================

    db_item = Model_file_records(model_front_users_id=u_id,
                                 file_name=file_name,
                                 file_path=file_path,
                                 # file_url='',
                                 model_question_records_id=int(title_id),
                                 file_path_name=f"{file_path}{file_name}",
                                 file_type=f"{filetype}/{muilt_type}",
                                 file_status="已上传"
                                 )

    # 将操作记录存入数据库 model_file_records
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    except Exception as e:
        print(e)
        db.rollback()
        return JSONResponse(status_code=400, content={"msg": "提交失败"})
    # ===============================================================================================
    content = {"msg": "上传成功", "file_path": f"{file_path}{file_name}", "file_name": f"{file_name}"}
    return JSONResponse(status_code=200, content=content)


@front_router.post("/upload_questionnaire/", summary="上传结构化数据表", tags=["文件上传"])
async def save_questionnaire(file: UploadFile = File(...)):
    '''
    保存音视频文件，这是面试回答录音
    这里需要书写逻辑。将记录存到数据库中  uid,title_id,filetype,muilt_type,file_path
    '''
    sub_path = "questionnaire"
    today = str(datetime.datetime.now().strftime('%Y%m%d'))
    file_path = f"{settings.UPLOAD_FILE_PATH}{sub_path}/{today}/"
    prefix_file = "结构化数据"

    file_name = f"{prefix_file}"  # question_1
    # ====================================================================================
    # file_path_return= save_upload_file(file_path=file_path,file_name=file_name,file=file)

    now = str(datetime.datetime.now().strftime('%H%M%S'))
    infix_file = today + now  # 中缀
    create_folder_if_not_exists(file_path)
    file_name = f"{file_name}_{infix_file}_{file.filename}"
    with open(f"{file_path}{file_name}", "wb") as f:
        f.write(await file.read())
    # ===============================================================================================
    content = {"msg": "上传成功", "file_path": f"{file_path}", "file_name": f"{file_name}",
               'absolute_path': f"{file_path}{file_name}"}
    return JSONResponse(status_code=200, content=content)


@front_router.post("/analyse_one_recording/", summary="上传单条信息，进行分析",
                   description="u_id为用户id。title_id为题目id。"
                               "filetype为文件类型:audio为音频video为视频;"
                               "muilt_type为文件类型的子类型：:text,interview为面试题目")
async def analyse_one_recording(file: UploadFile = File(...), u_id: str = 0, title_id: str = 0, filetype: str = "audio",
                                muilt_type="text"):
    '''
    保存音视频文件，这是面试回答录音
    这里需要书写逻辑。将记录存到数据库中  uid,title_id,filetype,muilt_type,file_path
    '''
    file_path = f"{settings.UPLOAD_FILE_PATH}{u_id}/{filetype}_{muilt_type}/"
    prefix_file = "question_"
    file_name = f"{prefix_file}{title_id}"  # question_1
    # ====================================================================================
    # file_path_return= save_upload_file(file_path=file_path,file_name=file_name,file=file)
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    # now = str(datetime.datetime.now().strftime('%M%S'))
    infix_file = today  # 中缀
    create_folder_if_not_exists(file_path)
    file_name = f"{file_name}_{infix_file}{file.filename}"
    with open(f"{file_path}{file_name}", "wb") as f:
        f.write(await file.read())

    '''
    执行分析步骤
        1 处理文件
        2 数据预处理
        3 算法模型
        4 结果预测
    使用后台任务接口 background_tasks.add_task(write_notification, email, message="some notification")

    '''
    # ===============================================================================================
    content = {"msg": "上传成功", "file_path": f"{file_path}{file_name}", "file_name": f"{file_name}"}
    return JSONResponse(status_code=200, content=content)


async def analyse_by_questionaire(file: UploadFile = File(...), u_id: str = 0, title_id: str = 0,
                                  filetype: str = "audio",
                                  muilt_type="text"):
    '''
    保存音视频文件，这是面试回答录音
    这里需要书写逻辑。将记录存到数据库中  uid,title_id,filetype,muilt_type,file_path
    '''
    file_path = f"{settings.UPLOAD_FILE_PATH}{u_id}/{filetype}_{muilt_type}/"
    prefix_file = "question_"
    file_name = f"{prefix_file}{title_id}"  # question_1
    # ====================================================================================
    # file_path_return= save_upload_file(file_path=file_path,file_name=file_name,file=file)
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    # now = str(datetime.datetime.now().strftime('%M%S'))
    infix_file = today  # 中缀
    create_folder_if_not_exists(file_path)
    file_name = f"{file_name}_{infix_file}{file.filename}"
    with open(f"{file_path}{file_name}", "wb") as f:
        f.write(await file.read())
    '''
    执行分析步骤
        1 处理文件
        2 数据预处理
        3 算法模型
        4 结果预测
    使用后台任务接口 background_tasks.add_task(write_notification, email, message="some notification")

    '''
    # test_model_bydata(flag, datasetname, choose_model=0, model_name=None, single=single)
    # ===============================================================================================
    content = {"msg": "上传成功", "file_path": f"{file_path}{file_name}", "file_name": f"{file_name}"}
    return JSONResponse(status_code=200, content=content)


class Post_questionnaire(BaseModel):
    user_id: str
    questionnaire_id: str
    questionnaire_file_name: str
    questionnaire_name: str
    answerlist: Dict[str, str] = {}


@front_router.post("/post_questionnaire/", summary="提交问卷作答", description="提交问卷作答")
async def post_questionnaire(item: Post_questionnaire, db: Session = Depends(get_db)):
    # 打印传递的参数
    filetype = "questionnaire"
    print("打印传递的参数")
    print(item)
    # 拿到用户的id
    user_id = item.user_id
    questionnaire_id = item.questionnaire_id
    questionnaire_file_name = item.questionnaire_file_name
    questionnaire_name = item.questionnaire_name
    answerlist = item.answerlist

    # 使用pandas将字典转换为dataframe
    df = pd.DataFrame(answerlist, index=[0])

    file_path = f"{settings.UPLOAD_FILE_PATH}{user_id}/{filetype}/"
    prefix_file = "questionnaire_"
    file_name = f"{prefix_file}{questionnaire_id}_{questionnaire_name}"  # questionnaire_1_SDS
    # ====================================================================================
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    infix_file = today  # 中缀
    create_folder_if_not_exists(file_path)
    file_name = f"{file_name}_{infix_file}"

    df.to_csv(f"{file_path}{file_name}.csv", index=False, sep=',')
    # ===============================================================================================

    db_item = Model_file_records(model_front_users_id=user_id,
                                 file_name=f"{file_name}.csv",
                                 file_path=file_path,
                                 # file_url=f"{file_path}{file_name}.csv",
                                 questionnaire_id=int(questionnaire_id),
                                 file_path_name=f"{file_path}{file_name}.csv",
                                 file_type=filetype,
                                 file_status="已上传",
                                 other=f"{questionnaire_name}")

    # 将操作记录存入数据库 model_file_records
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    except Exception as e:
        print(e)
        db.rollback()
        return JSONResponse(status_code=400, content={"msg": "提交失败"})
    # ===============================================================================================
    content = {"msg": "上传成功", "file_path": f"{file_path}{file_name}", "file_name": f"{file_name}"}
    return JSONResponse(status_code=200, content=content)


if __name__ == '__main__':
    # file_path = settings.UPLOAD_FILE_PATH + "1" + "audio" + "/"
    # if not os.path.lexists(file_path):  # 若存在该指定路径则创建子文件夹
    #     os.makedirs(file_path)  # 创建子文件夹
    get_all2()
