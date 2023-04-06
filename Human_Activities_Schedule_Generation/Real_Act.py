Norm_IntVal = 10000.
D_H, H_M = 24, 60
D_M = D_H*H_M


def Mid_dur(durs, floorplancode, oft_Days, sleep_noon):
    MD2D = [[0], [2, 1, 2], [5, 3, 4, 6], [7, 8, 15],
            [8, 9, 8], [10], [11], [12], [13], [14], [15], [16]] #map Mid_dur to dur
    MDurs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 0 sleep_noon, sleep, eat, bath, go_out, toilet(short), toilet(long), clean, work,
    # 9 watch_TV, Washing, Wandering
    MDurs[1] = durs[1] + 2*durs[2] #Go_to_Bathroom->Sleep->Go_to_Bathroom
    if sleep_noon:
        MDurs[0] = durs[0]
        MDurs[1] -= durs[0]/2
        durs[1] -= durs[0]/2

    MDurs[2] = durs[6] #Cooking2->Cooking0->Cooking1->Dining
    if floorplancode[10] != '0':
        MDurs[2] += durs[3] + durs[4] + durs[5]
    else: MD2D[2] = [6]
    if floorplancode[12] == '0': MDurs[2] -= 0.1
    if floorplancode[14] == '0': MDurs[2] -= 0.1

    MDurs[3] = durs[7] + durs[8] #Go_to_Bathroom->Dress_up->Washing,
    if floorplancode[0] == '0': MDurs[3] -= 0.1 # once pass to WAR
    if floorplancode[17] != '0':
        MDurs[3] += durs[15] # time to wash cloth
        MDurs[10] = durs[15] # time to wash cloth
    else: MD2D[3] = [7, 8]

    MDurs[4] = durs[9] + 2*durs[8] #Dress_up->Go_out->Dress_up
    if floorplancode[0] == '0': MDurs[4] -= 0.2
    if floorplancode[3] == '0': MDurs[4] += oft_Days[1]*durs[13]/oft_Days[3]
    else: MDurs[8] += durs[13] # Work, Desk
    if floorplancode[5] == '0': MDurs[4] += oft_Days[1]*durs[14]/oft_Days[4]
    else: MDurs[9] += durs[14] # Watch_TV, Sofa

    for i in [5, 6, 7, 11]:
        MDurs[i] = durs[i+5]

    Tot_Sle_Dur = MDurs[0] + MDurs[1]
    return MDurs, Tot_Sle_Dur, MD2D


def Mid_weight(Mdurs, Tot_Sle_Dur, oftDays, Toi_shor_Times, eatT4TL, Twan):
    weights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 0 sleep_noon, sleep, eat, bath, go_out, toilet(short), toilet(long), clean, work,
    # 9 watch_TV, Washing, Wandering
    for i in range(2):
        if Mdurs[i] != 0: weights[i] = Norm_IntVal/(D_M-Mdurs[i])
    weights[2] = Norm_IntVal/(3*(D_M-0.9*Tot_Sle_Dur-3*Mdurs[2])/8)
    js = [3, 4, 7, 8, 9]
    for i in range(5):
        if Mdurs[js[i]] != 0:
            weights[js[i]] = Norm_IntVal/(oftDays[i]*(D_M-Tot_Sle_Dur) - Mdurs[js[i]])
    weights[5] = Toi_shor_Times*Norm_IntVal / (D_M - 0.9*Tot_Sle_Dur)
    weights[6] = Norm_IntVal / eatT4TL # each meal, the Motivation value increase weights[6]
    if Mdurs[10] != 0: weights[10] = Norm_IntVal # each bath, the Motivation value increase
    weights[11] = Norm_IntVal / (Twan*(D_M-Tot_Sle_Dur))
    return weights


def real_act_dur(Mdurs, weights, MD2D):
    ReMD2D, Redurs, Reweights = [], [], []
    N = len(Mdurs)
    for i in range(N):
        if Mdurs[i] != 0:
            Redurs.append(Mdurs[i])
            Reweights.append(weights[i])
            ReMD2D.append(MD2D[i])
    ReMD2D.append([17])
    return ReMD2D, Redurs, Reweights