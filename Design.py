import handtracker
import cv2 as cv
import numpy as np
import os

class BoardDesign:

    def __init__(self):
        self.folderpath = "Elements"
        self.mylist = os.listdir(self.folderpath)

        self.overlaylist = []
        self.sidebar_open = False
        self.current_color = "black"
        self.eraser_selected = False
        self.color = (0,0,0)
        self.close_count = 0
        self.erasercount = 0

        for img_path in self.mylist:
            image = cv.imread(f'{self.folderpath}/{img_path}')
            self.overlaylist.append(image)

        self.sidebar = self.overlaylist[5]
        self.sidebar_open_button = self.overlaylist[1]
        self.sidebar_close_button = self.overlaylist[0]
        self.logo = self.overlaylist[4]
        self.eraser = self.overlaylist[3]
        self.ix = -1
        self.iy = -1
        self.frame_h = None
        self.frame_w = None
        self.hand = handtracker.handdetector()

# cap = cv.VideoCapture(1, cv.CAP_MSMF)

# #cap = cv.VideoCapture(2)

# cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
# hand = handtracker.handdetector()

    def drawsidebar(self , img):
        
        self.sidebar_open_button = cv.resize(self.sidebar_open_button, (60, 200))
        sidebar_h, sidebar_w, _ = self.sidebar_open_button.shape

        self.frame_h, self.frame_w, _ = img.shape

        y = (self.frame_h - sidebar_h) // 2
        x = 0

        img[y:y+sidebar_h, x:x+sidebar_w] = self.sidebar_open_button
        
        self.hand.gethands(img)
        index = self.hand.getindexlandmarks(img)

        if index is not None:
            self.ix, self.iy = index
            print(self.ix , self.iy)
            if x <= self.ix <= x + sidebar_w +10 and y <= self.iy <= y + sidebar_h:
                self.close_count = self.close_count - 1

            if self.close_count < -3:
                self.sidebar_open = True
                self.close_count = 0
            
            cv.circle(img, (self.ix, self.iy), 20, self.color, -1)
            


        if self.sidebar_open:

            if self.ix < 120:
                if 200<self.iy < 250 :
                    self.current_color = "black"
                    self.sidebar = self.overlaylist[5]
                    self.color =  (0,0,0)

                elif 250 < self.iy < 330:
                    self.current_color = "blue"
                    self.sidebar = self.overlaylist[6]
                    self.color =  (255, 0, 0)

                elif 330 < self.iy < 380:
                    self.current_color = "red"
                    self.sidebar = self.overlaylist[9]
                    self.color = (0, 0, 255)


                elif 380 < self.iy < 450:
                    self.current_color = "pink"
                    self.sidebar = self.overlaylist[8]
                    self.color = (180, 105, 255)

                elif 450 < self.iy < 500:
                    self.sidebar = self.overlaylist[7]
                
            
            self.sidebar = cv.resize(self.sidebar, (110, 360))

            sidebar_h, sidebar_w, _ = self.sidebar.shape
            
            y = (self.frame_h - sidebar_h) // 2
            x = 0

            img[y:y+sidebar_h, x:x+sidebar_w] = self.sidebar

            self.sidebar_close_button = cv.resize(self.sidebar_close_button, (60, 200))

            close_h, close_w, _ = self.sidebar_close_button.shape

            close_x = sidebar_w
            close_y = y + (sidebar_h - close_h) // 2  
            img[close_y:close_y+close_h,
            close_x:close_x+close_w] = self.sidebar_close_button

            if  close_x < self.ix < close_x+close_w and close_y < self.iy < close_y+close_h:
                self.close_count = self.close_count + 1
            
            
            if self.close_count > 10:
                self.sidebar_open = False
                self.close_count = 0

        if not self.eraser_selected : 
            self.eraser = self.overlaylist[3]
        elif self.eraser_selected : 
            self.eraser = self.overlaylist[2]
        
        self.eraser = cv.resize(self.eraser , (65 , 65))
        eraserh , eraserw , c = self.eraser.shape

        h = (self.frame_h - sidebar_h) // 2 + 20
        w = 10

        if self.sidebar_open : 
            h = h + sidebar_h
            w = sidebar_w//4

        elif not self.sidebar_open:
            
            sh , sw , sc = self.sidebar_open_button.shape
            h = h + sh
            w = sw //8

        img[h : h +eraserh , w: w +eraserw] = self.eraser

        if w-30 < self.ix < w + eraserw+30 and h-30 < self.iy < h + eraserh +30:
            self.erasercount = self.erasercount + 1
        
        if self.erasercount > 20:
            self.eraser_selected = not self.eraser_selected
            self.erasercount = -1

    def drawlogo(self , img):
            
        self.logo = cv.resize(self.logo , (70 , 70))
        logoh , logow , c = self.logo.shape

        x = self.frame_w - logow - 5
        y = 5
        img[y:y+logoh , x :x +logow] = self.logo


