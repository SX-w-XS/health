# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/28 10:20 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : Qestion_records-controller.py 
#@desc: 问题记录表的接口
'''
from apis.front_user.mySQLAlchemyCRUDRouter import MYSQLAlchemyCRUDRouter
from core.db import get_db
from core.db import get_db
from models import Front_User
from models.front.model_question_records import Model_Qestion_records
from schema.front.schema_question_records import *
from fastapi_crudrouter import SQLAlchemyCRUDRouter
# router= APIRouter()
# MemoryCRUDRouter将使用pydantic模型的名称作为前缀。但是，SQLAlchemyCRUDRouter将使用模型的表名作为前缀
# router_front_question_records = SQLAlchemyCRUDRouter(schema=mdoel_Base,
#                                          db_model=Model_Qestion_records, db=get_db,
#                                          create_schema=Create_model,
#                                          update_schema=Update_model,
#                                          delete_all_route=False,
#                                          # prefix="问题记录表"
#                                          )  # 设置分页paginate=50 每页50条
router_front_question_records = MYSQLAlchemyCRUDRouter(schema=mdoel_Base,
                                         db_model=Model_Qestion_records, db=get_db,
                                         create_schema=Create_model,
                                         update_schema=Update_model,
                                         delete_all_route=False,
                                         # prefix="问题记录表"
                                         )  # 设置分页paginate=50 每页50条
# router.include_router(router_front_question_records)