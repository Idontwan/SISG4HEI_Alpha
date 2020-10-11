import math as ma
import numpy.random as rd


B_A_min, B_A_max = 80000, 160000
K_A_min, K_A_max = 60000, 120000
L_A_min, L_A_max = 120000, 240000
len_step = 20


def bi_side(A_min, A_max, L_step, ratio=2):
    L_min, L_max = ma.sqrt(A_min), ma.sqrt(2 * A_max)
    i_min, i_max = int(L_min / L_step) + 1, int(L_max / L_step)
    i = rd.randint(i_min, i_max)
    j_min = int(max(i / ratio, A_min / i / L_step / L_step)) + 1
    j_max = int(min(i, A_max / i / L_step / L_step)) + 1
    j = rd.randint(j_min, j_max)
    return i*L_step, j*L_step

def si_side(A_min, A_max, L_step, L, kitchen=True, ratio=2, To_W=120):
    L_ = L - To_W if kitchen else L + To_W
    j_min = int(max(L/L_step/ratio, A_min/L/L_step)) + 1
    j_max = int(min(L/L_step*ratio, A_max/L/L_step))
    j_len = j_max - j_min if j_max > j_min else 0
    j_min_ = int(max(L_/L_step/ratio, A_min/L_/L_step)) + 1
    j_max_ = int(min(L_/L_step*ratio, A_max/L_/L_step))
    j_len_ = j_max_ - j_min_ if j_max_>j_min_ else 0
    t = rd.rand()
    if t < 0.7*j_len_/(0.7*j_len_+j_len):
    # increse the possibility of two zone has same length
        done = True
        j = rd.randint(j_min_, j_max_)
    else:
        done = False
        j = rd.randint(j_min, j_max)
    return j*L_step, done


def sizes_sample(topo, B_A_min, B_A_max, K_A_min, K_A_max, L_A_min, L_A_max, len_step, To_W=120):
    B_L_max = int(ma.sqrt(2* B_A_max)/len_step) * len_step - len_step
    B_L, B_W = bi_side(B_A_min, B_A_max, len_step)
    K_L, K_W, K_A, L_L, L_W, L_A = 0, 0, 0, 0, 0, 0

    K_cut, L_add = None, None
    B_A = B_L * B_W
    K_A_min = max(K_A_min, 0.6 * B_A)
    K_A_max = min(K_A_max, 0.9 * B_A)
    L_A_min = max(L_A_min, 1.2 * B_A)
    L_A_max = min(L_A_max, 1.8 * B_A)

    o_inds = [0.1, 0.15, 0.2, 0.3, 0.25] #[0: 10%, 1:15%, 2:20%, 3:30%, 4 or 5: 25%]
    inds = [o_inds[i]*topo[i] for i in range(5)]
    ind2k, ind2l = inds[0]+inds[2]+inds[4], inds[1]+inds[3]
    ind_sum = ind2k + ind2l
    t = rd.rand()
    se_is_K = True if t < (ind2k/ind_sum) else False # index0=(0+2+4)/all

    if not se_is_K:
        L_L = B_L
        L_W, L_add = si_side(L_A_min, L_A_max, len_step, L_L, kitchen=False)
        t = rd.rand()
        type = 1 if t < (inds[1]/ind2l) else 3 # index1=1/(1+3)
        if type == 3:
            K_L = B_L
            K_W, K_cut = si_side(K_A_min, K_A_max, len_step, K_L)

    else:
        K_L = B_L
        K_W, K_cut = si_side(K_A_min, K_A_max, len_step, K_L)
        t = rd.rand()
        if t < inds[0]/ind2k: type = 0 # index2=0/(0+2+4)
        elif t < (inds[0]+inds[2])/ind2k: # index3=(0+2)/(0+2+4)
            type = 2
            L_L = B_L
            L_W, L_add = si_side(L_A_min, L_A_max, len_step, L_L, kitchen=False)
        else:
            type = 4
            L_L, L_W = bi_side(L_A_min, L_A_max, len_step)
            t = rd.randint(0, 2)
            L_add = True if t else False
            if L_L > B_L_max or (L_L + To_W) >= 2 * L_W: L_add = False
            if (L_L + To_W) * L_W > L_A_max: L_add = False

    if K_cut: K_L -= To_W
    if L_add: L_L += To_W
    K_A, L_A = K_L * K_W, L_L * L_W
    if type == 4:
        if rd.randint(0, 2): type = 5
        temp = L_W
        L_W = L_L
        L_L = temp

    return type, [B_L, B_W], B_A, [K_L, K_W], K_A, [L_L, L_W], L_A \
            ,K_cut, L_add