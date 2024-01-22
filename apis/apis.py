from fastapi import APIRouter, Depends

from apis.algorithm.algorithm_api import algorithm_router
from apis.front_user.file_records_controller import router_front_file_records
# from apis.front_user.controller import front_user_router
from apis.front_user.front_user_controller import router_front_user
from apis.front_user.front_API import front_router
from apis.front_user.question_records_controller import router_front_question_records
from apis.front_user.schema_questionnaire_controller import router_front_questionnaire, router_front_questionnaire1
from apis.login.controller import get_current_active_user
from apis.login.controller import login_router
from apis.users.controller import user_router
from apis.record.controller import record_router
from apis.role.controller import role_router

api_router = APIRouter()

api_router.include_router(algorithm_router, prefix="/algorithm", tags=["algorithm"])

# router注册
# 实现前端显示的数据反馈，如：问卷，问题等集合。
api_router.include_router(front_router, prefix="/front", tags=["前端使用-李世楠使用"])
# 实现前端的用户个人信息提交，如：姓名，性别，年龄等。
api_router.include_router(router_front_user, prefix="/front_user", tags=["前端用户信息提交"])

# 后端--用户信息的管理，问卷的管理，问题的管理，文件的管理，结果的管理

api_router.include_router(router_front_user, prefix="/back", tags=["后端使用"])
api_router.include_router(router_front_question_records, prefix="/back", tags=["问卷记录"])
api_router.include_router(router_front_file_records, prefix="/back", tags=["文件管理"])
api_router.include_router(router_front_questionnaire, prefix="/back", tags=["问卷使用"])
api_router.include_router(router_front_questionnaire1, prefix="/back", tags=["问卷2-下载数据模板"])

api_router.include_router(login_router, tags=["login"], )
api_router.include_router(user_router, prefix="/users", tags=["users"], dependencies=[Depends(get_current_active_user)])
api_router.include_router(record_router, prefix="/record", tags=["record"],
                          dependencies=[Depends(get_current_active_user)])
api_router.include_router(role_router, prefix="/role", tags=["role"], dependencies=[Depends(get_current_active_user)])
# api_router.include_router(front_user_router, prefix="/front_user", tags=["front_user"], dependencies=[Depends(get_current_active_user)])
# api_router.include_router(front_user_router2, prefix="/front_user2", tags=["front_user"], dependencies=[Depends(get_current_active_user)])
