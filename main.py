import handtracker
import Design
import cv2 as cv
import numpy as np
import os

d = Design.BoardDesign()
cap = cv.VideoCapture(0)
# cap = cv.VideoCapture(1, cv.CAP_MSMF)

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
hand = handtracker.handdetector()

while True:

    Succcess , img = cap.read()
   
    img = cv.flip(img , 1)
    
    d.drawsidebar(img)
    d.drawlogo(img)
    cv.imshow('img' , img)
    cv.waitKey(1)

