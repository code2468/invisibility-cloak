# Importing Necessary Libraries #

import numpy as np
from cv2 import cv2
import time


# Capturing Webcam Feed
cap = cv2.VideoCapture(0)

time.sleep(3)

count = 0

background = 0

# Iteration for Capturing Static Background Frame

for i in range(60):

    ret, background = cap.read()


# Flip the Image

background = np.flip(background, axis=1)

 ##Reading every frame from the webcam, until the camera is open
while(cap.isOpened()):
    
    ret, img = cap.read()

    if not ret:
        break

    count+=1
    
    img = np.flip(img, axis=1)
    
#Converting from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #ranges should be chosen carefully
      # setting the lower and upper range
      #hsv values
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red) #seperating cloak

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red) #space except cloak
    
    mask1 = mask1 + mask2 #OR

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2) #refining mask & removing noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1) #refining mask & increasing smoothness

    mask2 = cv2.bitwise_not(mask1) #except cloak
    
     ## Segmenting the red color part out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(background, background, mask = mask1)

    ## Creating image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(img, img, mask = mask2)

    #final output
    #linearly added two images
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow('Invisible', final_output)
    k = cv2.waitKey(10)
    if k == 27: #Esc key
        break

cap.release()
cv2.destroyAllWindows()