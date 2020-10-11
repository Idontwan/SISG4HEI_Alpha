import numpy as np


D_H, H_M = 24, 60
D_M = D_H*H_M
Bre_Lun_bound = 9.5
balance_min = ((D_H/2)-Bre_Lun_bound)*H_M


def sample(I_Weights, t=0):
    N = len(I_Weights)
    if not t: t = np.random.rand()
    for i in range(N):
        if t < I_Weights[i]: return i


def Mval2TranP(Moti_value, Act2Moti_Map):
    N = len(Act2Moti_Map)
    TranPossI = []
    for i in range(N):
        num_l = Act2Moti_Map[i]
        P = 0
        for v in num_l:
            P += np.exp(Moti_value[v])
        TranPossI.append(P)
    for i in range(N-1):
        TranPossI[i+1] += TranPossI[i]
    TranPossI = [TranPossI[i]/TranPossI[-1] for i in range(N)]
    return TranPossI


def is_lundin(abs_mins):
    # determine whether this meal is lunch or dinner (not breakfast)
    return (abs_mins+balance_min)//(D_M//2)%2


def oft_order(oft_days):
    rs = np.random.rand(5)
    node2oft = {}
    nodes = ['3', '4', '7', '8', '9']
    for i in range(5):
        node2oft[nodes[i]] = oft_days[i] + rs[i]/5
    sort_nodes = sorted(nodes, key=lambda node:node2oft[node])
    orderednodes = [int(n) for n in sort_nodes]
    return orderednodes, node2oft


def gen_subtxt(absminu, act, dur):
    day, left_minu = int(absminu//D_M), absminu%D_M
    PorA = 'AM' if left_minu<D_M//2 else 'PM'
    hour, minu = int(left_minu//H_M), int(left_minu%H_M)
    if PorA == 'PM': hour -= int(D_H//2)
    second = int(60*((left_minu%H_M)-minu))
    d_hour, d_minu = int(dur//H_M), int(dur%H_M)
    d_second = int(60*((dur%H_M)-d_minu))
    txt1 = str(day)+'d '+PorA+' '+str(hour)+'h '+str(minu)+'m '+str(second)+'s'
    txt2 = act
    txt3 = str(d_hour)+'h '+str(d_minu)+'m '+str(d_second)+'s'
    txt_l = [txt1, txt2, txt3, '\n']
    return '   '.join(txt_l)