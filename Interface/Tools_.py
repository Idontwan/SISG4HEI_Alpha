import sys, os
import numpy.random as rd
import math as ma


edge = 10
edge_in_main = 50
# the definition of edge in Floorplan_Generation or Human_path_Generation Folder
g_L, g_W = 5, 5


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('/')]
upper_path = abs_path[:abs_path.rfind('/')]
if upper_path not in sys.path: sys.path.append(upper_path)


import Load


def load_disval(path):
    [h_v, fname0, fname1] = path.split('/')
    return Load.load_filed('Discomfortable_value', h_v, fname0, fname1)


def caldist(p0, p1):
    return ma.sqrt((p1[0]-p0[0])*(p1[0]-p0[0])+(p1[1]-p0[1])*(p1[1]-p0[1]))


def sample_rooms(rooms):
    N = len(rooms)
    r_As = [rooms[i][2] * rooms[i][3] for i in range(N)]
    r_sumA = sum(r_As)
    poss_list = [r_As[0] / r_sumA, 1.0] if N == 2 else [r_As[0] / r_sumA, 1 - r_As[2] / r_sumA, 1.0]
    t = rd.rand()
    for i in range(N):
        if t < poss_list[i]: return i


def cal_I_J(rooms, lims, i):
    ts = rd.rand(2)
    real_x = rooms[i][0] + ts[0]*rooms[i][2]
    real_y = rooms[i][1] + ts[1]*rooms[i][3]
    I = (real_x-lims[0][0]+edge_in_main)//g_L
    J = (real_y-lims[1][0]+edge_in_main)//g_W
    return real_x, real_y, int(I), int(J)


def robot_position(rooms, lims, dis_val_data, human, disval_Threshold=7.5):
    dis_val = 3*disval_Threshold
    dist = 0
    while dis_val>disval_Threshold or dist<50:
        choiced_room = sample_rooms(rooms)
        robot_x, robot_y, r_I, r_J = cal_I_J(rooms, lims, choiced_room)
        dis_val = dis_val_data[r_I][r_J]
        dist = caldist(human, [robot_x, robot_y])
    return robot_x, robot_y


def PIR_position(rooms, lims, dis_val_data, disval_Threshold=2.5):
    PIRs, N = [], 0
    while N<20 and len(PIRs)<4:
        N += 1
        choiced_room = sample_rooms(rooms)
        PIR_x, PIR_y, r_I, r_J = cal_I_J(rooms, lims, choiced_room)
        least_dist = 10000
        for [x, y] in PIRs:
            if caldist([PIR_x, PIR_y], [x, y])<least_dist: least_dist=caldist([PIR_x, PIR_y], [x, y])
        if dis_val_data[r_I][r_J]<disval_Threshold and least_dist>50:
            PIRs.append([PIR_x, PIR_y])
    return PIRs