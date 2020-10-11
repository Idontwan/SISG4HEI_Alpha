import numpy.random as rd


import Size_Sample as ss
import Tol_Ba as TB
import R_xy
import Furniture_Place as FP


def change_R(i, j, k, room):
    [x, y, L, W, _] = room
    if i :
        room[0] = - (x + L)
        x = room[0]
    if j :
        room[1] = - (y + W)
        y = room[1]
    if k :
        room[0], room[1] = y, x
        room[2], room[3] = W, L


def flip_rot(House, Toil_Bath, Furnitures, Doors, Walls):
    [i, j, k] = rd.randint(0, 2, size=3)
    for room in House:
        change_R(i, j, k, room)
    for room in Toil_Bath:
        change_R(i, j, k, room)
    for room in Furnitures:
        for furniture in room:
            change_R(i, j, k, furniture)
    for door in Doors:
        change_R(i, j, k, door)
    for wall in Walls:
        [[p0x, p0y], [p1x, p1y]] = wall
        if i:
            if p0x == p1x:
                wall[0], wall[1] = [-p0x, p0y], [-p1x, p1y]
            else:
                wall[0], wall[1] = [-p1x, p1y], [-p0x, p0y]
            [[p0x, p0y], [p1x, p1y]] = wall
        if j:
            if p0y == p1y:
                wall[0], wall[1] = [p0x, -p0y], [p1x, -p1y]
            else:
                wall[0], wall[1] = [p1x, -p1y], [p0x, -p0y]
            [[p0x, p0y], [p1x, p1y]] = wall
        if k:
            wall[0], wall[1] = [p0y, p0x], [p1y, p1x]


def Floor_Plan(topo, furs):
    type, [B_L, B_W], B_A, [K_L, K_W], K_A, [L_L, L_W], L_A, K_cut, L_add \
        = ss.sizes_sample(topo, ss.B_A_min, ss.B_A_max, ss.K_A_min, ss.K_A_max,
                          ss.L_A_min, ss.L_A_max, ss.len_step)
    # important
    if type > 3 and L_add: L_W = L_W - TB.To_W
    # important
    TB_x, TB_y, is_y, To_on, T_B_in = TB.TB_LD(type, B_L, B_W, K_W, L_W, L_L, TB.Size, K_cut)
    To_L, To_W, Ba_L, Ba_W, To_x, To_y, Ba_x, Ba_y = \
        TB.loc_TB(TB.Size, TB_x, TB_y, is_y, To_on)
    Bedroom, Kitchen, Livingroom = R_xy.rect_com(type, B_L, B_W, K_W, L_L, L_W)
    T_con = R_xy.who_con(type, To_x, To_y, Bedroom[0], Bedroom[1], Kitchen[1], Livingroom[1])
    B_con = R_xy.who_con(type, Ba_x, Ba_y, Bedroom[0], Bedroom[1], Kitchen[1], Livingroom[1])
    Kitchen, Livingroom = R_xy.cut_add(type, is_y, T_B_in, T_con, B_con, K_cut, L_add, Ba_y,
                                       Kitchen, Livingroom)
    Toilet = [To_x, To_y, To_L, To_W, 'Toilet']
    Bathroom = [Ba_x, Ba_y, Ba_L, Ba_W, 'Bathroom']
    Toil_Bath = [Toilet, Bathroom]
    Doors, Walls, Be_con, Ki_con, Li_con = R_xy.Pla_Door(type, Bedroom, Kitchen, Livingroom, Toilet, Bathroom)
    Be_con, Ki_con, Li_con = R_xy.add_TB_obs(Be_con, Ki_con, Li_con, Toilet, Bathroom, T_con, B_con)
    T_Door, B_Door = R_xy.TB_Door(Bedroom, Kitchen, Livingroom, Toilet, Bathroom, T_con, B_con)
    Doors.append(T_Door)
    Doors.append(B_Door)
    B_F = FP.PLF_B(furs[0], Bedroom, Bathroom, Be_con, Doors)
    if type == 0:
        House = [Bedroom, Kitchen]
        K_F = FP.PLF_K(furs[1], Kitchen, Toilet, Ki_con)
        Furnitures = [B_F, K_F]
    elif type == 1:
        House = [Bedroom, Livingroom]
        L_F = FP.PLF_L(furs[2], Livingroom, Toilet, Bathroom, Li_con, Doors)
        Furnitures = [B_F, L_F]
    else:
        House = [Bedroom, Kitchen, Livingroom]
        K_F = FP.PLF_K(furs[1], Kitchen, Toilet, Ki_con)
        L_F = FP.PLF_L(furs[2], Livingroom, Toilet, Bathroom, Li_con, Doors)
        Furnitures = [B_F, K_F, L_F]
    flip_rot(House, Toil_Bath, Furnitures, Doors, Walls)
    return House, Toil_Bath, Furnitures, Doors, Walls, T_con, B_con, type


def Boundary(House, Toil_Bath):
    X_lims = [[], []]
    Y_lims = [[], []]
    for room in House:
        [x, y, L, W, _] = room
        X_lims[0].append(x), X_lims[1].append(x + L)
        Y_lims[0].append(y), Y_lims[1].append(y + W)
    for room in Toil_Bath:
        [x, y, L, W, _] = room
        X_lims[0].append(x), X_lims[1].append(x + L)
        Y_lims[0].append(y), Y_lims[1].append(y + W)
    X_lim = [min(X_lims[0]), max(X_lims[1])]
    Y_lim = [min(Y_lims[0]), max(Y_lims[1])]
    return [X_lim, Y_lim]