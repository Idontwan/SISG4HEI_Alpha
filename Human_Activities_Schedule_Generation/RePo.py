# Resident Profile
import numpy as np


import Tools as Tl


Norm_EXP = 10.
Norm_IntVal = 10000.
N_Times = Norm_IntVal/Norm_EXP
D_H, H_M = 24, 60
D_M = D_H*H_M


def sam_bas_dura(paraDoActFast, paraSleepDur, parasGRW):
    # unit minutes
    #[ 0 Sleep_Noon, Sleep_Evening, Wash_Self(in Bathroom), Cooking0(in KS), Cooking1(in CB),
    #  5 Cooking2(in RFA), Eat, Bath, Dress_up, Go_out,
    #  10 Toilet_Short, Toilet_Long, Clean, Work, Watch_TV,
    #  15 Wash_Clothing(in WM), Wandering]
    paras = [[15., 60.], [360., 180.], [3., 4.], [5., 10.], [0.5, 1.],
             [0.5, 0.5], [10., 20.], [5., 20.], [0.5, 3.5], [210., 180.],
             [0.6, 1.], [4., 16.], [10., 20.], [180., 150.], [120., 120.],
             [0.2, 0.8], [0.3, 0.4]]
    N = len(paras)
    rts = np.random.rand(N)
    t = 0.3 - 0.3*paraDoActFast
    for i in range(2, N-3):
        rts[i] = t + 0.7*rts[i]
    rts[1] = paraSleepDur
    rts[9], rts[13], rts[14] = parasGRW[0], parasGRW[1], parasGRW[2]
    Durs = np.zeros(N)
    for i in range(N):
        Durs[i] = 0.1 + paras[i][0] + paras[i][1]*rts[i] #0.1min is passing time
    return Durs


def sam_fres(fresTandW, orders):
    # Determining how often the resident bath/ go out/ clean/ work/ watch_TV
    Oft_Days = [1, 1, 1, 1, 1]
    AddDay_num1 = Tl.sample([0.2, 0.8, 1]) + 2
    for i in range(AddDay_num1): Oft_Days[i] += 1
    AddDay_num2 = Tl.sample([0.2, 0.8, 1])
    for i in range(AddDay_num2): Oft_Days[i] += 1
    if np.random.rand() < 0.5: Oft_Days[0] += 1 + Tl.sample([0.1, 0.3, 0.7, 0.9, 1])
    n_Oft_Days = [Oft_Days[4-orders.index(i)] for i in range(5)]
    # Determining how many times the resident go toilet(short) every day
    Toi_shor_Times = Tl.sample([0.15, 0.45, 0.75, 0.95, 1], fresTandW[0]) + 3
    # Determining how many times the resident eat between go toilet(long)
    eatT4TL = 1/(0.07 + 0.28*fresTandW[0])
    # Determing how often the resident wander
    exp_Twan = 4.5 * (1-fresTandW[1]) - 1.1
    Twan = np.exp(exp_Twan)
    return n_Oft_Days, Toi_shor_Times, eatT4TL, Twan



