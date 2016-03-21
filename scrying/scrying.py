#!/usr/bin/env python
"""
Main file for a home monitoring system on the Raspberry Pi 2.

Requires --conf (JSON) and --car and --face (XML's) arguments.
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

# Path added to access default site packages (cv2) on RPi2.
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import scrying_utils.init_logger as scrying_log
import scrying_utils.preprocessing_func as prepro
import imutils
from imutils.object_detection import non_max_suppression
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

# Front matter.
__author__ = "Sze 'Ron' Chau"
__credits__ = ["Adrian Rosebrock", "Nelson Bamford", "Ariel Martinez"]
__license__ = "MIT"
__maintainer__ = "Sze 'Ron' Chau"
__email__ = "wodiesan@gmail.com"

# Init logging to console and files.
logger_rpi = 'history/'
user_log = 'log_scrying_user.log'
dev_log = 'log_scrying_dev.log'
logger = scrying_log.init_logger(__name__, logger_rpi, user_log, dev_log)
logger.debug('Init logging to console and files successful.')

# Construct the argument parse.
logger.debug('Parsing command-line arguments.')
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="JSON camera config path.")
ap.add_argument("-f", "--face", action='store_true', required=False,
                help="Face Haar path.")
ap.add_argument("-v", "--vehi", action='store_true', required=False,
                help="Vehicle Haar path.")
args = vars(ap.parse_args())

# Alert the user if any of the optional command-line options are missing.
if not args['face']:
    logger.error('No Haar facial classifer found. Skipping facial detect.')
if not args['vehi']:
    logger.error('No Haar vehicle classifier found. Skipping vehicle detect.')

# Supress expected warnings and access camera config file.
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
logger.debug('Command-line arguments loaded.')

# Init camera mocule with JSON config file.
logger.debug('Init camera module.')
camera = PiCamera()
camera.resolution = tuple(conf["480p"])
camera.framerate = conf["fps"]
camera.rotation = conf["rotation"]

# Complete init for camera.
rawCapture = PiRGBArray(camera, size=tuple(conf["480p"]))
time.sleep(conf["camera_warmup_time"])
logger.debug('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
             '|          Begin analyzing video stream.           |\n'
             '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

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
    frame = imutils.resize(frame, width=conf["width_480p"])
    # gray = prepro.grayscale(frame)
    gray = prepro.gauss(frame, (21, 21), 0)

    # Save a clone of the frame before preprocessing. Used for live preview.
    frameClone = frame.copy()

    # Detect silhouettes in frame. Adjust scale based on camera location.
    # winStride is the sliding window step size coordinates.
    # A > scale val evals < layers, t.f. it runs faster but less accurate.
    # weights is the confidence val returned from SVG per detection.
    (bodyRects, weights) = hog.detectMultiScale(gray, winStride=(4, 4),
                                                padding=(8, 8), scale=1.05)

    # Draw bounding boxes on detected regions of the clone frame.
    # for (x, y, w, h) in bodyRects:
    #     cv2.rectangle(frameClone,
    #                   (x, y),
    #                   (x + w, y + h),
    #                   tuple(conf["green"]),
    #                   1)

    # Apply non-maxima suppression to bounding boxes using a large overlap
    # thresh to try to maintain overlapping boxes.
    bodyRects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in bodyRects])
    pick = non_max_suppression(bodyRects, probs=None, overlapThresh=0.65)

    # Draw the final bounding boxes on the clone.
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(frameClone,
                      (xA, yA),
                      (xB, yB),
                      tuple(conf["tyrian"]),
                      2)
        text = 'Silhouette'

    # Populate the clone frame with datetime and relevant status information.
    # print("{} original boxes, {} after suppression".format(
    #       len(bodyRects), len(pick)))
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frameClone,
                "Sector: {}".format(text),
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                conf["font_sector"],
                tuple(conf["red"]),
                2)

    cv2.putText(frameClone,
                ts,
                (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                conf["font_time"],
                tuple(conf["red"]),
                1)

    # Verify whether the frames should be displayed to screen.
    if conf["show_video"]:
        cv2.imshow("Scrying", frameClone)
        key = cv2.waitKey(1) & 0xFF

        # Pressing 'q' at anytime to terminate and exit.
        if key == ord("q"):
            logger.debug('User terminated program. Exiting.')
            break

    # Clear stream in preparation for the next frame.
    rawCapture.truncate(0)
