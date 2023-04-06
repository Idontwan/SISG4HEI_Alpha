import numpy as np
import math as ma


g_L, g_W = 5, 5 #size of grid, unit:cm
local_cood = [[-2, -1], [-2, 1], [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [0, -1],
              [0, 1], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2], [2, -1], [2, 1]]


def real_distance(P0, P1):
    # input is node number
    [I0, J0], [I1, J1] = P0, P1
    return ma.sqrt(g_L*g_L*(I1-I0)*(I1-I0)+g_W*g_W*(J1-J0)*(J1-J0))


def topology(dis_v):
    Topology = {}
    for i in range(1, dis_v.shape[0]-1):
        for j in range(1, dis_v.shape[1]-1):
            if dis_v[i][j] < 99:
                Topology[(i, j)] = []
                for [ii, jj] in local_cood:
                    if dis_v[i+ii][j+jj] < 99:
                        Topology[(i, j)].append([i+ii, j+jj])
    return Topology


def weighted_dijistra(s_nodes, topo_graph, dis_val):
    distance = 99999 * np.ones(dis_val.shape, dtype=np.float32)
    boundry, max_dis = {}, 0
    for [k, t] in s_nodes:
        distance[k][t] = 0.0
        boundry[(k, t)] = 0.0
    while boundry != {}:
        (I, J) = min(boundry, key=boundry.get)
        Od = boundry.pop((I, J))
        neighbors = topo_graph.pop((I, J))
        if neighbors != []:
            for [II, JJ] in neighbors:
                real_d = real_distance([II, JJ],[I, J])
                n_dis = Od + real_d*dis_val[II][JJ]
                if n_dis < distance[II][JJ]:
                    distance[II][JJ] = n_dis
                    if n_dis > max_dis: max_dis = n_dis
                boundry[(II, JJ)] = distance[II][JJ]
                topo_graph[(II, JJ)].remove([I, J])
    return distance, round(max_dis, 2)


def connect_check(distance, max_dis, destinations):
    for act in destinations:
        e_nodes = destinations[act]
        value = 99998
        for node in e_nodes:
            [I, J] = node
            if distance[I][J] < value: value = distance[I][J]
        if value > max_dis: return False, act
    return True, None