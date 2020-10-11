import numpy.random as rd


Pass_Way = 60


def Cut(strings0, strings1, yD):
    # strings0 has 1 string and strings1 has 2 or string0 2, string1
    interL = [[0, 0], [0, 0]]
    if strings1 != []:
        [p00, p01], [p10, p11] = strings0.pop(0), strings1.pop(0)
        if p01[yD] <= p10[yD] or p00[yD] >= p11[yD]:
            strings0.append([p00, p01])
            strings1.append([p10, p11])
            [p00, p01], [p10, p11] = strings0.pop(0), strings1.pop(0)
        if p00[yD] < p10[yD] < p01[yD] or p00[yD] < p11[yD] < p01[yD] or \
                p10[yD] < p00[yD] < p11[yD] or p10[yD] < p01[yD] < p11[yD]:
            if p10[yD] > p00[yD]:
                strings0.append([p00, p10])
                interL[0] = p10
            if p10[yD] < p00[yD]:
                strings1.append([p10, p00])
                interL[0] = p00
            if p11[yD] < p01[yD]:
                strings0.append([p11, p01])
                interL[1] = p11
            if p11[yD] > p01[yD]:
                strings1.append([p01, p11])
                interL[1] = p01
            if p00[yD] == p10[yD]: interL[0] = p00
            if p01[yD] == p11[yD]: interL[1] = p01
        elif p00[yD] != p10[yD] or p01[yD] != p11[yD]:
            strings0.append([p00, p01])
            strings1.append([p10, p11])
        else: interL = [p00, p01]
    return interL


def Con(strings0, strings1, yD):
    N = len(strings0[0])
    if N > 0:
        [p10, p11] = strings1.pop(0)
        string0 = strings0.pop(0)
        if N == 2:
            [p00, p01] = string0
        else:
            [p, p00, p01] = string0
        if p01[yD] == p10[yD]:
            strings0.append([])
            if N == 2:
                strings1.append([p00, p10, p11])
            else:
                strings1.append([p, p00, p10, p11])
        else:
            strings1.append([p10, p11])
            strings0.append(string0)


def sample(n_list, T=None):
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


def rect_com(type, B_L, B_W, K_W, L_L, L_W):
    # Room = [x, y, L, W]
    Bedroom = [-B_L//2, -B_W//2, B_L, B_W, 'Bedroom']
    Kitchen, Livingroom = [0, 0, 0, 0, 'Kitchen'], [0, 0, 0, 0, 'Livingroom']
    if type == 0:
        Kitchen = [-B_L//2, B_W//2, B_L, K_W, 'Kitchen']
    elif type == 1:
        Livingroom = [-B_L//2, B_W//2, B_L, L_W, 'Livingroom']
    elif type == 2:
        Kitchen = [-B_L//2, B_W//2, B_L, K_W, 'Kitchen']
        Livingroom = [-B_L//2, B_W//2+K_W, B_L, L_W, 'Livingroom']
    elif type == 3:
        Livingroom = [-B_L//2, B_W//2, B_L, L_W, 'Livingroom']
        Kitchen = [-B_L//2, B_W//2+L_W, B_L, K_W, 'Kitchen']
    elif type == 4:
        Kitchen = [-B_L//2, B_W//2, B_L, K_W, 'Kitchen']
        Livingroom = [B_L//2, B_W//2+K_W-L_W, L_L, L_W, 'Livingroom']
    else:
        Kitchen = [-B_L//2, B_W//2, B_L, K_W, 'Kitchen']
        Livingroom = [B_L//2, -B_W//2, L_L, L_W, 'Livingroom']
    return Bedroom, Kitchen, Livingroom


def who_con(type, ToB_x, ToB_y, B_x, B_y, K_y, L_y):
    if type < 4:
        if ToB_y < -B_y:
            return 'Bedroom'
        elif type == 0:
            return 'Kitchen'
        elif type == 1:
            return 'Livingroom'
        elif type == 2:
            return 'Livingroom' if ToB_y >= L_y else 'Kitchen'
        else:
            return 'Kitchen' if ToB_y >= K_y else 'Livingroom'
    else:
        if ToB_x < -B_x:
            return 'Bedroom' if ToB_y < -B_y else 'Kitchen'
        else:
            return 'Livingroom'


def cut_add(type, is_y, T_B_in, T_con, B_con, K_cut, L_add, Ba_y,
            Kitchen, Livingroom, To_W=120):
    [K_x, K_y, K_L, K_W, _] = Kitchen
    [L_x, L_y, L_L, L_W, _] = Livingroom
    t_l = rd.randint(0, 2, size=2)
    if K_cut == True:
        K_L -= To_W
        if type < 4:
            if not T_B_in and T_con=='Kitchen':
                K_x += To_W
            else:
                if t_l[0]: K_x += To_W
        else:
            K_x += To_W
    if L_add == True:
        if type < 4:
            L_L += To_W
            if (T_con == 'Livingroom' or B_con == 'Livingroom') and (T_B_in or (not is_y)):
                L_x -= To_W
            else:
                if t_l[1]: L_x -= To_W
        else:
            L_W += To_W
            if (T_con == 'Livingroom' or B_con == 'Livingroom') and T_B_in and (not is_y):
                if Ba_y > L_y: L_y -= To_W
            else:
                if t_l[1]: L_y -= To_W
    Kitchen = [K_x, K_y, K_L, K_W, 'Kitchen']
    Livingroom = [L_x, L_y, L_L, L_W, 'Livingroom']
    return Kitchen, Livingroom


def add_obs_area(X_con, interL, W=Pass_Way//2):
    if interL != [[0, 0], [0, 0]]:
        [[p00, p01], [p10, p11]] = interL
        if p00 == p10: X_con.append([[p00-W, p01],[p10+W, p11]])
        elif p01 == p11: X_con.append([[p00, p01-W],[p10, p11+W]])


def origin_bounds(Bedr, Kitc, Livi, Toil, Bath):
    house = [Bedr, Kitc, Livi, Toil, Bath]
    x_y_lims, bounds = [], []
    for room in house:
        [x, y, L, W, _] = room
        x_y_lim = [[x, x+L], [y, y+W]]
        bound = [[[[x, y], [x, y+W]]], [[[x+L, y], [x+L, y+W]]], [[[x, y], [x+L, y]]],
                 [[[x, y+W], [x+L, y+W]]]]
        x_y_lims.append(x_y_lim)
        bounds.append(bound)
    return x_y_lims, bounds


def Cut_TB_R(x_y_lims, bounds, is_T):
    interLs = []
    x0, y0 = bounds[4 - is_T][0][0][0][0], bounds[4 - is_T][0][0][0][1]
    x1, y1 = bounds[4 - is_T][-1][-1][-1][0], bounds[4 - is_T][-1][-1][-1][1]
    for I in range(3):
        for j in range(2):
            for k in range(2):
                for t in range(2):
                    if x_y_lims[4-is_T][j][k] == x_y_lims[I][j][t]:
                        interL = Cut(bounds[I][2 * j + t], bounds[4 - is_T][2 * j + k], 1 - j)
                        bounds[4-is_T] = [[[[x0, y0], [x0, y1]]], [[[x1, y0], [x1, y1]]], [[[x0, y0], [x1, y0]]],
                                            [[[x0, y1], [x1, y1]]]]
                        interLs.append(interL)
    return interLs


def Con_R_R(x_y_lims, bounds, R0, R1, i):
    for j in range(2):
        if x_y_lims[R0][i][j] == x_y_lims[R1][i][j]:
            if bounds[R0][2*i+j] != [] and bounds[R1][2*i+j] != []:
                Con(bounds[R0][2*i+j], bounds[R1][2*i+j], 1-i)


def wall_and_Obs(x_y_lims, bounds, type):
    Be_con, Ki_con, Li_con = [], [], []
    interLs_T = Cut_TB_R(x_y_lims, bounds, 1)
    interLs_B = Cut_TB_R(x_y_lims, bounds, 0)

    if type == 1 or type == 3:
        interL = Cut(bounds[0][3], bounds[2][2], 0)
        add_obs_area(Be_con, interL)
        add_obs_area(Li_con, interL)
        if type == 3:
            interL = Cut(bounds[2][3], bounds[1][2], 0)
            add_obs_area(Li_con, interL)
            add_obs_area(Ki_con, interL)
    else:
        interL = Cut(bounds[0][3], bounds[1][2], 0)
        add_obs_area(Be_con, interL)
        add_obs_area(Ki_con, interL)
        if type == 2:
            interL = Cut(bounds[1][3], bounds[2][2], 0)
            add_obs_area(Ki_con, interL)
            add_obs_area(Li_con, interL)
        elif type > 3:
            interL = Cut(bounds[1][1], bounds[2][0], 1)
            add_obs_area(Ki_con, interL)
            add_obs_area(Li_con, interL)
            interL = Cut(bounds[0][1], bounds[2][0], 1)
            add_obs_area(Be_con, interL)
            add_obs_area(Li_con, interL)

    if type == 1 or type == 3:
        Con_R_R(x_y_lims, bounds, 0, 2, 0)
        if type == 3:
            Con_R_R(x_y_lims, bounds, 2, 1, 0)
    else:
        Con_R_R(x_y_lims, bounds, 0, 1, 0)
        if type == 2:
            Con_R_R(x_y_lims, bounds, 1, 2, 0)
        elif type > 3:
            Con_R_R(x_y_lims, bounds, 1, 2, 1)
            Con_R_R(x_y_lims, bounds, 0, 2, 1)
    return bounds[:-2], Be_con, Ki_con, Li_con


def Pla_Door(type, Bedr, Kitc, Livi, Toil, Bath, DW=60):
    Doors = []

    def Cal_W(length, is_mi=False, D_W=DW):
        if is_mi: length += D_W
        if length < 200:
            return (200-length)//10 + 3
        return (length-240)//30

    def ins_side(sp, ep, l0, l1, j_, i_, DW=DW, j1_= 6):
        if j1_ > 2: j1_ = j_
        if 119 < l0 < 181 or l0 > 269:
            Po_D_cen[j1_].append([[sp[0]+i_*DW, sp[1]+(1-i_)*DW], i_])
            W = Cal_W(l0)
            Weights[j1_].append(W)
        if 119 < l1 < 181 or l1 > 269:
            Po_D_cen[j_].append([[ep[0]-i_*DW, ep[1]-(1-i_)*DW], i_])
            W = Cal_W(l1)
            Weights[j_].append(W)

    def Cal_j1(T, j, i_, L):
        if L == 4: return 0
        elif i_ == 1: return 5-T
        elif T < 2: return 0
        elif T == 2: return j-1
        elif T == 3: return 0 if j==2 else 2
        else: return 0

    def ins_mild(p, j01, l0, l1, i_):
        if (59<l0<121 or l0>209) and (59<l1<121 or l1>209):
            Po_D_cen[j01].append([p, i_])
            W0 = Cal_W(l0, is_mi=True)
            W1 = Cal_W(l1, is_mi=True)
            Weights[j01].append(2*min(W0, W1))

    def Cal_C_W(l, j, i):
        L = len(l)
        i_ = i//2
        if L == 2:
            [p0, p1] = l
            leng = p1[1-i_] - p0[1-i_]
            ins_side(p0, p1, leng, leng, j, i_)
            Walls.append([p0, p1])
        elif L == 3:
            [p0, p1, p2] = l
            leng0, leng1 = p1[1-i_]-p0[1-i_], p2[1-i_]-p1[1-i_]
            j1 = Cal_j1(type, j, i_, L)
            ins_side(p0, p2, leng0, leng1, j, i_, j1_=j1)
            if [j, j1] == [1, 0]: j01 = 3
            elif [j, j1] == [2, 0]: j01 = 4
            else: j01 = 5
            ins_mild(p1, j01, leng0, leng1, i_)
            Walls.append([p0, p2])
        elif L == 4:
            [p0, p1, p2, p3] = l
            leng0, leng1, leng2 = p1[1]-p0[1], p2[1]-p1[1], p3[1]-p2[1]
            ins_side(p0, p3, leng0, leng2, j, 0, j1_=0)
            j01 = 3 if type == 2 else 4
            ins_mild(p1, j01, leng0, leng1, 0)
            ins_mild(p2, 5, leng1, leng2, 0)
            Walls.append([p0, p3])

    x_y_lims, bounds = origin_bounds(Bedr, Kitc, Livi, Toil, Bath)
    bounds, Be_con, Ki_con, Li_con = wall_and_Obs(x_y_lims, bounds, type)

    Po_D_cen = [[], [], [], [], [], []]
    # in B, K, L, BaK, BaL, KaL
    Weights = [[], [], [], [], [], []]
    Walls = []
    for i in range(4):
        for j in range(3):
            if bounds[j][i] != []:
                for l in bounds[j][i]:
                    Cal_C_W(l, j, i)

    Choices = []
    for i in range(6):
        Choices.append(sum(Weights[i]))

    I = sample(Choices)
    J = sample(Weights[I])
    [x, y], i_ = Po_D_cen[I][J][0], Po_D_cen[I][J][1]
    if i_ == 1:
        Door = [x - DW // 2, y, DW, 0, 'Entrance']
    else:
        Door = [x, y - DW // 2, 0, DW, 'Entrance']
    Doors.append(Door)
    Do_obs = [[x - DW, y - DW], [x + DW, y + DW]]
    if I == 0:
        Be_con.append(Do_obs)
    elif I == 1:
        Ki_con.append(Do_obs)
    elif I == 2:
        Li_con.append(Do_obs)
    elif I == 3:
        Be_con.append(Do_obs)
        Ki_con.append(Do_obs)
    elif I == 4:
        Be_con.append(Do_obs)
        Li_con.append(Do_obs)
    elif I == 5:
        Ki_con.append(Do_obs)
        Li_con.append(Do_obs)

    F_Walls = []
    for wall in Walls:
        if wall != [[0,0],[0,0]]: F_Walls.append(wall)
    return Doors, F_Walls, Be_con, Ki_con, Li_con


def add_TB_obs(Be_con, Ki_con, Li_con, Toil, Bath, T_con, B_con, W=Pass_Way):
    To_temp = [[Toil[0]-W, Toil[1]-W], [Toil[0]+Toil[2]+W, Toil[1]+Toil[3]+W]]
    Ba_temp = [[Bath[0]-W, Bath[1]-W], [Bath[0]+Bath[2]+W, Bath[1]+Bath[3]+W]]

    if T_con == 'Livingroom':
        Li_con.append(To_temp)
    else:
        Ki_con.append(To_temp)
    if B_con == 'Livingroom':
        Li_con.append(Ba_temp)
    else:
        Be_con.append(Ba_temp)
    return Be_con, Ki_con, Li_con


def TB_Door(Bedr, Kitc, Livi, Toil, Bath, T_con, B_con, TB_W=120, DW=60):
    Bedr_C = [Bedr[0]+Bedr[2]//2, Bedr[1]+Bedr[3]//2]
    Kitc_C = [Kitc[0]+Kitc[2]//2, Kitc[1]+Kitc[3]//2]
    Livi_C = [Livi[0]+Livi[2]//2, Livi[1]+Livi[3]//2]
    T_R_C = Livi_C if T_con == 'Livingroom' else Kitc_C
    B_R_C = Livi_C if B_con == 'Livingroom' else Bedr_C
    if Toil[2] == TB_W:
        T_Door = [Toil[0], Toil[1]+Toil[3]//2-DW//2, 0, DW, 'Toilet_Door'] if T_R_C[0] < Toil[0] \
            else [Toil[0]+Toil[2], Toil[1]+Toil[3]//2-DW//2, 0, DW, 'Toilet_Door']
        B_Door = [Bath[0], Bath[1]+Bath[3]//2-DW//2, 0, DW, 'Bathroom_Door'] if B_R_C[0] < Bath[0] \
            else [Bath[0]+Bath[2], Bath[1]+Bath[3]//2-DW//2, 0, DW, 'Bathroom_Door']
    elif Toil[3] == TB_W:
        T_Door = [Toil[0]+Toil[2]//2-DW//2, Toil[1], DW, 0, 'Toilet_Door'] if T_R_C[1] < Toil[1] \
            else [Toil[0]+Toil[2]//2-DW//2, Toil[1]+Toil[3], DW, 0, 'Toilet_Door']
        B_Door = [Bath[0]+Bath[2]//2-DW//2, Bath[1], DW, 0, 'Bathroom_Door'] if B_R_C[1] < Bath[1] \
            else [Bath[0]+Bath[2]//2-DW//2, Bath[1]+Bath[3], DW, 0, 'Bathroom_Door']
    return T_Door, B_Door