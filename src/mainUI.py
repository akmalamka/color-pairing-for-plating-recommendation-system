from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from tkinter.filedialog import asksaveasfile, asksaveasfilename
import os
import numpy as np
import pandas as pd
# import image

class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.mainPanel = Label(self.parent) # panel yang nampilin gambar
        self.initUI()
    
    def initUI(self):
        self.parent.title("Mini Photoshop")
        # self.parent.config(menu = self.menubar)
        self.openPlateImageButton = Button(self.parent, command=self.openPlateImageClick, text="Open Plate Image")
        self.openPlateImageButton.pack(side=TOP)
        # self.openPlateImageButton.grid()

    def open_filename(self): 
        # open file dialog box to select image 
        self.filename = filedialog.askopenfilename(title ='Open') 
        return self.filename 

    def openPlateImageClick(self):
        x = self.open_filename()
        self.rawImg = Image.open(x) # Image Object PIL
        self.img = ImageTk.PhotoImage(self.rawImg)
        self.mainPanel = Label(image = self.img)
        self.mainPanel.pack(side=TOP)

def main():
    root = Tk()
    root.geometry('500x400')
    app = App(root)
    # Allow Window to be resizable 
    root.resizable(width = True, height = True) 
    root.mainloop()


if __name__ == '__main__':
    main()