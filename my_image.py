#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

# 安装库 pip install reportlab

from PIL import Image


# 图片文件名称列表


def open_image(file):
    # 打开一张图
    img = Image.open(file)
    # 图片尺寸
    img_size = img.size
    h = img_size[1]  # 图片高度
    w = img_size[0]  # 图片宽度

    return img
