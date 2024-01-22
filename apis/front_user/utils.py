# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/24 15:06 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : utils.py 
#@desc:
'''
import datetime
import os

import pandas as pd
from fastapi import UploadFile


def create_folder_if_not_exists(folder_path):
    # 检查文件夹路径是否存在
    if not os.path.exists(folder_path):
        # 如果不存在，创建文件夹
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")


async def save_upload_file(file_path: str, file_name: str, file: UploadFile):
    today = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    # now = str(datetime.datetime.now().strftime('%M%S'))
    infix_file = today  # 中缀

    create_folder_if_not_exists(file_path)
    with open(f"{file_path}{file_name}_{infix_file}{file.filename}", "wb") as f:
        f.write(await file.read())
    return f"{file_path}{file_name}{infix_file}{file.filename}"


def result_to_dict(result):
    """
将一条查询结果转换为字典
    """
    return dict(zip(result.keys(), result))


def results_to_dict(results):
    '''
    将多条查询结果转换为字典
    '''
    return [dict(zip(result.keys(), result)) for result in results]


def load_excel_from_results(results):
    '''
    将多条查询结果转换为字典
    '''
    result_data = []
    for result in results:
        result_dic = dict(zip(result.keys(), result))
        result_dic['questions'] = load_excel_from_path(result_dic['questionnaire_path'], result_dic['questionnaire_file_name'])
        result_data.append(result_dic)
    return result_data


def load_excel_from_path(file_path, file_name):
    # 使用pandas读取excel文件
    df_q = pd.read_excel(file_path + file_name, sheet_name='question',header=1)
    df_answer = pd.read_excel(file_path + file_name, sheet_name='answer')

    df_answer.columns=["answer_text", "answer_value"]
    df_answer["order_id"]=df_answer[ "answer_value"]

    df_question = df_q[["序号","编码", "数据项含义"]]
    df_question["question_type"] = "radio"

    questions=generate_questionnaire_by_pandas(df_question, df_answer)
    # 将excel文件转换为字典
    # df_dict = df.to_dict(orient='records')
    return questions



def generate_questionnaire_by_pandas(df_question, df_answer):
    '''
    生成问卷
    :param df_question:         问卷问题
    :param df_answer:           问卷答案
    :return:
    '''

    questions= []
    for index, row in df_question.iterrows():
        question = {
            "question_order_id": row[0],        #问卷顺序
            "question_id": row[1],              #问卷id
            "question_text": row[2],             #问卷内容
            "question_type": row[3],            #问卷类型
            "answers": df_answer.to_dict(orient='records'),  # 转换成字典 问卷答案
        }
        questions.append(question)
    return questions
if __name__ == '__main__':
    path='../../static/'
    name='10心理健康.xlsx'
    load_excel_from_path(path,name)
