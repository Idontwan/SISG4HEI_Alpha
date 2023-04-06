D_H, H_M = 24, 60
D_M = D_H*H_M
g_L, g_W = 5, 5
Code = {'Toilet':'Toil', 'Bathroom':'Bath', 'Bed':'Bed', 'Nightstand':'NSt',
        'Wardrobe':'WaR', 'Desk':'Desk', 'Chair':'Cha', 'Sofa':'Sofa', 'TV':'TV',
         'Dinner_Table':'DTa', 'Kitchen_Stove':'KS', 'Cupboard':'Cb', 'Refrigerator':'Rfa',
        'Wash_Machine':'WM', 'Trash_Bin':'TB'}
Num2Act = ['Sleep', 'Sleep', 'Wash and Brush', 'Cook', 'Take TableWare', 'Take Food',
           'Eat', 'Bath', 'Dress up', 'Go out', 'Go to Toilet', 'Go to Toilet',
           'Clean', 'Read', 'Watch TV', 'Wash Clothes', 'Wander', 'Relax']
AScolors = ['navy', 'navy', 'mediumpurple', 'green', 'forestgreen', 'aquamarine',
          'lime', 'blue', 'purple', 'deeppink', 'darkorange', 'darkorange',
          'yellowgreen', 'yellow', 'gold', 'indigo', 'red', 'silver']


def realxy2can(real_size, x0, y0, scale, PW, PH, Rote, Is_Rect=True):
    # real_size is the [x, y, L, W], x0,yo is the coordinate of center of the house
    # PW, PH is the size of canvas, Rote is Rotation_Flag
    # if Is_Rect is True, transfer for a rectangle; else, for a point
    if not Is_Rect:
        [x, y] = real_size
        canx, cany = int(PW/2+(x-x0)/scale), int(PH/2-(y-y0)/scale)
        return [canx, cany] if not Rote else [int(PW/2+(PH/2-cany)), int(PH/2-(PW/2-canx))]
    else:
        [x, y, L, W] = real_size
        xm, ym = x+L//2, y+W//2
        [canxm, canym] = realxy2can([xm, ym], x0, y0, scale, PW, PH, Rote, Is_Rect=False)
        [HcanL,HcanW] = [int(L/scale/2), int(W/scale/2)] if not Rote else [int(W/scale/2), int(L/scale/2)]
        return [canxm-HcanL, canym-HcanW, canxm+HcanL, canym+HcanW]


def canxy2real(can_size, x0, y0, scale, PW, PH, Rote):
    [canx, cany] = can_size
    if Rote: canx, cany = int((PW-PH)//2+cany), int((PH+PW)//2-canx)
    return [int((x0+(canx-PW//2)*scale)//g_L*g_L), int((y0+(PH//2-cany)*scale)//g_W*g_W)]


def layoutplot(Canvas, Can_size, Rooms, T_Bs, Furns, Doors, Walls, Lims, showbg=True):
    Colors = {'Bedroom': 'blue', 'Kitchen': 'green', 'Livingroom': 'red', 'Toilet': 'yellow', 'Bathroom': 'purple'} if \
        showbg else {'Bedroom': 'white', 'Kitchen': 'white', 'Livingroom': 'white', 'Toilet': 'white', 'Bathroom': 'white'}
    NameFur_set = ['Bed', 'Wardrobe', 'Desk', 'Kitchen_Stove', 'Cupboard', 'Refrigerator', 'Wash_Machine',
                   'Trash_Bin', 'Dinner_Table', 'Sofa']
    Fur_set, Text = [[] for i in range(10)], [] # text is for locating the index of all text objective in canvas
    [Can_W, Can_H] = Can_size

    def scale(W, H):
        scales = [2, 2.5, 5]
        for i in range(3):
            if W/scales[i]<Can_W and H/scales[i]<Can_H: return scales[i]

    T_W, T_H = Lims[0][1]-Lims[0][0], Lims[1][1]-Lims[1][0]
    Offset = [(Lims[0][1]+Lims[0][0])//2, (Lims[1][1]+Lims[1][0])//2] #the real coordinates of the center of house
    Rotate_Flag = True if T_H>T_W else False
    Scale = scale(T_H, T_W) if Rotate_Flag else scale(T_W, T_H)
    font = 'Times 12'
    if Scale>2: font = 'Times 10' if Scale==2.5 else 'Times 7'
    T_rooms = Rooms + T_Bs
    for room in T_rooms:
        color = Colors[room[-1]]
        canxys = realxy2can(room[:4], Offset[0], Offset[1], Scale, Can_W, Can_H, Rotate_Flag) # [x0, y0, x1, y1]
        Canvas.create_rectangle(canxys[0], canxys[1], canxys[2], canxys[3], fill=color, outline='')
        if room[-1] == 'Toilet' or room[-1] == 'Bathroom':
            Canvas.create_line(canxys[0], canxys[1], canxys[0], canxys[3], width=3)
            Canvas.create_line(canxys[0], canxys[1], canxys[2], canxys[1], width=3)
            Canvas.create_line(canxys[2], canxys[3], canxys[2], canxys[1], width=3)
            Canvas.create_line(canxys[2], canxys[3], canxys[0], canxys[3], width=3)
    for i, room in enumerate(Furns):
        Text.append({})
        for fur in room:
            name = fur[-1]
            canxys = realxy2can(fur[:4], Offset[0], Offset[1], Scale, Can_W, Can_H, Rotate_Flag)
            fur_Obj = Canvas.create_rectangle(canxys[0], canxys[1], canxys[2], canxys[3])
            text_Obj = Canvas.create_text((canxys[0]+canxys[2])//2, (canxys[1]+canxys[3])//2,
                                          text=Code[name], font=font)
            if name in NameFur_set:
                j = NameFur_set.index(name)
                Fur_set[j].append(fur_Obj)
                Fur_set[j].append(text_Obj)
                Text[i][name] = [text_Obj]
            elif name == 'TV':
                Fur_set[9].append(fur_Obj)
                Fur_set[9].append(text_Obj)
                Text[i][name] = [text_Obj]
            elif name == 'Nightstand':
                Fur_set[0].append(fur_Obj)
                Fur_set[0].append(text_Obj)
                if name not in Text[i]: Text[i][name] = [text_Obj]
                else: Text[i][name].append(text_Obj)
            else:
                if name not in Text[i]: Text[i][name] = [text_Obj]
                else: Text[i][name].append(text_Obj)
                if i == 0:
                    Fur_set[2].append(fur_Obj)
                    Fur_set[2].append(text_Obj)
                else:
                    Fur_set[8].append(fur_Obj)
                    Fur_set[8].append(text_Obj)
    for wall in Walls:
        canxy0 = realxy2can(wall[0], Offset[0], Offset[1], Scale, Can_W, Can_H, Rotate_Flag, Is_Rect=False)
        canxy1 = realxy2can(wall[1], Offset[0], Offset[1], Scale, Can_W, Can_H, Rotate_Flag, Is_Rect=False)
        Canvas.create_line(canxy0[0], canxy0[1], canxy1[0], canxy1[1], width=3)
    for door in Doors:
        canxys = realxy2can(door[:4], Offset[0], Offset[1], Scale, Can_W, Can_H, Rotate_Flag)
        Canvas.create_line(canxys[0], canxys[1], canxys[2], canxys[3], fill='white', width=3)
    return Fur_set, Scale, Rotate_Flag, Text


def div_Mkchain(ActSeq, SDay=1, EDay=25):
    timess, timeIss, numss, time, n = [[]], [[]], [[]], 0, 0

    def write_data(t0, t1, no):
        # t0 is the start time of no, t1 is the end time of no
        timeIss[-1].append(t0)
        timess[-1].append(t1-t0)
        numss[-1].append(no)

    absminu = ActSeq[n][1]
    while absminu < SDay * D_M:
        n += 1
        node, absminu = ActSeq[n - 1][0], ActSeq[n][1]
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
            node, absminu = ActSeq[n - 1][0], ActSeq[n][1]
    write_data(time, D_M, node)
    return timess, timeIss, numss


def startend_nodes(startminu, scale, timeIs):
    N = len(timeIs)
    stn, edn,  = N-1, 0
    for i in range(N):
        if timeIs[i]>startminu and i<stn: stn = i
        if timeIs[i]<startminu+scale and i>edn: edn = i
    return stn, edn


def add_rectangle(Canvas, t0, dur, num, startminu, scale, Canvas_W):
    x0 = int((t0-startminu)/scale*Canvas_W)
    x1 = x0 + int(dur/scale*Canvas_W)
    Canvas.create_rectangle(x0, 10, x1, 260, fill=AScolors[num])
    text_list = Num2Act[num].split(' ')
    N, j = len(text_list), 0
    for i in range(N):
        if len(text_list[i])>j: j = len(text_list[i])
    if x1-x0 > 10*j:
        for i in range(N):
            y = 135 - (N-1)*8 + 16*i
            Canvas.create_text(int((x0+x1)/2), y, text=text_list[i], font=('Helvetica 11 bold'), fill='white')


def tick_text(time):
    aorpm = 'am' if time<D_M/2 else 'pm'
    h_time = time%(D_M//2)
    Hs, Ms = int(h_time//H_M), int(h_time%H_M)
    strHs, strMs = str(Hs), str(Ms)
    if len(strHs) == 1: strHs = '0' + strHs
    if len(strMs) == 1: strMs = '0' + strMs
    return strHs + ':' + strMs + aorpm


def add_ticks(Canvas, startminu, scale, tickstep, Canvas_W):
    n0, n1 = int(startminu//tickstep), int((startminu+scale)//tickstep)
    for i in range(n0, n1+1):
        x = int(((i*tickstep)-startminu)/scale*Canvas_W)
        if i == n0 and x>35: Canvas.create_text(x, 280, text=tick_text(i*tickstep), font=('Helvetica 11 bold'))
        elif i==n1 and x<Canvas_W-35: Canvas.create_text(x, 280, text=tick_text(i*tickstep), font=('Helvetica 11 bold'))
        Canvas.create_text(x, 280, text=tick_text(i*tickstep), font=('Helvetica 11 bold'))


def schedule_plot(Layout, W, times, timeIs, nums, statminu, scale, tickstep):
    stn, edn = startend_nodes(statminu, scale, timeIs)
    add_rectangle(Layout, statminu, timeIs[stn]-statminu, nums[stn-1], statminu, scale, W)
    for i in range(stn, edn):
        add_rectangle(Layout, timeIs[i], times[i], nums[i], statminu, scale, W)
    add_rectangle(Layout, timeIs[edn], statminu+scale-timeIs[edn], nums[edn], statminu, scale, W)
    add_ticks(Layout, statminu, scale, tickstep, W)


def noteline_plot(Layout, W, statminu, scale, minu):
    if minu==None or minu<statminu or minu>(statminu+scale):
        return None
    x = int((minu-statminu)/scale*W)
    line = Layout.create_line(x, 0, x, 300, width=2)
    return line


def plotBCline(Canvas, body_c, scale, isRoT, lims, cansize, fill='black'):
    x0, y0 = (lims[0][0]+lims[0][1])//2, (lims[1][1]+lims[1][0])//2
    [PW, PH] = cansize
    line = []
    for point in body_c:
        [x, y, _] = point
        [canx, cany] = realxy2can([x, y], x0, y0, scale, PW, PH, isRoT, Is_Rect=False)
        line.append(canx)
        line.append(cany)
    BCline = Canvas.create_line(line, dash=(10, 10), width=2, fill=fill)
    return BCline


def plotFPline(Canvas, left_f, right_f, scale, isRoT, lims, cansize):
    x0, y0 = (lims[0][0]+lims[0][1])//2, (lims[1][1]+lims[1][0])//2
    [PW, PH] = cansize
    line_l, line_r = [], []
    for point in left_f:
        [canx, cany] = realxy2can(point, x0, y0, scale, PW, PH, isRoT, Is_Rect=False)
        dot = Canvas.create_rectangle(canx-2, cany-2, canx+2, cany+2, fill='red')
        line_l.append(dot)
    for point in right_f:
        canx, cany = realxy2can(point, x0, y0, scale, PW, PH, isRoT, Is_Rect=False)
        dot = Canvas.create_rectangle(canx-2, cany-2, canx+2, cany+2, fill='blue')
        line_r.append(dot)
    return [line_l, line_r]


def plotcir(Canvas, point, scale, isRoT, lims, cansize, fill):
    x0, y0 = (lims[0][0]+lims[0][1])//2, (lims[1][1]+lims[1][0])//2
    [PW, PH] = cansize
    [canx, cany] = realxy2can(point, x0, y0, scale, PW, PH, isRoT, Is_Rect=False)
    circle = Canvas.create_oval(canx-5, cany-5, canx+5, cany+5, fill=fill)
    return circle