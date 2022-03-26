#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
# 安装库 pip install pymupdf Pillow
from getopt import getopt
import sys
import os
import fitz
from PIL import Image


def crop_file(file, row, column):
    # 打开一张图
    img = Image.open(file)
    # 图片尺寸
    img_size = img.size
    h = img_size[1]  # 图片高度
    w = img_size[0]  # 图片宽度

    assert(row >= 1)
    assert(column >= 1)

    dw = w / column
    dh = h / row

    # ###不填参数直接复制
    # region = img.crop()
    # ###保存图片
    # region.save("test123.jpg")
    k = file.rfind('.')
    name = file[:k]
    for i in range(row):
        for j in range(column):
            x = j * dw
            y = i * dh
            # 开始截取
            region = img.crop((x, y, x + dw, y + dh))
            # 保存图片
            name2 = '{}-{}_{}.png'.format(name, i, j)
            region.save(name2)
    return


def convert_file(pdf, **kwargs):
    # for pdf in pdf_dir:
    doc = fitz.open(pdf)
    #pdf_name = os.path.splitext(pdf)[0]
    pdf_name = os.path.splitext(pdf)[0]
    print("====================================")
    print("开始转换: %s.PDF文档" % pdf_name)
    print("====================================")
    print("共", doc.pageCount, "页")
    page_row = 1
    page_cloumn = 1
    if(kwargs != None):
        a = kwargs.get('page', '1,1')
        b = a.split(',')
        page_row = int(b[0])
        page_cloumn = int(b[1])
    for pg in range(0, doc.pageCount):
        print("\r转换为图片: ", pg+1, "/", doc.pageCount, end=";")
        page = doc[pg]
        rotate = int(0)  # 旋转角度
        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像
        zoom_x = 2.0
        zoom_y = 2.0
        print("")
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        outfile = str(pdf_name)+'-'+'{:04}.png'.format(pg)
        pm.writePNG(outfile)
        if(page_row > 1 or page_cloumn > 1):
            crop_file(outfile, page_row, page_cloumn)


def convert_dir(file, **kwargs):
    last_dir = None
    if(file != None):
        if(os.path.isfile(file)):
            convert_file(file, **kwargs)
            return
        if(not os.path.isdir(file)):
            return
        last_dir = os.getcwd()
        os.chdir(file)
    docunames = os.listdir()
    for docuname in docunames:
        if os.path.splitext(docuname)[1] == '.pdf':  # 目录下包含.pdf的文件
            convert_file(docuname, **kwargs)
    if(last_dir != None):
        os.chdir(last_dir)
    return


def convert(*args, **kwargs):
    if(len(args) == 0):
        convert_dir(None, **kwargs)
        return
    for s in args:
        convert_dir(s, **kwargs)
    return


def help():
    print('用法：')
    print('\tpdf_split [文件名称或者目录名称] [page=row,colume]')
    print('\t\trow,colume:\t每一页里面拆分成row * colume个子页面')
    print('例子1：递归查找当前目录及其子目录，对所有的pdf文件按页码进行分拆，分拆后的文件为png文件')
    print('\tpdf_split .')
    print('例子2：递归查找指定目录dir及其子目录，对所有的pdf文件按页码进行分拆，分拆后的文件为png文件')
    print('\tpdf_split dir')
    print('例子3：对指定的pdffile,按页码进行分拆，分拆后的文件为png文件')
    print('\tpdf_split pdffile')
    print('例子4：对指定的pdffile,按每页分拆为1*2个子页面,分拆后的文件为png文件')
    print('\tpdf_split pdffile page=1,2')
    return


if __name__ == '__main__':
    argv = sys.argv[1:]
    if(len(argv) == 0):
        help()
        sys.exit()
    args = []
    kwargs = {}
    for s in argv:
        i = s.find('=')
        if(i < 0):
            args.append(s)
            continue
        k = s[:i]
        v = s[i+1:]
        kwargs[k] = v
    convert(*argv, **kwargs)
