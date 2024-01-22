# -*- coding: utf-8 -*- 
'''
# @Time : 2023/9/24 16:04 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : api_service.py 
#@desc:
'''

# def test_model_bydata(flag=0, datasetname=None,choose_model=0,model_name=None,single=0):
#     test_data = None
#     if flag == 1 and datasetname is not None:
#         test_data = pd.read_csv(f"{uploadfile_path}test/{datasetname}")  # 存在缺失值的数据集
#     else:
#         test_data = pd.read_csv(basedir + "test_2000_x.csv")  # 存在缺失值的数据集
#
#
#     if choose_model==1 and model_name is not None:
#         use_model=load_model(model_name)
#     else:
#         use_model=load_model()
#
#     if single == 1:
#         test_data = test_data.iloc[0:1, :]
#     # 如果test_data.columns的属性中包含label，那么就删除label列
#     if "label" in test_data.columns:
#         test_data = test_data.drop(["label"], axis=1)
#
#     y_pred_test = use_model.predict(test_data)
#     y_pro_test = use_model.predict_proba(test_data)
#
#     pd_y_pred_new_sum = pd.DataFrame()
#     pd_y_pred_new_sum["id"] = test_data["sample_id"].astype(int).astype(str)
#     pd_y_pred_new_sum["label"] = y_pred_test
#     pd_y_pred_new_sum["label"] = pd_y_pred_new_sum["label"].astype(int)
#     summery=dict(pd_y_pred_new_sum.values)
#     json_path1=save_json(summery,"test")
#
#     pd_y_pred_new = pd.DataFrame()
#     pd_y_pred_new["id"] = test_data["sample_id"].astype(int).astype(str)
#     pd_y_pred_new["label"] = y_pred_test
#     #保存到文件
#     csv_path=save_csv(pd_y_pred_new,"test")
#
#     #统计不同label的数量，并且转换为字典
#     label_count_info=pd_y_pred_new.groupby("label", as_index=False).count().set_index("label")["id"].to_dict()
#     label_count_info2=pd_y_pred_new.groupby("label", as_index=False).count()
#     label_count_info2.rename(columns={'id':'value',"label":"name"}, inplace=True)
#     label_count_info2=label_count_info2.to_json(orient="records", force_ascii=False)
#     #分别统计每个label下的id集合
#     label_id_info=pd_y_pred_new.groupby("label", as_index=False).agg(lambda x: x.tolist()).set_index("label")["id"].to_dict()
#     if label_count_info.get(0) is None:
#         label_count_info[0]=0
#     if label_count_info.get(1) is None:
#         label_count_info[1]=0
#     if label_count_info.get(2) is None:
#         label_count_info[2]=0
#     if label_count_info.get(3) is None:
#         label_count_info[3]=0
#     if label_count_info.get(4) is None:
#         label_count_info[4]=0
#     if label_count_info.get(5) is None:
#         label_count_info[5]=0
#
#     test_info=  {"label_count_info":label_count_info,"label_count_info2":label_count_info2,"label_id_info":label_id_info}
#     #单个id对应的label
#     test_json = pd_y_pred_new.to_json(orient="records", force_ascii=False)
#     test_json = json.loads(test_json)
#
#     test_json2 = pd_y_pred_new.astype(str).set_index("id")["label"].to_dict()
#     #保存到文件中
#     # json_path=save_json(test_json2,"test")
#
#     pd_y_prob_new = pd.DataFrame(y_pro_test, columns=["label_0", "label_1", "label_2", "label_3", "label_4", "label_5"])
#     pd_y_prob_new.insert(0, 'id', test_data["sample_id"].astype(int).astype(str))
#     test_prob_json = pd_y_prob_new.to_json(orient="records", force_ascii=False)
#     test_prob_json = json.loads(test_prob_json)
#     all_test_count=len(test_data)
#     # return {"test_info":test_info,"csv_path":csv_path,"json_path":json_path,"y_pred": test_json, "y_pred2": test_json2, "y_Probability": test_prob_json}
#     return {"test_info":test_info,"all_test_count":all_test_count,"csv_path":csv_path,"json_path":json_path1,"y_pred": test_json, "y_pred2": summery, "y_Probability": test_prob_json}

