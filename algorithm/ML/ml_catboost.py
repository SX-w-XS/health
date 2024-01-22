# -*- coding: utf-8 -*- 
'''
# @Time : 2023/10/12 11:39 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : catboost.py 
#@desc:
'''
import datetime

import joblib
# 使用pandas加载数据集
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

import catboost as cb

model_dir="../model/outputs/"
def model_save(model):
    # 保存模型
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    joblib.dump(model, f"{model_dir}{today}_model.pkl")
    return {"model_name": f"{today}_model.pkl"}
if __name__ == '__main__':
    # 读取数据
    data = pd.read_csv('../data/shandong_dataset.csv', encoding="ANSI")
    # 数据的标签为 label_need_check,label_level,label_reason
    Y_data = data['label_need_check']
    X_data = data.drop(columns=['label_need_check', 'label_level', 'label_reason'], axis=1)
    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=0.2, random_state=2022)
    # 训练模型
    model = cb.CatBoostClassifier(iterations=1000, learning_rate=0.1, depth=6, loss_function='Logloss', verbose=True)
    model.fit(X_train, y_train)
    # 预测
    y_pred = model.predict(X_test)
    # 评估
    print("CatBoost=训练集_accuracy_score:{}".format(accuracy_score(y_train, model.predict(X_train))))
    print("CatBoost=测试集_accuracy_score:{}".format(accuracy_score(y_test, y_pred)))
    print("CatBoost=测试集score_Rf:{}".format(classification_report(y_test, y_pred)))
    print("CatBoost=测试集score_Rf:{}".format(confusion_matrix(y_test, y_pred)))
    print("CatBoost=测试集_roc_auc_score:{}".format(roc_auc_score(y_test, y_pred)))
    model_save(model)