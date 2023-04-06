import json, os, sys


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('\\')]
root_path = abs_path[:abs_path.rfind('\\')]
if root_path not in sys.path: sys.path.append(root_path)
data_path = root_path +'\\DataBase\\'


import FSave as FSa
import Floor_Plan as FLP
import Load


def generate_house(N, topo, furs):
    topo, furs = Pro_Input(topo, furs)
    Fail_N = 0
    if os.path.exists(data_path+'Content.json'): content, statistics = Load.load_cont_sta()
    else: content, statistics = {}, {}
    O_stat = FSa.get_stat(statistics)
    for i in range(N):
        try:
            House, Toil_Bath, Furnitures, Doors, Walls, T_con, B_con, type = FLP.Floor_Plan(topo, furs)
        except Exception as e: Fail_N += 1 #traceback.print_exc()
        else:
            bound = FLP.Boundary(House, Toil_Bath)
            tpstr, f_0, f_1, path = FSa.data_save(type, House, Toil_Bath, Furnitures, Doors, Walls, T_con, B_con, bound)

            if tpstr not in content:
                content[tpstr] = {f_0:[f_1]}
                statistics[tpstr] = 1
            else:
                statistics[tpstr] += 1
                if f_0 not in content[tpstr]:
                    content[tpstr][f_0] = [f_1]
                else:
                    content[tpstr][f_0].append(f_1)
            FSa.stat_update(statistics, f_0)

    N_stat = FSa.get_stat(statistics)
    stat_Incre = [N_stat[i]-O_stat[i] for i in range(14)]
    Js_Obj = json.dumps(content)
    f_name = data_path + 'Content.json'
    with open(f_name, 'w') as f:
        f.write(Js_Obj)
    Js_Obj = json.dumps(statistics)
    f_name = data_path + 'Statistics.json'
    with open(f_name, 'w') as f:
        f.write(Js_Obj)
    Suc_Rit = 1-Fail_N/N if N != 0 else 0
    return Suc_Rit, N, N_stat, stat_Incre


def Pro_Input(topo, furs):
    n_topo = [1, 1, 1, 1, 1]
    if topo[-1] == 0: n_topo = [topo[i] for i in range(5)]
    n_furs = []
    for i in range(3):
        if furs[i][-1]: n_fur = [furs[i][j]+1 for j in range(len(furs[i])-1)]
        else: n_fur = [2*furs[i][j] for j in range(len(furs[i])-1)]
        n_furs.append(n_fur)
    return n_topo, n_furs