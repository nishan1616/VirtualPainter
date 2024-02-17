import cv2
import numpy as np
import time
import os
import HandTrackingModule2 as htm

######################################
brush_thickness=15
eraser_thickness=50
######################################
folder_path = "Header"
my_list = os.listdir(folder_path)
print(my_list)
overlay_list = []
for img_path in my_list:
    image = cv2.imread(f'{folder_path}/{img_path}')
    overlay_list.append(image)
print(len(overlay_list))
header = overlay_list[0]
draw_color = (255,0,255)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = htm.HandDetector(detection_con=0.85)
xp=0
yp=0
img_canvas = np.zeros((720,1280,3),np.uint8)
while True:
    #1. Import image
    success, img = cap.read()
    img = cv2.flip(img,1)
    #2.Find Hand Landmarks
    img = detector.draw_hands(img)
    landmarks_list = detector.find_landmarks(img,draw=False)
    if len(landmarks_list)!=0:
        #print(landmarks_list)
        #tip of index and middle fingers
        x1,y1 = landmarks_list[8][1:]
        x2,y2 = landmarks_list[12][1:]
        #3.Check which fingers are up
        fingers = detector.fingers_up()
        #print(fingers)
        #4.If Selection Mode- 2 Fingers are up
        if fingers[1] and fingers[2]:

            print("Selection Mode")
            xp=0
            yp=0
            if y1<125:
                if 250<x1<450:
                    draw_color=(255,0,255)
                    header = overlay_list[0]
                elif 550<x1<750:
                    draw_color=(255,0,0)
                    header = overlay_list[1]
                elif 800<x1<950:
                    draw_color=(0,255,0)
                    header = overlay_list[2]
                elif 1050<x1<1200:
                    draw_color=(0,0,0)
                    header = overlay_list[3]
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), draw_color, cv2.FILLED)
        #5.If Drawing Mode- Index Finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),25,draw_color,cv2.FILLED)
            if xp==0 and yp==0:
                xp=x1
                yp=y1
            print("Drawing Mode")
            if draw_color==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), draw_color, eraser_thickness)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, eraser_thickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),draw_color,brush_thickness)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, brush_thickness)
            xp,yp=x1,y1
    img_gray = cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)
    _,img_inv = cv2.threshold(img_gray,50,255,cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,img_inv)
    img = cv2.bitwise_or(img,img_canvas)
    #Setting the header image
    img[0:125,0:1280] = header
    #img = cv2.addWeighted(img,0.5,img_canvas,0.5,0)
    cv2.imshow('Image',img)
    cv2.imshow('Canvas',img_canvas)
    cv2.waitKey(1)