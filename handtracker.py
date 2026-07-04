import cv2 as cv
import mediapipe as mp
import mediapipe.python.solutions.hands as mphands
import time
import math


class handdetector:
    def __init__(self ):
        self.hands = mphands.Hands()
        self.mpdraw = mp.solutions.drawing_utils
        self.ptime = time.time()
        self.prev_thumb_index = None
        self.prev_thumb_middle = None
        self.prev_middle_index = None
        self.wrist_reference = None

    def gethands(self , img):
        ptime = 0
        ctime = 0
        imgrgb = cv.cvtColor(img , cv.COLOR_BGR2RGB)
        
        results = self.hands.process(imgrgb)

        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:
                self.mpdraw.draw_landmarks(img , handlms , mphands.HAND_CONNECTIONS)
                for id , lm in enumerate(handlms.landmark):
                    h,w,c = img.shape
                    cx , cy = int(lm.x * w) , int(lm.y * h)
                
        ctime = time.time()
        fps = 1/(ctime - self.ptime)
        self.ptime = ctime
        cv.putText(img , str(int(fps)) , (10,70) , cv.FONT_HERSHEY_COMPLEX , 3 , (0,255,0) , 3)
        
        self.getcurrentpose(img)
    


    def getcurrentpose(self , img):
        imgrgb = cv.cvtColor(img , cv.COLOR_BGR2RGB)
        results = self.hands.process(imgrgb)
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            h , w ,c = imgrgb.shape

            thumb = hand.landmark[4]
            indexfinger = hand.landmark[8]
            middlefinger = hand.landmark[12]
            wrist = hand.landmark[0]

            thumbx , thumby = (thumb.x * w) , (thumb.y * h)
            indexfingerx , indexfingery = (indexfinger.x * w) , (indexfinger.y * h)
            middlefingerx , middlefingery = (middlefinger.x * w) , (middlefinger.y * h)
            


            thumb_index_distance = math.hypot(indexfingerx - thumbx , indexfingery - thumby)
            thumb_middle_distance = math.hypot(thumbx - middlefingerx , thumby - middlefingery) 
            middle_index_distance = math.hypot(middlefingerx - indexfingerx , middlefingery - indexfingery)

            if self.prev_thumb_index is None:
                self.prev_thumb_index = thumb_index_distance
            
            if self.prev_middle_index is None:
                self.prev_middle_index = middle_index_distance
            
            if self.prev_thumb_middle is None:
                self.prev_thumb_middle = thumb_middle_distance

            
            thumb_index_distance = 0.8 * self.prev_thumb_index + 0.2 * thumb_index_distance
            self.prev_thumb_index = thumb_index_distance
           
            thumb_middle_distance = 0.8 * self.prev_thumb_middle+ 0.2 * thumb_middle_distance
            self.prev_thumb_middle = thumb_middle_distance

            middle_index_distance = 0.8 * self.prev_middle_index + 0.2 * middle_index_distance
            self.prev_middle_index = middle_index_distance

            cv.line(img , (int(thumbx) , int(thumby)) , (int(indexfingerx) , int(indexfingery)) , (0 , 255 , 0) , thickness= 3)

            cv.putText(img , str(thumb_index_distance) , (80 , 100) , cv.FONT_HERSHEY_COMPLEX , 1 , (0 , 255 , 0 ) , thickness= 2)
            cv.putText(img , str(thumb_middle_distance) , (80 , 130) , cv.FONT_HERSHEY_COMPLEX , 1 , (0 , 255 , 0 ) , thickness= 2)
            cv.putText(img , str(middle_index_distance) , (80 , 160) , cv.FONT_HERSHEY_COMPLEX , 1 , (0 , 255 , 0 ) , thickness= 2)


            if thumb_index_distance < 60 and middle_index_distance < 30 and thumb_middle_distance < 60  :
                cv.putText(img , "Write mode" , (50 , 50) , cv.FONT_HERSHEY_COMPLEX , 1 , (255 , 0 , 0) , thickness= 2)
            
            else:
                cv.putText(img , "Halt mode" , (50 , 50) , cv.FONT_HERSHEY_COMPLEX , 1 , (0 , 0 , 255) , 2)

        cv.imshow('img' , img)
        cv.waitKey(1)



cap = cv.VideoCapture(0)


cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
h = handdetector()

while True:
    Succcess , img = cap.read()

    img = cv.flip(img , 1)
    h.gethands(img)



        


