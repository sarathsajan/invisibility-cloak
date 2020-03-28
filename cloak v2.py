import numpy as np
import cv2
import time

time.sleep(3)

#red_low = [[0, 120, 50], [20, 255, 255]]
#red_up = [[160, 120, 50], [179, 255, 255]]

red_low = [[0, 130, 60], [15, 255, 255]]
red_up = [[164, 130, 60], [179, 255, 255]]

url = "http://192.168.1.101:8080/video"
cap = cv2.VideoCapture(url)
#time.sleep(3)
ret, background = cap.read()


while True:
    ret, img = cap.read()
    #rgb2hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    bgr2hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #lower red range
    lower_red = np.array(red_low[0])
    upper_red = np.array(red_low[1])
    mask1 = cv2.inRange(bgr2hsv, lower_red, upper_red)
        
    #upper red range
    lower_red = np.array(red_up[0])
    upper_red = np.array(red_up[1])
    mask2 = cv2.inRange(bgr2hsv, lower_red, upper_red)

    mask = mask1 + mask2

    mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask2 = cv2.bitwise_not(mask1)

    result1 = cv2.bitwise_and(img, img, mask = mask2)
    result2 = cv2.bitwise_and(background, background, mask = mask1)

    final_output = cv2.addWeighted(result1, 1, result2, 1, 0)

#-----------------------------------------------------------------------------------------------------------------------------
    cv2.imshow("background_rgb", background)
    cv2.imshow('img', img)
    cv2.imshow('bgr2hsv', bgr2hsv)
    cv2.imshow('mask1', mask1)
    cv2.imshow('mask2', mask2)
    cv2.imshow('result1', result1)
    cv2.imshow('result2', result2)
    cv2.imshow('final', final_output)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break