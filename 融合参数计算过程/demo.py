# -*- coding: utf-8 -*-

'''
@File         : demo.py
@Date         : 2021-06-08
@Author       : hejinlong
@Description  : Description
'''
import numpy as np
from PIL import Image, ImageDraw

Tr = np.array([
        [-0.02070199, -0.99958328, -0.02011693,  0.15540699],
        [-0.02597315,  0.02065215, -0.99944929,  0.07732665],
        [0.99944826,-0.02016809, -0.02638987, -0.14022058],
        [0,0,0,1]
    ])

K = np.array([
        [1971.21386418223, 0, 941.189941543722, 0],
        [0, 1969.46477577276, 552.308752181988, 0],
        [0, 0, 1, 0],
        [0,0,0,1]
    ])

Trans = np.matmul(K, Tr)

print(Trans.tolist())
# exit()

#畸变参数,注意径向畸变是小写的k
k1, k2, k3 = -0.592329526472428, 0.410550659853592, -0.190321629469791
p1,p2 = -0.000866128952253595, -0.00161841235516720
fx, fy = 1971.21386418223, 1969.46477577276
cx, cy = 941.189941543722, 552.308752181988

file = open("0_1595574171.166545.txt")

image = Image.open("0_1595574171.166545.jpeg")

draw = ImageDraw.Draw(image)

for line in file:
    [x,y,z,i] = line.split(',')

    pin = [[float(x), float(y), float(z), 1]]

    imgPoint = np.matmul(Trans, np.mat(pin).T).T

    xc = imgPoint[0,0]
    yc = imgPoint[0,1]
    zc = imgPoint[0,2]

    x = xc/zc
    y = yc/zc

    draw.ellipse((x-1, y-1, x+1, y+1), fill = (255, 0, 0))
    #畸变逻辑
    # u = x
    # v = y
    # x1 = (u - cx) / fx
    # y1 = (v - cy) / fy
    # r = x1*x1 + y1*y1
    # x2 = x1 * (1 + k1 * r + k2 * r * r) + 2 * p1 * x1 * y1 + p2 * (r + 2 * x1 * x1)
    # y2 = y1 * (1 + k1 * r + k2 * r * r) + p1 * (r + 2 * y1 * y1) + 2 * p2 * x1 * y1
    # u_d = fx * x2 + cx
    # v_d = fy * y2 + cy

    # draw.ellipse((u_d-1, v_d-1, u_d+1, v_d+1), fill = (255, 0, 0))

image.show()