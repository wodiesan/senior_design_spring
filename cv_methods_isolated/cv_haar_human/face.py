#!/usr/bin/env python
# sys added to access default site packages folder.
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

"""
ELEC4500 Senior Design 1 | Spring 2016
Stand-alone human facial detection through Haar Cascades.

Requires a JSON config list and a XML cascade classifier.
"""

from pyimagesearch.facedetector import FaceDetector
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2

# Front Matter
__author__      = "Sze 'Ron'Chau"
__copyright__   = "Copyright 2016, Sze Chau"
__credits__     = "Adrian Rosebrock, Ph.D."
__license__     = "MIT"
__version__     = "0.0.1"
__maintainer__  = "Sze 'Ron' Chau"
__email__       = "wodiesan@gmail.com"
__status__      = "Prototype"

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True,
                help="path to where the face cascade resides")
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-c", "--conf", required=True,
                help="path to the JSON configuration file")
args = vars(ap.parse_args())

# construct the face detector
fd = FaceDetector(args["face"])

# Filter all warnings and load the configuration.
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]

# Added rotation to camera to negate physical limitations.
camera.rotation = 270

rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

# Allow the camera to warmup, then init the average frame, last
# uploaded timestamp, and frame motion counter/
print "[INFO] Initializing camera..."
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr",
                                   use_video_port=True):
    # Grab the raw NumPy array representing the image and initialize
    # the timestamp and occupied/unoccupied text.
    frame = f.array
    timestamp = datetime.datetime.now()
    text = "Clear"

    # Resize the frame, convert it to grayscale, and blur it.
    # IMUTILS.RESIZE MODIFIED D/T RESIZING OF PREVIEW STREAM
    frame = imutils.resize(frame, width=480)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Detect faces in the image and then clone the frame
    # so that we can draw on it.
    faceRects = fd.detect(gray, scaleFactor=1.1, minNeighbors=5,
                          minSize=(30, 30))
    frameClone = frame.copy()

    # Loop over the face bounding boxes and draw them.
    for (fX, fY, fW, fH) in faceRects:
        # Attempt: Predator shoulder cannon crosshairs.
        # sixteen = fW//16
        # bottomLeft = sixteen*2
        # bottomRight = sixteen*10
        # bottomY = sixteen*12
        # topLeft = sixteen*7
        # topRight = sixteen*9
        # cv2.line(frameClone, (topLeft, sixteen), (sixteen, topLeft), (0, 0, 255), 3)
        # cv2.line(frameClone, (topRight, sixteen), (sixteen, topRight), (0, 0, 255), 3)
        # cv2.line(frameClone, (bottomLeft, bottomY), (bottomRight, bottomY), (0, 0, 255), 3)
        #cv2.line(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 3)
        cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 3)
        text = 'Encounter!'

    # Show our detected faces.
    # cv2.imshow("Face", frameClone)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # if the average frame is None, initialize it
    # if avg is None:
    #   print "[INFO] Initializing and averaging sector..."
    #   avg = gray.copy().astype("float")
    #   rawCapture.truncate(0)
    #   continue

    # accumulate the weighted average between the current frame and
    # previous frames, then compute the difference between the current
    # frame and running average
    # cv2.accumulateWeighted(gray, avg, 0.5)
    # frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # threshold the delta image, dilate the thresholded image to fill
    # in holes, then find contours on thresholded image
    # thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
    #   cv2.THRESH_BINARY)[1]
    # thresh = cv2.dilate(thresh, None, iterations=2)

    # MODIFICATION FROM OPENCV 2.4 TO OPENCV 3
    # #(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    # # cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    #   cv2.CHAIN_APPROX_SIMPLE)[-2]

    # loop over the contours
    # for c in cnts:
    #   # if the contour is too small, ignore it
    #   if cv2.contourArea(c) < conf["min_area"]:
    #       continue

    #   # compute the bounding box for the contour, draw it on the frame,
    #   # and update the text
    #   (x, y, w, h) = cv2.boundingRect(c)
    #   cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #   text = "Contact!"

    # # draw the text and timestamp on the frame
    # ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    # #cv2.putText(frame, "Sector: {}".format(text), (10, 20),
    # cv2.putText(frame, "Sector", (10, 20),
    #   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
    #   0.35, (0, 0, 255), 1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # draw the text and timestamp on the frame
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frameClone, "Sector: {}".format(text), (10, 20),
                #cv2.putText(frameClone, "Sector", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frameClone, ts, (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # check to see if the room is occupied
    if text == "Encounter!":
        # check to see if enough time has passed between uploads
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
            # increment the motion counter
            motionCounter += 1

            # check to see if the number of frames with consistent motion is
            # high enough
            if motionCounter >= conf["min_motion_frames"]:

                # update the last uploaded timestamp and reset the motion
                # counter
                lastUploaded = timestamp
                motionCounter = 0

    # otherwise, the room is not occupied
    else:
        motionCounter = 0

    # Verify whether the frames should be displayed to screen.
    if conf["show_video"]:
        # Show detected faces.
        cv2.imshow("Face", frameClone)
        key = cv2.waitKey(1) & 0xFF

        # Pressing 'q' at anytime will terminate the program.
        if key == ord("q"):
            break

    # Clear the stream in preparation for the next frame.
    rawCapture.truncate(0)
