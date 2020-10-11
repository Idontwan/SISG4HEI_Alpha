import numpy as np
import random as rd
import json, os


Flodername = {'Wardrobe':[0, 'WAR'], 'Desk':[1, 'De'], 'Sofa':[2, 'So'], 'Dinner_Table':[3, 'DTA'],
              'Kitchen_Stove':[4, 'KS'], 'Cupboard':[5, 'CB'], 'Refrigerator':[6, 'RFA'],
              'Wash_Machine':[7, 'WM'], 'Trash_Bin':[8, 'TB']}


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('/')]
data_path = abs_path[:abs_path.rfind('/')]+'/DataBase/'


import Height_Function as HF


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def creat_floder(path):
    if not os.path.exists(path): os.makedirs(path)


def data_save(type, House, Toil_Bath, Furnitures, Doors, Walls, T_con, B_con, Boundary, rj=None):
    F0_name_l = ['000', '00', '00', '000', '00', '00', '000', '00', '00']
    if type > 4: type = 4
    F1_name = ''
    Json_File = {}
    for i in range(len(House)):
        x, y, L, W, N = House[i][0], House[i][1], House[i][2], House[i][3], House[i][4]
        Area = (L*W)//100
        F1_name += str(Area)+','
        Json_File[N] = {}
        Json_File[N]['Size'] = [x, y, L, W]
        Json_File[N]['Furnitures'] = {}
        if T_con == N:
            x, y, L, W, N0 = Toil_Bath[0][0], Toil_Bath[0][1], Toil_Bath[0][2], \
                            Toil_Bath[0][3], Toil_Bath[0][4]
            Json_File[N][N0] = {'Size': [x, y, L, W]}
        if B_con == N:
            x, y, L, W, N0 = Toil_Bath[1][0], Toil_Bath[1][1], Toil_Bath[1][2], \
                            Toil_Bath[1][3], Toil_Bath[1][4]
            Json_File[N][N0] = {'Size': [x, y, L, W]}
        for furniture in Furnitures[i]:
            x, y, L, W, N1 = furniture[0], furniture[1], furniture[2], \
                            furniture[3], furniture[4]
            if N1 in Flodername:
                F0_name_l[Flodername[N1][0]] = Flodername[N1][1]
            if N1 not in Json_File[N]['Furnitures']:
                Json_File[N]['Furnitures'][N1] = {'Size': [[x, y, L, W]]}
            else: Json_File[N]['Furnitures'][N1]['Size'].append([x, y, L, W])
    Json_File['Doors'] = {}
    for door in Doors:
        x, y, L, W, N = door[0], door[1], door[2], door[3], door[4]
        Json_File['Doors'][N] = {'Size': [x, y, L, W]}
    Json_File['Walls'] = Walls
    Json_File['Boundary'] = Boundary
    [lx0, lx1], [ly0, ly1] = Boundary[0], Boundary[1]
    Ratio = (lx1-lx0)/(ly1-ly0)
    if Ratio<1: Ratio = 1/Ratio
    Ratio = int(100*Ratio)
    F1_name += str(Ratio)+','
    Js_Obj = json.dumps(Json_File, cls=MyEncoder)

    if rj==None: rj = str(rd.randint(0, 999))
    F1_name += rj + T_con[0] + B_con[0]
    F0_name = ''.join(F0_name_l)
    path0 = data_path + str(type)
    creat_floder(path0)
    path1 = path0 + '/'+ F0_name
    creat_floder(path1)
    path2 = path1 + '/'+ F1_name
    creat_floder(path2)
    f_name = path2 + '/Semantic.json'
    with open(f_name, 'w') as f:
        f.write(Js_Obj)
    return str(type), F0_name, F1_name, path2


def Height_SampleSave(type, House, Toil_Bath, Furnitures, path):
    floor_H = HF.floorH(House, type)
    fur_Hs = HF.furnitureH(floor_H, House, Toil_Bath, Furnitures)
    save_normaljson(path, fur_Hs, 'Height_Function')


def save_normaljson(path, data, name):
    Js_obj = json.dumps(data, cls=MyEncoder)
    file_name =  path + '/' + name + '.json'
    with open(file_name, 'w') as f:
        f.write(Js_obj)


def stat_update(statistics, Fname0):
    ind_l = [0, 3, 5, 7, 10, 12, 14, 17, 19, 21]
    for i in range(9):
        if Fname0[ind_l[i]] != '0':
            code = Fname0[ind_l[i]:ind_l[i+1]]
            if code not in statistics: statistics[code] = 1
            else: statistics[code] += 1


def get_stat(stat):
    keys = ['0', '1', '2', '3', '4', 'WAR', 'De', 'KS', 'CB', 'RFA', 'WM', 'TB', 'So', 'DTA']
    stat_rec = []
    for i in range(14):
        if keys[i] in stat: stat_rec.append(stat[keys[i]])
        else: stat_rec.append(0)
    return stat_rec