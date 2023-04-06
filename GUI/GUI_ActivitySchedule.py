import sys, os
import tkinter as tk
import tkinter.messagebox
import numpy.random as rd
from tkinter import scrolledtext
from tkinter import ttk


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind('\\')]
root_path = abs_path[:abs_path.rfind('\\')]
if root_path not in sys.path: sys.path.append(root_path)
if root_path+'\\Human_Activities_Schedule_Generation' not in sys.path:
    sys.path.append(root_path+'\\Human_Activities_Schedule_Generation')


import GUI_Base as GB
import GUI_TravelPattern as GT
import ScreenPlot as SP
import HAS_main
import HASave
import Load


class Page1st():
    def __init__(self, master, Savelist):
        self.savelist = Savelist
        self.master = master
        self.fvars = [tk.DoubleVar() for i in range(7)]
        self.f = [6, 2, 1, 1, 0, 0, 0]
        self.t = [3, 3, 1, 1, 1, 1, 1]
        self.order = [0, 1, 2, 3, 4]
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow, extras=[['Random', self.random]])
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, "Please determine preference and durations of the virtual residents' activities:")
        frame1 = tk.Frame(self.face, )
        frame1_le = tk.Frame(frame1, )
        tk.Label(frame1_le, text='Average duration of sleep at night: ', font=('Helvetica 12 bold'), height=2).pack(side='left')
        tk.Scale(frame1_le, variable=self.fvars[0], from_=6, to=9, resolution=0.05, orient='horizontal',
                 length=150, font=('Times 10')).pack(side='left')
        tk.Label(frame1_le, text=' hours', font=('Helvetica 12 bold'), height=2).pack(side='right')
        frame1_le.pack(padx=10, side='left')
        self.ivar = tk.IntVar()
        tk.Checkbutton(frame1, text='Does resident sleep at noon?', font=('Helvetica 12 bold'), variable=self.ivar,
                       onvalue=1, offvalue=0).pack(padx=10, side='right')
        frame1.pack(pady=10)
        self.orderframe()
        self.bottomframe()
        self.face.pack()

    def previous(self):
        tkinter.messagebox.showerror(title='Error', message='You CAN NOT go to the previous step!')

    def follow(self):
        self.face.destroy()
        self.Bots.destroy()
        paras = [(self.fvars[i].get()-self.f[i])/self.t[i] for i in range(7)]
        is_sleep_noon = self.ivar.get()
        Page2nd(self.master, self.savelist, paras, is_sleep_noon, self.order)

    def random(self):
        self.ivar.set(rd.randint(2))
        for i in range(7):
            self.fvars[i].set(self.f[i]+self.t[i]*rd.rand())
        rd.shuffle(self.order)
        self.Canvas.destroy()
        self.Canvas = self.cavas(self.subframe, self.order)
        self.Canvas.pack(side='right')

    def orderframe(self):
        oframe = tk.Frame(self.face, )
        tk.Label(oframe, text='Please determine the order of preference of the virtual residents for the following activities:',
                 font=('Helvetica 14 bold'), height=2, width=72, anchor='w').pack()
        tk.Label(oframe, text='(The virtual resident does leftmost activity most frequently)',
                 font=('Helvetica 14 bold'), height=2, width=72, anchor='w').pack()
        self.subframe = tk.Frame(oframe, )
        tk.Label(self.subframe, text='Change order by dragging ', font=('Helvetica 12 bold'), height=2).pack(side='left')
        self.Canvas = self.cavas(self.subframe, self.order)
        self.Canvas.pack(side='right')
        self.subframe.pack()
        oframe.pack(pady=10)

    def cavas(self, root, order):
        Acts = ['Bath', 'Go out', 'Clean', 'Read', 'Watch TV']
        Colors = ['blue', 'deeppink', 'yellowgreen', 'yellow', 'gold']
        TColors = ['white', 'white', 'black', 'black', 'black']
        Canvas = tk.Canvas(root, bg='white', height=50, width=500)
        self.Icons = {}
        self.item, self.mousexy = 0, [0, 0]
        for i in range(5):
            rect = Canvas.create_rectangle(20+100*i, 10, 80+100*i, 40, fill=Colors[order[i]], outline="black", width=3)
            text = Canvas.create_text(50+100*i, 25, text=Acts[order[i]], font=('Helvetica 12 bold'),
                                      fill=TColors[order[i]])
            self.Icons[rect] = [text, i]
            self.Icons[text] = [rect, i]
        Canvas.bind('<Button-1>', self.mouseselect)
        Canvas.bind('<B1-Motion>', self.mousedrag)
        Canvas.bind('<ButtonRelease-1>', self.mouserelease)
        return Canvas

    def mouseselect(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        self.item = widget.find_closest(xc, yc)[0]
        self.originx = xc
        self.mousexy = [xc, yc]

    def mousedrag(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        self.Canvas.move(self.item, xc - self.mousexy[0], yc - self.mousexy[1])
        self.Canvas.move(self.Icons[self.item][0], xc - self.mousexy[0], yc - self.mousexy[1])
        self.mousexy = [xc, yc]

    def mouserelease(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        self.update_order(self.Icons[self.item][1], self.originx, xc)
        self.Canvas.destroy()
        self.Canvas = self.cavas(self.subframe, self.order)
        self.Canvas.pack(side='right')

    def update_order(self, item, x0, x1):
        place_Incre = (x1-x0)//100 if x1>x0 else -((x0-x1)//100)
        newplace = int(item + place_Incre)
        if newplace<0: newplace = 0
        elif newplace>4: newplace = 4
        o = self.order.pop(item)
        self.order.insert(newplace, o)

    def bottomframe(self):
        frame = tk.Frame(self.face, )
        frame_0 = tk.Frame(frame, )
        tk.Label(frame_0, text='Average durations:  Go out', font=('Helvetica 12 bold'), height=2).pack(side='left')
        tk.Scale(frame_0, variable=self.fvars[1], from_=2, to=5, resolution=0.02, orient='horizontal',
                 length=100, font=('Times 10')).pack(side='left')
        tk.Label(frame_0, text='  Read  ', font=('Helvetica 12 bold'), height=2).pack(side='left')
        tk.Scale(frame_0, variable=self.fvars[2], from_=1, to=2, resolution=0.02, orient='horizontal',
                 length=100, font=('Times 10')).pack(side='left')
        tk.Label(frame_0, text='  Watch TV  ', font=('Helvetica 12 bold'), height=2).pack(side='left')
        tk.Scale(frame_0, variable=self.fvars[3], from_=1, to=2, resolution=0.02, orient='horizontal',
                 length=100, font=('Times 10')).pack(side='left')
        frame_0.pack()
        frame_1 = tk.Frame(frame, )
        tk.Label(frame_1, text='Average frequency:  Go to Toilet  (low)', font=('Helvetica 12 bold'), height=2).pack(side='left')
        tk.Scale(frame_1, variable=self.fvars[4], from_=0, to=1, resolution=0.01, orient='horizontal',
                 length=100, font=('Times 10')).pack(side='left')
        tk.Label(frame_1, text='(high)    Wander  (low)', font=('Helvetica 12 bold'), height=2).pack(side='left')
        tk.Scale(frame_1, variable=self.fvars[5], from_=0, to=1, resolution=0.01, orient='horizontal',
                 length=100, font=('Times 10')).pack(side='left')
        tk.Label(frame_1, text='(high)', font=('Helvetica 12 bold'), height=2).pack(side='left')
        frame_1.pack()
        frame_2 = tk.Frame(frame, )
        tk.Label(frame_2, text='The virtual resident does activities  (slow)', font=('Helvetica 12 bold'),
                 height=2).pack(side='left')
        tk.Scale(frame_2, variable=self.fvars[6], from_=0, to=1, resolution=0.01, orient='horizontal',
                 length=200, font=('Times 10')).pack(side='left')
        tk.Label(frame_2, text='(fast)', font=('Helvetica 12 bold'), height=2).pack(side='left')
        frame_2.pack()
        frame.pack(pady=10)


class Page2nd():
    def __init__(self, master, Savelist, paras, intvar, order):
        self.savelist, self.pindex = Savelist, 0
        self.paras, self.intvar, self.order = paras, intvar, order
        self.master = master
        self.stimes, self.etimes = [], []
        for i in range(len(self.savelist)):
            self.stimes.append([None, None])
            self.etimes.append([None, None])
        self.Actseqs = HAS_main.actseq_gen(self.savelist, self.paras[6], self.paras[0], self.intvar, self.paras[1:4],
                                      self.paras[4:6], self.order)
        self.timescales = [1440, 360, 120, 30, 10] # unit is s
        self.ticksteps = [240, 60, 20, 5, 2]
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow)
        self.face = tk.Frame(self.master, )
        GB.Top_Info(self.face, 'Please determine the start and end time of generated scenarios:')
        self.Vframe = self.visualframe(self.Actseqs[self.pindex])
        self.Vframe.pack(pady=10)
        Bots2 = tk.Frame(self.face, )
        texts = ['Previous House', 'Previous Day', 'Regeneration', 'Next Day', 'Next House']
        funcs = [self.prevLay, self.prevDay, self.reGene, self.nextDay, self.nextLay]
        for i in range(5):
            tk.Button(Bots2, text=texts[i], width=15, height=1, font=('Helvetica 12 bold'), command=funcs[i]) \
                .grid(row=0, column=i, padx=10, pady=10)
        Bots2.pack(side='bottom')
        self.face.pack()

    def previous(self):
        self.face.destroy()
        self.Bots.destroy()
        Page1st(self.master, self.savelist)

    def follow(self):
        flag = True
        for i in range(len(self.stimes)):
            if None in self.stimes[i] or None in self.etimes[i]: flag = False
        if flag:
            self.face.destroy()
            self.Bots.destroy()
            Page3rd(self.master, self.savelist, self.Actseqs, self.stimes, self.etimes)
        else: tkinter.messagebox.showerror(title='Error', message='You Have NOT determined all start or end time!')

    def visualframe(self, Mkchain):
        Frame = tk.Frame(self.face, )
        self.timess, self.timeIss, self.numss = SP.div_Mkchain(Mkchain)
        self.day, self.canvas_W = 0, 720
        self.Frame_up = tk.Frame(Frame, )
        self.is_Zoom, self.scaind, self.sminu = tk.IntVar(), 0, 0
        tk.Checkbutton(self.Frame_up, text='Zoom', font=('Helvetica 12 bold'), variable=self.is_Zoom, onvalue=1,
                       offvalue=0).pack(side='left')
        self.Canvas = self.showSchedule(self.timess[0], self.timeIss[0], self.numss[0], self.timescales[0], self.ticksteps[0])
        self.Canvas.pack(side='right')
        self.Frame_up.pack(pady=5)
        self.ivars = [tk.IntVar() for i in range(2)]
        self.sline, self.eline = None, None
        self.ESframe = self.startendtimeframe(Frame)
        self.ESframe.pack()
        return Frame

    def startendtimeframe(self, root):
        Frame = tk.Frame(root, )
        texts = [' start time:  ', ' end time:  ']
        all_times = [self.stimes[self.pindex], self.etimes[self.pindex]]
        for i in range(2):
            self.ivars[i].set(0)
            sub_frame = tk.Frame(Frame, )
            tk.Checkbutton(sub_frame, text='Determine'+texts[i], font=('Helvetica 12 bold'), variable=self.ivars[i],
                           onvalue=1, offvalue=0).pack(side='left')
            timetxt = 'None' if None in all_times[i] else 'Day '+str(all_times[i][0]+1)+ '  '+SP.tick_text(all_times[i][1])
            tk.Label(sub_frame, text=timetxt, font=('Helvetica 12 bold'), height=2).pack(side='left')
            sub_frame.grid(padx=20, row=0, column=i)
        return Frame

    def showSchedule(self, times, timeIs, nums, scale, tickstep):
        Canvas = tk.Canvas(self.Frame_up, bg='white', height=300, width=self.canvas_W)
        SP.schedule_plot(Canvas, self.canvas_W, times, timeIs, nums, self.sminu, scale, tickstep)
        stime, etime = self.stimes[self.pindex], self.etimes[self.pindex]
        if stime[0]==self.day: self.sline = SP.noteline_plot(Canvas, self.canvas_W, self.sminu, scale, stime[1])
        if etime[0]==self.day: self.eline = SP.noteline_plot(Canvas, self.canvas_W, self.sminu, scale, etime[1])
        Canvas.bind('<Button-1>', self.mouseleft)
        Canvas.bind('<Button-3>', self.mouseright)
        return Canvas

    def prevLay(self):
        if self.pindex > 0:
            self.pindex -= 1
            self.Vframe.destroy()
            self.Vframe = self.visualframe(self.Actseqs[self.pindex])
            self.Vframe.pack(pady=10)
        else: tkinter.messagebox.showerror(title='Error', message='This is the FIRST house!')

    def nextLay(self):
        if self.pindex < len(self.Actseqs) - 1:
            self.pindex += 1
            self.Vframe.destroy()
            self.Vframe = self.visualframe(self.Actseqs[self.pindex])
            self.Vframe.pack(pady=10)
        else: tkinter.messagebox.showerror(title='Error', message='This is the LAST house!')

    def prevDay(self):
        if self.day > 0:
            self.day -= 1
            self.Canvas.destroy()
            self.Canvas = self.showSchedule(self.timess[self.day], self.timeIss[self.day], self.numss[self.day],
                                            self.timescales[0], self.ticksteps[0])
            self.Canvas.pack(side='right')
        else: tkinter.messagebox.showerror(title='Error', message='This is the FIRST day!')

    def nextDay(self):
        if self.day < 24:
            self.day += 1
            self.Canvas.destroy()
            self.Canvas = self.showSchedule(self.timess[self.day], self.timeIss[self.day], self.numss[self.day],
                                            self.timescales[0], self.ticksteps[0])
            self.Canvas.pack(side='right')
        else: tkinter.messagebox.showerror(title='Error', message='This is the LAST day!')

    def reGene(self):
        self.Vframe.destroy()
        fpc = self.savelist[self.pindex].split('\\')[1]
        Actseq = HAS_main.main(fpc, self.paras[6], self.paras[0], self.intvar, self.paras[1:4], self.paras[4:6], self.order)
        self.Actseqs[self.pindex] = Actseq
        self.stimes[self.pindex], self.etimes[self.pindex] = [None, None], [None, None]
        self.Vframe = self.visualframe(Actseq)
        self.Vframe.pack(pady=10)

    def mouseleft(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        if self.ivars[0].get()==1 and self.ivars[1].get()==1:
            tkinter.messagebox.showerror(title='Error', message='You CAN NOT determine the start and end time at the same time!')
        elif self.ivars[0].get()==1:
            self.placeline(xc, True)
            self.ESframe.destroy()
            self.ESframe = self.startendtimeframe(self.Vframe)
            self.ESframe.pack()
        elif self.ivars[1].get()==1:
            self.placeline(xc, False)
            self.ESframe.destroy()
            self.ESframe = self.startendtimeframe(self.Vframe)
            self.ESframe.pack()
        elif self.is_Zoom.get()==1 and self.scaind<4: self.zoominout(xc, True)

    def mouseright(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        if self.is_Zoom.get()==1 and self.scaind>0: self.zoominout(xc, False)

    def zoominout(self, xc, is_in):
        scale0 = self.timescales[self.scaind]
        time = self.sminu + xc/self.canvas_W*scale0
        self.scaind = self.scaind + 1 if is_in else self.scaind - 1
        scale = self.timescales[self.scaind]
        if time<scale/2: time = scale/2
        elif time>1440-scale/2: time = 1440-scale/2
        self.sminu = time - scale/2
        self.Canvas.destroy()
        self.Canvas = self.showSchedule(self.timess[self.day], self.timeIss[self.day], self.numss[self.day],
                                        self.timescales[self.scaind], self.ticksteps[self.scaind])
        self.Canvas.pack(side='right')

    def placeline(self, xc, is_stime):
        scale = self.timescales[self.scaind]
        time = self.sminu + xc/self.canvas_W*scale
        if is_stime:
            self.stimes[self.pindex] = [self.day, time]
            if self.sline != None: self.Canvas.delete(self.sline)
            self.sline = SP.noteline_plot(self.Canvas, self.canvas_W, self.sminu, scale, time)
        else:
            self.etimes[self.pindex] = [self.day, time]
            if self.eline != None: self.Canvas.delete(self.eline)
            self.eline = SP.noteline_plot(self.Canvas, self.canvas_W, self.sminu, scale, time)


class Page3rd():
    def __init__(self, master, Savelist, Actseqs, stimes, etimes):
        self.master = master
        self.savelist, self.pindex = Savelist, 0
        self.actseqs = Actseqs
        self.stimes, self.etimes = stimes, etimes
        self.Txts = []
        for i in range(len(self.savelist)):
            Txt = HASave.Mark2Txt(Actseqs[i], Savelist[i], stimes[i], etimes[i])
            self.Txts.append(Txt)
        self.Bots = GB.Bot_Butts(self.master, self.previous, self.follow)
        self.face0 = self.makeface()
        self.face0.pack()
        self.face1 = tk.Frame(self.master, )
        GB.Top_Info(self.face1, 'Please determine parameters for travel pattern generation:')
        frame = tk.Frame(self.face1, )
        tk.Label(frame, text='The most comfortable walking stride length for the virtual resident is ', \
                 font=('Helvetica 12 bold'), height=2).pack(side='left')
        self.stride = tk.StringVar()
        self.stride.set('55')
        tk.Entry(frame, textvariable=self.stride, font=('Helvetica 12 bold'), width=4).pack(side='left')
        tk.Label(frame, text=' cm. (in [40cm, 65cm])', font=('Helvetica 12 bold'), height=2).pack(side='left')
        frame.pack()
        frame2 = tk.Frame(self.face1, )
        tk.Label(frame2, text='The virtual resident puts its ', font=('Helvetica 12 bold'), height=2).pack(side='left')
        self.whichfoot = tk.StringVar()
        Combox = ttk.Combobox(frame2, textvariable=self.whichfoot, font=('Helvetica 12 bold'), width=7)
        Combox['values'] = ('left', 'right')
        Combox.current(1)
        Combox.pack(side='left')
        tk.Label(frame2, text=' foot first when it walks a path.', font=('Helvetica 12 bold'), height=2).pack(
            side='left')
        frame2.pack()
        self.face1.pack(side='bottom')

    def makeface(self):
        Face = tk.Frame(self.master, )
        GB.Top_Info(Face, 'Selected activity schedules:')
        self.showschedule(Face)
        Bots2 = tk.Frame(Face, )
        tk.Button(Bots2, text='Previous House', width=15, height=1, font=('Helvetica 12 bold'),
                  command=self.prevLay).pack(side='left', padx=20, pady=10)
        tk.Button(Bots2, text='Next House', width=15, height=1, font=('Helvetica 12 bold'),
                  command=self.nextLay).pack(side='left', padx=20, pady=10)
        Bots2.pack(side='bottom')
        return Face

    def showschedule(self, root):
        Txt = self.Txts[self.pindex]
        SCR = scrolledtext.ScrolledText(root, width=70, height=10, font=('Helvetica 12 bold'))
        SCR.pack()
        SCR.insert('end', Txt)

    def prevLay(self):
        if self.pindex > 0:
            self.pindex -= 1
            self.face0.destroy()
            self.face0 = self.makeface()
            self.face0.pack()
        else: tkinter.messagebox.showerror(title='Error', message='This is the FIRST house!')

    def nextLay(self):
        if self.pindex < len(self.savelist)-1:
            self.pindex += 1
            self.face0.destroy()
            self.face0 = self.makeface()
            self.face0.pack()
        else: tkinter.messagebox.showerror(title='Error', message='This is the LAST house!')

    def previous(self):
        self.face0.destroy()
        self.face1.destroy()
        self.Bots.destroy()
        Page1st(self.master, self.savelist)

    def follow(self):
        self.face0.destroy()
        self.face1.destroy()
        self.Bots.destroy()
        timess, locationss = [], []
        for path in self.savelist:
            [h_v, fname0, fname1] = path.split('\\')
            times, locations = Load.load_actseq(h_v, fname0, fname1)
            timess.append(times)
            locationss.append(locations)
        stride, perferfoot = self.stride.get(), self.whichfoot.get()
        GT.Page1st(self.master, self.savelist, timess, locationss, stride, perferfoot)