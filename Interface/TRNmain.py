import sys, os
import matplotlib.pyplot as plt
from PIL import Image


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('/')]
upper_path = abs_path[:abs_path.rfind('/')]
outputs_path = upper_path + '/Outputs/'
if upper_path not in sys.path: sys.path.append(upper_path)


edge = 10
edge_in_main = 50
# the definition of edge in Floorplan_Generation or Human_path_Generation Folder
g_L, g_W = 5, 5


def creat_floder(path):
    if not os.path.exists(path): os.makedirs(path)


def plot_bitmap(f_height, blocks_0, walls, lims):
    fur_block = []

    plt.figure()
    ax = plt.gca()
    ax.set_aspect(1)
    plt.xlim((lims[0][0]-edge, lims[0][1]+edge))
    plt.ylim((lims[1][0]-edge, lims[1][1]+edge))

    for wall in walls:
        x = [wall[0][0], wall[1][0]]
        y = [wall[0][1], wall[1][1]]
        plt.plot(x, y, '0.0')
    for block in blocks_0:
        [x, y, L, W, H] = block
        if H == f_height:
            rect = plt.Rectangle((x, y), L, W, edgecolor='0.0', facecolor='0.0')
            ax.add_patch(rect)
        else: fur_block.append(block)


    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    return fur_block


def cal_resolution(lims, picture):
    weight = lims[0][1] - lims[0][0]
    height = lims[1][1] - lims[1][0]
    pic_L = picture.convert('L')
    (I, J) = pic_L.size
    I0, I1 = 0, I
    J0, J1 = 0, J
    for i in range(I):
        for j in range(J):
            value = pic_L.getpixel((i, j))
            if value < 2:
                if i > I0: I0 = i
                if i < I1: I1 = i
                if j > J0: J0 = j
                if j < J1: J1 = j
    w_pix, h_pix = I0 - I1, J0 - J1
    res = (weight/100/(w_pix-1) + (height/100/(h_pix-1)))/2
    # (0,0) of PIL in the upper left corner
    # calculate the coordinate of lower-left pixel
    x_origin = lims[0][0]/100 - (I1+1)*res
    y_origin = lims[1][0]/100 - (J-J0+1)*res
    return res, x_origin, y_origin, I, J


def check_collision(block,fur):
    flag = False
    [x0, y0, L0, W0, H0 ] = block
    [x1, y1, L1, W1, H1] = fur
    if x1<x0+L0/2<x1+L1 and y1<y0+W0/2<y1+W1:
        block = [x0, y0, L0, W0, H0-H1, H1]
        flag = True
    return flag, block


def write_a_fur(file, L, W, H, i):
    content = 'define furniture' + str(i) + ' model\n(\n  size [' + \
              str(L/100)+ ' ' + str(W/100) + ' ' + str(H/100) + \
              ']\n  gui_nose 0\n)\n\n'
    with open(file, 'a') as f:
        f.write(content)


def write_furs_size(file, fur_blocks, blocks_1=[]):
    blocks_1_ = []
    if blocks_1 != []:
        for block in blocks_1:
            for fur in fur_blocks:
                flag, block = check_collision(block, fur)
                if flag:
                    blocks_1_.append(block)
                    break
    Len0, Len1 = len(fur_blocks), len(blocks_1_)
    for i in range(Len0):
        [_, _, L, W, H] = fur_blocks[i]
        write_a_fur(file, L, W, H, i)
    for i in range(Len1):
        [_, _, L, W, H, _] = blocks_1_[i]
        write_a_fur(file, L, W, H, i+Len0)
    return blocks_1_


def write_robot_defin(file, L, W, H):
    content = '# Definition of the robot\n define kinect ranger\n' + \
              '(\n  sensor\n  (\n    range_max 6.5\n    fov 58.0\n' +  \
              '    samples 640\n  )\n  # generic model properties\n' + \
              '  color "blaxk"\n  size [ 0.06 0.15 0.03 ]\n)\n\n' + \
              'define e_bio position\n(\n  pose [ 0.0 0.0 0.0 0.0 ]\n' + \
              '  odom_error [0.03 0.03 999999 999999 999999 0.02]\n' + \
              '  size [ ' + str(L) + ' ' + str(W) + ' ' + str(H) + ' ]\n' + \
              '  gui_nose 1\n  gui_nose 1\n  color "red"\n\n' + \
              '  kinect(pose [ -0.1 0.0 -0.11 0.0 ])\n)\n\n' + \
              '# Definition the size of all furniture\n'
    with open(file, 'w') as f:
        f.write(content)


def write_put_robot(file, robot_x, robot_y):
    content = '# put in a robot\ne_bio\n(\n  pose [ ' + \
              str(robot_x) + ' ' + str(robot_y) + ' 0.000 0.000 ]\n' + \
              '  name "e_bio1"\n  color "red"\n  gui_nose 1\n)\n\n'
    with open(file, 'a') as f:
        f.write(content)


def write_put_a_fur(file, x, y, H_, i):
    content = 'furniture' + str(i) + '( pose [ ' + str(x) + ' ' + str(y) + \
              ' ' + str(H_) + ' 0.000 ] color "gray")\n'
    with open(file, 'a') as f:
        f.write(content)


def write_put_furs(file, fur_blocks, blocks_1_=[]):
    content = '# put furnitures\n'
    with open(file, 'a') as f:
        f.write(content)
    Len0, Len1 = len(fur_blocks), len(blocks_1_)
    for i in range(Len0):
        [x, y, L, W, _] = fur_blocks[i]
        write_put_a_fur(file, (x+L/2)/100, (y+W/2)/100, 0.000, i)
    for i in range(Len1):
        [x, y, L, W, _, H_] = blocks_1_[i]
        write_put_a_fur(file, (x+L/2)/100, (y+W/2)/100, H_/100, i + Len0)


def generate_world_file(file_path, fur_blocks, blocks_1, x_origin, y_origin,
                        P_W, P_H, f_height, I, J, robot_x, robot_y):
    file_path = file_path + '/Scene.world'
    write_robot_defin(file_path, 0.2552, 0.2552, 0.40)
    blocks_1_ = write_furs_size(file_path, fur_blocks, blocks_1=blocks_1)
    write_put_robot(file_path, robot_x, robot_y)
    write_put_furs(file_path, fur_blocks, blocks_1_=blocks_1_)

    content = '\ndefine floorplan model\n(\n' + '  color "gray30"\n  boundary 0' + \
               '\n  gui_nose 0\n  gui_grid 0\n  gui_outline 0\n  gripper_return 0' + \
               '\n  fiducial_return 0\n  laser_return 1\n)\n\n# set the resolution' + \
               ' of the underlying raytrace model in meters\nresolution 0.01\n\n' + \
               'interval_sim 100  # simulation timestep in milliseconds\n\n'
    with open(file_path, 'a') as f:
        f.write(content)

    content = 'window\n(\n  size [ ' + str(I+100) + ' ' + str(J+100) + ' ]\n' + \
              '  rotate [ 0.000 0.000 ]\n)\n\n# load an environment bitmap\n' + \
              'floorplan\n(\n  name "Scene"\n  bitmap "Scene.png"\n' + \
              '  size [' + str(P_W) + ' ' + str(P_H) + ' ' + str(f_height/100) + ']\n' + \
              '  pose [ ' + str(x_origin+P_W/2) + ' ' + str(y_origin+P_H/2) + ' ' + \
              '0.000 0.000 ]\n)'
    with open(file_path,'a') as f:
        f.write(content)


def main(j, H_dict, Se_dict, robot_x, robot_y):
    f_height, rooms = H_dict['0'], H_dict['1']
    blocks_0, blocks_1 = H_dict['2'], H_dict['3']
    walls, lims = Se_dict['Walls'], Se_dict['Boundary']
    o_path = outputs_path + str(j) + '/Stage'
    creat_floder(o_path)
    fur_blocks = plot_bitmap(f_height, blocks_0, walls, lims)
    plt.savefig(o_path + '/Scene.png', bbox_inches='tight')
    plt.close()
    picture = Image.open(o_path + '/Scene.png')
    res, x_origin, y_origin, I_, J_ = cal_resolution(lims, picture)
    P_W, P_H = res * I_, res * J_
    generate_world_file(o_path, fur_blocks, blocks_1, x_origin, y_origin, P_W, P_H,
                        f_height, I_, J_, robot_x/100, robot_y/100)