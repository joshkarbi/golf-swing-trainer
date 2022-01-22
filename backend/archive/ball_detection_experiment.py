
import cv2
import numpy as np

### CREATE MASK OF IMAGE HIGHLIGHTING WHITE/GRAY REGIONS ###

im = cv2.imread("assets/ball_close_up.jpg")
cv2.imshow("Original", im)
im = cv2.GaussianBlur(im, (3, 3), 0)
im = cv2.inRange(im, (180, 180, 180), (255,255,255))
im = cv2.bitwise_not(im)
cv2.imshow("Blurred, Masked, and Inverted", im)

### BLOB DETECTION ###

params = cv2.SimpleBlobDetector_Params()

params.filterByCircularity = False
params.minCircularity = 0.9

# params.minThreshold = 250
# params.maxThreshold = 255
# params.minRepeatability = 1
params.blobColor = 0
detector = cv2.SimpleBlobDetector_create(parameters=params)
keypoints = detector.detect(im)

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Blob Detection", im_with_keypoints)

### EDGE DETECTION ###

img_blur = cv2.GaussianBlur(im, (3,3), 0)

sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
# cv2.imshow('Sobel X', sobelx)
# cv2.imshow('Sobel Y', sobely)
# cv2.imshow('Sobel X Y using Sobel() function', sobelxy)

### HOUGH TRANSFORM ON MASKED IMAGE ###
hough_image = im
circles = cv2.HoughCircles(hough_image, cv2.HOUGH_GRADIENT, 1.2, 100)
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")        
    for (x, y, r) in circles:
        hough_image = cv2.circle(hough_image, (x,y), r, (0,0,255), 4)
    
    cv2.imshow("Hough Circles", hough_image)

cv2.waitKey(0)
cv2.destroyAllWindows()