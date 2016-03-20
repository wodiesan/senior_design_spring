#!/usr/bin/env python
"""
Main file for a home monitoring system on the Raspberry Pi 2.

Requires --conf (JSON) and --face (XML) arguments.
Utilizes the Raspberry Pi 2 camera module and OpenCV framework.
Part of ELEC4500 Senior Electronic Design I, Spring 2016
Dept. of Electrical Engineering and Technology
Wentworth Institute of Technology.
"""
import argparse
import datetime
import json
import sys
import time
from threading import Thread
import warnings

import cv2
import imutils
from imutils.object_detection import non_max_suppression
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

# Path added to access default site packages on RPi2.
sys.path.append('/usr/local/lib/python2.7/site-packages')

# Front matter.
__author__ = "Sze 'Ron' Chau"
__credits__ = ["Adrian Rosebrock", "Nelson Bamford", "Ariel Martinez"]
__license__ = "MIT"
__maintainer__ = "Sze 'Ron' Chau"
__email__ = "wodiesan@gmail.com"

# Construct the argument parse.
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="JSON camera config.")
args = vars(ap.parse_args())

# Supress expected warnings and access camera config file.
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

# Populate JSON camera config.
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
camera.rotation = conf["rotation"]
print 'Initializing camera module.'

# Complete init for camera.
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))
time.sleep(conf["camera_warmup_time"])

# Init HOG detector, set SVM to pre-trained human silhouette detector.
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Capture frames from camera module.
for f in camera.capture_continuous(rawCapture, format="bgr",
                                   use_video_port=True):

    # Grab raw numpy array representing the img.
    # Init timestamp and on-screen status text.
    frame = f.array
    timestamp = datetime.datetime.now()
    text = "Clear"

    # Resize frame, preprocess with grayscale and Gaussian blur.
    frame = imutils.resize(frame, width=conf["frame_width"])
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(frame, (21, 21), 0)

    # Save a clone of the frame before preprocessing. Used for live preview.
    frameClone = frame.copy()

    # Detect silhouettes in frame. Adjust scale based on camera location.
    # winStride is the sliding window step size coordinates.
    # A > scale val evals < layers, t.f. it runs faster but less accurate.
    # weights is the confidence val returned from SVG per detection.
    (bodyRects, weights) = hog.detectMultiScale(gray, winStride=(4, 4),
                                                padding=(8, 8), scale=1.05)

    # Draw bounding boxes on detected regions of the clone frame.
    for (x, y, w, h) in bodyRects:
        cv2.rectangle(frameClone, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Apply non-maxima suppression to bounding boxes using a large overlap
    # thresh to try to maintain overlapping boxes.
    bodyRects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in bodyRects])
    pick = non_max_suppression(bodyRects, probs=None, overlapThresh=0.65)

    # Draw the final bounding boxes on the clone.
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(frameClone, (xA, yA), (xB, yB), (0, 255, 0), 2)
        text = 'Silhouette'

    # Populate the clone frame with datetime and relevant status information.
    # print("{} original boxes, {} after suppression".format(
    #       len(bodyRects), len(pick)))
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frameClone, "Sector: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frameClone, ts, (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # Verify whether the frames should be displayed to screen.
    if conf["show_video"]:
        cv2.imshow("Silhouette", frameClone)
        key = cv2.waitKey(1) & 0xFF

        # Pressing 'q' at anytime to terminate and exit.
        if key == ord("q"):
            break

    # Clear stream in preparation for the next frame.
    rawCapture.truncate(0)
