import os,sys
import tkinter as tk
import tkinter.messagebox


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('\\')]
pic_path = abs_path + '\\Pics\\'
root_path = abs_path[:abs_path.rfind('\\')]
if root_path+'\\Floorplan_Generation' not in sys.path: sys.path.append(root_path+'\\Floorplan_Generation')


import GUI_Base as GB
import GUI_Layout as GL
import FP_main


Dict_ZF = {'Resting': ['Bed', 'Wardrobe', 'Nightstand', 'Desk and Chair', 'Random'],
           'Living': ['Table and Chair', 'Sofa and TV', 'Random'],
           'Cooking': ['Kitchen Stove', 'Cupboard', 'Refrigerator', 'Trash Bin', 'Wash Machine', 'Random']}
Dict_ZC = {'Resting':'blue', 'Living':'red', 'Cooking':'green'}


class Page1st():
    def __init__(self, master):
        global img0, img1, img2, img3, img4
        self.master = master
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow)
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, 'Please select topologies of the layouts of the simulated houses:')
        self.topos = tk.Frame(self.face, )
        self.topos_u, self.topos_d = tk.Frame(self.topos, ), tk.Frame(self.topos, )
        img0 = GB.read_img(pic_path+'RC.JPG', 180, 65)
        img1 = GB.read_img(pic_path+'RL.JPG', 180, 65)
        img2 = GB.read_img(pic_path+'RCL.JPG', 300, 65)
        img3 = GB.read_img(pic_path+'RLC.JPG', 300, 65)
        img4 = GB.read_img(pic_path+'tRLC.JPG', 220, 160)
        self.v0, pc_frame0 = self.pic_check(self.topos_u, 'Resting-Cooking Zones', img0)
        pc_frame0.pack(side='left', padx=20, pady=20)
        self.v1, pc_frame1 = self.pic_check(self.topos_u, 'Resting-Living Zones', img1)
        pc_frame1.pack(side='left', padx=20, pady=20)
        self.v2, pc_frame2 = self.pic_check(self.topos_u, 'Resting-Cooking-Living Zones', img2)
        pc_frame2.pack(side='left', padx=20, pady=20)
        self.topos_u.pack()
        self.v3, pc_frame3 = self.pic_check(self.topos_d, 'Resting-Living-Cooking Zones', img3)
        pc_frame3.pack(side='left', padx=20, pady=20)
        self.v4, pc_frame4 = self.pic_check(self.topos_d, 'Triangle Topology', img4)
        pc_frame4.pack(side='left', padx=20, pady=20)
        self.v5 = tk.IntVar()
        tk.Checkbutton(self.topos_d, text='All Topologies', variable=self.v5, onvalue=1, offvalue=0, height=2).\
            pack(side='left', padx=20, pady=20)
        self.topos_d.pack()
        self.topos.pack()
        self.face.pack()

    def previous(self):
        tkinter.messagebox.showerror(title='Error', message='You CAN NOT go to the previous step!')

    def follow(self):
        global topo
        topo = [self.v0.get(), self.v1.get(), self.v2.get(), self.v3.get(), self.v4.get(), self.v5.get()]
        if topo == [0, 0, 0, 0, 0, 0]:
            tkinter.messagebox.showerror(title='Error', message='Please select at least one topology!')
        else:
            self.face.destroy()
            self.Bots.destroy()
            Page2nd(self.master)

    def pic_check(self, root, text, img):
        pc_frame = tk.Frame(root, )
        tk.Label(pc_frame, image=img).pack()
        var = tk.IntVar()
        tk.Checkbutton(pc_frame, text=text, variable=var, onvalue=1, offvalue=0, height=2).pack()
        return var, pc_frame


class Page2nd():
    def __init__(self, master):
        self.master = master
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow)
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, 'Please select the pieces of furniture in the simulated houses:')
        self.CheckButtons = tk.Frame(self.face, )
        self.tk_vars0 = self.CheButCol('Resting', Dict_ZF['Resting'])
        self.tk_vars1 = self.CheButCol('Cooking', Dict_ZF['Cooking'])
        self.tk_vars2 = self.CheButCol('Living', Dict_ZF['Living'])
        self.CheckButtons.pack()
        self.TextEntry = tk.Frame(self.face, )
        tk.Label(self.TextEntry, text='How many virtual houses will you generate?', font=('Helvetica 14 bold'), \
                 height=2).pack(side='left', padx=5, pady=10)
        self.Gennum = tk.StringVar()
        self.Gennum.set('0')
        tk.Entry(self.TextEntry, textvariable=self.Gennum, width=15, font=('Helvetica 12 bold')).pack(side='left', padx=5, pady=10)
        self.TextEntry.pack(padx=5, pady=10)
        self.face.pack()

    def previous(self):
        self.face.destroy()
        self.Bots.destroy()
        Page1st(self.master)

    def follow(self):
        list = [self.tk_vars0, self.tk_vars1, self.tk_vars2]
        varss = []
        for i in range(3):
            vars = []
            for tk_var in list[i]: vars.append(tk_var.get())
            varss.append(vars)
        N = int(self.Gennum.get())
        if N != 0 and varss[-1] == [0, 0, 0]:
            tkinter.messagebox.showerror(title='Error', message=\
                'Please select at least one piece of furniture in living zone!')
        else:
            S_r, N, stat, stat_Incre = FP_main.generate_house(N, topo, varss)
            self.face.destroy()
            self.Bots.destroy()
            GL.Page1st(self.master, S_r, N, stat, stat_Incre)



    def CheButCol(self, zone, furniture):
        color = Dict_ZC[zone]
        CheButCol = tk.Frame(self.CheckButtons, bg=color)
        tk.Label(CheButCol, text=zone+' Zone', font=('Helvetica 13 bold'), width=17, height=2, anchor='w', bg=color,
                 fg='white').pack()
        N = 6 - len(furniture)
        not_Lroom = len(furniture) > 3
        if not_Lroom:
            P_fur = furniture[0]
            tk.Label(CheButCol, text=P_fur, font=('Helvetica 11 bold'), width=12, height=2, anchor='w', bg=color,
                     fg='white').pack()
        tk_vars = []
        for fur in furniture[not_Lroom:]:
            var = tk.IntVar()
            tk.Checkbutton(CheButCol, text=fur, variable=var, font=('Helvetica 11 bold'), onvalue=1, offvalue=0,
                           width=14, height=2, anchor='w', bg=color, fg='white', selectcolor='black').pack()
            tk_vars.append(var)
        for i in range(N):
            tk.Label(CheButCol, text=' ', font=('Helvetica 11 bold'), width=12, height=2, bg=color, fg='white').pack()
        CheButCol.pack(side='left', padx=20, pady=10)
        return tk_vars

