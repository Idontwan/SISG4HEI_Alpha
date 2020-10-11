import sys, os
import tkinter as tk
import tkinter.messagebox


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('/')]
root_path = abs_path[:abs_path.rfind('/')]
if root_path not in sys.path: sys.path.append(root_path)
if root_path+'/Human_Path_Generation' not in sys.path: sys.path.append(root_path + '/Human_Path_Generation')


import GUI_Base as GB
import GUI_Interface as GI
import HP_main
import Load
import ScreenPlot as SP


Iact2Pla = {'Sleep': 'Bed', 'Dress_up': 'Wardrobe', 'Work': 'Desk', 'Watch_TV': 'Sofa', 'Dining': 'Dining Table',
            'Cooking0': 'Kitchen Stove', 'Cooking1': 'Cupboard', 'Cooking2': 'Refrigerator', 'Washing': 'Wash Machine',
            'Cleaning': 'Trash Bin', 'Go_out': 'Entrance', 'Go_to_Toilet': 'Toilet Door', 'Go_to_Bathroom': 'Bathroom Door'}


class Page1st():
    def __init__(self, master, Savelist, Timess, Locationss, stride, perferfoot):
        self.savelist, self.savedTPs = Savelist, {}
        self.timess, self.locationss = Timess, Locationss
        self.stride, self.perferf = int(stride), perferfoot
        self.pindex, self.TPindex, self.saindex = 0, 1, 0
        self.hasBCline, self.hasFPline = tk.IntVar(), tk.IntVar()
        self.key, self.key_ = '', ''
        self.master = master
        self.TPs, self.Records = HP_main.path_generate(self.savelist, self.timess, self.locationss, self.stride, self.perferf)
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow)
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, 'Please select travel patterns:')
        self.Vframe = self.visualframe()
        self.Vframe.pack()
        Bots2 = tk.Frame(self.face, )
        texts = ['Previous House', 'Previous Sample', 'Save', 'Next Sample', 'Next House']
        funcs = [self.prevLay, self.prevSam, self.save, self.nextSam, self.nextLay]
        for i in range(5):
            tk.Button(Bots2, text=texts[i], width=15, height=1, font=('Helvetica 12 bold'), command=funcs[i]) \
                .grid(row=0, column=i, padx=10, pady=10)
        Bots2.pack(side='bottom')
        self.face.pack()

    def previous(self):
        tkinter.messagebox.showerror(title='Error', message='You CAN NOT go to the previous step!')

    def follow(self):
        self.face.destroy()
        self.Bots.destroy()
        GI.Page1st(self.master, self.savelist, self.timess, self.locationss, self.TPs, self.Records, self.savedTPs,
                self.stride, self.perferf)

    def visualframe(self):
        Frame = tk.Frame(self.face, )
        self.BCline, self.FPline = None, [[], []]
        self.Canvas = self.layout(Frame)
        self.plotTP()
        self.Canvas.pack(side='left')
        self.Frame_r = tk.Frame(Frame, )
        BCche = tk.Checkbutton(self.Frame_r, text='Body centers', font=('Helvetica 12 bold'), variable=self.hasBCline,
                               onvalue=1, offvalue=0, command=self.plotTP)
        BCche.pack(side='top')
        FPche = tk.Checkbutton(self.Frame_r, text='Foot steps', font=('Helvetica 12 bold'), variable=self.hasFPline,
                               onvalue=1, offvalue=0, command=self.plotTP)
        FPche.pack(side='top')
        tk.Button(self.Frame_r, text='Previous Pattern', width=15, height=1, font=('Helvetica 12 bold'), command=self.prevP) \
            .pack(side='top', pady=5)
        self.InfoF = self.patterninfo()
        self.InfoF.pack(pady=10)
        tk.Button(self.Frame_r, text='Next Pattern', width=15, height=1, font=('Helvetica 12 bold'), command=self.nextP) \
            .pack(side='bottom')
        self.Frame_r.pack(side='right', pady=5)
        return Frame

    def layout(self, root):
        Canvas = tk.Canvas(root, bg='white', height=370, width=640)
        path = self.savelist[self.pindex]
        path_l = path.split('/')
        house_js = Load.load_se_map(path_l[0], path_l[1], path_l[2])
        rooms, T_Bs, furnitures, doors, walls, self.lims = Load.dic2house(house_js)
        Fur_set, self.scale, self.IsROT, Fur_indexs = SP.layoutplot(Canvas, [640, 370], rooms, T_Bs, furnitures, doors,
                                                                    walls, self.lims, showbg=False)
        self.key, self.key_ = self.deterkey(self.TPindex, self.saindex)
        [self.body_c, self.left_f, self.right_f] = self.TPs[self.pindex][self.key]
        return Canvas

    def plotTP(self):
        if self.BCline != None: self.Canvas.delete(self.BCline)
        if [] not in self.FPline:
            for i in range(2):
                for dot in self.FPline[i]: self.Canvas.delete(dot)
        if self.hasBCline.get():
            self.BCline = SP.plotBCline(self.Canvas, self.body_c, self.scale, self.IsROT, self.lims, [640, 370])
        if self.hasFPline.get():
            self.FPline = SP.plotFPline(self.Canvas, self.left_f, self.right_f, self.scale, self.IsROT, self.lims, [640, 370])

    def deterkey(self, i, j):
        locations = self.locationss[self.pindex]
        start = locations[i - 1]
        if locations[i] != 'Wander':
            end = locations[i]
            key0 = 'Direct,' + start + ',' + end
            key1 = self.Records[self.pindex][key0][j]
            return key0 + ',' + key1, key0
        else:
            end = locations[i + 1]
            key_ = 'Wander,' + start + ',' + end
            return self.Records[self.pindex][key_][j], key_

    def patterninfo(self):
        Frame = tk.Frame(self.Frame_r, )
        key_l = self.key.split(',')
        pattern, start, end = key_l[0], key_l[1], key_l[-2]
        tk.Label(Frame, text='Pattern: '+pattern, width=20, font=('Helvetica 12 bold')).pack()
        tk.Label(Frame, text='From: '+Iact2Pla[start], width=20, font=('Helvetica 12 bold')).pack()
        tk.Label(Frame, text='To: '+Iact2Pla[end], width=20, font=('Helvetica 12 bold')).pack()
        return Frame

    def save(self):
        self.savedTPs[(self.pindex, self.TPindex)] = self.saindex

    def prevLay(self):
        if self.pindex > 0:
            self.pindex -= 1
            self.TPindex = 1
            self.saindex = 0 if (self.pindex, self.TPindex) not in self.savedTPs else self.savedTPs[(self.pindex, self.TPindex)]
            self.Vframe.destroy()
            self.Vframe = self.visualframe()
            self.Vframe.pack()
        else: tkinter.messagebox.showerror(title='Error', message='This is the FIRST house!')

    def nextLay(self):
        if self.pindex < len(self.savelist) - 1:
            self.pindex += 1
            self.TPindex = 1
            self.saindex = 0 if (self.pindex, self.TPindex) not in self.savedTPs else self.savedTPs[(self.pindex, self.TPindex)]
            self.Vframe.destroy()
            self.Vframe = self.visualframe()
            self.Vframe.pack()
        else: tkinter.messagebox.showerror(title='Error', message='This is the LAST house!')

    def prevSam(self):
        if self.saindex > 0:
            self.saindex -= 1
            self.key, self.key_ = self.deterkey(self.TPindex, self.saindex)
            [self.body_c, self.left_f, self.right_f] = self.TPs[self.pindex][self.key]
            self.plotTP()
        else: tkinter.messagebox.showerror(title='Error', message='This is the FIRST sample!')

    def nextSam(self):
        if self.saindex < len(self.Records[self.pindex][self.key_]) - 1:
            self.saindex += 1
            self.key, self.key_ = self.deterkey(self.TPindex, self.saindex)
            [self.body_c, self.left_f, self.right_f] = self.TPs[self.pindex][self.key]
            self.plotTP()
        else: tkinter.messagebox.showerror(title='Error', message='This is the LAST sample!')

    def prevP(self):
        if self.TPindex > 2:
            if self.locationss[self.pindex][self.TPindex-2]=='Wander': nTPindex = self.TPindex - 2
            else: nTPindex = self.TPindex - 1
        else: nTPindex = self.TPindex - 1
        if nTPindex > 0:
            self.TPindex = nTPindex
            self.saindex = 0 if (self.pindex, self.TPindex) not in self.savedTPs else self.savedTPs[(self.pindex, self.TPindex)]
            self.key, self.key_ = self.deterkey(self.TPindex, self.saindex)
            [self.body_c, self.left_f, self.right_f] = self.TPs[self.pindex][self.key]
            self.plotTP()
            self.InfoF.destroy()
            self.InfoF = self.patterninfo()
            self.InfoF.pack()
        else: tkinter.messagebox.showerror(title='Error', message='This is the FIRST pattern!')

    def nextP(self):
        nTPindex = self.TPindex+2 if self.locationss[self.pindex][self.TPindex]=='Wander' else self.TPindex+1
        if nTPindex < len(self.locationss[self.pindex]):
            self.TPindex = nTPindex
            self.saindex = 0 if (self.pindex, self.TPindex) not in self.savedTPs else self.savedTPs[(self.pindex, self.TPindex)]
            self.key, self.key_ = self.deterkey(self.TPindex, self.saindex)
            [self.body_c, self.left_f, self.right_f] = self.TPs[self.pindex][self.key]
            self.plotTP()
            self.InfoF.destroy()
            self.InfoF = self.patterninfo()
            self.InfoF.pack()
        else: tkinter.messagebox.showerror(title='Error', message='This is the LAST pattern!')