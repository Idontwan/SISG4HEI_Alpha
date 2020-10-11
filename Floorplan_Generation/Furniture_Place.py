# unit is cm
import numpy.random as rd
import math as ma
import random


B_A0, B_A1 = 80000, 160000
K_A0, K_A1 = 60000, 120000
L_A0, L_A1 = 120000, 240000
To_W, Pass_W = 120, 60

Bed_S = [[210, 150], [210, 180]]
Wardrobe_S = [[60, 60], [80, 60], [100, 60], [120, 60]]
Writing_T_C_S = [[100, 100], [120, 100]]
Nstand_S = [40, 40]
Dinner_T_S = [[80, 80], [100, 80], [120, 80], [140, 80], [160, 80]]
Chair = [40, 40]
Sofa_TV_S = [[300, 90], [300, 140], [300, 190]]
Kitchen_S_S = [[60, 60], [120, 60], [180, 60]]
Cupboard_S = [[100, 50], [120, 50], [150, 50]]
Fridge_S = [60, 60]
Washer_S = [60, 60]
T_Bin_S = [[30, 30], [60, 30]]


def sample(OPs_list, tr):
    OPs_sum = sum(OPs_list)
    N = len(OPs_list)
    OPsI = [sum(OPs_list[:i+1]) for i in range(N)]
    PsI = [OPsI[i]/OPs_sum for i in range(N)]
    for i in range(N):
        if tr<PsI[i]: return i


def Sample_Size_F(Sizes, A_i):
    t = rd.rand()
    L = len(Sizes)
    p = 1 / L
    i = int(A_i/p)
    if i == 0:
        return Sizes[i] if t<0.67 else Sizes[i+1]
    elif i > L-2:
        return Sizes[L-1] if t<0.67 else Sizes[L-2]
    else:
        if t < 0.25: return Sizes[i-1]
        elif t < 0.75: return Sizes[i]
        else: return Sizes[i+1]


def sample_fcstr(n_list, T=None):
    # Decide which wall does the furniture be against
    if not T: T = sum(n_list)
    list = [e/T for e in n_list]
    choice = [0]
    L = len(list)
    for i in range(1, L):
        choice.append(choice[i-1]+list[i-1])
    t = rd.rand()
    T, N = L//2, L//2 - 1
    while N < L-1 and (choice[N]>t or choice[N+1]<=t):
        T = max(T//2, 1)
        if choice[N]>t: N = N - T
        else: N = N + T
    return N


def complement(strings, areas):
    '''strings = [string1, string2, ...]
       string1 = [start_point, end_point]
       start_point on the left down of end_point
       start_point = [x_cor, y_cor]
       area = [bottle_left_point, top_right_point]
       bottle_left_point = [x_cor, y_cor]'''

    for area in areas:
        for i in range(len(strings)):
            string = strings.pop(0)
            if string[0][0] == string[1][0]:
                if area[0][0] < string[0][0] < area[1][0]:
                    if area[0][1] >= string[1][1] or area[1][1] <= string[0][1]:
                        strings.append(string)
                    else:
                        if area[1][1] < string[1][1]:
                            strings.append([[string[0][0], area[1][1]], string[1]])
                        if string[0][1] < area[0][1]:
                            strings.append([string[0], [string[1][0], area[0][1]]])
                else:
                    strings.append(string)
            else:
                if area[0][1] < string[0][1] < area[1][1]:
                    if area[0][0] >= string[1][0] or area[1][0] <= string[0][0]:
                        strings.append(string)
                    else:
                        if area[1][0] < string[1][0]:
                            strings.append([[area[1][0], string[0][1]], string[1]])
                        if string[0][0] < area[0][0]:
                            strings.append([string[0], [area[0][0], string[1][1]]])
                else:
                    strings.append(string)


def place_f_c(strings, strings_len, T_len):
    N = sample_fcstr(strings_len, T=T_len)
    string = strings[N]
    t = rd.rand()
    if t < 0.4: return string[0]
    elif t < 0.8: return string[1]
    else: return [(string[0][0]+string[1][0])//2, (string[0][1]+string[1][1])//2]


def select_f_c(strings0, strings1):
    '''strings = [string1, string2, ...]
       string1 = [start_point, end_point]
       start_point on the left down of end_point'''
    flag, Place = 0, True
    strings0_len, strings1_len = [], []
    for string in strings0:
        len = string[1][0]+string[1][1]-string[0][0]-string[0][1]
        strings0_len.append(len)
    for string in strings1:
        len = string[1][0] + string[1][1] - string[0][0] - string[0][1]
        strings1_len.append(len)
    T0, T1 = sum(strings0_len), sum(strings1_len)
    if T0+T1==0: return None, None
    else:
        T_len0_r = T0 / (T0 + T1)
        t = rd.rand()
        if t < T_len0_r:
            f_center = place_f_c(strings0, strings0_len, T0)
        else:
            flag = 1
            f_center = place_f_c(strings1, strings1_len, T1)

    return f_center, flag


def poss_strings(room, F_size, far_X, far_Y):
    # in most cast far_X = 0, far_Y = 0
    R_x, R_y, R_L, R_W, _ = room
    X, Y = F_size[0]//2, F_size[1]//2
    XYS = [[R_x+X+far_X, R_x+R_L-X-far_X], [R_y+Y+far_Y, R_y+R_W-Y-far_Y]]
    Ps = [[XYS[0][i],XYS[1][j]] for i in range(2) for j in range(2)]
    Strings = [[Ps[0],Ps[1]], [Ps[1], Ps[3]], [Ps[2], Ps[3]], [Ps[0], Ps[2]]]
    return Strings


def pla_f(exist, room, F_size, F_name, room_con, far_X=0, far_Y =0):
    if exist == 1:
        if rd.rand()<0.45: return None
    F_s = [F_size, [F_size[1], F_size[0]]]
    L0, W0, L1, W1 = F_s[0][0]//2, F_s[0][1]//2, F_s[1][0]//2, F_s[1][1]//2
    temp_con0, temp_con1 = [], []
    for rect in room_con:
        [x0, y0], [x1, y1] = rect[0], rect[1]
        temp_con0.append([[x0-L0-far_X, y0-W0-far_Y], [x1+L0+far_X, y1+W0+far_Y]])
        temp_con1.append([[x0-L1-far_X, y0-W1-far_Y], [x1+L1+far_X, y1+W1+far_Y]])

    strings0 = poss_strings(room, F_s[0], far_X, far_Y)
    complement(strings0, temp_con0)
    strings1 = poss_strings(room, F_s[1], far_X, far_Y)
    complement(strings1, temp_con1)
    F_cen, flag = select_f_c(strings0, strings1)
    # !
    if F_cen == None: return None
    F_size = F_s[flag]
    X, Y = F_size[0]//2, F_size[1]//2
    return [F_cen[0]-X, F_cen[1]-Y, F_size[0], F_size[1], F_name]


def Cal_Ai(Room, TB, R_A0, R_A1, TB1=None):
    R_A = Room[2] * Room[3]
    TB_cen = [TB[0]+TB[2]//2, TB[1]+TB[3]//2]
    if Room[0]<TB_cen[0]<(Room[0]+Room[2]) and Room[1]<TB_cen[1]<(Room[1]+Room[3]):
        T_or_B_A = TB[2]*TB[3]
        R_A -= T_or_B_A
    if TB1:
        TB1_cen = [TB1[0]+TB1[2]//2, TB1[1]+TB1[3]//2]
        if Room[0]<TB1_cen[0]<(Room[0]+Room[2]) and Room[1]<TB1_cen[1]<(Room[1]+Room[3]):
            T_or_B_A = TB1[2] * TB1[3]
            R_A -= T_or_B_A
    Ai = (R_A-R_A0) / (R_A1-R_A0)
    return Ai


def Sam_far_XY(N, Ai):
    if Ai <0.2: N = N*2//5
    elif Ai<0.5: N = N*3//5
    elif Ai<0.8: N = N*4//5
    i_l = rd.randint(0, N+1, size=2)
    far_X, far_Y = i_l[0] * 10, i_l[1] * 10
    return far_X, far_Y


def add_obstacle(Obastcles, New_Ob, PW=Pass_W):
    # New_Ob = [x, y, L, W], Obatacle = [[x,y],[x,y]]
    [x, y, L, W, name] = New_Ob
    Obastcle = [[x-PW, y-PW], [x+L+PW, y+W+PW]]
    Obastcles.append(Obastcle)


def Cal_Dist(R, F):
    D0, D1 = F[0]-R[0], F[1]-R[1]
    D2, D3 = R[0]+R[2]-F[0]-F[2], R[1]+R[3]-F[1]-F[3]
    return [D0, D1, D2, D3]


def Cal_D_D(P, Ds):
    [Px, Py] = P
    Dist = []
    for D in Ds:
        [x, y, L, W, _] = D
        CP = [x+L//2, y+W//2]
        D = ma.sqrt((Px-CP[0])**2+(Py-CP[1])**2)
        Dist.append(D)
    return min(Dist)


def Pla_Nstands(NS_e, Bedr, Bed, Doors, N=Nstand_S):
    if min(Bed[2], Bed[3]) < 150: return None
    rts = [0.3, 0.4, 0.3] if NS_e==2 else [0, 0.4, 0.3]
    rt = rd.rand()
    t = sample(rts, rt)
    if t == 0: return None
    [Bx, By, BL, BW, _] = Bed
    [NL, NW] = N
    N_S_centers = [[[Bx-NL//2, By+NW//2], [Bx-NL//2, By+BW-NW//2]], [[Bx+NL//2, By-NW//2], [Bx+NL-NL//2, By-NW//2]],
                     [[Bx+BL+NL//2, By+NW//2], [Bx+BL+NL//2, By+BW-NW//2]], [[Bx+NL//2, By+BW+NW//2], [Bx+NL-NL//2, By+BW+NW//2]]]
    Dist = Cal_Dist(Bedr, Bed)
    for i in range(4):
        temp0 = N_S_centers.pop(0)
        if Dist[i]>=40:
            for i in range(2):
                temp1 = temp0.pop(0)
                if Cal_D_D(temp1, Doors)>=90: temp0.append(temp1)
                else: temp0.append([])
            N_S_centers.append(temp0)
        else: N_S_centers.append([[],[]])
    if Bed[2] == 210: N_S_cen = [N_S_centers[1], N_S_centers[3]]
    else: N_S_cen = [N_S_centers[0], N_S_centers[2]]
    if t == 1:
        N_S_Cp = []
        for i in range(2):
            for P in N_S_cen[i]:
                if P != []: N_S_Cp.append(P)
        if N_S_Cp == []: return None
        else:
            N_S_C = random.choice(N_S_Cp)
            return [[N_S_C[0]-NL//2, N_S_C[1]-NW//2, NL, NW, 'Nightstand']]
    else:
        N_S_C2 = []
        for i in range(2):
            if N_S_cen[0][i]!=[] and N_S_cen[1][i]!=[]:
                N_S_C2.append([N_S_cen[0][i], N_S_cen[1][i]])
        if N_S_C2 == []: return None
        else:
            N_S_Cs = random.choice(N_S_C2)
            return [[N_S_Cs[0][0]-NL//2, N_S_Cs[0][1]-NW//2, NL, NW, 'Nightstand'],
                     [N_S_Cs[1][0]-NL//2, N_S_Cs[1][1]-NW//2, NL, NW, 'Nightstand']]


def Pla_Wri_T_C(T_C, DW=50, CL=40, CW=40):
    [x, y, L, W, name] = T_C
    i = rd.randint(0, 2)
    Desks = [[x, y, L, DW, 'Desk'], [x, y+W-DW, L, DW, 'Desk'], [x, y, DW, W, 'Desk'],
             [x+L-DW, y, DW, W, 'Desk']]
    Chairs = [[x+L//2-CL//2, y+W-CW, CL, CW, 'Chair'], [x+L//2-CL//2, y, CL, CW, 'Chair'],
              [x+L-CW, y+W//2-CL//2, CW, CL, 'Chair'], [x, y+W//2-CL//2, CW, CL, 'Chair']]
    if T_C[2] > T_C[3]:
        if i: Desk, Chair = Desks[1], Chairs[1]
        else: Desk, Chair = Desks[0], Chairs[0]
    elif T_C[3] > T_C[2]:
        if i: Desk, Chair = Desks[3], Chairs[3]
        else: Desk, Chair = Desks[2], Chairs[2]
    else:
        j = rd.randint(0, 2)
        N = 2 * i + j
        Desk, Chair = Desks[N], Chairs[N]
    return Desk, Chair


def sam_cha_num(L):
    t = rd.rand()
    if L == Dinner_T_S[0][0]:
        return 1 if t < 0.67 else 2
    elif L == Dinner_T_S[1][0]:
        if t<0.25: return 1
        else: return 2 if t<0.75 else 3
    elif L == Dinner_T_S[2][0]:
        if t<0.15: return 1
        elif t<0.5: return 2
        else: return 3 if t< 0.85 else 4
    elif L == Dinner_T_S[3][0]:
        if t<0.25: return 2
        else: return 3 if t<0.75 else 4
    else:
        return 3 if t < 0.33 else 4


def Pla_Din_Cs(Dinner_T, Livi, Doors, far=10, CL=40, CW=40):
    [x, y, L, W, _] = Dinner_T
    T_L = max(Dinner_T[2], Dinner_T[3])
    n = sam_cha_num(T_L)
    Chairs_cen_P = [[x-far-CL//2, y+W//2], [x+L//2, y-far-CW//2], [x+L+far+CL//2, y+W//2], [x+L//2, y+W+far+CW//2]]
    Dist = Cal_Dist(Livi, Dinner_T)
    for i in range(4):
        center = Chairs_cen_P.pop(0)
        if Dist[i] >= 50:
            Dist_D = Cal_D_D(center, Doors)
            if Dist_D >= 90: Chairs_cen_P.append(center)
    if n > len(Chairs_cen_P): n = len(Chairs_cen_P)
    centers = random.sample(Chairs_cen_P, n)
    Chairs = []
    for center in centers:
        Chairs.append([center[0]-CL//2, center[1]-CW//2, CL, CW, 'Chair'])
    return Chairs


def Sam_TV_size(L):
    P_Ws = [40, 60]
    P_Ls = [60, 80, 100, 120]
    t = rd.rand()
    i = rd.randint(0, 2)
    if L == Sofa_TV_S[0][1]:
        TV_W = P_Ws[0]
        TV_L = P_Ls[0+i]
    elif L == Sofa_TV_S[1][1]:
        TV_W = P_Ws[0] if t < 0.67 else P_Ws[1]
        TV_L = P_Ls[1+i]
    else:
        TV_W = P_Ws[1] if t < 0.67 else P_Ws[0]
        TV_L = P_Ls[2+i]
    return TV_L, TV_W


def Pla_Sofa_TV(L_center, S_TV, S_W=80):
    [x, y, L, W, name] = S_TV
    TV_L, TV_W = Sam_TV_size(min(L, W))
    [xl, yl] = L_center
    if L > W:
        if abs(x-xl) > abs(x+L-xl):
            Sofa, TV = [x+L-S_W, y, S_W, W, 'Sofa'], [x, y+W//2-TV_L//2, TV_W, TV_L, 'TV']
        else:
            Sofa, TV = [x, y, S_W, W, 'Sofa'], [x+L-TV_W, y+W//2-TV_L//2, TV_W, TV_L, 'TV']
    else:
        if abs(y-yl) > abs(y+W-yl):
            Sofa, TV = [x, y+W-S_W, L, S_W, 'Sofa'], [x+L//2-TV_L//2, y, TV_L, TV_W, 'TV']
        else:
            Sofa, TV = [x, y, L, S_W, 'Sofa'], [x+L//2-TV_L//2, y+W-TV_W, TV_L, TV_W, 'TV']
    return Sofa, TV


def PLF_B(fur_B, Bedr, Bath, B_con, Doors, B_A0=B_A0, B_A1=B_A1):
    [WR_e, NS_e, De_e] = fur_B # e means exist
    B_furniture = []
    Ai = Cal_Ai(Bedr, Bath, B_A0, B_A1)
    Bed_Size = Sample_Size_F(Bed_S, Ai)
    Bed = pla_f(2, Bedr, Bed_Size, 'Bed', B_con)
    add_obstacle(B_con, Bed)
    B_furniture.append(Bed)
    if NS_e > 0:
        N_stands = Pla_Nstands(NS_e, Bedr, Bed, Doors)
        if N_stands:
            for N_stand in N_stands:
                add_obstacle(B_con, N_stand)
                B_furniture.append(N_stand)
    if WR_e > 0:
        Wardr_Size = Sample_Size_F(Wardrobe_S, Ai)
        Wardr = pla_f(WR_e, Bedr, Wardr_Size, 'Wardrobe', B_con)
        if Wardr:
            add_obstacle(B_con, Wardr)
            B_furniture.append(Wardr)
    if De_e > 0:
        Wri_T_C_Size = Sample_Size_F(Writing_T_C_S, Ai)
        far_X, far_Y = Sam_far_XY(5, Ai)
        Wri_T_C = pla_f(De_e, Bedr, Wri_T_C_Size, 'Wri_T_C', B_con, far_X=far_X, far_Y=far_Y)
        if Wri_T_C:
            Wri_T, Wri_C = Pla_Wri_T_C(Wri_T_C)
            B_furniture.append(Wri_T)
            B_furniture.append(Wri_C)
    return B_furniture


def PLF_L(fur_L, Livi, Toil, Bath, L_con, Doors, L_A0=L_A0, L_A1=L_A1):
    [Ta_e, ST_e] = fur_L
    [x, y, L, W, _] = Livi
    Livi_c = [x+L//2, y+W//2]
    L_furniture = []
    Ai = Cal_Ai(Livi, Bath, L_A0, L_A1, TB1=Toil)
    if Ta_e>ST_e: I = 1
    elif Ta_e<ST_e: I = 0
    else: I = rd.randint(0, 2)
    if I:
        Dinner_T_Size = Sample_Size_F(Dinner_T_S, Ai)
        far_X, far_Y = Sam_far_XY(10, Ai)
        Dinner_T = pla_f(2, Livi, Dinner_T_Size, 'Dinner_Table', L_con, far_X=far_X, far_Y=far_Y)
        add_obstacle(L_con, Dinner_T)
        L_furniture.append(Dinner_T)
        Dinner_Cs = Pla_Din_Cs(Dinner_T, Livi, Doors)
        for Dinner_C in Dinner_Cs:
            add_obstacle(L_con, Dinner_C)
            L_furniture.append(Dinner_C)
        if ST_e > 0:
            Sofa_TV_Size = Sample_Size_F(Sofa_TV_S, Ai)
            Sofa_TV = pla_f(ST_e, Livi, Sofa_TV_Size, 'Sofa_TV', L_con)
            if Sofa_TV:
                Sofa, TV = Pla_Sofa_TV(Livi_c, Sofa_TV)
                L_furniture.append(Sofa)
                L_furniture.append(TV)
    else:
        Sofa_TV_Size = Sample_Size_F(Sofa_TV_S, Ai)
        Sofa_TV = pla_f(2, Livi, Sofa_TV_Size, 'Sofa_TV', L_con)
        add_obstacle(L_con, Sofa_TV)
        Sofa, TV = Pla_Sofa_TV(Livi_c, Sofa_TV)
        L_furniture.append(Sofa)
        L_furniture.append(TV)
        if Ta_e > 0:
            Dinner_T_Size = Sample_Size_F(Dinner_T_S, Ai)
            far_X, far_Y = Sam_far_XY(5, Ai)
            Dinner_T = pla_f(Ta_e, Livi, Dinner_T_Size, 'Dinner_Table', L_con, far_X=far_X, far_Y=far_Y)
            if Dinner_T:
                Dinner_Cs = Pla_Din_Cs(Dinner_T, Livi, Doors)
                if Dinner_Cs:
                    add_obstacle(L_con, Dinner_T)
                    L_furniture.append(Dinner_T)
                    for Dinner_C in Dinner_Cs:
                        add_obstacle(L_con, Dinner_C)
                        L_furniture.append(Dinner_C)
    return L_furniture


def PLF_K(fur_K, Kitc, Toil, K_con, K_A0=K_A0, K_A1=K_A1):
    [CB_e,Re_e, TB_e, WM_e] = fur_K
    K_furniture = []
    Ai = Cal_Ai(Kitc, Toil, K_A0, K_A1)
    Kitc_Stove_Size = Sample_Size_F(Kitchen_S_S, Ai)
    Kitc_Stove = pla_f(2, Kitc, Kitc_Stove_Size, 'Kitchen_Stove', K_con)
    add_obstacle(K_con, Kitc_Stove)
    K_furniture.append(Kitc_Stove)
    if CB_e > 0:
        Cupboard_Size = Sample_Size_F(Cupboard_S, Ai)
        Cupboard = pla_f(CB_e, Kitc, Cupboard_Size, 'Cupboard', K_con)
        if Cupboard:
            add_obstacle(K_con, Cupboard)
            K_furniture.append(Cupboard)
    if Re_e > 0:
        Fridge = pla_f(Re_e, Kitc, Fridge_S, 'Refrigerator', K_con)
        if Fridge:
            add_obstacle(K_con, Fridge)
            K_furniture.append(Fridge)
    if WM_e > 0:
        Washer = pla_f(WM_e, Kitc, Washer_S, 'Wash_Machine', K_con)
        if Washer:
            add_obstacle(K_con, Washer)
            K_furniture.append(Washer)
    if TB_e > 0:
        T_Bin_Size = Sample_Size_F(T_Bin_S, Ai)
        T_Bin = pla_f(TB_e, Kitc, T_Bin_Size, 'Trash_Bin', K_con)
        if T_Bin: K_furniture.append(T_Bin)
    return K_furniture