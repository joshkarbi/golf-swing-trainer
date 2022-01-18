## Possible Approaches to Golf Ball Tracking in Video ##

### Attempted: ###
- **Hough transforms** for circle detection
 - this sometimes works but in outdoor video it detected too many circles.. i.e. clouds trick it.

### Ideas: ###
- Train an **object detection model** using Keras and then use that on incoming video
 - Need a dataset of images and annotations .. a lot of work, but proven technique (done for soccer balls + players on Github)

- **Blob detection**: detect blob that's whiteish and circle-ish (these can be specified in OpenCV).

- **inRange filtering**: mask the image to color values that are white-ish (golf ball color)

- **Edge detection**: detect the ball boundary.

- **Background estimation**: use this to remove the background and get a video mask that only has the player+club+ball.

- **Any combination of the above techniques**.... i.e. background estimation + blob detection

