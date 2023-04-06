import math as ma


Furniture2Activity = {'Bedroom':{'Bed':'Sleep', 'Wardrobe': 'Dress_up', 'Chair':'Work'},
                      'Livingroom':{'Sofa':'Watch_TV', 'Chair':'Dining'},
                      'Kitchen': {'Kitchen_Stove':'Cooking0', 'Cupboard':'Cooking1',
                                    'Refrigerator':'Cooking2', 'Wash_Machine':'Washing',
                                    'Trash_Bin':'Cleaning'}}
Door2Activity = {'Entrance':'Go_out', 'Toilet_Door':'Go_to_Toilet', 'Bathroom_Door':'Go_to_Bathroom'}


def distance(p0, p1):
    [x0, y0], [x1, y1] = p0, p1
    return ma.sqrt((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))


def calc_key_centers(rooms, furnitures):
    # calculate bedroom center, kitchen center, Desk center, Table center, TV center
    Bed_c, Kit_c, Des_c, Tab_c, TV_c = None, None, None, None, None
    for i in range(len(rooms)):
        rx, ry, rL, rW, rn = rooms[i]
        if rn == 'Bedroom':
            Bed_c = [rx+rL//2, ry+rW//2]
        elif rn == 'Kitchen':
            Kit_c = [rx+rL//2, ry+rW//2]
        for fur in furnitures[i]:
            fx, fy, fL, fW, fn = fur
            if fn == 'Desk':
                Des_c = [fx+fL//2, fy+fW//2]
            elif fn == 'Dinner_Table':
                Tab_c = [fx+fL//2, fy+fW//2]
            elif fn == 'TV':
                TV_c = [fx+fL//2, fy+fW//2]
    return Bed_c, Kit_c, Des_c, Tab_c, TV_c


def correct_side(x, y, L, W, p, flag='longest_nearst'):
    side_centers = [[x+L//2, y], [x, y+W//2], [x+L//2, y+W], [x+L, y+W//2]]
    # return nearest long sides
    v1 = [L * 10, W * 10, L * 10, W * 10]
    v2 = [distance(e, p) for e in side_centers]
    v = [v1[i] - v2[i]/10 for i in range(4)]
    if flag=='longest_nearst': return [v.index(max(v))]
    v2_min_i, v2_max_i = v2.index(min(v2)), v2.index(max(v2))
    sides = [0, 1, 2, 3]
    sides.remove(v2_min_i)
    sides.remove(v2_max_i)
    return sides

def fur_dest(X0, Y0, x, y, L, W, index, g_L=5, g_W=5):
    nodes = [[], [], [], []]
    dest = []
    I0, J0 = (x-X0)//g_L, (y-Y0)//g_W
    I1, J1 = I0+L//g_L, J0+W//g_W
    for t in range(I0, I1):
        nodes[0].append([t, J0-5])
        nodes[2].append([t, J1+4])
    for t in range(J0, J1):
        nodes[1].append([I0-5, t])
        nodes[3].append([I1+4, t])
    for i in index:
        for [I, J] in nodes[i]: dest.append([I, J])
    return dest


def door_dest(X0, Y0, x, y, L, W, g_L=5, g_W=5):
    nodes = []
    I0, J0 = (x-X0)//g_L, (y-Y0)//g_W
    I1, J1 = I0+L//g_L, J0+W//g_W
    if L == 0:
        for t in range(J0, J1):
            nodes.append([I0-6, t])
            nodes.append([I0+5, t])
    elif W == 0:
        for k in range(I0, I1):
            nodes.append([k, J0-6])
            nodes.append([k, J0+5])
    return nodes


def cal_destinations(rooms, furnitures, doors, dis_val, X0, Y0):
    Bed_c, Kit_c, Des_c, Tab_c, TV_c = calc_key_centers(rooms, furnitures)
    Destinations = {}
    for i in range(len(rooms)):
        _, _, _, _, r_n = rooms[i]
        for furniture in furnitures[i]:
            x, y, L, W, name = furniture
            if name in Furniture2Activity[r_n]:
                key = Furniture2Activity[r_n][name]
                if key not in Destinations:
                    Destinations[key] = []
                index = [0, 1, 2, 3]
                if name == 'Wardrobe':
                    index = correct_side(x, y, L, W, Bed_c)
                elif name == 'Kitchen_Stove':
                    index = correct_side(x, y, L, W, Kit_c)
                elif name == 'Cupboard':
                    index = correct_side(x, y, L, W, Kit_c)
                elif name == 'Refrigerator':
                    index = correct_side(x, y, L, W, Kit_c)
                elif name == 'Sofa':
                    index = correct_side(x, y, L, W, TV_c)
                elif name == 'Chair':
                    if r_n == 'Bedroom': index = correct_side(x, y, L, W, Des_c, flag='middle')
                    elif r_n == 'Livingroom': index = correct_side(x, y, L, W, Tab_c, flag='middle')
                nodes = fur_dest(X0, Y0, x, y, L, W, index)
                for [k, t] in nodes:
                    if dis_val[k][t]<99: Destinations[key].append([k, t])
    for door in doors:
        x, y, L, W, d_n = door
        key = Door2Activity[d_n]
        Destinations[key] = []
        nodes = door_dest(X0, Y0, x, y, L, W)
        for [k, t] in nodes:
            if dis_val[k][t] < 99: Destinations[key].append([k, t])
    return Destinations