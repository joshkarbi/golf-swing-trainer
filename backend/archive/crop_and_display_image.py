import cv2

image = cv2.imread("assets/player_swinging_2.jpg")
cropped = image[840:940, 400:500]

cv2.imshow("Original Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Cropped image", cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
