import os
import tkinter as tk
from PIL import Image,ImageTk


abs_file = os.path.abspath(__file__)
abs_path = abs_file[:abs_file.rfind("\\")]
pic_path = abs_path + '\\Pics\\'


import GUI_Semantic as GS


class GUIbase():
    def __init__(self, master):
        self.root = master
        self.root.config()
        self.root.title('SISG4HEI_Alpha') #Simulated Indoor Scenario Generator for Houses with Elderly Individuals
        self.root.geometry('930x620')
        top_Frame = tk.Frame(self.root, )
        tk.Label(top_Frame, text='Simulated Indoor Scenario Generator ', font=('Helvetica 20 bold'),
                 height=2).pack(side='left')
        tk.Label(top_Frame, text='for Houses with Elderly Individuals', font=('Helvetica 12 bold'),
                 height=2, anchor='s').pack(side='left')
        top_Frame.pack()
        GS.Page1st(self.root)


def Bot_Butts(root, prev, next, extras=[]):
    N = len(extras)
    Bot_Butts = tk.Frame(root, )
    Bot_Butts.pack(side='bottom')
    def Put_Butt(text,COM,col):
        tk.Button(Bot_Butts,text=text,width=12,height=1,font=('Helvetica 14 bold'),command=COM)\
        .grid(row=0,column=col,padx=20, pady=20)
    Put_Butt('Previous Step', prev, 0)
    Put_Butt('Exit', root.quit, N+1)
    Put_Butt('Next Step', next, N+2)
    if extras != []:
        for i in range(N): Put_Butt(extras[i][0], extras[i][1], i+1)
    return Bot_Butts


def Top_Info(root, text):
    tk.Label(root, text=''+text, font=('Helvetica 14 bold'), width=72, height=2, anchor='w').pack()


def read_img(pic_name, w, h):
    return ImageTk.PhotoImage(Image.open(pic_name).resize((w, h)))


if __name__ == '__main__':
    SISCGUI = tk.Tk()
    GUIbase(SISCGUI)
    SISCGUI.mainloop()
