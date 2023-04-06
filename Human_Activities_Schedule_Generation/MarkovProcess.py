import numpy as np


import Tools as Tl
import MvUpdate as MvU

'''
MD2D = [[0], [2, 1, 2], [3, 4, 5, 6], [7, 8, 15],
            [8, 9, 8], [10], [11], [12], [13], [14], [15], [16]]
    #[ 0 Sleep_Noon, Sleep_Evening, Wash_Self(in Bathroom), Cooking0(in KS), Cooking1(in CB),
    #  5 Cooking2(in RFA), Eat, Bath, Dress_up, Go_out,
    #  10 Toilet_Short, Toilet_Long, Clean, Work, Watch_TV,
    #  15 Wash_Clothing(in WM), Wandering]
'''

Norm_EXP = 10.
Norm_IntVal = 10000.
N_Times = Norm_IntVal/Norm_EXP
D_H, H_M = 24, 60
D_M = D_H*H_M
eat_toil_lag = 2.5*60
bath_wash_lag = 1*60


def Markchain(start_absminu, start_node, MVs, Node2Act, weights, ReDurs,
              lags=[[False, -1],[False, -1]], MVlog=False, update_Days=30):
    # lags for toilet_L and Washing

    if MVlog:
        MVlog = []
        for i in range(len(MVs)):
            MVlog.append([MVs[i]])

    Markchains = [[start_node, start_absminu]]
    absminu = Markchains[-1][-1]

    while absminu < update_Days*D_M:
        act_code = Markchains[-1][0]
        act_dur = 5+15*np.random.rand() if act_code==len(MVs)-1 else ReDurs[act_code]
        duration = Sample_duration(act_code, Node2Act, act_dur)
        updateMV(MVs, lags, absminu, act_code, weights, Node2Act, ReDurs, act_dur, duration)

        if lags[0][1] <= 0: lags[0][0] = False
        if lags[1][1] <= 0: lags[1][0] = False

        act_code = sample_next_actcode(MVs)
        absminu += duration
        if act_code!= Markchains[-1][0]:
            Markchains.append([act_code, absminu])

            if MVlog:
                for i in range(len(MVs)):
                    MVlog[i].append(MVs[i])
    if MVlog: return MVlog, Markchains

    return Markchains


def Sample_duration(act_code, ReMD2D, act_dur):
    act = ReMD2D[act_code]
    rt = np.random.rand()
    if act == [2, 1, 2]: w = 0.97+0.06*rt
    elif act == [8, 9, 8]: w = 0.4 + 0.5*rt
    elif act == [13] or act == [14]: w = 0.3 + 0.4*rt
    else: w = 0.95+0.1*rt
    return w*act_dur


def updateMV(MVs, lags, absminu, actcode, weights, ReMD2D, ReDurs, act_dur, redur):
    if ReMD2D[0] == [0]: Tol_l_code = 6
    else: Tol_l_code = 5
    N = len(MVs) - 1
    act = ReMD2D[actcode]
    if act == [0] or act == [2, 1, 2]: # sleep
        for i in range(N):
            if i == actcode: MVs[i] = MvU.norm_decrese(MVs[i], act_dur, redur)
            elif ReMD2D[i] == [0] or ReMD2D[i] == [2, 1, 2]:
                MVs[i] = MvU.daytimeinc(MVs[i], redur, weights[i])
            elif i== Tol_l_code-1 or 6 in ReMD2D[i]:
                MVs[i] = MvU.sleeptimeinc(MVs[i], redur, weights[i])
            elif i == Tol_l_code:
                if lags[0][0]: MVs[i], lags[0][1] = MvU.lag(MVs[i], weights[i], redur, lags[0][1])
            elif ReMD2D[i] == [15]:
                if lags[1][0]: MVs[i], lags[1][1] = MvU.lag(MVs[i], weights[i], redur, lags[1][1])
    elif 6 in act: # eat
        for i in range(N):
            if i == actcode: MVs[i] = MvU.eat_hungry(absminu, MVs[i])
            elif i == Tol_l_code:
                lags[0][0], lags[0][1] = True, eat_toil_lag
            elif ReMD2D[i] == [15]:
                if lags[1][0]: MVs[i], lags[1][1] = MvU.lag(MVs[i], weights[i], redur, lags[1][1])
            else: MVs[i] = MvU.daytimeinc(MVs[i], redur, weights[i])
    elif actcode == Tol_l_code - 3: # bath
        for i in range(N):
            if i == actcode: MVs[i] = MvU.norm_decrese(MVs[i], act_dur, redur)
            elif ReMD2D[i] == [15]:
                lags[1][0], lags[1][1] = True, bath_wash_lag
            elif i == Tol_l_code:
                if lags[0][0]: MVs[i], lags[0][1] = MvU.lag(MVs[i], weights[i], redur, lags[0][1])
            else: MVs[i] = MvU.daytimeinc(MVs[i], redur, weights[i])
    elif act == [8, 9, 8]: # go_out
        eat_code = actcode - 2
        hun_v, toiL_v, toL_lag, remins = MvU.goout_eat_toilL_value(absminu, redur, MVs[eat_code], ReDurs[eat_code],
                                                                   weights[eat_code], MVs[Tol_l_code], weights[Tol_l_code],
                                                                   ReDurs[Tol_l_code], toL_lag=lags[0][0],
                                                                   remain_minu=lags[0][1])
        for i in range(N):
            if i == actcode: MVs[i] = MvU.norm_decrese(MVs[i], act_dur, redur)
            elif i == eat_code: MVs[i] = hun_v
            elif i == Tol_l_code: MVs[i], lags[0][0], lags[0][1] = toiL_v, toL_lag, remins
            elif i == Tol_l_code-1: MVs[i] = MvU.goout_toilS_val(MVs[i], redur, ReDurs[i], weights[i])
            elif ReMD2D[i] == [15]:
                if lags[1][0]: MVs[i], lags[1][1] = MvU.lag(MVs[i], weights[i], redur, lags[1][1])
            else: MVs[i] = MvU.daytimeinc(MVs[i], redur, weights[i])
    elif actcode == Tol_l_code: # Toilet(long)
        for i in range(N):
            if i == actcode:
                MVs[i] -= Norm_IntVal
                if lags[0][0]: MVs[i], lags[0][1] = MvU.lag(MVs[i], weights[i], redur, lags[0][1])
            elif ReMD2D[i] == [15]:
                if lags[1][0]: MVs[i], lags[1][1] = MvU.lag(MVs[i], weights[i], redur, lags[1][1])
            else: MVs[i] = MvU.daytimeinc(MVs[i], redur, weights[i])
    elif act == [15]: # washing
        for i in range(N):
            if i == actcode:
                MVs[i] -= Norm_IntVal
                if lags[1][0]: MVs[i], lags[1][1] = MvU.lag(MVs[i], weights[i], redur, lags[1][1])
            elif i == Tol_l_code:
                if lags[0][0]: MVs[i], lags[0][1] = MvU.lag(MVs[i], weights[i], redur, lags[0][1])
            else: MVs[i] = MvU.daytimeinc(MVs[i], redur, weights[i])
    else:
        for i in range(N):
            if i == actcode: MVs[i] = MvU.norm_decrese(MVs[i], act_dur, redur)
            elif i == Tol_l_code:
                if lags[0][0]: MVs[i], lags[0][1] = MvU.lag(MVs[i], weights[i], redur, lags[0][1])
            elif ReMD2D[i] == [15]:
                if lags[1][0]: MVs[i], lags[1][1] = MvU.lag(MVs[i], weights[i], redur, lags[1][1])
            else: MVs[i] = MvU.daytimeinc(MVs[i], redur, weights[i])


def sample_next_actcode(MVs):
    N = len(MVs)
    expweights = []
    for i in range(N):
        expwei = np.exp(MVs[i]/N_Times-9.8) if MVs[i]/N_Times > 9.8 else 0
        expweights.append(expwei)
    sum_expwei = sum(expweights)
    possIs = []
    for i in range(N):
        possI = sum(expweights[0:i+1])/sum_expwei
        possIs.append(possI)
    actcode = Tl.sample(possIs)
    return actcode