import os
from matplotlib import pyplot as plt
import Tools as Tl


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('/')]
upper_path = abs_path[:abs_path.rfind('/')]
data_path = upper_path+'/DataBase/'


D_H, H_M = 24, 60
D_M = D_H*H_M


Num2Act = ['Sleep', 'Sleep', 'Wash and Brush', 'Cook', 'Take TableWare', 'Take Food',
           'Eat', 'Bath', 'Dress up', 'Go out', 'Go to Toilet', 'Go to Toilet',
           'Clean', 'Read', 'Watch TV', 'Wash Clothes', 'Wander', 'Relax']


def creat_floder(path):
    if not os.path.exists(data_path+path): os.makedirs(data_path+path)


def Mark2Txt(ACTSEQ, path, stime, etime):
    N, Txt = 0, ''
    [node, absminu] = ACTSEQ[N]
    sminu, eminu = stime[0]*D_M+stime[1]+D_M, etime[0]*D_M+etime[1]+D_M
    while absminu < sminu:
        N += 1
        [node, absminu] = ACTSEQ[N]
    [fnode, _] = ACTSEQ[N-1]
    subtxt = Tl.gen_subtxt(sminu, Num2Act[fnode], absminu-sminu)
    Txt += subtxt
    while absminu < eminu:
        dur = ACTSEQ[N+1][1]-absminu if ACTSEQ[N+1][1]<eminu else eminu-absminu
        act = Num2Act[node]
        subtxt = Tl.gen_subtxt(absminu, act, dur)
        N += 1
        [node, absminu] = ACTSEQ[N]
        Txt += subtxt
    creat_floder(path)
    filename = data_path + path + '/ACTS.txt'
    with open(filename, "w") as f:
        f.write(Txt)
    return Txt


def process_seq(ActSeq, SDay, EDay):
    timess, timeIss, numss, time, n = [[]], [[]], [[]], 0, 0

    def write_data(t0, t1, no):
        # t0 is the start time of no, t1 is the end time of no
        timeIss[-1].append(t0/H_M)
        timess[-1].append((t1-t0)/H_M)
        numss[-1].append(no)

    absminu = ActSeq[n][1]
    while absminu < SDay*D_M:
        n += 1
        node, absminu = ActSeq[n-1][0], ActSeq[n][1]
    while absminu < EDay * D_M:
        minu = absminu % D_M
        if minu < time:
            write_data(time, D_M, node)
            timeIss.append([])
            timess.append([])
            numss.append([])
            time = 0
        else:
            write_data(time, minu, node)
            time = minu
            n += 1
            node, absminu = ActSeq[n-1][0], ActSeq[n][1]
    write_data(time, D_M, node)
    return timess, timeIss, numss


def save_actseq(path, times, acts, durs):
    Txt = ''
    for i in range(len(times)):
        subtxt = Tl.gen_subtxt(times[i], acts[i], durs[i])
        Txt += subtxt
    with open(path+'/ACTS.txt', "w") as f:
        f.write(Txt)