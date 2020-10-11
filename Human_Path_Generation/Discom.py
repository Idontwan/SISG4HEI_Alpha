import math as ma
import numpy as np


edge, g_L, g_W = 50, 5, 5


def p2odis(p, obj):
    [x, y, L, W, _], [px, py] = obj, p
    if x<=px<=x+L and y<=py<=y+W: return 0
    dy = min(abs(py-y),abs(y+W-py))
    dx = min(abs(px-x),abs(x+L-px))
    if x<=px<=x+L: return dy
    if y<=py<=y+W: return dx
    return ma.sqrt(dx*dx+dy*dy)


def p2wdis(p,wall):
    [[w00,w01],[w10,w11]], [px, py] = wall, p
    dx = min(abs(px-w00), abs(px-w10))
    dy = min(abs(py-w01), abs(py-w11))
    if w00==w10:
        if w01<=py<=w11: return dx
    if w01==w11:
        if w00<=px<=w10: return dy
    return ma.sqrt(dx*dx+dy*dy)


def sub_dis_val_c(d, type='obj'):
    # 'wall' class include walls and toilet-bathroom combination
    if type=='wall': return max(ma.sqrt(250/d)-1, 0)
    return max(ma.sqrt(150/d)-1, 0)


def com_T_B(T_B):
    [x0, y0, L0, W0, _] = T_B[0]
    [x1, y1, L1, W1, _] = T_B[1]
    if x0==x1: return [x0, min(y0, y1), L0, W0+W1, 'T_B_con']
    else: return [min(x0, x1), y0, L0+L1, W0, 'T_B_con']


def T_B2obj_W(T_B, rooms):
    # input [[toilet], [bathroom]]
    # [bathroom] [p0, p1] represent bathroom in toilet out, [p0, p1] is the wall of toilet inside the room
    #[T_B_combination] represent all in
    flag = [0, 0]
    T_B_walls = []
    room_lims = []
    for room in rooms:
        [rx, ry, rL, rW, _] = room
        room_lims.append([[rx, rx+rL], [ry, ry+rW]])
    for n in range(2):
        [x, y, L, W, _] = T_B[n]
        cx, cy = x+L//2, y+W//2
        wall_cens = [[x,y+W//2], [x+L//2,y], [x+L,y+W//2], [x+L//2,y+W]]
        walls = [[[x,y],[x,y+W]], [[x,y],[x+L,y]], [[x+L,y],[x+L,y+W]], [[x,y+W],[x+L,y+W]]]
        for lim in room_lims:
            if lim[0][0]<cx<lim[0][1] and lim[1][0]<cy<lim[1][1]: flag[n] = 1
        if flag[n] == 0:
            for i in range(4):
                for lim in room_lims:
                    if lim[0][0]<=wall_cens[i][0]<=lim[0][1] and lim[1][0]<=wall_cens[i][1]<=lim[1][1]:
                        T_B_walls.append(walls[i])
                        break
    if flag==[0, 0]: return None, T_B_walls
    if flag==[1, 0]: return T_B[0], T_B_walls
    if flag==[0, 1]: return T_B[1], T_B_walls
    return com_T_B(T_B), None


def mod_walls(walls, T_B_Walls):
    if T_B_Walls != None:
        for wall in T_B_Walls:
            walls.append(wall)


def cal_p_xy(room, i, j):
    [x, y] = room[:2]
    return [x+g_L/2+g_L*i, y+g_W/2+g_W*j]


def cal_dis_val(rooms, furnitures , walls, lims, t_b_in=None):
    dis_val, obstacles = [], []
    for r in furnitures:
        for f in r: obstacles.append(f)
    for n in range(len(rooms)):
        _, _, L, W, _ = rooms[n]
        sub_dis_val = np.ones((L//g_L, W//g_W), dtype=np.float32)
        for i in range(L//g_L):
            for j in range(W//g_W):
                p = cal_p_xy(rooms[n], i, j)
                disws = []
                for wall in walls:
                    dis = p2wdis(p, wall)
                    disws.append(dis)
                if t_b_in:
                    dis = p2odis(p, t_b_in)
                    disws.append(dis)
                disw = min(disws)
                if disw<25: sub_dis_val[i][j] = 100
                else: sub_dis_val[i][j] += sub_dis_val_c(disw, type='wall')
                for obj in obstacles:
                    dis = p2odis(p, obj)
                    if dis<20: sub_dis_val[i][j] = 100
                    elif sub_dis_val[i][j] != 100:
                        sub_dis_val[i][j] += sub_dis_val_c(dis)
        dis_val.append(sub_dis_val)

    X_lim = [lims[0][0] - edge, lims[0][1] + edge]
    Y_lim = [lims[1][0] - edge, lims[1][1] + edge]
    l_x = np.arange(X_lim[0], X_lim[1] + g_L, g_L)
    l_y = np.arange(Y_lim[0], Y_lim[1] + g_W, g_W)
    data = 100*np.ones((len(l_x)-1, len(l_y)-1), dtype=np.float32)
    for n in range(len(rooms)):
        [x, y, L, W, _] = rooms[n]
        N_i, N_j, N_L, N_W = (x-X_lim[0])//g_L, (y-Y_lim[0])//g_W, L//g_L, W//g_W
        for i in range(N_L):
            for j in range(N_W):
                data[i+N_i][j+N_j] = dis_val[n][i][j]
    return data