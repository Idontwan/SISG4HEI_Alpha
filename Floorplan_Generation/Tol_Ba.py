# (0, 0) is in the middle of Bedroom

import numpy.random as rd


To_L, To_W = 90, 120
Ba_L, Ba_W = 180, 120
Size = [To_L, To_W, Ba_L, Ba_W]
Door_L = 60
# Door in the middle of To and Ba


def loc_TB(Size, TB_x, TB_y, is_y, To_on):
    [To_L, To_W, Ba_L, Ba_W] = Size
    if is_y:
        temp = [To_W, Ba_W]
        To_W, Ba_W = To_L, Ba_L
        To_L, Ba_L = temp[0], temp[1]
        if To_on:
            Ba_x, Ba_y = TB_x, TB_y
            To_x, To_y = TB_x, TB_y+Ba_W
        else:
            To_x, To_y = TB_x, TB_y
            Ba_x, Ba_y = TB_x, TB_y+To_W
    else:
        if To_on:
            Ba_x, Ba_y = TB_x, TB_y
            To_x, To_y = TB_x+Ba_L, TB_y
        else:
            To_x, To_y = TB_x, TB_y
            Ba_x, Ba_y = TB_x+To_L, TB_y
    return To_L, To_W, Ba_L, Ba_W, To_x, To_y, Ba_x, Ba_y


def TB_in_ou(Value):
    #Value maybe B_L, B_W, K_W, L_W, L_L
    T_B_in = False
    t = rd.rand()
    Q = (Value-360) / 300
    if t<Q: T_B_in = True
    return T_B_in


def TB_LD(type, B_L, B_W, K_W, L_W, L_L, Size, K_cut):
    # for type 4 or 5 L_W = L_W - 120 if L_add is on
    [To_L, To_W, Ba_L, Ba_W] = Size
    # To_L, To_W, Ba_L, Ba_W = 90, 120, 180, 120
    B_ri, B_up = B_L//2, B_W//2
    B_le, B_do = -B_ri, -B_up

    if type == 0:
        is_y, To_on = True, True
        TB_x, TB_y = B_ri, B_up-Ba_L
        T_B_in = TB_in_ou(B_L)
        if T_B_in: TB_x -= To_W
        return TB_x, TB_y, is_y, To_on, T_B_in

    if type == 1:
        l_1 = [[B_ri, B_up-Ba_L], [B_ri, B_up], [B_ri, B_up+L_W-Ba_L-To_L]]
        l_2 = [[B_ri, B_up], [B_ri, B_up+L_W-Ba_L-To_L]]
        if L_W<(To_L+Ba_L): l_1, l_2 = [[B_ri, B_up-Ba_L]], []
        l_3 = [[B_ri-Ba_L-To_L, B_up+L_W]]
        l_4 = [[B_ri-Ba_L-To_L, B_up+L_W]]
    elif type == 2:
        l_1 = [[B_ri, B_up-Ba_L], [B_ri, B_up+K_W], [B_ri, B_up+K_W+L_W-Ba_L-To_L]]
        l_2 = [[B_ri, B_up+K_W-To_L], [B_ri, B_up+K_W], [B_ri, B_up+K_W+L_W-Ba_L-To_L]]
        if L_W<(To_L+Ba_L): l_1, l_2 = [[B_ri, B_up-Ba_L]], [[B_ri, B_up+K_W-To_L]]
        l_3 = [[B_ri-Ba_L-To_L, B_up+K_W+L_W]]
        l_4 = [[B_ri-Ba_L-To_L, B_up+K_W+L_W]]
    elif type == 3:
        l_1 = [[B_ri, B_up-Ba_L], [B_ri, B_up], [B_ri, B_up+L_W-Ba_L-To_L], [B_ri, B_up+L_W-Ba_L]]
        l_2 = [[B_ri, B_up], [B_ri, B_up+L_W-Ba_L-To_L]]
        if L_W<(To_L+Ba_L): l_1, l_2 = [[B_ri, B_up-Ba_L], [B_ri, B_up+L_W-Ba_L]], []
        l_3 = []
        l_4 = []
    elif type == 4:
        l_1 = [[B_le-Ba_W, B_up-Ba_L], [B_ri+L_L, B_up+K_W-L_W], [B_ri+L_L, B_up+K_W-Ba_L-To_L]]
        # Attention on l_1[0]
        l_2 = [[B_ri+L_L, B_up+K_W-L_W], [B_ri+L_L, B_up+K_W-Ba_L-To_L]]
        l_3 = [[B_ri, B_up+K_W], [B_ri+L_L-Ba_L-To_L, B_up+K_W], [B_ri, B_up+K_W-L_W-To_W],
               [B_ri+L_L-Ba_L-To_L, B_up+K_W-L_W-To_W]]
        l_4 = [[B_ri-To_L, B_up+K_W], [B_ri, B_up+K_W], [B_ri+L_L-Ba_L-To_L, B_up+K_W], [B_ri, B_up+K_W-L_W-To_W],
               [B_ri+L_L-Ba_L-To_L, B_up+K_W-L_W-To_W]]
        if L_L<(To_L+Ba_L): l_3, l_4 = [], [[[B_ri-To_L, B_up+K_W]]]
    elif type == 5:
        l_1 = [[B_le-Ba_W, B_up-Ba_L], [B_ri+L_L, B_do], [B_ri+L_L, B_do+L_W-Ba_L-To_L]]
        l_2 = [[B_ri+L_L, B_do], [B_ri+L_L, B_do+L_W-Ba_L-To_L]]
        l_3 = [[B_ri-Ba_L, B_do-Ba_W], [B_ri, B_do-Ba_W], [B_ri+L_L-Ba_L-To_L, B_do-Ba_W],
                [B_ri, B_do+L_W], [B_ri+L_L-Ba_L-To_L, B_do+L_W]]
        l_4 = [[B_ri, B_do-Ba_W], [B_ri+L_L-Ba_L-To_L, B_do-Ba_W], [B_ri, B_do+L_W],
                [B_ri+L_L-Ba_L-To_L, B_do+L_W]]
        if L_L<(To_L+Ba_L): l_3, l_4 = [[B_ri-Ba_L, B_do-Ba_W]], []

    t1, t2, t3, t4 = len(l_1), len(l_2), len(l_3), len(l_4)
    TT = t1+t2+t3+t4
    t = rd.randint(0, TT)
    if t < t1:
        is_y, To_on = True, True
        [TB_x, TB_y] = l_1[t]
    elif t < t1+t2:
        is_y, To_on = True, False
        [TB_x, TB_y] = l_2[t-t1]
    elif t < t1+t2+t3:
        is_y, To_on = False, True
        [TB_x, TB_y] = l_3[t-t1-t2]
    else:
        is_y, To_on = False, False
        [TB_x, TB_y] = l_4[t-t1-t2-t3]

    if is_y and type > 3 and TB_x<0 and K_cut:
        T_B_in = True
        TB_x += To_W
        return TB_x, TB_y, is_y, To_on, T_B_in

    if is_y:
        Value, Cut = B_L, -To_W
        if type > 3:
            if TB_x > 0: Value = L_L
            else: Cut = To_W
    else:
        Value, Cut = L_W, -To_W
        if type==4:
            if t==t1+t2+t3: Value = K_W
            if TB_y<(B_up+K_W): Cut = To_W
        if type==5:
            if t==t1+t2: Value = B_W
            if TB_y<B_do: Cut = To_W

    T_B_in = TB_in_ou(Value)
    if T_B_in:
        if is_y: TB_x += Cut
        else: TB_y += Cut

    return TB_x, TB_y, is_y, To_on, T_B_in