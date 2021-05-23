from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from tkinter.filedialog import asksaveasfile, asksaveasfilename
import os
import numpy as np
import pandas as pd
import cv2
from sklearn.cluster import KMeans

class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.mainPanel = Label(self.parent) # panel yang nampilin gambar
        self.CLUSTERS = 2
        self.IMAGE = None
        self.COLORS = None
        self.LABELS = None
        self.initUI()
    
    def initUI(self):
        self.parent.title("Mini Photoshop")
        self.openPlateImageButton = Button(self.parent, command=self.open_plate_image_click, text="Open Plate Image")
        self.openPlateImageButton.pack(side=TOP)

    def open_filename(self): 
        # open file dialog box to select image 
        self.filename = filedialog.askopenfilename(title ='Open') 
        return self.filename 

    def open_plate_image_click(self):
        x = self.open_filename()
        self.rawImg = Image.open(x) # Image Object PIL
        self.img = ImageTk.PhotoImage(self.rawImg)
        self.mainPanel = Label(image = self.img)
        self.mainPanel.pack(side=TOP)
        self.extract_section()

    def extract_section(self):
        img_rgb = cv2.imread(self.filename)

        img = cv2.cvtColor(img_rgb,cv2.COLOR_RGB2HSV)
        img = cv2.bilateralFilter(img,9,105,105)
        r,g,b=cv2.split(img)
        equalize1= cv2.equalizeHist(r)
        equalize2= cv2.equalizeHist(g)
        equalize3= cv2.equalizeHist(b)
        equalize=cv2.merge((r,g,b))

        equalize = cv2.cvtColor(equalize,cv2.COLOR_RGB2GRAY)

        ret,thresh_image = cv2.threshold(equalize,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
        equalize= cv2.equalizeHist(thresh_image)

        canny_image = cv2.Canny(equalize,250,255)
        canny_image = cv2.convertScaleAbs(canny_image)
        kernel = np.ones((3,3), np.uint8)
        dilated_image = cv2.dilate(canny_image,kernel,iterations=1)

        contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours= sorted(contours, key = cv2.contourArea, reverse = True)[:10]
        c=contours[0]
        print(cv2.contourArea(c))
        final = cv2.drawContours(img, [c], -1, (255,0, 0), 3)

        mask = np.zeros(img_rgb.shape,np.uint8)
        self.extracted_image = cv2.drawContours(mask,[c],0,255,-1,)

        self.extracted_image = cv2.bitwise_and(img_rgb, img_rgb, mask = equalize)
        # print('aaa')
        # status = cv2.imwrite("extracted_image.jpg", self.extracted_image)
        # print(status)

        self.dominantColors = self.dominant_colors()
        print(self.dominantColors)

    def dominant_colors(self):
        
        #convert to rgb from bgr
        img = cv2.cvtColor(self.extracted_image, cv2.COLOR_BGR2RGB)
                
        #reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))
        
        #save image after operations
        self.IMAGE = img
        
        #using k-means to cluster pixels
        kmeans = KMeans(n_clusters = self.CLUSTERS)
        kmeans.fit(img)
        
        #the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_
        
        #save labels
        self.LABELS = kmeans.labels_
        
        #returning after converting to integer from float
        return self.COLORS.astype(int)

def main():
    root = Tk()
    root.geometry('500x400')
    app = App(root)
    # Allow Window to be resizable 
    root.resizable(width = True, height = True) 
    root.mainloop()

if __name__ == '__main__':
    main()