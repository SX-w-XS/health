# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/28 11:45 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : schema_questionnaire_controller.py 
#@desc:
'''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from apis.front_user.mySQLAlchemyCRUDRouter import MYSQLAlchemyCRUDRouter
from core.db import get_db
from models.front.model_questionnaire import Model_questionnaire
from schema.front.schema_questionnaire import *
from fastapi_crudrouter import SQLAlchemyCRUDRouter

router_front_questionnaire1 = APIRouter()

# router_front_questionnaire = SQLAlchemyCRUDRouter(schema=mdoel_Base,
#                                                   db_model=Model_questionnaire, db=get_db,
#                                                   create_schema=Create_model,
#                                                   update_schema=Update_model,
#                                                   delete_all_route=False,
#                                                   # prefix="问卷管理"
#                                                   )  # 设置分页paginate=50 每页50条
router_front_questionnaire = MYSQLAlchemyCRUDRouter(schema=mdoel_Base,
                                                  db_model=Model_questionnaire, db=get_db,
                                                  create_schema=Create_model,
                                                  update_schema=Update_model,
                                                  delete_all_route=False,
                                                  # prefix="问卷管理"
                                                  )  # 设置分页paginate=50 每页50条



# def download_template():
#     return "下载数据模板文件"

# 下载数据模板文件
@router_front_questionnaire1.get("/download_questionnaire_template", summary="下载数据模板文件", description="下载数据模板文件")
async def download_template(db: Session = Depends(get_db)):
    Model_questionnaire_list=db.query(Model_questionnaire.questionnaire_name,Model_questionnaire.questionnaire_path,Model_questionnaire.questionnaire_file_name).filter(Model_questionnaire.questionnaire_status=='模板',Model_questionnaire.is_delete==0,Model_questionnaire.questionnaire_name.like('%模板%')).first()
    if Model_questionnaire_list:
        filepath = f"{Model_questionnaire_list.questionnaire_path}{Model_questionnaire_list.questionnaire_file_name}"
        return FileResponse(filepath, media_type="application/octet-stream", filename="模板文件.xlsx")
    else:
        filepath = f"static/模板文件.xlsx"
        return FileResponse(filepath, media_type="application/octet-stream", filename="模板文件.xlsx")