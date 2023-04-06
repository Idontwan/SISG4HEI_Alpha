import sys, os
import tkinter as tk
import tkinter.messagebox
import numpy.random as rd


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('\\')]
root_path = abs_path[:abs_path.rfind('\\')]
if root_path not in sys.path: sys.path.append(root_path)
if root_path+'\\Interface' not in sys.path: sys.path.append(root_path + '\\Interface')
if root_path+'\\Floorplan_Generation' not in sys.path: sys.path.append(root_path+'\\Floorplan_Generation')
if root_path+'\\Human_Path_Generation' not in sys.path: sys.path.append(root_path + '\\Human_Path_Generation')
if root_path+'\\Human_Activities_Schedule_Generation' not in sys.path:
    sys.path.append(root_path+'\\Human_Activities_Schedule_Generation')
Data_path = root_path + '\\DataBase\\'
Outputspath = root_path + '\\Outputs\\'


import Tools_ as Tl
import GUI_Base as GB
import GUI_TravelPattern as GT
import Load, Plot
import ScreenPlot as SP
import FSave
import HSave
import HASave
import PIRRecord as PR
import TRNmain as TRN
import TGazebo as TGz


Colors = ['yellow', 'darkorange', 'black', 'purple', 'green']


def creat_floder(path):
    if not os.path.exists(path): os.makedirs(path)


class Page1st():
    def __init__(self, master, Savelist, Timess, Locationss, TPs, Records, savedTPs, stride, prefoot):
        self.savelist, self.savedTPs = Savelist, savedTPs
        self.timess, self.locationss = Timess, Locationss
        self.stride, self.perferf = stride, prefoot
        self.pindex, self.TPsindex, self.shownpaths = 0, 0, []
        self.robots, self.PIRSS = [[] for path in Savelist], [[] for path in Savelist]
        self.master = master
        self.TPs, self.Records = TPs, Records
        self.resample(plot=False)
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow)
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, 'Please determine the location of PIR sensors and robots:')
        self.Vframe = self.visualframe()
        self.Vframe.pack()
        Bots2 = tk.Frame(self.face, )
        texts = ['Previous House', 'Resample', 'Next House']
        funcs = [self.prevLay, self.resample, self.nextLay]
        for i in range(3):
            tk.Button(Bots2, text=texts[i], width=15, height=1, font=('Helvetica 12 bold'), command=funcs[i]) \
                .grid(row=0, column=i, padx=10, pady=10)
        Bots2.pack(side='bottom')
        self.face.pack()

    def previous(self):
        self.face.destroy()
        self.Bots.destroy()
        GT.Page1st(self.master, self.savelist, self.timess, self.locationss, self.stride, self.perferf)

    def follow(self):
        if ([] not in self.robots) and ([] not in self.PIRSS):
            SavedTPs = [[] for path in self.savelist]
            self.pindex = 0
            while self.pindex < len(self.savelist):
                for j in range(len(self.endidss[self.pindex])):
                    j_ = self.endidss[self.pindex][j]
                    key_ = self.deter_key_(self.locationss[self.pindex], j_)
                    key = self.deterkey(key_, self.patidss[self.pindex][j])
                    SavedTPs[self.pindex].append([key, self.TPs[self.pindex][key]])
                self.pindex += 1
            self.face.destroy()
            self.Bots.destroy()
            Page2nd(self.master, self.savelist, self.timess, self.locationss, SavedTPs, self.endidss, self.patidss,
                    self.robots, self.PIRSS)
        else:
            for i in range(len(self.savelist)):
                if self.robots[i] == []:
                    tkinter.messagebox.showerror(title='Error', message='You DID NOT place a robot in house %d!' % (i))
                if self.PIRSS[i] == []:
                    tkinter.messagebox.showerror(title='Error', message='You DID NOT place a PIR sensor in house %d!' % (i))

    def visualframe(self):
        Frame = tk.Frame(self.face, )
        self.ivPIR, self.ivROB = tk.IntVar(), tk.IntVar()
        self.Canvas = self.layout(Frame)
        self.plotTP()
        self.plotROBPIRs()
        self.Canvas.pack(side='left')
        Frame_r = tk.Frame(Frame, )
        tk.Button(Frame_r, text='Random', width=15, height=1, font=('Helvetica 12 bold'), command=self.random) \
            .pack(pady=5)
        tk.Checkbutton(Frame_r, text='Place PIR sensors', font=('Helvetica 12 bold'), variable=self.ivPIR, onvalue=1,
                       offvalue=0).pack(pady=5)
        tk.Checkbutton(Frame_r, text='Place robot', font=('Helvetica 12 bold'), variable=self.ivROB, onvalue=1,
                       offvalue=0).pack(pady=5)
        tk.Button(Frame_r, text='Previous Pattern', width=15, height=1, font=('Helvetica 12 bold'), command=self.prevP) \
            .pack(pady=5)
        tk.Button(Frame_r, text='Next Pattern', width=15, height=1, font=('Helvetica 12 bold'), command=self.nextP) \
            .pack(pady=5)
        Frame_r.pack(side='right')
        return Frame

    def layout(self, root):
        Canvas = tk.Canvas(root, bg='white', height=370, width=640)
        path = self.savelist[self.pindex]
        path_l = path.split('\\')
        house_js = Load.load_se_map(path_l[0], path_l[1], path_l[2])
        self.rooms, T_Bs, furnitures, doors, walls, self.lims = Load.dic2house(house_js)
        Fur_set, self.scale, self.IsROT, Fur_indexs = SP.layoutplot(Canvas, [640, 370], self.rooms, T_Bs, furnitures, doors,
                                                                    walls, self.lims, showbg=False)
        Canvas.bind('<Button-1>', self.mouseleft)
        Canvas.bind('<Button-3>', self.mouseright)
        self.shownpaths = []
        self.shownRP = [[], []]
        return Canvas

    def plotTP(self):
        self.pathnum = min(5, len(self.patidss[self.pindex]))
        for i in range(self.TPsindex, self.TPsindex+self.pathnum):
            key_ = self.deter_key_(self.locationss[self.pindex], self.endidss[self.pindex][i])
            key = self.deterkey(key_, self.patidss[self.pindex][i])
            bcxys = self.TPs[self.pindex][key][0]
            BCline = SP.plotBCline(self.Canvas, bcxys, self.scale, self.IsROT, self.lims, [640, 370],
                                   fill=Colors[i-self.TPsindex])
            self.shownpaths.append(BCline)

    def deter_key_(self, locations, j):
        return 'Direct,'+locations[j-1]+','+locations[j] if locations[j] != 'Wander' \
            else 'Wander,'+locations[j-1]+','+locations[j+1]

    def deterkey(self, key_, j):
        if key_[0] == 'D': return key_+','+self.Records[self.pindex][key_][j]
        return self.Records[self.pindex][key_][j]

    def plotROBPIRs(self):
        point = self.robots[self.pindex]
        if point != []:
            robP = SP.plotcir(self.Canvas, point, self.scale, self.IsROT, self.lims, [640, 370], 'red')
            self.shownRP[0].append(robP)
        points = self.PIRSS[self.pindex]
        if points != []:
            for point in points:
                robP = SP.plotcir(self.Canvas, point, self.scale, self.IsROT, self.lims, [640, 370], 'blue')
                self.shownRP[1].append(robP)

    def prevLay(self):
        if self.pindex > 0:
            self.pindex -= 1
            self.Canvas.destroy()
            self.Canvas = self.layout(self.Vframe)
            self.plotTP()
            self.plotROBPIRs()
            self.Canvas.pack(side='left')
        else: tkinter.messagebox.showerror(title='Error', message='This is the FIRST house!')

    def nextLay(self):
        if self.pindex < len(self.savelist)-1:
            self.pindex += 1
            self.Canvas.destroy()
            self.Canvas = self.layout(self.Vframe)
            self.plotTP()
            self.plotROBPIRs()
            self.Canvas.pack(side='left')
        else: tkinter.messagebox.showerror(title='Error', message='This is the LAST house!')

    def random(self):
        path = self.savelist[self.pindex]
        disval = Tl.load_disval(path)
        robot_x, robot_y = Tl.robot_position(self.rooms, self.lims, disval, self.originbcs[self.pindex])
        self.robots[self.pindex] = [robot_x, robot_y]
        PIRs = Tl.PIR_position(self.rooms, self.lims, disval)
        self.PIRSS[self.pindex] = PIRs
        for i in range(2):
            for point in self.shownRP[i]: self.Canvas.delete(point)
        self.shownRP = [[], []]
        self.plotROBPIRs()

    def resample(self, plot=True):
        self.endidss, self.patidss, self.originbcs = [], [], []
        for i in range(len(self.savelist)):
            self.endidss.append([])
            self.patidss.append([])
            for j in range(1, len(self.locationss[i])):
                if self.locationss[i][j-1] != 'Wander':
                    self.endidss[-1].append(j)
                    if (i, j) in self.savedTPs: rk = self.savedTPs[(i, j)]
                    else:
                        key_ = self.deter_key_(self.locationss[i], j)
                        rk = rd.randint(len(self.Records[i][key_]))
                    self.patidss[-1].append(rk)
            key_ = self.deter_key_(self.locationss[i], 1)
            key = key_+','+self.Records[i][key_][self.patidss[i][0]] if key_[0] == 'D' \
                else self.Records[i][key_][self.patidss[i][0]]
            bcxys = self.TPs[i][key][0][0][:2]
            self.originbcs.append(bcxys)
        for path in self.shownpaths: self.Canvas.delete(path)
        self.shownpaths = []
        if plot: self.plotTP()

    def prevP(self):
        if self.TPsindex > 0:
            self.TPsindex -= 1
            deleted_path = self.shownpaths.pop()
            self.Canvas.delete(deleted_path)
            key_ = self.deter_key_(self.locationss[self.pindex], self.endidss[self.pindex][self.TPsindex])
            key = self.deterkey(key_, self.patidss[self.pindex][self.TPsindex])
            bcxys = self.TPs[self.pindex][key][0]
            BCline = SP.plotBCline(self.Canvas, bcxys, self.scale, self.IsROT, self.lims, [640, 370], fill=Colors[0])
            self.shownpaths = [BCline] + self.shownpaths
            for i in range(1, self.pathnum): self.Canvas.itemconfig(self.shownpaths[i], fill=Colors[i])
        else: tkinter.messagebox.showerror(title='Error', message='This is the FIRST pattern!')

    def nextP(self):
        if self.TPsindex+self.pathnum < len(self.endidss[self.pindex]) - 1:
            self.TPsindex += 1
            deleted_path = self.shownpaths.pop(0)
            self.Canvas.delete(deleted_path)
            key_ = self.deter_key_(self.locationss[self.pindex], self.endidss[self.pindex][self.TPsindex+self.pathnum])
            key = self.deterkey(key_, self.patidss[self.pindex][self.TPsindex+self.pathnum])
            bcxys = self.TPs[self.pindex][key][0]
            BCline = SP.plotBCline(self.Canvas, bcxys, self.scale, self.IsROT, self.lims, [640, 370],
                                   fill=Colors[self.pathnum-1])
            self.shownpaths.append(BCline)
            for i in range(self.pathnum-1): self.Canvas.itemconfig(self.shownpaths[i], fill=Colors[i])
        else: tkinter.messagebox.showerror(title='Error', message='This is the LAST pattern!')

    def mouseleft(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        x0, y0 = (self.lims[0][0]+self.lims[0][1])//2, (self.lims[1][0]+self.lims[1][1])//2
        realpoint = SP.canxy2real([xc, yc], x0, y0, self.scale, 640, 370, self.IsROT)
        if self.ivPIR.get()==1 and self.ivROB.get()==1:
            tkinter.messagebox.showerror(title='Error', message='You CAN NOT place robot and PIR sensor at the same time!')
        elif self.ivROB.get() == 1:
            self.robots[self.pindex] = realpoint
            if self.shownRP[0] != []: self.Canvas.delete(self.shownRP[0][0])
            robP = SP.plotcir(self.Canvas, realpoint, self.scale, self.IsROT, self.lims, [640, 370], 'red')
            self.shownRP[0] = [robP]
        elif self.ivPIR.get() == 1:
            if len(self.shownRP[1])>3:
                tkinter.messagebox.showerror(title='Error', message='You CAN NOT place more PIR sensor!')
            else:
                self.PIRSS[self.pindex].append(realpoint)
                pirP = SP.plotcir(self.Canvas, realpoint, self.scale, self.IsROT, self.lims, [640, 370], 'blue')
                self.shownRP[1].append(pirP)

    def mouseright(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        if self.ivPIR.get()==1 and self.ivROB.get()==1:
            tkinter.messagebox.showerror(title='Error', message='You CAN NOT delete robot and PIR sensor at the same time!')
        elif self.ivROB.get() == 1:
            if self.shownRP[0] != []: self.Canvas.delete(self.shownRP[0][0])
            self.shownRP[0], self.robots[self.pindex] = [], []
        elif self.ivPIR.get()==1 and self.shownRP[1]!=[]:
            deleted_item = self.Canvas.find_closest(xc, yc)[0]
            if deleted_item in self.shownRP[1]:
                self.Canvas.delete(deleted_item)
                self.shownRP[1].remove(deleted_item)


class Page2nd():
    def __init__(self, master, Savelist, timess, locationss, SavedTPs, endidss, patidss, robots, PIRSS):
        self.master = master
        self.savelist, self.timess, self.locationss = Savelist, timess, locationss
        self.TPss, self.endidss, self.patidss = SavedTPs, endidss, patidss
        self.robots, self.PIRSS = robots, PIRSS
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow)
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, 'Please select the classes of data which you want to save:')
        Terms = ['Semantic Layout', 'Height Function', 'Discomfortable Field', 'Weighted Distances',
                 'Travel Patterns', 'Activity Schedule', 'PIR Sensor Records', 'Files for Stage',
                 'Files for Gazebo']
        self.ivars = [tk.IntVar() for i in range(15)]
        up_Frame = tk.Frame(self.face, )
        for i in range(3):
            subF = tk.Frame(up_Frame, )
            for j in range(2):
                subsubF = tk.Frame(subF, )
                tk.Label(subsubF, text=Terms[i*2+j], font=('Helvetica 12 bold'), height=2).pack(side='left')
                tk.Checkbutton(subsubF, text='Data', variable=self.ivars[4*i+2*j], font=('Helvetica 12 bold'),
                               onvalue=1, offvalue=0).pack(side='left')
                tk.Checkbutton(subsubF, text='Figure', variable=self.ivars[4*i+2*j+1], font=('Helvetica 12 bold'),
                               onvalue=1, offvalue=0).pack(side='left')
                subsubF.pack(padx=10, side='left')
            subF.pack()
        up_Frame.pack(pady=20)
        down_Frame = tk.Frame(self.face, )
        for i in range(6, 9):
            tk.Checkbutton(down_Frame, text=Terms[i], variable=self.ivars[i+6], font=('Helvetica 12 bold'),
                           onvalue=1, offvalue=0).pack(side='left', padx=2)
        down_Frame.pack(pady=20)
        self.face.pack()

    def previous(self):
        tkinter.messagebox.showerror(title='Error', message='You CAN NOT go to the previous step!')

    def follow(self):
        if self.ivars[12].get()==0 and self.ivars[13].get()==0 and self.ivars[14].get()==0:
            tkinter.messagebox.showerror(title='Error', message='You SHOULD select one output at least!')
        elif self.ivars[4].get()==0 and self.ivars[5].get()!=0:
            tkinter.messagebox.showerror(title='Error', message='You CAN NOT plot discomfortable field without data!')
        elif self.ivars[6].get()==0 and self.ivars[7].get()!=0:
            tkinter.messagebox.showerror(title='Error', message='You CAN NOT plot weighted distances without data!')
        elif self.ivars[8].get()==0 and self.ivars[9].get()!=0:
            tkinter.messagebox.showerror(title='Error', message='You CAN NOT plot travel patterns without data!')
        elif self.ivars[10].get()==0 and self.ivars[11].get()!=0:
            tkinter.messagebox.showerror(title='Error', message='You CAN NOT plot activity schedule without data!')
        else:
            for i in range(len(self.savelist)):
                outputpath = Outputspath + str(i)
                datapath = Data_path + self.savelist[i]
                creat_floder(outputpath)
                [h_v, fname0, fname1] = self.savelist[i].split('\\')
                House_dict = Load.load_se_map(h_v, fname0, fname1)
                rooms, TBs, furs, doors, walls, lims = Load.dic2house(House_dict)
                H_dict = Load.load_normaljson('Height_Function', h_v, fname0, fname1)
                TPs = [self.TPss[i][k][1][0] for k in range(len(self.TPss[i]))]
                if self.ivars[0].get(): FSave.save_normaljson(outputpath, House_dict, 'Semantic')
                if self.ivars[1].get():
                    Plot.layout_plot(TBs, furs, doors, walls, lims)
                    Plot.save_plot(outputpath, 'Layout')
                if self.ivars[2].get(): FSave.save_normaljson(outputpath, H_dict, 'Height_Function')
                if self.ivars[3].get():
                    Hdata = Plot.height2feild(lims, H_dict)
                    Plot.filed_plot(None, None, None, None, lims, Hdata, 0, 340, layout=False)
                    Plot.save_plot(outputpath, 'Height_Function')
                if self.ivars[4].get():
                    Disfield = Load.load_filed('Discomfortable_value', h_v, fname0, fname1)
                    HSave.save_filed('Discomfortable_value', outputpath, '%5.2f', Disfield)
                if self.ivars[5].get():
                    Plot.filed_plot(TBs, furs, doors, walls, lims, Disfield, 1, 5, masked_v=99)
                    Plot.save_plot(outputpath, 'Discomfortable_value')
                if self.ivars[6].get():
                    acts = Load.fname2act(fname0)
                    Distances = []
                    max_diss_d = Load.load_normaljson('Max_Distances', h_v, fname0, fname1)
                    for act in acts:
                        f_name = act + '_distance'
                        Distance = Load.load_filed(f_name, h_v, fname0, fname1)
                        Distances.append(Distance)
                        HSave.save_filed(f_name, outputpath, '%7.2f', Distance)
                if self.ivars[7].get():
                    for j in range(len(acts)):
                        Plot.filed_plot(TBs, furs, doors, walls, lims, Distances[j], 0, max_diss_d[acts[j]],
                                        masked_v=99998)
                        f_name = acts[j] + '_distance'
                        Plot.save_plot(outputpath, f_name)
                if self.ivars[8].get():
                    TP_dict = {}
                    for [key, TraP] in self.TPss[i]:
                        TP_dict[key] = TraP
                    HSave.save_normaljson(outputpath, TP_dict, 'Human_Path')
                if self.ivars[9].get():
                    keys = list(TP_dict)
                    for key in keys:
                        Plot.path_plot(TBs, furs, doors, walls, lims, key, TP_dict[key][0], TP_dict[key][1:])
                        Plot.save_plot(outputpath, 'Path,'+key)
                if self.ivars[10].get():
                    times, nacts, durs = Load.read_actseq(h_v, fname0, fname1)
                    HASave.save_actseq(outputpath, times, nacts, durs)
                if self.ivars[11].get():
                    Plot.Plot_ActSeq(times, durs, nacts, outputpath)
                if self.ivars[12].get():
                    PIRlog = PR.PIRrecords(self.PIRSS[i], TPs, self.timess[i], self.endidss[i], self.locationss[i])
                    PR.save_records(outputpath, PIRlog)
                if self.ivars[13].get():
                    robot_x, robot_y = self.robots[i][0], self.robots[i][1]
                    TRN.main(i, H_dict, House_dict, robot_x, robot_y)
                if self.ivars[14].get():
                    TGz.main(rooms, TBs, doors, walls, lims, H_dict, i, TPs)
            tkinter.messagebox.showinfo(title='Info', message='CONGRATULATION! You have completed all procedures!')
            self.master.quit()