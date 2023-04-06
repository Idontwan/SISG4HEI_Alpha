import numpy as np


import Tools as Tl


Norm_IntVal = 10000.
D_H, H_M = 24, 60
D_M = D_H*H_M


def origin_MVs_minu(weights, MDurs, Oft_days, Tot_sle_dur, eatT4TL):
    # determining origin_MVs by determining when will them first time be happened
    O_Mvs = [0, Norm_IntVal, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 0 sleep_noon, sleep, eat, bath, go_out, toilet(short), toilet(long), clean, work,
    # 9 watch_TV, Washing, Wandering
    if weights[0] != 0: # sleep_noon after 11 to 15 hours after sleep_evening
        O_Mvs[0] = Norm_IntVal - (11+4*np.random.rand())*60*weights[0]
    O_Mvs[2] = Norm_IntVal - (0.1*MDurs[1]+15+30*np.random.rand())*weights[2]

    ord_nodes, n2oft = Tl.oft_order(Oft_days)
    minus_0 = MDurs[2] + 15 + 60*np.random.rand()
    O_Mvs[5] = Norm_IntVal - (0.1*MDurs[1]+minus_0)*weights[5]
    for node in ord_nodes:
        if weights[node] != 0:
            O_Mvs[node] = Norm_IntVal - minus_0*weights[node]
            minus_0 = minus_0 + (int(n2oft[str(node)])*(D_M-Tot_sle_dur)-minus_0)*np.random.rand()

    N = int(eatT4TL)
    O_Mvs[6] = weights[6]*np.random.randint(N)
    O_Mvs[11] = Norm_IntVal/3*np.random.rand()
    if weights[10] != 0: O_Mvs[10] = 0.02*Norm_IntVal

    start_minus = H_M - 3.5*H_M*np.random.rand()
    Mvs, NN = [], len(weights)
    for i in range(NN):
        if weights[i] != 0: Mvs.append(O_Mvs[i])
    Mvs.append(1.02*Norm_IntVal)
    return Mvs, start_minus