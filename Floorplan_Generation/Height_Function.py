import random as rd


edge, g_L, g_W = 50, 5, 5


B_A0, B_A1 = 80000, 160000
K_A0, K_A1 = 60000, 120000
L_A0, L_A1 = 120000, 240000


FloorHeight = [280, 300, 320, 340]
Bed_H = [5, 30, 35, 40, 45, 50]
Poss_Hs = {'Wardrobe': [140, 155, 70], 'Nightstand': [45, 50, 55], 'Desk': [60, 65, 70], 'Chair': [40, 45],
           'Sofa': [40, 45], 'TV': [40, 45, 50, 55, 60, 65, 70], 'Dinner_Table': [60, 65, 70],
           'Kitchen_Stove': [75, 80, 85], 'Cupboard': [100, 105, 110, 115, 120], 'Refrigerator': [125, 145, 165],
           'Wash_Machine': [85], 'Trash_Bin': [30, 45, 60]}


Sofa_Plus_H = [[20, 25], [0, 20, 25, 30]]
TV_Sizes = [[40, 25], [50, 30], [70, 40], [90, 55], [110, 65]]
W_TV, W_Sofa = 10, 20


def floorH(House, type):
    Ps = [[0.5,0.8,1,1],[0.2,0.5,0.8,1],[0,0.2,0.5,1]]
    B_A = House[0][2] * House[0][3]
    B_A_i = (B_A-B_A0)/(B_A1-B_A0)
    if type == 0:
        K_A = House[1][2] * House[1][3]
        K_A_i = (K_A-K_A0)/(K_A1-K_A0)
        index = (B_A_i + K_A_i) / 2
    elif type == 1:
        L_A = House[1][2] * House[1][3]
        L_A_i = (L_A-L_A0)/(L_A1-L_A0)
        index = (B_A_i + L_A_i) / 2
    else:
        K_A = House[1][2] * House[1][3]
        K_A_i = (K_A-K_A0)/(K_A1-K_A0)
        L_A = House[2][2] * House[2][3]
        L_A_i = (L_A-L_A0)/(L_A1-L_A0)
        index = (B_A_i + K_A_i + L_A_i) / 3
    if index < 0.33: P = Ps[0]
    elif index < 0.66: P = Ps[1]
    else: P = Ps[2]
    rf = rd.random()
    for i in range(4):
        if P[i] > rf: return FloorHeight[i]


def fur_height(na, loca, arrs, has_nist):
    if na == 'Bed':
        if has_nist:
            f_height = rd.choice(Bed_H[1:])
        else:
            rj = rd.random()
            if rj < 0.35: f_height = Bed_H[0]
            else: f_height = rd.choice(Bed_H)
    else:
        f_height = rd.choice(Poss_Hs[na])
    arr = loca + [f_height]
    arrs.append(arr)
    return f_height


def Sample_TV_Size(L, W):
    LL = max(L, W)
    if LL == 60: return rd.choice(TV_Sizes[:2])
    if LL == 80: return rd.choice(TV_Sizes[:3])
    if LL == 100: return rd.choice(TV_Sizes[1:4])
    if LL == 120: return rd.choice(TV_Sizes[2:])


def Sofa_TV_height(S_T, arrs):
    Sofa = S_T['Sofa']
    TV = S_T['TV']
    [x0, y0, L0, W0, HSo] = Sofa
    [x1, y1, L1, W1, HT] = TV
    [L_TV, H_TV] = Sample_TV_Size(L1, W1)
    Sofa_H1 = HSo + rd.choice(Sofa_Plus_H[0])
    Sofa_H2 = Sofa_H1 + rd.choice(Sofa_Plus_H[1])
    TV_H3 = HT + H_TV
    S_c, TV_c = [x0+L0//2, y0+W0//2], [x1+L1//2, y1+W1//2]
    if S_c[0] == TV_c[0]:
        S_3_w_0 = [x0, y0, W_Sofa, W0, Sofa_H1]
        S_3_w_1 = [x0+L0-W_Sofa, y0, W_Sofa, W0, Sofa_H1]
        if S_c[1] > TV_c[1]:
            TV_3 = [x1+L1//2-L_TV//2, y1, L_TV, W_TV, TV_H3]
            S_3_r = [x0, y0+W0-W_Sofa, L0, W_Sofa, Sofa_H2]
        elif S_c[1] < TV_c[1]:
            TV_3 = [x1+L1//2-L_TV//2, y1+W1-W_TV, L_TV, W_TV, TV_H3]
            S_3_r = [x0, y0, L0, W_Sofa, Sofa_H2]
    elif S_c[1] == TV_c[1]:
        S_3_w_0 = [x0, y0, L0, W_Sofa, Sofa_H1]
        S_3_w_1 = [x0, y0+W0-W_Sofa, L0, W_Sofa, Sofa_H1]
        if S_c[0] > TV_c[0]:
            TV_3 = [x1, y1+W1//2-L_TV//2, W_TV, L_TV, TV_H3]
            S_3_r = [x0+L0-W_Sofa, y0, W_Sofa, W0, Sofa_H2]
        elif S_c[0] < TV_c[0]:
            TV_3 = [x1+L1-W_TV, y1+W1//2-L_TV//2, W_TV, L_TV, TV_H3]
            S_3_r = [x0, y0, W_Sofa, W0, Sofa_H2]
    arrs.append(S_3_r)
    arrs.append(S_3_w_0)
    arrs.append(S_3_w_1)
    rt = rd.randint(0, 1)
    if rt:
        arrs.pop(0)
        arrs.append(S_3_r)
    arrs.append(TV_3)


def furnitureH(f_H, House, T_B, Furnitures):
    Heights = {'0': f_H}
    Has_NS = 0
    Sofa_TV = {}
    if len(Furnitures[0]) > 1:
        if Furnitures[0][1][4] == 'Nightstand': Has_NS = 1
    height_1 = []
    for room in House:
        height_1.append(room[0:4])
    Heights['1'] = height_1
    height_2 = []
    height_3 = []
    for room in T_B:
        temp = room[0:4] + [f_H]
        height_2.append(temp)
    for room in Furnitures:
        for furni in room:
            name = furni[-1]
            temp = furni[0:4]
            fur_H = fur_height(name, temp, height_2, Has_NS)
            if name == 'Sofa' or name == 'TV':
                temp.append(fur_H)
                Sofa_TV[name] = temp
    Heights['2'] = height_2
    if Sofa_TV != {}:
        Sofa_TV_height(Sofa_TV, height_3)
    Heights['3'] = height_3
    return Heights