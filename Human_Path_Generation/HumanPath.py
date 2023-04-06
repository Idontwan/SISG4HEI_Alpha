import math as ma
import random as rd


edge, g_L, g_W = 50, 5, 5


def node2xy(I, J, X0, Y0):
    return X0+g_L/2+I*g_L, Y0+g_W/2+J*g_W


def O_dist(I, J):
    return ma.sqrt((I*g_L)**2+(J*g_W)**2)


def cal_an_dif(n_ang, o_ang):
    [n_I, n_J], [o_I, o_J] = n_ang, o_ang
    angl1 = ma.atan2(n_J, n_I)
    angl0 = ma.atan2(o_J, o_I)
    return min(abs(angl1-angl0), 2*ma.pi-abs(angl1-angl0))


def cal_an_val(an_diff):
    if an_diff > 3/4*ma.pi: return 200
    if an_diff > ma.pi/4: return 75
    if an_diff > ma.pi/12: return (180*an_diff/ma.pi)**2/45
    return (180*an_diff/ma.pi)/3


def orig_dist(Distances, Discom, O_node):
    # weighted-distance to objection of selective nodes
    Wd = {}
    [I, J] = O_node
    O_discom = Discom[I][J]
    M, N = Distances.shape
    for ii in range(-14, 15):
        for jj in range(-14, 15):
            if (abs(ii)>6 or abs(jj)>6) and (-1<I+ii<M and -1<J+jj<N):
                ii_h, jj_h = ii//2, jj//2
                disc_mean = (O_discom+Discom[I+ii_h][J+jj_h]+Discom[I+ii][J+jj])/3
                Wd[(ii, jj)] = Distances[I+ii][J+jj] + disc_mean * O_dist(ii, jj)
    return Wd


def od_add_ang_len(Od, Slen, angle):
    for key in Od:
        (ii, jj) = key
        sslen = O_dist(ii, jj)
        len_value = (sslen-Slen)**2/4
        Od[key] += len_value
        if angle != None:
            an_dif = cal_an_dif([ii, jj], angle)
            an_value = cal_an_val(an_dif)
            Od[key] += an_value


def add_noise(Od):
    for key in Od:
        noise = 2*rd.random()
        Od[key] += noise


def next_step(distance, discomf, location, best_slen, angle, path, angles, max_dis):
    MWd = orig_dist(distance, discomf, location)
    od_add_ang_len(MWd, best_slen, angle)
    add_noise(MWd)
    n_key = min(MWd, key=MWd.get)
    (II, JJ) = n_key
    angle = [II, JJ]
    angles.append(ma.atan2(JJ, II))
    [I, J] = location
    I, J = I + II, J + JJ
    path.append([I, J])
    if len(path) > (max_dis/best_slen):
        return None, None, None
    return angle, I, J


def det_startends(type, destinations, start, ends, distances, max_diss):
    # start is not in ends
    spoints = destinations[start]
    if type == 'Direct':
        return spoints, distances[ends], None, max_diss[ends]
    if type == 'Pacing':
        return spoints, distances[ends], distances[start], max_diss[ends]
    dist_Es = []
    for end in ends:
        dist_E = distances[end]
        dist_Es.append(dist_E)
    dist_S = distances[start]
    dist_Es.append(dist_S)
    return spoints, dist_Es, None, max_diss[ends[0]]


def dire_pacing_path(SPoints, Best_Slen, Discom, Distance_E, max_dis, type='Direct', Distance_S=None, OneSP=False):
    # direct and pacing travel patterns
    # Best_Slen represent Best step length
    # OneSP determine whether SPoints is a list of points or a point.
    spoint = rd.choice(SPoints) if not OneSP else SPoints
    HPath, Angles = [spoint], []
    [I, J] = spoint
    angle = None
    if type == 'Pacing':
        HPaths, Angless = [], []
        Distances = [Distance_E, Distance_S]
        iss = 0
        for k in range(5):
            kk = rd.randint(4, 9)
            while kk>0 and Distances[iss][I][J] > 80:
                angle, I, J = next_step(Distances[iss], Discom, [I, J], Best_Slen, angle, HPath, Angles, max_dis)
                kk -= 1
            HPaths.append(HPath)
            Angless.append(Angles)
            HPath = [[I, J]]
            Angles = []
            angle = None
            iss = 1 - iss
        return HPaths, Angless
    while Distance_E[I][J] > 30:
        angle, I, J = next_step(Distance_E, Discom, [I, J], Best_Slen, angle, HPath, Angles, max_dis)
    return [HPath], [Angles]


def lap_rand_path(SPoints, Best_Slen, Discom, Distances, max_dis, type='Random'):
    # lapping and random travel patterns
    # one start and many Ends
    spoint = rd.choice(SPoints)
    HPath, Angles = [spoint], []
    [I, J] = spoint
    angle = None
    if type == 'Lapping':
        HPaths, Angless = [], []
        for cy in range(2):
            for Distance in Distances:
                n_step = rd.randint(3, 6)
                while n_step>0 and Distance[I][J] > 100:
                    angle, I, J = next_step(Distance, Discom, [I, J], Best_Slen, angle, HPath, Angles, max_dis)
                    n_step -= 1
                HPaths.append(HPath)
                Angless.append(Angles)
                HPath = [[I, J]]
                Angles = []
        return HPaths, Angless
    n_step = rd.randint(9, 15)
    Distance = Distances[0]
    while n_step>0 and Distance[I][J] > 50:
        angle, I, J = next_step(Distance, Discom, [I, J], Best_Slen, angle, HPath, Angles, max_dis)
        n_step -= 1
        rt, rj = rd.random(), rd.randint(3, 5)
        if rt < (1/rj): Distance = rd.choice(Distances)
    return [HPath], [Angles]


def footprint(Hpath, Angles, Best_Slen, PreferFoot):
    L_I, W_J = Best_Slen/6/g_L, Best_Slen/6/g_W
    Real_angs, Real_Bcs, footprints, An_diff = [], [], [[], []], []

    def calinstep(Body_c, angle_, flags):
        [I0, J0] = Body_c
        ang0_l, ang0_r = angle_+ma.pi/2, angle_-ma.pi/2
        I0_l, I0_r = I0+L_I*ma.cos(ang0_l), I0+L_I*ma.cos(ang0_r)
        J0_l, J0_r = J0+W_J*ma.sin(ang0_l), J0+W_J*ma.sin(ang0_r)
        Real_Bcs.append([I0, J0])
        Real_angs.append(angle_)
        if flags[0]: footprints[0].append([I0_l, J0_l])
        if flags[1]: footprints[1].append([I0_r, J0_r])

    N = len(Angles)
    for i in range(N-1):
        temp = abs(Angles[i+1]-Angles[i])
        ang_dif = min(temp, 2*ma.pi-temp)
        # by this way, ang_dif belongs to [0, 2*pi], but real delta angle may be ang_dif of -ang_dif
        An_diff.append(ang_dif)
    calinstep(Hpath[0], Angles[0], [1, 1])
    count = 1 if PreferFoot == 'right' else 0
    for i in range(N-1):
        if An_diff[i] < ma.pi/4:
            # the angel of direction of human body is the middle angle between Angles[i] and Angles[i+1]
            # But you can not let ang = (Angles[i]+Angles[i+1])/2 directly, because in this way, the result
            # may be the inverse direction of you wanted ang. (may be ang+pi or ang-pi)
            ang = Angles[i] + An_diff[i]/2 # for the case when real delta angle is ang_dif
            if abs(min(abs(ang-Angles[i+1]), 2*ma.pi-abs(ang-Angles[i+1]))-An_diff[i]/2) > 0.001:
                # min(abs(ang-Angles[i+1]), 2*ma.pi-abs(ang-Angles[i+1]) is the delta angle between (Angles[i]+ang_dif/2)
                # and the (Angles[i+1]), it may be ang_dif/2 of 3*ang_dif/2. It depends on real delta angle equal to
                # an_dif of -an_dif
                ang = Angles[i] - An_diff[i]/2 # for the case when real delta angle is -ang_dif
            m_c = count%2
            calinstep(Hpath[i+1], ang, [1-m_c, m_c])
            count += 1
        else:
            calinstep(Hpath[i+1], Angles[i], [1, 1])
            calinstep(Hpath[i+1], Angles[i+1], [1, 1])
    calinstep(Hpath[N], Angles[N-1], [1, 1])
    return Real_Bcs, footprints, Real_angs


def normal_bcfp(Hpaths, Angless, Best_Slen, lims, Preferfoot):
    # return real coordinate of body_center, left_foot, right_foot trajectory
    real_XYs = [[], [], []] #body_c, left_f, right_f
    X0, Y0 = lims[0][0]-edge, lims[1][0]-edge
    N, M = len(Hpaths), 0
    for i in range(N):
        Hpath, Angles = Hpaths[i], Angless[i]
        realbcs, footprints, realangs = footprint(Hpath, Angles, Best_Slen, Preferfoot)
        real_IJ = [realbcs, footprints[0], footprints[1]]
        for ii in range(3):
            for [I, J] in real_IJ[ii]:
                x, y = node2xy(I, J, X0, Y0)
                real_XYs[ii].append([round(x, 2), round(y, 2)])
        for j in range(len(realangs)):
            real_XYs[0][M].append(round(realangs[j], 3))
            M += 1
    return real_XYs[0], real_XYs[1], real_XYs[2] # real_XYs[1] include the angles