# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/24 1:26 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : controller2.py 
#@desc:
'''

# front_user_router2 = APIRouter()

from apis.front_user.mySQLAlchemyCRUDRouter import MYSQLAlchemyCRUDRouter
from core.db import get_db
from models import Front_User
from schema.front.front_user import Create_Front_User, Update_Front_User, Front_User_Base

# 前端基本信息搜集的接口
# router_front_user = SQLAlchemyCRUDRouter(schema=Front_User_Base,
#                                          db_model=Front_User, db=get_db,
#                                          create_schema=Create_Front_User,
#                                          update_schema=Update_Front_User,
#                                          delete_all_route=False
#                                          )  # 设置分页paginate=50 每页50条
router_front_user = MYSQLAlchemyCRUDRouter(schema=Front_User_Base,
                                           db_model=Front_User, db=get_db,
                                           create_schema=Create_Front_User,
                                           update_schema=Update_Front_User,
                                           delete_all_route=False
                                           )  # 设置分页paginate=50 每页50条


# front_user_router2.include_router(router_front_user)

# 重写部分路由
# @router_front_user.post("")
@router_front_user.get("/get_all")
async def get_all():
    return await Front_User.all()
