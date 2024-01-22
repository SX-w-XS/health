# -*- coding: utf-8 -*- 
"""
# @Time : 2023/10/12 11:35
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : algorithm_service.py
#@desc:
"""
import datetime
import json
import os
import time

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn import metrics
from sklearn.impute import KNNImputer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

uploadfile_path = "data/uploads/"
outputfile_path = "data/output/"
dataset_basedir = "data/"
model_dir = "model/outputs/"
defaut_model_dir = "model/"
defaut_model_name = "0000_default_model.pkl"
defaut_model_name = "20231012171621_model.pkl"
defaut_data_train_name = "train.csv"
defaut_data_test_name = "test.csv"
defaut_data_valid_name = "validate.csv"
labels = ['label_need_check', 'label_level', 'label_reason']
label_name = "label_need_check"
label_name = "label_level"
global_model = None

# 使用KNN填补
imputer = KNNImputer(n_neighbors=5)


def get_model(use_model, model_path=defaut_model_dir + defaut_model_name):
    """
    获取模型
    """
    # 获取或者创建模型
    if use_model is not None:
        return use_model
    if model_path is not None and os.path.exists(model_path):
        use_model = joblib.load(filename=model_path)
    else:
        use_model = CatBoostClassifier(random_state=1)
    return use_model


def get_all_features(flag=0, datasetname=None):
    data = None
    if flag == 1 and datasetname is not None:
        data = pd.read_csv(f"{uploadfile_path}{datasetname}")  # 存在缺失值的数据集
    else:
        data = pd.read_csv(dataset_basedir + defaut_data_train_name)  # 存在缺失值的数据集
    return {"all_features": data.columns.tolist()}


def train_model_bydata(flag=0, datasetname=None, need_attrcount=0, label_name="label_need_check",
                       exclude_features=labels):
    if flag == 1 and datasetname is not None:
        train_data = pd.read_csv(f"{uploadfile_path}train/{datasetname}")  # 存在缺失值的数据集
    else:
        train_data = pd.read_csv(dataset_basedir + defaut_data_train_name)  # 读取默认数据集
    if train_data is None:
        return {"code": 500, "msg": "训练数据集不存在"}
    # 数据提取
    train_y_data = train_data[label_name]
    train_X_data = train_data.drop(exclude_features, axis=1)

    new_train_X_data = imputer.fit_transform(train_X_data)  # 进行数据填充

    new_train_X_data_MM = pd.DataFrame(new_train_X_data, columns=train_X_data.columns)

    X_train, X_test, y_train, y_test = train_test_split(new_train_X_data_MM, train_y_data, test_size=0.2,
                                                        random_state=2022, stratify=train_y_data)

    print("start train use_model")
    start = time.time()
    # use_model.fit(new_train_X_data_MM, train_y_data,
    #             cat_classifier__eval_set=[(new_valida_X_data_MM, valida_y_data)])
    global global_model
    model = get_model(global_model, model_path=None)
    model.fit(X_train, y_train)
    global_model = model

    # global_model=model
    end = round(time.time() - start, 3)
    print("end train use_model")
    print('train time：', end, 'seconds')
    # 程序代码

    y_pred_test = model.predict(X_test)
    y_pro_test = model.predict_proba(X_test)
    test_f1 = metrics.f1_score(y_test, y_pred_test, average="macro")
    test_accuracy_score = metrics.accuracy_score(y_test, y_pred_test)

    y_pred_train = model.predict(X_train)
    y_pro_train = model.predict_proba(X_train)
    train_f1 = metrics.f1_score(y_train, y_pred_train, average="macro")
    # train_f1 = metrics.f1_score(y_train, y_pred_train)
    train_accuracy_score = metrics.accuracy_score(y_train, y_pred_train)

    model_save_path = model_save(model)
    print("macro_f1:", test_f1)
    print("valida_accuracy_score:", test_accuracy_score)

    return {"code": 200, "msg": "success", "model_name": model_save_path,
            "time": end,
            "train f1_macro": train_f1, "train_accuracy_score": train_accuracy_score,
            "test f1_macro": test_f1, "test_accuracy_score": test_accuracy_score,
            }


def validate_model_bydata(flag=0, datasetname=None, choose_model=0, model_name=None, label_name="label_need_check",
                          exclude_features=labels):
    if flag == 1 and datasetname is not None:
        valida_data = pd.read_csv(f"{uploadfile_path}valid/{datasetname}")  # 存在缺失值的数据集
    else:
        valida_data = pd.read_csv(dataset_basedir + defaut_data_valid_name)  # 存在缺失值的数据集
    if valida_data is None:
        return {"code": 500, "msg": "验证数据集不存在"}
    # 数据提取
    valida_y_data = valida_data[label_name]
    valida_X_data = valida_data.drop(exclude_features, axis=1)

    if choose_model == 1 and model_name is not None:
        model = get_model(None, model_dir + model_name)
    else:
        model = get_model(global_model)
    y_pred_valida = model.predict(valida_X_data)
    y_pro_valida = model.predict_proba(valida_X_data)
    valida_f1 = metrics.f1_score(valida_y_data, y_pred_valida, average="macro")
    accuracy_score = metrics.accuracy_score(valida_y_data, y_pred_valida)
    # print("macro_f1:", valida_f1)
    print("accuracy_score:", accuracy_score)
    # print(classification_report(valida_y_data, y_pred_valida))
    return {"model_name": model_name, "macro_f1": valida_f1, "accuracy_score": accuracy_score,
            "classification_report": classification_report(valida_y_data, y_pred_valida, output_dict=True)}


def use_test_model_bydata(flag=0, datasetname=None, choose_model=0, model_name=None, single=0):
    if flag == 1 and datasetname is not None:
        test_data = pd.read_csv(f"{uploadfile_path}test/{datasetname}")  # 存在缺失值的数据集
    else:
        test_data = pd.read_csv(dataset_basedir + defaut_data_test_name)  # 存在缺失值的数据集
    if test_data is None:
        return {"code": 500, "msg": "测试数据集不存在"}
    global global_model
    if choose_model == 1 and model_name is not None:
        model = get_model(None, model_dir + model_name)
    else:
        model = get_model(global_model)

    if single == 1:
        test_data = test_data.iloc[0:1, :]

    y_pred_test = model.predict(test_data)
    y_pro_test = model.predict_proba(test_data)

    pd_y_pred_new_sum = pd.DataFrame()
    pd_y_pred_new_sum["id"] = test_data["sample_id"].astype(int).astype(str)
    pd_y_pred_new_sum["label"] = y_pred_test
    pd_y_pred_new_sum["label"] = pd_y_pred_new_sum["label"].astype(int)
    summery = dict(pd_y_pred_new_sum.values)
    json_path1 = save_json(summery, "test")
    # 保存到文件
    pd_y_pred_new = pd_y_pred_new_sum[['id', "label"]]
    csv_path = save_csv(pd_y_pred_new, "test")

    # 统计不同label的数量，并且转换为字典
    label_count_info = pd_y_pred_new.groupby("label", as_index=False).count().set_index("label")["id"].to_dict()
    label_count_info2 = pd_y_pred_new.groupby("label", as_index=False).count()
    label_count_info2.rename(columns={'id': 'value', "label": "name"}, inplace=True)
    label_count_info2 = label_count_info2.to_json(orient="records", force_ascii=False)
    # 分别统计每个label下的id集合
    label_id_info = pd_y_pred_new.groupby("label", as_index=False).agg(lambda x: x.tolist()).set_index("label")[
        "id"].to_dict()
    # label_id_info=json.loads(json.dumps(label_id_info))
    # 计算某一列的属性个数
    unique_values = [label_item for label_item in model.classes_]
    unique_values = [int(x) for x in unique_values]
    for i in unique_values:
        if label_count_info.get(i) is None:
            label_count_info[i] = 0
        if label_id_info.get(i) is None:
            label_id_info[i] = []
    # label_id_info=json.loads(json.dumps(label_id_info))
    test_info = {"label_count_info": label_count_info, "label_count_info2": label_count_info2,
                 "label_id_info": label_id_info}
    test_info = json.dumps(test_info)
    test_info = json.loads(test_info)
    # 单个id对应的label
    test_json = pd_y_pred_new.to_json(orient="records", force_ascii=False)
    test_json = json.loads(test_json)

    test_json2 = pd_y_pred_new.astype(str).set_index("id")["label"].to_dict()
    # 保存到文件中
    # json_path=save_json(test_json2,"test")

    pd_y_prob_new = pd.DataFrame(y_pro_test, columns=[f"label_{label_item}" for label_item in model.classes_])
    pd_y_prob_new.insert(0, 'id', test_data["sample_id"].astype(int).astype(str))
    test_prob_json = pd_y_prob_new.to_json(orient="records", force_ascii=False)
    test_prob_json = json.loads(test_prob_json)
    all_test_count = len(test_data)
    # return {"test_info":test_info,"csv_path":csv_path,"json_path":json_path,"y_pred": test_json, "y_pred2": test_json2, "y_Probability": test_prob_json}
    return {"test_info": test_info, "all_test_count": all_test_count, "csv_path": csv_path, "json_path": json_path1,
            "y_pred": test_json, "y_pred2": summery, "y_Probability": test_prob_json}


def upload_file(file):
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    now = str(datetime.datetime.now().strftime('%M%S'))
    with open(f"{uploadfile_path}{today}_{file.filename}", 'wb') as f:
        for i in iter(lambda: file.file.read(1024 * 1024 * 10), b''):
            f.write(i)
    f.close()
    return {"file_name": f"{today}_{file.filename}"}


def upload_file_by_filetype(file, filetype="test"):
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    now = str(datetime.datetime.now().strftime('%M%S'))

    with open(f"{uploadfile_path}{filetype}/{today}_{file.filename}", 'wb') as f:
        for i in iter(lambda: file.file.read(1024 * 1024 * 10), b''):
            f.write(i)
    f.close()
    return {"file_name": f"{today}_{file.filename}"}


def save_json(json_data, file_name="test"):
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    with open(f"{outputfile_path}{today}_{file_name}.json", 'w') as f:
        json.dump(json_data, f)
    f.close()
    return {"file_name": f"{today}_{file_name}.json"}


def save_csv(pd_data, file_name="test"):
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    pd_data.to_csv(f"{outputfile_path}{today}_{file_name}.csv", index=False)
    return {"file_name": f"{today}_{file_name}.csv"}


def download_file(filename, type="testcsv"):
    if type == "testcsv":
        base = uploadfile_path + "test/"
    if type == "resultjson":
        base = outputfile_path
    if type == "resultcsv":
        base = outputfile_path
    return f"{base}{filename}"


def model_status():
    # 返回模型训练进度
    return {"status": "success", "progress": 0.5, "message": "模型训练中"}


def list_dataset():
    # 读取uploadfile_path下的所有文件名，并返回文件名列表
    file_list = os.listdir(uploadfile_path)
    return {"file_list": file_list}


def list_datasetby_filetype(filetype):
    # 读取uploadfile_path下的所有文件名，并返回文件名列表
    file_list = os.listdir(uploadfile_path + filetype + "/")
    return {"file_list": file_list}


def list_outputs():
    # 读取uploadfile_path下的所有文件名，并返回文件名列表
    file_list = os.listdir(outputfile_path)
    return {"file_list": file_list}


def model_importance():
    # 返回模型特征重要性
    return {"feature_importance": {"feature": "feature_importance"}}  # 返回模型特征重要性


import joblib


def model_save(model):
    # 保存模型
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    joblib.dump(model, f"{model_dir}{today}_model.pkl")
    return {"model_name": f"{today}_model.pkl"}


def load_model(model_name=defaut_model_name):
    # 加载模型
    model = joblib.load(f"{model_dir}{model_name}")
    return model


def list_model():
    file_model_list = os.listdir(model_dir)
    return {"file_model_list": file_model_list}


def download_model(filename):
    if filename == None or filename == "":
        filename = defaut_model_name
    return f"{model_dir}{filename}", filename


if __name__ == '__main__':
    # train_model_bydata()
    use_test_model_bydata()
