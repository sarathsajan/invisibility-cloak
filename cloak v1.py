import numpy as np
import cv2
import time
from PIL import ImageGrab

def capture_image():
    image = np.array(ImageGrab.grab(bbox=(100, 100, 500, 500)))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return image_hsv, image_rgb, image

bg_hsv, bg_rgb, bg_bgr = capture_image()

while True:
    start_time = time.time()

    img_hsv, img_rgb, img_bgr = capture_image()
    
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([160, 100, 100])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_red, upper_red)

    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    mask2 = cv2.bitwise_not(mask1)

    result1 = cv2.bitwise_and(bg_rgb, bg_rgb, mask=mask1)
    result2 = cv2.bitwise_and(img_rgb, img_rgb, mask = mask2)
    final_output = cv2.addWeighted(result1, 1, result2, 1, 0)

    cv2.imshow("bg_rgb", bg_rgb)
    #cv2.imshow("img_bgr", img_bgr)
    #cv2.imshow("img_hsv", img_hsv)
    cv2.imshow("mask1", mask1)
    cv2.imshow("mask2", mask2)
    #cv2.imshow("result1", result1)
    #cv2.imshow("result2", result2)
    cv2.imshow("Final Render", final_output)

    print "One frame took {} seconds to process".format(time.time() - start_time)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break