#!/usr/bin/env python
"""
ELEC4500 Senior Design 1 | Spring 2016
Stand-alone human silhouette detection through HOG + Linear SVM.

Requires a directory where the detection will be executed.
"""

from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
# sys added to access default site packages folder.
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

# Front Matter
__author__      = "Sze 'Ron'Chau"
__copyright__   = "Copyright 2016, Sze Chau"
__credits__     = "Adrian Rosebrock, Ph.D."
__license__     = "MIT"
__version__     = "0.0.1"
__maintainer__  = "Sze 'Ron' Chau"
__email__       = "wodiesan@gmail.com"
__status__      = "Prototype"

# Construct the argument parse and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="""path to
                images directory""")
args = vars(ap.parse_args())

# Init HOG detector and set SVM to pre-trained silhouette detector.
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Loop over the image paths.
for imagePath in paths.list_images(args["images"]):
    # Load the image and resize it to:
    # 1. Reduce detection time.
    # 2. Improve detection accuracy.
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=min(400, image.shape[1]))
    orig = image.copy()

    # Detect people in the image. Scale is the MOST IMPORTANT TO TUNE.
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                                            padding=(8, 8), scale=1.05)

    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # show some information on the number of bounding boxes
    filename = imagePath[imagePath.rfind("/") + 1:]
    print("[INFO] {}: {} original boxes, {} after suppression".format(
        filename, len(rects), len(pick)))

    # show the output images
    cv2.imshow("Before NMS", orig)
    cv2.imshow("After NMS", image)
    cv2.waitKey(0)

# Previous work. Ignore.
# # import the necessary packages
# # sys added to access default site packages folder.
# import sys
# sys.path.append('/usr/local/lib/python2.7/site-packages')

# from picamera.array import PiRGBArray
# from picamera import PiCamera
# import time
# import cv2

# # initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(640, 480))

# # allow the camera to warmup
# time.sleep(0.1)

# # capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#   # grab the raw NumPy array representing the image, then initialize the timestamp
#   # and occupied/unoccupied text
#   image = frame.array

#   # show the frame
#   cv2.imshow("Frame", image)
#   key = cv2.waitKey(1) & 0xFF

#   # clear the stream in preparation for the next frame
#   rawCapture.truncate(0)

#   # if the `q` key was pressed, break from the loop
#   if key == ord("q"):
#       break
