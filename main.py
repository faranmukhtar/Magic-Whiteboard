import handtracker
import cv2 as cv
import numpy as np
import os

folderpath = "Elements"
mylist = os.listdir(folderpath)
print(mylist)
overlaylist = []
sidebar_open = False
current_color = "black"
eraser_selected = False
color = (0,0,0)
close_count = 0
erasercount = 0


for img_path in mylist:
    image = cv.imread(f'{folderpath}/{img_path}')
    overlaylist.append(image)

print(len(overlaylist))

sidebar_open_button = overlaylist[1]
sidebar_close_button = overlaylist[0]
logo = overlaylist[4]
eraser = overlaylist[3]

# cap = cv.VideoCapture(2, cv.CAP_MSMF)
cap = cv.VideoCapture(2)

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
hand = handtracker.handdetector()

ix, iy = -1, -1
sidebar = overlaylist[5]  # default color panel, e.g. black

while True:
    Succcess , img = cap.read()
    img = cv.flip(img , 1)
    sidebar_open_button = cv.resize(sidebar_open_button, (60, 200))
    sidebar_h, sidebar_w, _ = sidebar_open_button.shape

    frame_h, frame_w, _ = img.shape

    y = (frame_h - sidebar_h) // 2
    x = 0

    img[y:y+sidebar_h, x:x+sidebar_w] = sidebar_open_button
    
    hand.gethands(img)
    index = hand.getindexlandmarks(img)

    if index is not None:
        ix, iy = index
        print(ix , iy)
        if x <= ix <= x + sidebar_w +10 and y <= iy <= y + sidebar_h:
            close_count = close_count - 1

        if close_count < -3:
            sidebar_open = True
            close_count = 0
        
        cv.circle(img, (ix, iy), 20, color, -1)
        


    if sidebar_open:

        if ix < 120:
            if 200<iy < 250 :
                current_color = "black"
                sidebar = overlaylist[5]
                color =  (0,0,0)

            elif 250 < iy < 330:
                current_color = "blue"
                sidebar = overlaylist[6]
                color =  (255, 0, 0)

            elif 330 < iy < 380:
                current_color = "red"
                sidebar = overlaylist[9]
                color = (0, 0, 255)


            elif 380 < iy < 450:
                current_color = "pink"
                sidebar = overlaylist[8]
                color = (180, 105, 255)

            elif 450 < iy < 500:
                sidebar = overlaylist[7]
            
           
        sidebar = cv.resize(sidebar, (110, 360))

        sidebar_h, sidebar_w, _ = sidebar.shape
        frame_h, frame_w, _ = img.shape

        y = (frame_h - sidebar_h) // 2
        x = 0

        img[y:y+sidebar_h, x:x+sidebar_w] = sidebar

        sidebar_close_button = cv.resize(sidebar_close_button, (60, 200))

        close_h, close_w, _ = sidebar_close_button.shape

        close_x = sidebar_w
        close_y = y + (sidebar_h - close_h) // 2  
        img[close_y:close_y+close_h,
        close_x:close_x+close_w] = sidebar_close_button

        if  close_x < ix < close_x+close_w and close_y < iy < close_y+close_h:
            close_count = close_count + 1
        
        
        if close_count > 10:
            sidebar_open = False
            close_count = 0

    if not eraser_selected : 
        eraser = overlaylist[3]
    elif eraser_selected : 
        eraser = overlaylist[2]
    
    eraser = cv.resize(eraser , (65 , 65))
    eraserh , eraserw , c = eraser.shape

    h = (frame_h - sidebar_h) // 2 + 20
    w = 10

    if sidebar_open : 
        h = h + sidebar_h
        w = sidebar_w//4

    elif not sidebar_open:
        
        sh , sw , sc = sidebar_open_button.shape
        h = h + sh
        w = sw //8

    img[h : h +eraserh , w: w +eraserw] = eraser

    if w-30 < ix < w + eraserw+30 and h-30 < iy < h + eraserh +30:
        erasercount = erasercount + 1
    
    if erasercount > 20:
        eraser_selected = not eraser_selected
        erasercount = -1

    
    logo = cv.resize(logo , (70 , 70))
    logoh , logow , c = logo.shape

    x = frame_w - logow - 5
    y = 5
    img[y:y+logoh , x :x +logow] = logo



    cv.imshow('img' , img)
    cv.waitKey(1)

