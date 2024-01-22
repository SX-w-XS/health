# -*- coding: utf-8 -*- 
'''
# @Time : 2023/10/12 11:33 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : api.py 
#@desc: 本模块为算法模块的API接口，主要包括模型训练、模型验证、模型测试、模型预测等功能
基于问卷的情感识别模型，使用CatBoost算法，考虑是
'''
from fastapi import APIRouter, UploadFile, File
from starlette.responses import FileResponse

from algorithm.algorithm_service import get_all_features, train_model_bydata, validate_model_bydata, \
    use_test_model_bydata, list_datasetby_filetype, list_model, list_outputs, download_model, upload_file_by_filetype,download_file

algorithm_router = APIRouter()
@algorithm_router.get("/freaturesNames", summary="根据文件名获取属性名",
         description="直接调用默认数据集训练模型，flag=1,且datasetname不为空时使用指定数据集训练模型")
async def freaturesNames(flag: int = 0, datasetname: str = None):
    return get_all_features(flag, datasetname)


@algorithm_router.get("/model_train_all", summary="模型训练总和",
         description="直接调用默认数据集训练模型，flag=1,且datasetname不为空时使用指定数据集训练模型")
async def model_train_all(flag: int = 0, datasetname: str = None,need_attrcount:int=0,label_name:str="label_level",exclude_features:str=None):
    try:
        exclude_features=['label_need_check', 'label_level', 'label_reason']
        msg = train_model_bydata(flag, datasetname,need_attrcount,label_name,exclude_features)
    except Exception as e:
        msg = {"code": 400, "msg": "模型训练失败", "error": str(e)}
    return msg


@algorithm_router.get("/model_valid_all", summary="模型验证总和",
         description="直接调用默认数据集验证模型，flag=1,且datasetname不为空时使用指定数据集训练模型")
async def model_validate_bydata(flag: int = 0, datasetname: str = None,choose_model: int = 0, model_name: str = None):
    try:
        msg = validate_model_bydata(flag, datasetname,choose_model=choose_model,model_name=model_name)
    except Exception as e:
        msg = {"msg": "模型验证失败", "error": str(e)}
    return msg


@algorithm_router.get("/model_test_all", summary="模型测试总和",
         description="flag=1且datasetname不为空时使用指定数据集测试模型,"
                     "choose_model=1时且model_name不为空时使用指定模型测试。上述都不满足时使用默认数据集测试模型")
async def model_test_all(flag: int = 0, datasetname: str = None, choose_model: int = 0, model_name: str = None,
                         single: int = 0,):
    try:
        msg = use_test_model_bydata(flag, datasetname, choose_model=0, model_name=None, single=single,)
    except Exception as e:
        msg = {"msg": "测试失败", "error": str(e)}
    return msg


@algorithm_router.post("/datasetlist", summary="获取上传的数据集列表",
          description="filetype:文件类型，test:测试数据集，train:训练数据集，valid:验证数据集")
async def datasetlist(fileType: str = "test"):
    # return list_dataset()
    return list_datasetby_filetype(fileType)


@algorithm_router.post("/modellist", summary="获取模型列表")
async def modellist():
    return list_model()


@algorithm_router.post("/outputslist", summary="结果列表")
async def outputslist():
    return list_outputs()


@algorithm_router.post("/download_model", summary="根据文件名下载模型文件")
async def model_download(fileName: str = None):
    filepath,fileName = download_model(fileName)
    return FileResponse(filepath, media_type="algorithm_routerlication/octet-stream", filename=fileName)


@algorithm_router.post("/upload_file", summary="上传文件",
          description="filetype:文件类型，test:测试数据集，train:训练数据集，valid:验证数据集")
async def file_upload(file: UploadFile = File(...), filetype: str = "test"):
    """
    使用UploadFile类的优势：
    1.文件开始存储在内存中，使用内存达到阈值后，将被保存在磁盘中
    2.适合于图片、视频大文件
    3.可以获取上传的文件的元数据，如文件名，创建时间等
    4.有文件对象的异步接口
    5.上传的文件是Python文件对象，可以使用write()、read()、seek()、close()等操做
    :param file:
    :return:
    """
    # return upload_file(file)
    return upload_file_by_filetype(file, filetype)

@algorithm_router.post("/download_file", summary="根据文件名下载文件",
          description="fileName:文件名,filetype:文件类型，testcsv:测试数据集（默认），resultjson:下载json结构文件,resultcsv:下载csv结构文件")
async def file_download(fileName: str = None, filetype: str = "testcsv"):
    if fileName is None:
        return {"message": "fileName is None"}
    filepath = download_file(fileName, filetype)
    return FileResponse(filepath, media_type="application/octet-stream", filename=fileName)
