import os, sys


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('/')]
upper_path = abs_path[:abs_path.rfind('/')]
outputs_path = upper_path + '/Outputs/'
if upper_path not in sys.path: sys.path.append(upper_path)


Pi = 3.1416
Door_Height = 210
Wall_Width = 10


def creat_floder(path):
    if not os.path.exists(path): os.makedirs(path)


def unit_tran(list, last=True):
    [a, b, c] = list
    a, b = a/100, b/100
    if last: c = c/100
    return [a, b, c]


def write_config(path):
    content = '<?xml version="1.0" ?>\n<model>\n    <name>House_Model</name>\n    <version>1.0</version>\n    '+ \
              '<sdf version="1.7">model.sdf</sdf>\n    <author>\n        <name></name>\n        <email></email>\n'+ \
              '    </author>\n    <description></description>\n</model>'
    with open(path+'/model.config', 'w') as f:
        f.write(content)


def write_viscol(file_path, name0, name1, s_l, p_l):
    [s0, s1, s2] = s_l
    [p0, p1, p2] = p_l
    content = "      <collision name='"+name0+"_Collision"+name1+"'>\n        <geometry>\n          <box>\n"+\
              "            <size>"+str(s0)+" "+str(s1)+" "+str(s2)+"</size>\n          </box>\n        </geometry>\n"+\
              "        <pose>"+str(p0)+" "+str(p1)+" "+str(p2)+" 0 -0 0</pose>\n      </collision>\n"+\
              "      <visual name='"+name0+"_Visual"+name1+"'>\n        <pose>"+str(p0)+" "+str(p1)+" "+str(p2)+\
              "0 -0 0</pose>\n        <geometry>\n          <box>\n            <size>"+str(s0)+" "+str(s1)+" "+\
              str(s2)+"</size>\n          </box>\n        </geometry>\n        <material>\n          <script>\n"+\
              "            <uri>file://media/materials/scripts/gazebo.material</uri>\n            <name>Gazebo/"+\
              "Grey</name>\n          </script>\n          <ambient>1 1 1 1</ambient>\n        </material>\n"+\
              "        <meta>\n          <layer>0</layer>\n        </meta>\n      </visual>\n"
    with open(file_path, 'a') as f:
        f.write(content)


def write_link(file_path, p_l, name0, name1s, subs_ls, subp_ls):
    [p0, p1, p2] = p_l
    with open(file_path, 'a') as f:
        f.write("    <link name='"+name0+"'>\n")
    for i in range(len(name1s)):
        write_viscol(file_path, name0, name1s[i], subs_ls[i], subp_ls[i])
    with open(file_path, 'a') as f:
        f.write("      <pose>"+str(p0)+" "+str(p1)+" 0 0 -0 "+str(p2)+"</pose>\n    </link>\n")


def wallinlord(chex, chey, rooms):
    # check this whether this wall in left or bottom of a room:
    for [rx, ry, rL, rW, _] in rooms:
        if rx<chex<rx+rL and ry<chey<ry+rW: return -1
    return 1


def isTBwconwall(TBwall, wall, is_y):
    [[TBx0,TBy0], [TBx1, TBy1]] = TBwall
    [[p0x, p0y],[p1x, p1y]] = wall
    if is_y:
        if p0x==TBx0:
            if TBy0==p1y or TBy1==p0y: return True
    else:
        if p0y==TBy0:
            if TBx0==p1x or TBx1==p0x: return True
    return False


def detTBwalls(TBs):
    [Tx, Ty, TL, TW, _], [Bx, By, BL, BW, _] = TBs[0], TBs[1]
    x0, y0 = min(Tx, Bx), min(Ty, By)
    x1, y1 = max(Tx+TL, Bx+BL), max(Ty+TW, By+BW)
    wall0, wall1 = [[x0, y0], [x1, y0]], [[x0, y1], [x1, y1]]
    wall2, wall3 = [[x0, y0], [x0, y1]], [[x1, y0], [x1, y1]]
    if Tx==Bx: wall4 = [[Tx, max(By, Ty)], [Tx+TL, max(By, Ty)]]
    else: wall4 = [[max(Tx, Bx), Ty], [max(Tx, Bx), Ty+TW]]
    return wall0, wall1, wall2, wall3, wall4


def moveTBwall(oW0, oW1, oW4, lm, rm, dm, um, TBd):
    [Tx, Ty, _, _, _ ] = TBd
    [x0, y0], [x1, y1] = oW0[0], oW1[1]
    if Ty==y0: i = 0
    elif Ty==y1: i = 1
    elif Tx==x0: i = 2
    else: i = 3
    [[xm0, ym0], [xm1, ym1]] = oW4
    x0, y0 = x0+lm*Wall_Width/2, y0+dm*Wall_Width/2
    x1, y1 = x1+rm*Wall_Width/2, y1+um*Wall_Width/2
    if xm0 == xm1: ym0, ym1 = ym0+dm*Wall_Width/2, ym1+um*Wall_Width/2
    else: xm0, xm1 = xm0+lm*Wall_Width/2, xm1+rm*Wall_Width/2
    wall0, wall1 = [[x0, y0], [x1, y0], round(Pi, 4)], [[x0, y1], [x1, y1], 0]
    wall2, wall3 = [[x0, y0], [x0, y1], round(Pi/2, 4)], [[x1, y0], [x1, y1], round(-Pi/2, 4)]
    wall4 = [[xm0, ym0], [xm1, ym1], round(Pi/2, 4)] if xm0==xm1 else [[xm0, ym0], [xm1, ym1], 0]
    return wall0, wall1, wall2, wall3, wall4, i


def wall_plsl(rooms, TBs, doors, walls, W_H, ox0, oy0):
    Pose_list, subP_list, subS_list = [], [], []
    wall0, wall1, wall2, wall3, wall4 = detTBwalls(TBs)
    left_move, right_move, down_move, up_move = 1, -1, 1, -1

    def write2subPS(pl, sl):
        subP_list[-1].append(pl)
        subS_list[-1].append(sl)

    [edx, edy, edL, edW, _] = doors[0]
    for [[x0, y0], [x1, y1]] in walls:
        subP_list.append([])
        subS_list.append([])
        if x0 == x1:
            wchex, wchey = x0+50, (y0+y1)/2
            is_left = wallinlord(wchex, wchey, rooms)
            if is_left == -1:
                is_con = isTBwconwall(wall2, [[x0, y0], [x1, y1]], True)
                if is_con: left_move = -1
            else:
                is_con = isTBwconwall(wall3, [[x0, y0], [x1, y1]], True)
                if is_con: right_move = 1
            ang = round(-is_left*Pi/2, 4)
            Pose_list.append([x0+is_left*Wall_Width/2-ox0, wchey-oy0, ang])
            if edL == 0 and edx == x0 and y0<(edy+edW/2)<y1:
                write2subPS([-is_left*((y0+edy)/2-wchey), 0, W_H/2], [edy-y0, Wall_Width, W_H])
                write2subPS([-is_left*(edy+edW/2-wchey), 0, (W_H+Door_Height)/2], [edW, Wall_Width, W_H-Door_Height])
                write2subPS([-is_left*((y1+edy+edW)/2-wchey), 0, W_H/2], [y1-edy-edW, Wall_Width, W_H])
            else: write2subPS([0, 0, W_H/2], [y1-y0, Wall_Width, W_H])
        else:
            wchex, wchey = (x0+x1)/2, y0+50
            is_down = wallinlord(wchex, wchey, rooms)
            if is_down == -1:
                is_con = isTBwconwall(wall0, [[x0, y0], [x1, y1]], False)
                if is_con: down_move = -1
            else:
                is_con = isTBwconwall(wall1, [[x0, y0], [x1, y1]], False)
                if is_con: up_move = 1
            ang = round(Pi/2-is_down*Pi/2, 4)
            Pose_list.append([wchex-ox0, y0+is_down*Wall_Width/2-oy0, ang])
            if edW == 0 and edy == y0 and x0<(edx+edL/2)<x1:
                write2subPS([is_down*((x0+edx)/2-wchex), 0, W_H/2], [edx-x0, Wall_Width, W_H])
                write2subPS([is_down*(edx+edL/2-wchex), 0, (W_H+Door_Height)/2], [edL, Wall_Width, W_H-Door_Height])
                write2subPS([is_down*((x1+edx+edL)/2-wchex), 0, W_H/2], [x1-edx-edL, Wall_Width, W_H])
            else: write2subPS([0, 0, W_H/2], [x1-x0, Wall_Width, W_H])

    wall0, wall1, wall2, wall3, wall4, wallwithdoor = moveTBwall(wall0, wall1, wall4, left_move, right_move, down_move,
                                                                 up_move, doors[1])
    [TDx, TDy, TDL, TDW, _], [BDx, BDy, BDL, BDW, _] = doors[1], doors[2]
    for i, [[x0, y0], [x1, y1], ang] in enumerate([wall0, wall1, wall2, wall3]):
        subP_list.append([])
        subS_list.append([])
        Pose_list.append([(x0+x1)/2 - ox0, (y0+y1)/2 - oy0, ang])
        if i == wallwithdoor:
            flag0 = 1 if (TDx+TDy)<(BDx+BDy) else -1
            flag1 = 1 if -Pi/4<ang<3*Pi/4 else -1
            flag = flag0*flag1
            write2subPS([-flag*127.5, 0, W_H/2], [15, Wall_Width, W_H])
            write2subPS([-flag*90, 0, (W_H+Door_Height)/2], [60, Wall_Width, W_H-Door_Height])
            write2subPS([-flag*22.5, 0, W_H/2], [75, Wall_Width, W_H])
            write2subPS([flag*45, 0, (W_H+Door_Height)/2], [60, Wall_Width, W_H-Door_Height])
            write2subPS([flag*105, 0, W_H/2], [60, Wall_Width, W_H])
        else: write2subPS([0, 0, W_H/2], [max((x1-x0), (y1-y0)), Wall_Width, W_H])
    [[xm0, ym0], [xm1, ym1], ang] = wall4
    Pose_list.append([(xm0+xm1)/2 - ox0, (ym0+ym1)/2 - oy0, ang])
    subP_list.append([[0, 0, W_H/2]])
    subS_list.append([[max((xm1-xm0), (ym1-ym0)), Wall_Width, W_H]])
    return Pose_list, subP_list, subS_list


def fur_plsl(blocks_0, blocks_1, f_H, ox0, oy0):
    Pose_list, subP_list, subS_list = [], [], []
    for [x, y, L, W, H] in blocks_0:
        if H < f_H:
            Pose_list.append([x+L/2-ox0, y+W/2-oy0, 0])
            subP_list.append([[0, 0, H/2]])
            subS_list.append([[L, W, H]])
            for [x1, y1, L1, W1, H1] in blocks_1:
                xm, ym = x1 + L1/2, y1 + W1/2
                if x<xm<x+L and y<ym<y+W:
                    subP_list[-1].append([x1+L1/2-x-L/2, y1+W1/2-y-W/2, (H+H1)/2])
                    subS_list[-1].append([L1, W1, H1-H])
    return Pose_list, subP_list, subS_list


def deter_name(SubP_list, name):
    name0s, name1s = [], []
    for i in range(len(SubP_list)):
        name0s.append(name+'_'+str(i))
        name1s.append([])
        for j in range(len(SubP_list[i])):
            name1s[-1].append('_'+str(j))
    return name0s, name1s


def write_model(rj, name0s, name1s, P_ls, subS_lss, subP_lss, ox0, oy0):
    path = outputs_path + str(rj) + '/Gazebo/My_Model'
    creat_floder(path)
    write_config(path)
    content = "<?xml version='1.0'?>\n<sdf version='1.7'>\n  <model name='My_Model'>\n    <pose>"+str(ox0)+" "+ \
              str(oy0)+" 0 0 -0 0</pose>\n"
    file_path = path+'/model.sdf'
    with open(file_path, 'w') as f:
        f.write(content)
    for i in range(len(name0s)):
        write_link(file_path, P_ls[i], name0s[i], name1s[i], subS_lss[i], subP_lss[i])
    with open(file_path, 'a') as f:
        f.write("    <static>1</static>\n  </model>\n</sdf>")


def write_waypoint(filepath, i, step_time, waypoint):
    waypoint = unit_tran(waypoint, last=False)
    [x, y, ang], time = waypoint, i*step_time
    content = "          <waypoint>\n            <time>"+str(time)+"</time>\n            <pose>"+str(x)+" "+str(y)+ \
              " 0 0 0 "+str(ang)+"</pose>\n          </waypoint>\n"
    with open(filepath, 'a') as f:
        f.write(content)


def write_TP(rj, k, TP, step_time=0.8):
    file_path = outputs_path + str(rj) + '/Gazebo/Travel_Pattern_' + str(k) + '.world'
    content = "<?xml version='1.0' ?>\n<sdf version='1.7'>\n   <world name='Travel_Pattern_"+str(k)+"'>\n      "+ \
              "<include>\n         <uri>model://ground_plane</uri>\n      </include>\n      <include>\n         "+ \
              "<uri>:model://My_Model</uri>\n      </include>\n      <include>\n         <uri>model://sun</uri>\n"+ \
              "      </include>\n      <actor name='actor'>\n      <skin>\n        <filename>walk.dae</filename>\n"+ \
              "      </skin>\n      <animation name='walking'>\n        <filename>walk.dae</filename>\n        "+ \
              "<interpolate_x>true</interpolate_x>\n        <interpolate_y>true</interpolate_y>\n      </animation>"+ \
              "\n      <script>\n        <trajectory id='0' type='walking'>\n"
    with open(file_path, 'w') as f:
        f.write(content)
    for i in range(len(TP)):
        write_waypoint(file_path, i, step_time, TP[i])
    with open(file_path, 'a') as f:
        f.write("        </trajectory>\n      </script>\n    </actor>\n   </world>\n</sdf>")


def main(rooms, TBs, doors, walls, lims, H_dict, rj, savedTPs):
    ox0, oy0 = (lims[0][0]+lims[0][1])/2, (lims[1][0]+lims[1][1])/2
    f_height, blocks_0, blocks_1 = H_dict['0'], H_dict['2'], H_dict['3']
    WPose_list, WsubP_list, WsubS_list = wall_plsl(rooms, TBs, doors, walls, f_height, ox0, oy0)
    Wname0s, Wname1s = deter_name(WsubP_list, "Wall")
    FPose_list, FsubP_list, FsubS_list = fur_plsl(blocks_0, blocks_1, f_height, ox0, oy0)
    Fname0s, Fname1s = deter_name(FsubP_list, "Cube")
    Name0s, Name1s = Wname0s+Fname0s, Wname1s+Fname1s
    P_lists, subS_lists, subP_lists = WPose_list+FPose_list, WsubS_list+FsubS_list, WsubP_list+FsubP_list
    ox0, oy0 = ox0/100, oy0/100
    for i in range(len(P_lists)):
        P_lists[i] = unit_tran(P_lists[i], last=False)
        for k in range(len(subS_lists[i])):
            subS_lists[i][k] = unit_tran(subS_lists[i][k])
            subP_lists[i][k] = unit_tran(subP_lists[i][k])
    path = outputs_path + str(rj) + '/Gazebo'
    creat_floder(path)
    write_model(rj, Name0s, Name1s, P_lists, subS_lists, subP_lists, ox0, oy0)
    for i in range(len(savedTPs)):
        write_TP(rj, i, savedTPs[i])