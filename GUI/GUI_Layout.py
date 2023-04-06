import sys, os
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('\\')]
root_path = abs_path[:abs_path.rfind('\\')]
if root_path not in sys.path: sys.path.append(root_path)
if root_path+'\\Floorplan_Generation' not in sys.path: sys.path.append(root_path + '\\Floorplan_Generation')
if root_path+'\\Human_Path_Generation' not in sys.path: sys.path.append(root_path + '\\Human_Path_Generation')


import GUI_Base as GB
import GUI_Semantic as GS
import GUI_ActivitySchedule as GAS
import Load
import ScreenPlot as SP
import FSave
import HP_main


Fur_list = [['Bed', 'Wardrobe', 'Desk and Chair'], ['Kitchen Stove', 'Cupboard', 'Refrigerator',
            'Wash Machine', 'Trash Bin'], ['Sofa and TV', 'Table and Chair']]
Map_act2Fur = {'Sleep': 'Bed', 'Dress_up': 'Wardrobe', 'Work': 'Desk Chair', 'Watch_TV': 'Sofa',
               'Dining': 'Dining Table Chair', 'Cooking0': 'Kitchen Stove', 'Cooking1': 'Cupboard',
               'Cooking2': 'Refrigerator', 'Washing': 'Wash Machine', 'Cleaning': 'Trash _Bin',
               'Go_out': 'Entrance', 'Go_to_Toilet': 'Toilet Door', 'Go_to_Bathroom': 'Bathroom Door'}


class Page1st():
    def __init__(self, master, S_r, N, stat, stat_Incre):
        self.S_r, self.N = S_r, N
        self.stat = [stat[i] for i in range(len(stat))]
        self.stat_Incre = [stat_Incre[i] for i in range(len(stat_Incre))]
        stat.insert(5, sum(stat[:5]))
        stat_Incre.insert(5, int(S_r*N))
        self.master = master
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow)
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, 'Statistics of semantics of houses in the database:')
        text0 = 'You successfully generated %d simulated houses, the successful ratio is %.2f%%.' \
                %(int(S_r*N), 100*S_r)
        tk.Label(self.face, text=text0, width=80, height=2, font=('Helvetica 13 bold')).pack()
        texts1 = ['Topo%d: %d(+%d)' % (i, stat[i], stat_Incre[i]) for i in range(5)]
        texts1.append('All: %d(+%d)' % (stat[5], stat_Incre[5]))
        texts2, ii = [], 0
        for i in range(3):
            for j in range(5):
                if j < len(Fur_list[i]):
                    text = ': %d(+%d)' % (stat[5+ii], stat_Incre[5+ii])
                    ii += 1
                    texts2.append(Fur_list[i][j] + text)
                else: texts2.append(' ')
        Lab_Fra_up = tk.Frame(self.face, )
        self.build_LabFra(Lab_Fra_up, texts1, col_pre=False)
        Lab_Fra_up.pack(padx=10, pady=10)
        Lab_Fra_down = tk.Frame(self.face, )
        self.build_LabFra(Lab_Fra_down, texts2)
        Lab_Fra_down.pack(padx=10, pady=10)
        self.face.pack()

    def previous(self):
        self.face.destroy()
        self.Bots.destroy()
        GS.Page1st(self.master)

    def follow(self):
        self.face.destroy()
        self.Bots.destroy()
        Page2nd(self.master, self.S_r, self.N, self.stat, self.stat_Incre)

    def build_LabFra(self, root, texts, column=3, col_pre=True):
        N = len(texts)
        row = N // column
        [T0, T1] = [column, row] if col_pre else [row, column]
        for i in range(T0):
            for j in range(T1):
                [tt0, tt1] = [i, j] if col_pre else [j, i]
                tk.Label(root, text=texts[i*T1+j], font=('Helvetica 12 bold'), width=22, height=2,\
                         anchor='w').grid(padx=10, row=tt1, column=tt0)


class Page2nd():
    def __init__(self, master, S_r, N, stat, stat_Incre):
        self.S_r, self.N = S_r, N
        self.stat = [stat[i] for i in range(len(stat))]
        self.stat_Incre = [stat_Incre[i] for i in range(len(stat_Incre))]
        total_num = sum(stat[:5])
        self.varvals = [2 if stat[i] == total_num else 0 for i in range(14)]
        self.map_Che_val, self.map_Com_val = [], []
        for i in range(5):
            if 0 < stat[i] < total_num: self.map_Che_val.append(i)
        for i in range(5, 14):
            if 0 < stat[i] < total_num: self.map_Com_val.append(i)
        self.vars = [tk.IntVar() for i in range(len(self.map_Che_val))]
        self.var_count = 0
        self.strs = [tk.StringVar() for i in range(len(self.map_Com_val))]
        self.str_count = 0
        self.Pathlist = []
        self.master = master
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow, extras=[['Search', self.search]])
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, 'Please select the houses with topologies, sizes and furniture from database:')
        self.topoFra()
        self.sizeFra()
        self.furnFra()
        self.face.pack()


    def previous(self):
        self.face.destroy()
        self.Bots.destroy()
        Page1st(self.master, self.S_r, self.N, self.stat, self.stat_Incre)

    def follow(self):
        if self.Pathlist == []:
            tkinter.messagebox.showerror(title='Error', message='You DID NOT select any houses!')
        else:
            self.face.destroy()
            self.Bots.destroy()
            Page3rd(self.master, self.Pathlist)


    def search(self):
        for i in range(len(self.map_Che_val)):
            self.varvals[self.map_Che_val[i]] = 2*self.vars[i].get()
        for i in range(len(self.map_Com_val)):
            if self.strs[i].get() == 'Must be in': self.varvals[self.map_Com_val[i]] = 2
            elif self.strs[i].get() == 'May be in': self.varvals[self.map_Com_val[i]] = 1
        Ranges = [self.ranges[i].get() for i in range(10)]
        N, self.Pathlist = Load.search(self.varvals, Ranges)
        Info = 'There are %d houses which satisfy your requirement' % (N)
        tkinter.messagebox.showinfo(title='Info', message=Info)

    def topoFra(self):
        TopoFra = tk.Frame(self.face, )
        for i in range(5):
            if i not in self.map_Che_val:
                mustornot = 'o ' if self.varvals == 2 else 'x '
                text = mustornot + 'Topo' + str(i)
                tk.Label(TopoFra, text=text, font=('Helvetica 12 bold'), width=10, height=2\
                         ).pack(side='left', padx=5)
            else:
                tk.Checkbutton(TopoFra, text='Topo'+str(i), font=('Helvetica 12 bold'), \
                               variable=self.vars[self.var_count], onvalue=1, offvalue=0, \
                               width=8, height=2).pack(side='left', padx=5)
                self.var_count += 1
        TopoFra.pack(pady=10)

    def sizeFra(self):
        rooms = ['House', 'Resting Zone', 'Cooking Zone', 'Living Zone']
        strs = ['area of '+rooms[i]+' [' for i in range(4)]
        strs.insert(1, 'aspect ratio of House')
        SizeFra = tk.Frame(self.face, )
        self.ranges = []
        Rangestrs = [['29', '56'], ['1.0', '3.5'], ['8', '16'], ['6', '12'], ['12', '24']] # original lims
        SizeFra_up = tk.Frame(SizeFra, )
        for i in range(2): self.LabmixTen(SizeFra_up, strs[i], Rangestrs[i][0], Rangestrs[i][1])
        SizeFra_up.pack()
        SizeFra_down = tk.Frame(SizeFra, )
        for i in range(2, 5): self.LabmixTen(SizeFra_down, strs[i], Rangestrs[i][0], Rangestrs[i][1])
        SizeFra_down.pack()
        SizeFra.pack(pady=10)

    def LabmixTen(self, root, text, downlim, uplim):
        LabmixTen = tk.Frame(root, )
        tk.Label(LabmixTen, text=text, font=('Helvetica 12 bold'), height=2).pack(side='left')
        strTK0 = tk.StringVar(value=downlim)
        Ent0 = tk.Entry(LabmixTen, textvariable=strTK0, font=('Helvetica 12 bold'), width=4)
        self.ranges.append(strTK0)
        Ent0.pack(side='left')
        tk.Label(LabmixTen, text=', ', font=('Helvetica 12 bold'), height=2).pack(side='left')
        strTK1 = tk.StringVar(value=uplim)
        Ent1 = tk.Entry(LabmixTen, textvariable=strTK1, font=('Helvetica 12 bold'), width=4)
        self.ranges.append(strTK1)
        Ent1.pack(side='left')
        str = ']m^2' if text[:4]=='area' else ']'
        tk.Label(LabmixTen, text=str, font=('Helvetica 12 bold'), height=2).pack(side='left')
        LabmixTen.pack(side='left', padx=2)

    def furnFra(self):
        FurnFra = tk.Frame(self.face)
        C = 0
        C = self.col_frunFra(FurnFra, Fur_list[0], 4, C, self.map_Com_val, [2]+self.varvals[5:7])
        C = self.col_frunFra(FurnFra, Fur_list[1], 7, C, self.map_Com_val, self.varvals[7:12])
        C = self.col_frunFra(FurnFra, Fur_list[2], 12, C, self.map_Com_val, self.varvals[7:12])
        FurnFra.pack(pady=10)

    def Combox(self, root, strvar):
        Combox = ttk.Combobox(root, textvariable=strvar, font=('Helvetica 12 bold'), width=9)
        Combox['values'] = ('Not be in', 'May be in', 'Must be in')
        Combox.current(1)
        Combox.pack(side='right')

    def col_frunFra(self, root, furnames, C0, C1, maps, varvals):
        Col_furFra = tk.Frame(root, )
        N = len(furnames)
        for i in range(5):
            if i < N:
                Frame = tk.Frame(Col_furFra, )
                tk.Label(Frame, text=furnames[i]+': ', font=('Helvetica 12 bold'), width=15, height=2, \
                         anchor='e').pack(side='left')
                if i+C0 not in maps:
                    if varvals[i] == 2:
                        tk.Label(Frame, text='Must be in', font=('Helvetica 12 bold'), width=9, height=2, \
                                 anchor='w').pack(side='right')
                    else:
                        tk.Label(Frame, text='Not be in', font=('Helvetica 12 bold'), width=9, height=2, \
                                 anchor='w').pack(side='right')
                else:
                    self.Combox(Frame, self.strs[C1])
                    C1 += 1
                Frame.pack()
            else:
                tk.Label(Col_furFra, text=' ', font=('Helvetica 12 bold'), width=24, height=2).pack()
        Col_furFra.pack(side='left', padx=5)
        return C1


class Page3rd():
    def __init__(self, master, Pathlist):
        self.master = master
        self.Pathlist = Pathlist
        self.Savedlist = []
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow)
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, 'Please select the houses (you can modify the layout):')
        self.path_index, self.path_num = 0, len(Pathlist)
        self.Layout = self.canvas(self.face, self.Pathlist[0])
        self.Layout.pack(pady=5)
        Bots2 = tk.Frame(self.face, )
        tk.Button(Bots2, text='Previous House', width=16, height=1, font=('Helvetica 12 bold'), \
                  command=self.prevLay) .grid(row=0, column=0, padx=10, pady=5)
        tk.Button(Bots2, text='Reset', width=16, height=1, font=('Helvetica 12 bold'), \
                  command=self.reset).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(Bots2, text='Save', width=16, height=1, font=('Helvetica 12 bold'), \
                  command=self.save).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(Bots2, text='Next House', width=16, height=1, font=('Helvetica 12 bold'), \
                  command=self.nextLay).grid(row=0, column=3, padx=10, pady=5)
        Bots2.pack(side='bottom')

    def previous(self):
        tkinter.messagebox.showerror(title='Error', message='You CAN NOT go to the previous step!')

    def follow(self):
        if self.Savedlist == []:
            tkinter.messagebox.showerror(title='Error', message='You DID NOT save any houses!')
        else:
            Is_Connect, Nocon_act, Nocon_path = HP_main.all_distance(self.Savedlist)
            if not Is_Connect:
                self.path_index = self.Savedlist.index(Nocon_path)
                self.Layout.destroy()
                self.Layout = self.canvas(self.face, Nocon_path)
                self.Layout.pack(pady=5)
                ertext = '%s CAN NOT be arrived in this house!' % (Map_act2Fur[Nocon_act])
                tkinter.messagebox.showerror(title='Error', message=ertext)
            else:
                self.face.destroy()
                self.Bots.destroy()
                GAS.Page1st(self.master, self.Savedlist)

    def prevLay(self):
        if self.path_index > 0:
            self.path_index -= 1
            self.Layout.destroy()
            self.Layout = self.canvas(self.face, self.Pathlist[self.path_index])
            self.Layout.pack(pady=5)
        else: tkinter.messagebox.showinfo(title='Info', message='This is the FIRST house!')

    def nextLay(self):
        if self.path_index < self.path_num-1:
            self.path_index += 1
            self.Layout.destroy()
            self.Layout = self.canvas(self.face, self.Pathlist[self.path_index])
            self.Layout.pack(pady=5)
        else: tkinter.messagebox.showinfo(title='Info', message='This is the LAST house!')

    def save(self):
        s_path = self.Pathlist[self.path_index]
        if s_path not in self.Savedlist: self.Savedlist.append(s_path)
        s_pathli = s_path.split('\\')
        rjTBcon = s_pathli[-1].split(',')[-1]
        type, rj, T_con, B_con = int(s_pathli[0]), rjTBcon[:-2], rjTBcon[-2], rjTBcon[-1][-1]
        House_name = ['Bedroom', 'Kitchen', 'Livingroom']
        for i in range(3):
            if T_con == House_name[i][0]: T_con = House_name[i]
            if B_con == House_name[i][0]: B_con = House_name[i]
        self.update_Fur()
        _, _, _, _ = FSave.data_save(type, self.rooms, self.T_Bs, self.furnitures, self.doors, self.walls, \
                                     T_con, B_con, self.lims, rj=rj)
        FSave.Height_SampleSave(type, self.rooms, self.T_Bs, self.furnitures, root_path+'\\DataBase\\'+s_path)

    def reset(self):
        self.Layout.destroy()
        self.Layout = self.canvas(self.face, self.Pathlist[self.path_index])
        self.Layout.pack(pady=5)

    def canvas(self, root, path):
        Canvas = tk.Frame(root, )
        self.figure(Canvas, path)
        Right = tk.Frame(Canvas, )
        Legend = tk.Frame(Right, )
        name_color = [['Legend', None], ['Resting Zone', 'blue'], ['Living Zone', 'red'],
                      ['Cooking Zone', 'green'], ['Toilet', 'yellow'], ['Bathroom', 'purple']]
        for i in range(6):
            tk.Label(Legend, text=name_color[i][0], bg=name_color[i][1], font=('Helvetica 12 bold'), \
                     width=15).pack(pady=5)
        Legend.pack(pady=10)
        self.Modify = tk.IntVar()
        tk.Checkbutton(Right, text='Modification', width=15, font=('Helvetica 12 bold'), \
                       variable=self.Modify, onvalue=1, offvalue=0).pack(pady=5)
        self.Furniture = tk.StringVar()
        self.Combox = ttk.Combobox(Right, textvariable=self.Furniture, font=('Helvetica 12 bold'), width=20)
        self.Combox['values'] = ('Bed', 'Wardrobe (WaR)', 'Desk and Chair', 'Kitchen Stove (KS)', 'Cupboard (Cb)',
                            'Refrigerator (Rfa)', 'Wash Machine (WM)', 'Trash Bin (TB)', 'Table and Chair (DTa)',
                            'Sofa and TV')
        self.Combox.current(1)
        self.Combox.pack(pady=5)
        Right.pack(padx=10, side='right')
        self.face.pack()
        return Canvas

    def figure(self, root, path):
        self.Canvas = tk.Canvas(root, bg='white', height=370, width=640)
        path_l = path.split('\\')
        house_js = Load.load_se_map(path_l[0], path_l[1], path_l[2])
        self.rooms, self.T_Bs, self.furnitures, self.doors, self.walls, self.lims = Load.dic2house(house_js)
        self.Fur_set, self.scale, self.IsROT, self.Fur_indexs = \
            SP.layoutplot(self.Canvas, [640, 370], self.rooms, self.T_Bs, self.furnitures, self.doors, self.walls, self.lims)
        self.Canvas.pack(side='left')
        self.Canvas.bind('<Button-1>', self.mousepick)
        self.Canvas.bind('<B1-Motion>', self.mousedrag)

    def mousepick(self, event):
        if self.Modify.get() == 1:
            widget = event.widget
            self.mousexy = [widget.canvasx(event.x), widget.canvasx(event.y)]

    def mousedrag(self, event):
        if self.Modify.get() == 1:
            index = self.Combox['values'].index(self.Furniture.get())
            widget = event.widget
            xc = widget.canvasx(event.x)
            yc = widget.canvasx(event.y)
            for item in self.Fur_set[index]:
                self.Canvas.move(item, xc - self.mousexy[0], yc - self.mousexy[1])
            self.mousexy = [xc, yc]

    def update_Fur(self):
        new_Fur = []
        oxo, oyo = (self.lims[0][0]+self.lims[0][1])//2, (self.lims[1][0]+self.lims[1][1])//2
        for i, room in enumerate(self.furnitures):
            new_Fur.append([])
            for fur in room:
                [x, y, L, W, name] = fur
                fur_index = self.Fur_indexs[i][name].pop()
                canxys = self.Canvas.coords(fur_index)
                self.Fur_indexs[i][name].append(fur_index)
                [nx, ny] = SP.canxy2real(canxys, oxo, oyo, self.scale, 640, 370, self.IsROT)
                new_Fur[i].append([nx-L//2, ny-W//2, L, W, name])
        self.furnitures = new_Fur