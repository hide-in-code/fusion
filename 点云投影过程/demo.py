# -*- coding: utf-8 -*-

'''
@File         : demo.py
@Date         : 2021-06-08
@Author       : hejinlong
@Description  : Description
'''
import os
import sys
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math


def drawPoint(draw, point, color=(255, 0, 0), index=0):
    xc = point[0,0]
    yc = point[0,1]
    zc = point[0,2]
    x = xc/zc
    y = yc/zc

    # x, y = antiDistortion(x, y)

    if x < 0:
        x = 0
    if y < 0:
        y = 0

    if x > 1920:
        x = 1920
    if y > 1080:
        y = 1080

    font = ImageFont.truetype("arial.ttf", 25, encoding="unic")#设置字
    draw.text((x - 40, y - 40), str(index), 'fuchsia', font)
    # draw.text((x - 30, y - 30), f"{x}", 'green', font)

    draw.ellipse([x - 10, y -10, x + 10, y + 10], fill=color, width=1)

def drawLine(draw, point1, point2):
    xc1 = point1[0,0]
    yc1 = point1[0,1]
    zc1 = point1[0,2]
    x1 = xc1/zc1
    y1 = yc1/zc1

    # x1, y1 = antiDistortion(x1, y1)

    xc2 = point2[0,0]
    yc2 = point2[0,1]
    zc2 = point2[0,2]
    x2 = xc2/zc2
    y2 = yc2/zc2

    # x2, y2 = antiDistortion(x2, y2)

    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0

    if x1 > 1920:
        x1 = 1920
    if y1 > 1080:
        y1 = 1080

    if x2 < 0:
        x2 = 0
    if y2 < 0:
        y2 = 0

    if x2 > 1920:
        x2 = 1920
    if y2 > 1080:
        y2 = 1080

    draw.line((x1, y1, x2, y2), width=3, fill='red')

def antiDistortion(x, y):
    k1, k2, k3 = -0.592329526472428, 0.410550659853592, -0.190321629469791
    p1,p2 = -0.000866128952253595, -0.00161841235516720
    fx, fy = 1971.21386418223, 1969.46477577276
    cx, cy = 941.189941543722, 552.308752181988

    u = x
    v = y
    x1 = (u - cx) / fx
    y1 = (v - cy) / fy
    r = x1*x1 + y1*y1
    x2 = x1 * (1 + k1 * r + k2 * r * r) + 2 * p1 * x1 * y1 + p2 * (r + 2 * x1 * x1)
    y2 = y1 * (1 + k1 * r + k2 * r * r) + p1 * (r + 2 * y1 * y1) + 2 * p2 * x1 * y1
    u_d = fx * x2 + cx
    v_d = fy * y2 + cy

    return u_d, v_d

def vis(imgPath, label3DPath):
    img = Image.open(imgPath)
    draw = ImageDraw.Draw(img)

    with open(label3DPath) as F_3d:

        jsonData = json.load(F_3d)

        for mark in jsonData["marks"]:
            x = mark["position"]["x"]
            y = mark["position"]["y"]
            z = mark["position"]["z"]
            sx = mark["scale"]["x"]
            sy = mark["scale"]["y"]
            sz = mark["scale"]["z"]
            rx = 0
            ry = 0
            rz = mark["rotation"]["z"]

            #构造3D基准点
            p1 = [[sx /2, sy / 2, -sz / 2, 1]]
            p2 = [[-sx /2, sy / 2, -sz / 2, 1]]
            p3 = [[-sx /2, -sy / 2, -sz / 2, 1]]
            p4 = [[sx /2, -sy / 2, -sz / 2, 1]]

            p5 = [[sx /2, sy / 2, sz / 2, 1]]
            p6 = [[-sx /2, sy / 2, sz / 2, 1]]
            p7 = [[-sx /2, -sy / 2, sz / 2, 1]]
            p8 = [[sx /2, -sy / 2, sz / 2, 1]]

            #3D内部的平移旋转
            t = np.array([
                [1,0,0,x],
                [0,1,0,y],
                [0,0,1,z],
                [0,0,0,1]
            ])

            Rx = [
                [1, 0, 0, 0],
                [0, np.cos(rx), -np.sin(rx), 0],
                [0, np.sin(rx), np.cos(rx), 0],
                [0, 0, 0, 1]
            ]

            Ry = [
                [np.cos(ry), 0, np.sin(ry), 0],
                [0, 1, 0, 0],
                [-np.sin(ry), 0, np.cos(ry), 0],
                [0, 0, 0, 1]
            ]

            Rz = [
                [np.cos(rz), -np.sin(rz), 0, 0],
                [np.sin(rz), np.cos(rz), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]

            R = np.mat(Rx) * np.mat(Ry) * np.mat(Rz)
            Rt = np.mat(t) * np.mat(R)

            point3D1 = np.matmul(Rt, np.mat(p1).T).T
            point3D2 = np.matmul(Rt, np.mat(p2).T).T
            point3D3 = np.matmul(Rt, np.mat(p3).T).T
            point3D4 = np.matmul(Rt, np.mat(p4).T).T
            point3D5 = np.matmul(Rt, np.mat(p5).T).T
            point3D6 = np.matmul(Rt, np.mat(p6).T).T
            point3D7 = np.matmul(Rt, np.mat(p7).T).T
            point3D8 = np.matmul(Rt, np.mat(p8).T).T

            Trans = np.array([
                [899.8625997012127, -1989.3744233888965, -64.49265152342986, 174.36621378540235],
                [500.8508173101968, 29.534669347181378, -1982.955527996039, 74.84705983347406],
                [0.99944826, -0.02016809, -0.02638987, -0.14022058],
                [0.0, 0.0, 0.0, 1.0]
            ])

            #是否存在图片内的点
            pointImage1 = np.matmul(Trans, np.mat(point3D1).T).T
            pointImage2 = np.matmul(Trans, np.mat(point3D2).T).T
            pointImage3 = np.matmul(Trans, np.mat(point3D3).T).T
            pointImage4 = np.matmul(Trans, np.mat(point3D4).T).T
            pointImage5 = np.matmul(Trans, np.mat(point3D5).T).T
            pointImage6 = np.matmul(Trans, np.mat(point3D6).T).T
            pointImage7 = np.matmul(Trans, np.mat(point3D7).T).T
            pointImage8 = np.matmul(Trans, np.mat(point3D8).T).T

            points = [pointImage1, pointImage2, pointImage3, pointImage4, pointImage5, pointImage6, pointImage7, pointImage8]

            drawFlag = False
            for point in points:
                if point[0, 2] < 0:
                    drawFlag = True
                    break
            
            if drawFlag:
                continue

            drawPoint(draw, pointImage1, index=1)
            drawPoint(draw, pointImage2, index=2)
            drawPoint(draw, pointImage3, index=3)
            drawPoint(draw, pointImage4, index=4)
            drawPoint(draw, pointImage5, index=5)
            drawPoint(draw, pointImage6, index=6)
            drawPoint(draw, pointImage7, index=7)
            drawPoint(draw, pointImage8, index=8)

            drawLine(draw, pointImage1, pointImage2)
            drawLine(draw, pointImage4, pointImage1)
            drawLine(draw, pointImage2, pointImage3)
            drawLine(draw, pointImage3, pointImage4)

            drawLine(draw, pointImage5, pointImage6)
            drawLine(draw, pointImage8, pointImage5)
            drawLine(draw, pointImage6, pointImage7)
            drawLine(draw, pointImage7, pointImage8)

            drawLine(draw, pointImage1, pointImage5)
            drawLine(draw, pointImage2, pointImage6)
            drawLine(draw, pointImage3, pointImage7)
            drawLine(draw, pointImage4, pointImage8)

    img.show()
    exit()

if __name__ == "__main__":
    imgPath = sys.argv[1]
    label3DPath = sys.argv[2]
    vis(imgPath, label3DPath)
