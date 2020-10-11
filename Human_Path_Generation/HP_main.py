import sys, os


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('/')]
upper_path = abs_path[:abs_path.rfind('/')]
if upper_path not in sys.path: sys.path.append(upper_path)


import Discom as Dis
import Distance as Dist
import Dest_nodes as Dest
import HSave as HSa
import Load

edge = 50


def all_distance(SavedList):
    for s_path in SavedList:
        path = upper_path + '/DataBase/'+ s_path
        [stj, fname0, fname1] = s_path.split('/')
        acts = Load.fname2act(fname0)
        hou_dict = Load.load_se_map(stj, fname0, fname1)
        rooms, T_Bs, furnitures, doors, walls, lims = Load.dic2house(hou_dict)
        T_B_in, T_B_walls = Dis.T_B2obj_W(T_Bs, rooms)
        Dis.mod_walls(walls, T_B_walls)
        discom = Dis.cal_dis_val(rooms, furnitures, walls, lims, t_b_in=T_B_in)
        X0, Y0 = lims[0][0] - edge, lims[1][0] - edge
        destinations = Dest.cal_destinations(rooms, furnitures, doors, discom, X0, Y0)
        max_diss_d = {}
        connectflag = 0
        for act in acts:
            s_nodes = destinations[act]
            topo = Dist.topology(discom)
            distance, max_dis = Dist.weighted_dijistra(s_nodes, topo, discom)
            if connectflag == 0:
                che_con, e_act = Dist.connect_check(distance, max_dis, destinations)
                if che_con: connectflag = 1
                else: return False, e_act, s_path
            max_diss_d[act] = max_dis
            f_name = act + '_distance'
            HSa.save_filed(f_name, path, '%7.2f', distance)
        HSa.save_filed('Discomfortable_value', path, '%5.2f', discom)
        HSa.save_normaljson(path, destinations, 'Destinations')
        HSa.save_normaljson(path, max_diss_d, 'Max_Distances')
    return True, None, None


def deterlocrelax(hou_dict, locations, times):
    def cal_dist(xy0, xy1):
        return (xy1[0]-xy0[0])**2+(xy1[1]-xy0[1])**2

    Act2Place0 = {'Dress_up': ['Bedroom', 'Wardrobe'], 'Work':['Bedroom', 'Chair'], 'Cooking0': ['Kitchen', 'Kitchen_Stove'],
                  'Cooking1': ['Kitchen', 'Cupboard'], 'Cooking2': ['Kitchen', 'Refrigerator'], 'Washing': ['Kitchen', 'Wash_Machine'],
                  'Cleaning': ['Kitchen', 'Trash_Bin']}
    Act2Place1 = {'Go_out': 'Entrance', 'Go_to_Toilet': 'Toilet_Door', 'Go_to_Bathroom': 'Bathroom_Door'}
    [bed], [sofa] = hou_dict['Bedroom']['Furnitures']['Bed']['Size'], hou_dict['Livingroom']['Furnitures']['Sofa']['Size']
    bed_c, sofa_c = [bed[0]+bed[2]//2, bed[1]+bed[3]//2], [sofa[0]+sofa[2]//2, sofa[1]+sofa[3]//2]
    if locations[0] == 'Relax': locations[0] = 'Sleep'
    i = 1
    while i < len(locations):
        flag = 1
        if locations[i]=='Relax':
            if locations[i-1]=='Wander': prevact = locations[i-2]
            else: prevact = locations[i-1]
            if prevact=='Sleep' or prevact=='Watch_TV':
                if locations[i-1]=='Wander': locations[i] = prevact
                else:
                    flag = 0
                    locations.pop(i)
                    times.pop(i)
            else:
                if prevact=='Dining':
                    prevlocas = hou_dict['Livingroom']['Furnitures']['Chair']['Size']
                    prev2B, prev2S = 99999999, 99999999
                    for prelo in prevlocas:
                        prevc = [prelo[0]+prelo[2]//2, prelo[1]+prelo[3]//2]
                        if cal_dist(prevc, bed_c)<prev2B: prev2B = cal_dist(prevc, bed_c)
                        if cal_dist(prevc, sofa_c)<prev2S: prev2S = cal_dist(prevc, sofa_c)
                else:
                    if prevact[:2] == 'Go':
                        door = Act2Place1[prevact]
                        prevloca = hou_dict['Doors'][door]['Size']
                    else:
                        [room, fur] = Act2Place0[prevact]
                        [prevloca] = hou_dict[room]['Furnitures'][fur]['Size']
                    prevc = [prevloca[0]+prevloca[2]//2, prevloca[1]+prevloca[3]//2]
                    prev2B, prev2S = cal_dist(prevc, bed_c), cal_dist(prevc, sofa_c)
                locations[i] = 'Watch_TV' if prev2B>prev2S else 'Sleep'
        i += flag
    i = 1
    while i < len(locations):
        if locations[i]==locations[i-1]:
            locations.pop(i)
            times.pop(i)
        else: i += 1


def path_generate(path_list, timess, locationss, best_stride, preferfoot):
    TPs, Records = [], []
    for i in range(len(path_list)):
        [stj, fname0, fname1] = path_list[i].split('/')
        path = upper_path + '/DataBase/' + path_list[i]
        hou_dict = Load.load_se_map(stj, fname0, fname1)
        lims = hou_dict['Boundary']
        if fname0[5]!='0': deterlocrelax(hou_dict, locationss[i], timess[i])
        acts = Load.fname2act(fname0)
        discom = Load.load_filed('Discomfortable_value', stj, fname0, fname1)
        destinations = Load.load_normaljson('Destinations', stj, fname0, fname1)
        max_diss = Load.load_normaljson('Max_Distances', stj, fname0, fname1)
        distances = {}
        for act in acts:
            f_name = act + '_distance'
            distance = Load.load_filed(f_name, stj, fname0, fname1)
            distances[act] = distance
        TP, Record = HSa.sample_save_path(path, acts, locationss[i], distances, discom, destinations, max_diss, lims,
                                         best_stride, preferfoot)
        TPs.append(TP)
        Records.append(Record)
    return TPs, Records