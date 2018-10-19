#!usr/bin/env python3

from tkinter import *

fruit = ['apple','ss','banana','pear']

class app:
    def __init__(self):
        self.root = Tk()
        self.root.title("MonkeyTool")
        self.frm = Frame(self.root)
        self.frm_L = Frame(self.frm)
        self.fruit = StringVar()
        Label(self.frm_L, text='手机:', font=('Arial', 10)).pack(side=LEFT)
        self.list = Listbox(self.frm_L,listvariable =self.fruit, font=('Arial', 10)).pack(side=RIGHT)
        # self.list.bind('<ButtonRlease-1>',fruit)
        self.frm_L.pack(side=LEFT)
        #self.root.resizable(0, 0)
        self.frm.pack(side=LEFT)

        self.root.mainloop()


if __name__ == '__main__':
    app()
