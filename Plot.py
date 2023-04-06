import matplotlib.pyplot as plt
import numpy as np
import os


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('\\')]
envi_path = abs_path + '\\DataBase\\'
Outputspath = abs_path + '\\Outputs\\'


edge, g_L, g_W = 50, 5, 5
D_H, H_M = 24, 60
D_M = D_H*H_M
Code = {'Toilet':'Toil', 'Bathroom':'Bath', 'Bed':'Bed', 'Nightstand':'NSt',
        'Wardrobe':'WaR', 'Desk':'Desk', 'Chair':'Cha', 'Sofa':'Sofa', 'TV':'TV',
         'Dinner_Table':'DTa', 'Kitchen_Stove':'KS', 'Cupboard':'Cb', 'Refrigerator':'Rfa',
        'Wash_Machine':'WM', 'Trash_Bin':'TB'}
colors = {'Sleep':'navy', 'Wash and Brush': 'mediumpurple', 'Cook': 'green', 'Take TableWare': 'forestgreen',
          'Take Food': 'aquamarine', 'Eat': 'lime', 'Bath': 'blue', 'Dress up': 'purple', 'Go out': 'deeppink',
          'Go to Toilet': 'darkorange', 'Clean': 'yellowgreen', 'Read': 'yellow', 'Watch TV': 'gold',
          'Wash Clothes': 'indigo', 'Wander': 'red', 'Relax': 'silver'}


def creat_floder(path):
    if not os.path.exists(path): os.makedirs(path)


def fill_value(martix_, x, y, L, W, x0, y0, value=0):
    I0, J0, II, JJ = (x-x0)//g_L, (y-y0)//g_W, L//g_L, W//g_W
    for i in range(I0, I0+II):
        for j in range(J0, J0+JJ):
            martix_[i][j] = value


def height2feild(lims, Heights):
    X_lim = [lims[0][0] - edge, lims[0][1] + edge]
    Y_lim = [lims[1][0] - edge, lims[1][1] + edge]
    l_x = np.arange(X_lim[0], X_lim[1] + g_L, g_L)
    l_y = np.arange(Y_lim[0], Y_lim[1] + g_W, g_W)
    data = Heights['0']*np.ones((len(l_x)-1, len(l_y)-1), dtype=np.int16)
    for [x, y, L, W] in Heights['1']:
        fill_value(data, x, y, L, W, X_lim[0], Y_lim[0])
    for [x, y, L, W, H] in Heights['2']:
        fill_value(data, x, y, L, W, X_lim[0], Y_lim[0], value=H)
    if Heights['3'] != []:
        for [x, y, L, W, H] in Heights['3']:
            fill_value(data, x, y, L, W, X_lim[0], Y_lim[0], value=H)
    return data


def layout_plot(Toil_Bath, Furnitures, Doors, Walls, Lims, show=False):
    plt.figure()
    ax = plt.gca()
    ax.set_aspect(1)
    X_lim = [Lims[0][0] - edge, Lims[0][1] + edge]
    Y_lim = [Lims[1][0] - edge, Lims[1][1] + edge]
    plt.xlim((X_lim[0], X_lim[1]))
    plt.ylim((Y_lim[0], Y_lim[1]))

    for room in Toil_Bath:
        [x, y, L, W, name] = room
        rect = plt.Rectangle((x, y), L, W, edgecolor='k', facecolor='none')
        ax.add_patch(rect)
        ax.text(x+L//2, y+W//2, Code[name], fontsize=10, va='center', ha='center')
    for room in Furnitures:
        for furniture in room:
            [x, y, L, W, name] = furniture
            rect = plt.Rectangle((x, y), L, W, edgecolor='k', facecolor='none')
            ax.add_patch(rect)
            ax.text(x+L//2, y+W//2, Code[name], fontsize=10, va='center', ha='center')
    for wall in Walls:
        x = [wall[0][0], wall[1][0]]
        y = [wall[0][1], wall[1][1]]
        plt.plot(x, y, 'k-')
    for door in Doors:
        x = [door[0], door[0] + door[2]]
        y = [door[1], door[1] + door[3]]
        plt.plot(x, y, 'w-')
    if show: plt.show()


def filed_plot(TBs, furnitures, doors, walls, lims, data, cbmin, cbmax, masked_v=None, layout=True, show=False):
    if layout: layout_plot(TBs, furnitures, doors, walls, lims)
    else:
        plt.figure()
        ax = plt.gca()
        ax.set_aspect(1)
    X_lim = [lims[0][0] - edge, lims[0][1] + edge]
    Y_lim = [lims[1][0] - edge, lims[1][1] + edge]
    l_x = np.arange(X_lim[0], X_lim[1] + g_L, g_L)
    l_y = np.arange(Y_lim[0], Y_lim[1] + g_W, g_W)
    XX, YY = np.meshgrid(l_x, l_y)
    if masked_v==None: Z = data.T
    else: Z = np.ma.masked_greater(data.T, masked_v)
    plt.pcolor(XX, YY, Z, cmap=plt.cm.rainbow, vmin=cbmin, vmax=cbmax)
    plt.colorbar()
    if show: plt.show()


def divide_xy(traj):
    Xs, Ys = [], []
    for point in traj:
        x, y = point[0], point[1]
        Xs.append(x)
        Ys.append(y)
    return Xs, Ys


def path_plot(TBs, furnitures, doors, walls, lims, key, bodyc, footps, show=False):
    layout_plot(TBs, furnitures, doors, walls, lims)
    BCx, BCy = divide_xy(bodyc)
    plt.plot(BCx, BCy, 'k--')
    if key[0] == 'D':
        Lx, Ly = divide_xy(footps[0])
        Rx, Ry = divide_xy(footps[1])
        plt.plot(Lx, Ly, 'ro')
        plt.plot(Rx, Ry, 'bo')
    if show: plt.show()


def save_plot(path, name):
    plt.savefig(path + '\\' + name + '.png')
    plt.close()


def plot_bar(time, timeI, act, j):
    plt.plot()
    plt.figure(figsize=(14,6))
    x = [j]
    tT = len(time)
    for t in range(tT):
        plt.barh(x, [time[t]/H_M], left=[timeI[t]/H_M], height=0.8, label=act[t], color=colors[act[t]])
    plt.xlim(0, 35)
    plt.ylim(j-2, j+2)
    plt.xticks([0, 6, 12, 18, 24], ['AM 0:00', 'AM 6:00', 'PM 0:00', 'PM 6:00', 'AM 0:00'], fontsize=18)
    plt.xlabel('Time', fontsize=20)
    plt.yticks(x, ['Day'+str(j)], fontsize=18)
    plt.legend(fontsize=16)


def Plot_ActSeq(Ttimes, durs, acts, path):
    SDay, EDay, count = int(Ttimes[0]//D_M), int((Ttimes[-1]+durs[-1])//D_M), 0
    for j in range(SDay, EDay+1):
        if count < len(Ttimes):
            timeI, time, act = [], [], []
            if SDay < j: timeI, time, act = [0], [Ttimes[count]-j*D_M], [act[count-1]]
            while Ttimes[count]<j*D_M+D_M:
                timeI.append(Ttimes[count]-j*D_M)
                time.append(durs[count])
                act.append(acts[count])
                count += 1
                if count > len(Ttimes)-1: break
            if j < EDay: time[-1] = j*D_M+D_M - Ttimes[count-1]
            plot_bar(time, timeI, act, j)
            filename = path + '\\Activity_Schedule,Day' + str(j) + '.png'
            plt.savefig(filename)
            plt.close()