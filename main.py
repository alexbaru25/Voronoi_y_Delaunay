# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:11:14 2023

@author: Alex b
"""
import tkinter as tk

from Voronoi import Voronoi

class MainWindow:
    # radius of drawn points on canvas
    RADIUS = 3

    # flag to lock the canvas when drawn
    LOCK_FLAG = False
    
    def __init__(self, master):
        self.master = master
        self.master.title("Voronoi")

        self.frmMain = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.frmMain.pack(fill=tk.BOTH, expand=1)

        self.w = tk.Canvas(self.frmMain, width=600, height=600)
        self.w.config(background='white')
        self.w.bind('<Double-1>', self.onDoubleClick)
        self.w.pack()       

        self.frmButton = tk.Frame(self.master)
        self.frmButton.pack()
        
        self.btnCalculate = tk.Button(self.frmButton, text='Voronoi', width=25, command=self.onClickCalculate)
        self.btnCalculate.pack(side=tk.LEFT)
        
        self.btnClear = tk.Button(self.frmButton, text='Clear', width=25, command=self.onClickClear)
        self.btnClear.pack(side=tk.LEFT)
        
        self.btnCalculate_d = tk.Button(self.frmButton, text='Delaunay', width=25, command=self.onClickCalculate_d)
        self.btnCalculate_d.pack(side=tk.LEFT)
        
    def onClickCalculate(self):
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True
        
            pObj = self.w.find_all()
            points = []
            for p in pObj:
                coord = self.w.coords(p)
                points.append((coord[0]+self.RADIUS, coord[1]+self.RADIUS))

            vp = Voronoi(points,'false')
            vp.process()
            lines = vp.get_output()
            self.drawLinesOnCanvas(lines,'blue')
            print (lines)
            
    def onClickCalculate_d(self):
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True
        
            pObj = self.w.find_all()
            points = []
            for p in pObj:
                coord = self.w.coords(p)
                points.append((coord[0]+self.RADIUS, coord[1]+self.RADIUS))

            vp = Voronoi(points,'true')
            vp.process()
            lineas=vp.get_del()
            vp = Voronoi(points,'false')
            vp.process()
            lines = vp.get_output()
            self.drawLinesOnCanvas(lines,'white')
            self.drawLinesOnCanvas(lineas,'red')

    def onClickClear(self):
        self.LOCK_FLAG = False
        self.w.delete(tk.ALL)

    def onDoubleClick(self, event):
        if not self.LOCK_FLAG:
            self.w.create_oval(event.x-self.RADIUS, event.y-self.RADIUS, event.x+self.RADIUS, event.y+self.RADIUS, fill="black")

    def drawLinesOnCanvas(self, lines,color):
        for l in lines:
            self.w.create_line(l[0], l[1], l[2], l[3], fill=color)

def main(): 
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()