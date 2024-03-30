# program to capture a single image from the webcam in Python

# importing OpenCV library
from cv2 import VideoCapture, imshow, imwrite, waitKey, destroyWindow

# initialize the camera
# If you have multiple cameras connected,
# assign a value to cam_port according to the desired camera
cam_port = 0
cam = VideoCapture(cam_port)

# reading the input using the camera
result, image = cam.read()

# If an image is detected without any error, show the result
if result:

    # showing result, it takes frame name and image output
    imshow("Capture Image", image)
    print("Captured!")

    # saving the image in local storage
    imwrite("images/capture.png", image)
    print("Image is now save on folder!")

    # If a keyboard interrupt occurs, destroy the image window
    #waitKey(0)
    destroyWindow("Capture Image")

# If the captured image is corrupted, move to the else part
else:
    print("No image detected. Please try again")
