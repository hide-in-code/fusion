# -*- coding: utf-8 -*-

'''
@File         : demo.py
@Date         : 2021-06-08
@Author       : hejinlong
@Description  : Description
'''
import numpy as np

np.set_printoptions(precision=6, threshold=8, edgeitems=6, linewidth=75, suppress=True, nanstr='nan', infstr='inf')

px = -0.0004217634029916384
py = -0.21683144949675118
pz = -1.0553445472201475

rx = 1.5518043975723739
ry = -0.003024701217351147
rz = 0.0014742699607357519

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

T = np.array([
    [1,0,0,px],
    [0,1,0,py],
    [0,0,1,pz],
    [0,0,0,1]
])

R = np.mat(Rx) * np.mat(Ry) * np.mat(Rz)
Tr = np.mat(T) * np.mat(R)

print(Tr)