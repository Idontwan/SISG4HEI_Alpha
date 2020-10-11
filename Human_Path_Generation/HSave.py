import json
import numpy as np
import random as rd


import HumanPath as HP


Acts_possibility = {'Go_out': 2, 'Go_to_Toilet': 6, 'Go_to_Bathroom': 2, 'Sleep': 2, 'Dress_up': 2,
                    'Work': 2, 'Watch_TV': 2, 'Dining': 3, 'Cooking0': 3, 'Cooking1': 3,
                    'Cooking2': 3, 'Washing': 1, 'Cleaning': 1}


def save_filed(name, path, format, data):
    file_name = path + '/' + name + '.csv'
    np.savetxt(file_name, data, fmt=format, delimiter=',')


def save_normaljson(path, data, name):
    Js_obj = json.dumps(data)
    file_name =  path + '/' + name + '.json'
    with open(file_name, 'w') as f:
        f.write(Js_obj)


def sample_act(acts):
    acts_P, P_f = [], 0
    for act in acts:
        P_f += Acts_possibility[act]
        acts_P.append(P_f)
    acts_P = [e/acts_P[-1] for e in acts_P]
    rj = rd.random()
    N = len(acts)
    for i in range(N):
        if rj < acts_P[i]:
            act = acts.pop(i)
            return act


def sample_acts(acts, type, has_end0=True):
    ends = []
    N = min(4, len(acts))
    act_num = rd.randint(1, 2) if type=='Lapping' else rd.randint(2, N)
    if not has_end0: act_num += 1
    for i in range(act_num):
        end = sample_act(acts)
        ends.append(end)
    return ends


def deter_HPkey(type, start, ends, end0):
    rj = str(rd.randint(0, 99))
    if len(rj)==1: rj = '0' + rj
    if type=='Lapping' or type=='Random':
        end = ','.join(ends)
        end = end + ','+end0
    elif type == 'Pacing': end = ends+','+end0
    else: end = ends
    return type+','+start+','+end+ ',' + str(rj)


def min_dist_bet_dests(distance, points):
    value = 99999
    for [I, J] in points:
        if distance[I][J] < value:
            value = distance[I][J]
    return value


def check_ends_dist(type, start, ends, distances, destinations, min_dis=250):
    if type=='Pacing':
        dist_E = distances[ends]
        SPoints = destinations[start]
        return min_dist_bet_dests(dist_E, SPoints)>min_dis
    dests = [start]
    for end in ends:
        dests.append(end)
    N = len(dests)
    for i in range(N-1):
        dest0 = dests.pop(0)
        for dest in dests:
            dist_E = distances[dest]
            SPoints = destinations[dest0]
            if min_dist_bet_dests(dist_E, SPoints)<min_dis: return False
    return True


def sample_save_path(path, acts, locations, distances, discom, destinations, max_diss, lims, Best_Slen, preferfoot):
    # locations[0] can not be 'Wander'
    HumanPath_d, Record, i = {}, {}, 1

    def dist_check(n_type, n_acts, start, has_e0): # avoid randomly picked locations too close each other for Lapping and Pacing
        flag, r_time, ends = False, 6, []
        while (not flag) and r_time > 0:
            r_time -= 1
            nnacts = [act for act in n_acts]
            if n_type == 'Lapping':
                ends = sample_acts(nnacts, n_type, has_end0=has_e0)
            else:
                ends = sample_act(nnacts)
            flag = check_ends_dist(n_type, start, ends, distances, destinations)
        return flag, ends

    def sample_type():
        rt = rd.random()
        if rt < 0.6: return 'Pacing'
        if rt < 0.9: return 'Lapping'
        return 'Random'

    def randompattern_generation(start, n_acts, end0):
        type = sample_type()
        if type == 'Pacing' or type == 'Lapping':
            if end0!=start:
                if check_ends_dist('Pacing', start, end0, distances, destinations):
                    if type=='Pacing': dischekflag, ends = True, end0
                    else:
                        dischekflag, ends = dist_check(type, n_acts, start, True)
                        ends = [end0] + ends
                else: dischekflag, ends = dist_check(type, n_acts, start, False)
            else: dischekflag, ends = dist_check(type, n_acts, start, False)
        else:
            dischekflag = True
            nnacts = [act for act in n_acts]
            ends = sample_acts(nnacts, type, has_end0=end0 != start)
            if end != start: ends = [end0] + ends
        if not dischekflag: return False, None, None, None, None
        SPoints, dist_Es, dist_S, max_dis = HP.det_startends(type, destinations, start, ends, distances, max_diss)
        try:
            if type=='Pacing':
                HPaths, Angless = HP.dire_pacing_path(SPoints, Best_Slen, discom, dist_Es, max_dis, type=type,
                                                      Distance_S=dist_S)
            else: HPaths, Angless = HP.lap_rand_path(SPoints, Best_Slen, discom, dist_Es, max_dis, type=type)
            [FI, FJ] = HPaths[-1][-1]
            body_c0, left_f0, right_f0 = HP.normal_bcfp(HPaths, Angless, Best_Slen, lims, preferfoot)
            dist_Es, max_dis, dist_S = distances[end0], max_diss[end0], None
            HPaths, Angless = HP.dire_pacing_path([FI, FJ], Best_Slen, discom, dist_Es, max_dis, OneSP=True)
            body_c1, left_f1, right_f1 = HP.normal_bcfp(HPaths, Angless, Best_Slen, lims, preferfoot)
            key = deter_HPkey(type, start, ends, end0)
        except: return False, None, None, None, None
        return True, body_c0+body_c1, left_f0+left_f1, right_f0+right_f1, key

    while i < len(locations):
        start = locations[i-1]
        if locations[i] != 'Wander':
            end = locations[i]
            SPoints, dist_Es, dist_S, max_dis = HP.det_startends('Direct', destinations, start, end, distances, max_diss)
            for j in range(8):
                try:
                    HPaths, Angless = HP.dire_pacing_path(SPoints, Best_Slen, discom, dist_Es, max_dis)
                    body_c, left_f, right_f = HP.normal_bcfp(HPaths, Angless, Best_Slen, lims, preferfoot)
                    key = deter_HPkey('Direct', start, end, end)
                    HumanPath_d[key] = [body_c, left_f, right_f]
                    if key[:-3] not in Record: Record[key[:-3]] = [key[-2:]]
                    elif key[-2:] not in Record[key[:-3]]: Record[key[:-3]].append(key[-2:])
                except: pass
            i += 1
        else:
            n_acts = []
            for act in acts:
                if act != start: n_acts.append(act)
            i += 1
            end0 = locations[i]
            if end0 != start:
                n_acts = []
                for act in acts:
                    if act!=start and act!=end0: n_acts.append(act)
            for j in range(8):
                is_SUC, body_c, left_f, right_f, key = randompattern_generation(start, n_acts, end0)
                if is_SUC:
                    HumanPath_d[key] = [body_c, left_f, right_f]
                    key_ = 'Wander,'+start+','+end0
                    if key_ not in Record: Record[key_] = [key]
                    elif key not in Record[key_]: Record[key_].append(key)
            i += 1
    save_normaljson(path, HumanPath_d, 'Human_Path,'+str(Best_Slen)+','+preferfoot)
    return HumanPath_d, Record
