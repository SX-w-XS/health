from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware
from core.config import settings
from apis.apis import api_router
import uvicorn
def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.org/swagger-ui/4.15.5/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.org/swagger-ui/4.15.5/swagger-ui.min.css")


applications.get_swagger_ui_html = swagger_monkey_patch
# 初始化app实例
app = FastAPI(title=settings.APP_NAME, openapi_url=f"{settings.API_PREFIX}/openapi.json")


# 设置CORS站点
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(CORSMiddleware,
                       allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"],
                       )
# 路由注册
app.include_router(api_router, prefix=settings.API_PREFIX)
if __name__ == '__main__':
    exclude_dirs=['static','templates','__pycache__','catboost_info','data','model']
    uvicorn.run(app="main:app", host='0.0.0.0', port=settings.PORT, reload=settings.RELOAD)
