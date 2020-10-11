import json, os
import random as rd
import numpy as np


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('/')]
envi_path = abs_path + '/DataBase/'


D_H, H_M = 24, 60
D_M = D_H*H_M


def search(varvals, Ranges):
    def mulitpy(l0, l1):
        lmul = []
        for l in l0:
            for ll in l1: lmul.append(l+ll)
        return lmul

    def recur(ls):
        if len(ls) == 1: return ls[0]
        else: return mulitpy(ls[0], recur(ls[1:]))

    Topo_choice = []
    for i in range(5):
        if varvals[i]==2: Topo_choice.append(str(i)+'/')
    fur_vals = varvals[5:7] + varvals[12:14] + varvals[7:12]
    Fur_choice = [['WAR', '000'], ['De', '00'], ['So', '00'], ['DTA', '000'], ['KS', '00'],
                  ['CB', '00'], ['RFA', '000'], ['WM', '00'], ['TB', '00']]
    for i in range(9):
        if fur_vals[i] == 2: Fur_choice[i].pop()
        elif fur_vals[i]==0: Fur_choice[i].pop(0)
    limstrs = Ranges[2:] + Ranges[:2]
    arealim = [10000*int(limstrs[i])+(-1)**(i+1)*100 for i in range(2, 10)]
    ratiolim = [float(limstrs[0])-0.01, float(limstrs[1])+0.01]
    midpaths = recur([Topo_choice]+Fur_choice)
    path_list = []
    for midpath in midpaths:
        if os.path.exists(envi_path+midpath):
            dirs = os.listdir(envi_path+midpath)
            for dir in dirs:
                if size_jude(dir, midpath[0], arealim, ratiolim): path_list.append(midpath+'/'+dir)
    return len(path_list), path_list


def size_jude(name, topo, arealim, ratiolim):
    me_list = name.split(',')[:-1]
    me_val = [int(me_list[i]) for i in range(len(me_list))]
    bedR_A = 100*me_val[0]
    H_AsRi = me_val[-1]/100
    if topo == '0':
        kitR_A, LivR_A = 100*me_val[1], (arealim[4]+arealim[5])/2
    elif topo == '1':
        kitR_A, LivR_A = (arealim[2]+arealim[3])/2, 100*me_val[1]
    else:
        kitR_A, LivR_A = 100*me_val[1], 100*me_val[2]
    THou_A = bedR_A + kitR_A + LivR_A + 32400
    Judes = [arealim[0]<bedR_A<arealim[1], arealim[2]<kitR_A<arealim[3], arealim[4]<LivR_A<arealim[5],
             arealim[6]<THou_A<arealim[7], ratiolim[0]<H_AsRi<ratiolim[1]]
    return Judes[0] and Judes[1] and Judes[2] and Judes[3] and Judes[4]


def Sample_element(e_l, p_l):
    N = len(e_l)
    Ps_L_ = [sum(p_l[:i+1]) for i in range(N)]
    Ps_l = [e/Ps_L_[-1] for e in Ps_L_]
    r =  rd.random()
    for i in range(N):
        if r< Ps_l[i]: return e_l[i]


def load_cont_sta():
    Js_Dicts = []
    for name in ['Content.json', 'Statistics.json']:
        file_name = envi_path + name
        with open(file_name, 'r') as f:
            Js_Dicts.append(json.load(f))
    return Js_Dicts[0], Js_Dicts[1]


def path_sample(content, statistic):
    h_v_l = list(content)
    h_v_p = [statistic[e] for e in h_v_l]
    h_v = Sample_element(h_v_l, h_v_p)
    dic0 = content[h_v]
    fname0_l = list(dic0)
    fname0_p = [statistic[e] for e in fname0_l]
    fname0 = Sample_element(fname0_l, fname0_p)
    li0 = dic0[fname0]
    fname1 = rd.choice(li0)
    return h_v, fname0, fname1


def fname2act(foldername0):
    acts = ['Go_out', 'Go_to_Toilet', 'Go_to_Bathroom', 'Sleep']
    fn2act = [[0,'Dress_up'], [3,'Work'], [5,'Watch_TV'],[7,'Dining'],[10,'Cooking0'],[12,'Cooking1'],
              [14,'Cooking2'],[17,'Washing'],[19,'Cleaning']]
    for i in range(9):
        if foldername0[fn2act[i][0]] != '0': acts.append(fn2act[i][1])
    return acts


def csv_sample(fname0):
    names = ['Discomfortable_value']
    acts = fname2act(fname0)
    for act in acts:
        name = act + '_distance'
        names.append(name)
    name = rd.choice(names)
    return name


def load_se_map(h_v, fname0, fname1):
    file_path = envi_path + h_v + '/' + fname0 + '/' + fname1
    file_name = file_path + '/Semantic.json'
    with open(file_name, 'r') as f:
        Js_Dict = json.load(f)
    return Js_Dict


def dic2house(hou_dict):
    rooms, T_Bs, furnitures, doors = [], [], [], []
    
    def expand_room(dict, key):
        if key in dict:
            list = dict[key]['Size']
            list.append(key)
            rooms.append(list)
            furnitures.append([])
            for f in dict[key]['Furnitures']:
                for i in range(len(dict[key]['Furnitures'][f]['Size'])):
                    list = dict[key]['Furnitures'][f]['Size'][i]
                    list.append(f)
                    furnitures[-1].append(list)
            for T_B in ['Toilet', 'Bathroom']:
                if T_B in dict[key]:
                    list = dict[key][T_B]['Size']
                    list.append(T_B)
                    T_Bs.append(list)
                
    expand_room(hou_dict, 'Bedroom')
    expand_room(hou_dict, 'Kitchen')
    expand_room(hou_dict, 'Livingroom')
    for d in hou_dict['Doors']:
        list = hou_dict['Doors'][d]['Size']
        list.append(d)
        doors.append(list)
    walls = hou_dict['Walls']
    lims = hou_dict['Boundary']
    return rooms, T_Bs, furnitures, doors, walls, lims


def load_filed(field, h_v, fname0, fname1):
    file_name = envi_path+h_v+'/'+fname0+'/'+fname1+'/'+field+'.csv'
    data = np.loadtxt(file_name, dtype=np.float32, delimiter=',')
    return data


def load_normaljson(name, h_v, fname0, fname1):
    file_name = envi_path+h_v+'/'+fname0+'/'+fname1+'/'+name+'.json'
    with open(file_name, 'r') as f:
        data = f.read()
    j_dict = json.loads(data)
    return j_dict


def load_actseq(h_v, fname0, fname1):
    times, locations, durs = read_actseq(h_v, fname0, fname1, process=True)
    i = 1
    while i < len(locations):
        if locations[i]==locations[i-1]:
            locations.pop(i)
            times.pop(i)
        else: i += 1
    return times, locations


def processtime(stime_tex, dur=False):
    sPA = 'AM'
    if dur:
        [shour, smin, ssec] = stime_tex.split(' ')
        times = int(shour[:-1])*H_M+int(smin[:-1])+int(ssec[:-1])/60
    else:
        [sday, sPA, shour, smin, ssec] = stime_tex.split(' ')
        times = int(sday[:-1])*D_M+int(shour[:-1])*H_M+int(smin[:-1])+int(ssec[:-1])/60
    if sPA == 'PM': times += D_M//2
    return times

def processact(act, fname0):
    Oact2Iact = {'Sleep': 'Sleep', 'Wash and Brush': 'Go_to_Bathroom', 'Cook': 'Cooking0', 'Bath': 'Go_to_Bathroom',
                 'Go out': 'Go_out', 'Go to Toilet': 'Go_to_Toilet', 'Wash Clothes': 'Washing', 'Watch TV': 'Watch_TV'}
    if act in Oact2Iact: return Oact2Iact[act]
    if act == 'Take TableWare': return 'Cooking0' if fname0[12]=='0' else 'Cooking1'
    if act == 'Take Food': return 'Cooking0' if fname0[14]=='0' else 'Cooking2'
    if act == 'Eat': return 'Go_out' if fname0[7]=='0' else 'Dining'
    if act == 'Dress up': return 'Sleep' if fname0[0]=='0' else 'Dress_up'
    if act == 'Clean': return 'Go_out' if fname0[19]=='0' else 'Cleaning'
    if act == 'Read':
        if fname0[3] != '0': return 'Work'
        if fname0[5] != '0': return 'Watch_TV'
        if fname0[7] != '0': return 'Dining'
        return 'Sleep'
    if act=='Relax' and fname0[5]=='0': return 'Sleep'
    return act


def read_actseq(h_v, fname0, fname1, process=False):
    times, locations, durs = [], [], []
    file_name = envi_path+h_v+'/'+fname0+'/'+fname1+'/ACTS.txt'
    with open(file_name, 'r') as f:
        Txts = f.readlines()
    for line in Txts:
        [stime_tex, act, dur_tex, _] = line.split('   ')
        times.append(processtime(stime_tex))
        durs.append(processtime(dur_tex, dur=True))
        if process:
            locations.append(processact(act, fname0))
        else:
            locations.append(act)
    return times, locations, durs