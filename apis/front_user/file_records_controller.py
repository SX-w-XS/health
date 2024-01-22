# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/28 11:15 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : question_records_controller.py 
#@desc:
'''

from fastapi_crudrouter import SQLAlchemyCRUDRouter

from apis.front_user.mySQLAlchemyCRUDRouter import MYSQLAlchemyCRUDRouter
from core.db import get_db
from models.front.model_file_records import *
from schema.front.schema_file_records import *

# router= APIRouter()

# router_front_file_records = SQLAlchemyCRUDRouter(schema=mdoel_Base,
#                                          db_model=Model_file_records, db=get_db,
#                                          create_schema=Create_model,
#                                          update_schema=Update_model,
#                                          delete_all_route=False,
#                                             # prefix="文件存取记录表"
#                                          )  # 设置分页paginate=50 每页50条

router_front_file_records = MYSQLAlchemyCRUDRouter(schema=mdoel_Base,
                                         db_model=Model_file_records, db=get_db,
                                         create_schema=Create_model,
                                         update_schema=Update_model,
                                         delete_all_route=False,
                                            # prefix="文件存取记录表"
                                         )  # 设置分页paginate=50 每页50条