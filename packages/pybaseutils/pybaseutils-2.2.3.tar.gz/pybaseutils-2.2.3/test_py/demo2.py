# -*-coding: utf-8 -*-
"""
    @Author : PKing
    @E-mail : 390737991@qq.com
    @Date   : 2022-12-31 11:37:30
    @Brief  : https://blog.csdn.net/qdPython/article/details/121381363
"""
import os
import cv2
import random
import types
import torch
import numpy as np
from typing import Callable
from pybaseutils import image_utils, file_utils, text_utils
from pybaseutils.cvutils import video_utils
import cv2
import re

if __name__ == '__main__':
    file = "/home/PKing/nasdata/dataset-dmai/AIJE/dataset/aije-action-cvlm-v2/action-names.txt"
    files = file_utils.read_data(file, split=None)
    names = []
    for file in files:
        name = os.path.basename(file)
        names.append(name)
    names = list(set(names))
    names = text_utils.find_match_texts(texts=names, pattern=["手拿*"])
    names = list(set(names))
    print(names)
    names = ['手拿钳形电流表', '手拿相序表', '手拿护目镜', '手拿万用表', '手拿尖嘴钳', '手拿螺丝刀', '手拿万能表', '手拿扳手',
             '手拿安全帽', '手拿安全带', '手拿安全围网', '手拿安全绳', '手拿吊物绳', '手拿抹布', '手拿熔断器熔管', '手拿工具袋',
             '手拿采集器', '手拿瓷横担绝缘子', '手拿玻璃绝缘子', '手拿棉纱手套', '手拿绝缘手套,手拿橡胶手套,手拿其他手套',
             '手拿长筒靴', '手拿绝缘垫', '手拿垫子', '手拿熔断器', '手拿卡线器', '手拿紧线器', '手拿验电器', '手拿验电笔', '手拿遮拦杆',
             '手拿核相器', '手拿钢丝绳', '手拿美工刀', '手拿脚扣', '手拿兆欧表', '手拿绝缘胶布', '手拿绝缘杆', '手拿绝缘棒',
             '手拿绝缘挡板', '手拿从此进入指示牌,手拿从此进出标示牌,手拿止步高压危险指示牌,手拿止步高压危险表示牌,手拿止步高压危险标示牌,手拿在此工作标示牌,手拿禁止合闸线路有人工作标示牌']
    print(len(names))
