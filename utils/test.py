# -*- coding: utf-8 -*- 
'''
# @Time : 2023/10/30 18:06 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : test.py 
#@desc:
'''
a=[-1,-1,0,1,-1,2]
# a=set(a)

# 使用python实现三元组实现求和为0


import random
import numpy as np
def so():
    length=len(a)
    for i in range(100000):
        b=random.sample(a,3,)
        sum=np.sum(b)
        if sum==0:
            print(b)
