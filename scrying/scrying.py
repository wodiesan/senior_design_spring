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
import json
import sys
import time
from threading import Thread
import warnings

# Path added to access default site packages (cv2) on RPi2.
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
from scrying_utils.camera_func import Scry
import scrying_utils.init_logger as scrying_log
from scrying_utils.haarcascade import HaarDetect
import scrying_utils.preprocessing_func as prepro
import scrying_utils.time_disp as time_disp
import imutils
from imutils.video import FPS
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

# Get the local timezone to convert UTC time for display.
local_tz = time_disp.get_localzone()

# Init logging to console and files.
logger_rpi = 'history/'
user_log = 'log_scrying_user.log'
dev_log = 'log_scrying_dev.log'
logger = scrying_log.init_logger(__name__, logger_rpi, user_log, dev_log)
logger.debug('Init logging to console and files successful.')

# Construct the argument parse.
logger.debug('Parsing command-line arguments.')
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
                help="# of frames to loop over for FPS test")
ap.add_argument("-c", "--conf", required=True, help="JSON camera config path.")
ap.add_argument("-f", "--face", required=False,
                help="Face Haar path.")
ap.add_argument("-v", "--vehi", action='store_true', required=False,
                help="Vehicle Haar path.")
args = vars(ap.parse_args())

# Facial detection.
fd = HaarDetect(args['face'])

# Alert the user if any of the optional command-line options are missing.
if not args['face']:
    logger.error('No Haar facial classifer found. Skipping facial detect.')
if not args['vehi']:
    logger.error('No Haar vehicle classifier found. Skipping vehicle detect.')

# Supress expected warnings and access camera config file.
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
logger.debug('Command-line arguments loaded.')

# Init camera module with JSON config file.
logger.debug('Initiating camera module.')
res = tuple(conf["480p"])
fps = conf["fps"]
rot = conf["rotation"]

# try:
#     camera = PiCamera()
#     camera.resolution = tuple(conf["480p"])
#     camera.framerate = conf["fps"]
#     camera.rotation = conf["rotation"]

# except PiCamera.exc.PiCameraError:
#     logger.critical('Unable to access camera module. Exiting.')
#     sys.exit()

# Init seperate thread for pipeline.
# rawCapture = PiRGBArray(camera, size=tuple(conf["480p"]))
camera = Scry().start()
time.sleep(conf["camera_warmup_time"])
logger.debug('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
             '     Streaming {} resolution at {} fps.           \n'
             '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
             ''.format(res, fps))

# Init HOG detector, set SVM to pre-trained human silhouette detector.
# DISABLED FOR SENIOR DESIGN SHOWCASE ON 09AUG2016.
# hog = cv2.HOGDescriptor()
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Capture frames from camera module.
# camera.start()
# for f in camera.capture_continuous(rawCapture, format="bgr",
#                                    use_video_port=True):

logger.debug('Begin FPS counter.')
fps = FPS().start()

# While statement for multithreaded approach; for statement otherwise.
# for f in camera.capture_continuous(rawCapture, format="bgr",
#                                    use_video_port=True):
while camera:

    # Grab raw numpy array representing img and init on-screen status text.
    # frame = f.array
    frame = camera.read()
    text = "Clear"

    # Resize frame, preprocess with grayscale and Gaussian blur.
    # frame = imutils.resize(frame, width=conf["width_480p"])
    gray = prepro.grayscale(frame)
    # gray = prepro.gauss(frame, (21, 21), 0)

    # Detect faces in the image and then clone the frame
    # so that we can draw on it.
    # faceRects = fd.detect(gray, scaleFac=1.1, minNbrs=5,
    #                       minSize=(30, 30))
    faceRects = fd.detect(gray, 1.1, 5, (30, 30))
    frameClone = frame.copy()

    # Loop over the face bounding boxes and draw them.
    for (fX, fY, fW, fH) in faceRects:
        cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 3)
        text = 'Face detected!'

    # Detect silhouettes in frame. Adjust scale based on camera location.
    # winStride is the sliding window step size coordinates.
    # A > scale val evals < layers, t.f. it runs faster but less accurate.
    # weights is the confidence val returned from SVG per detection.
    # DISABLED FOR SENIOR DESIGN SHOWCASE ON 09AUG2016.
    # (bodyRects, weights) = hog.detectMultiScale(gray, winStride=(4, 4),
    #                                             padding=(8, 8), scale=1.05)

    # Draw bounding boxes on detected regions of the clone frame.
    # for (x, y, w, h) in bodyRects:
    #     cv2.rectangle(frameClone,
    #                   (x, y),
    #                   (x + w, y + h),
    #                   tuple(conf["green"]),
    #                   1)

    # Apply non-maxima suppression to bounding boxes using a large overlap
    # thresh to try to maintain overlapping boxes.
    # DISABLED FOR SENIOR DESIGN SHOWCASE ON 09AUG2016.
    # bodyRects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in bodyRects])
    # pick = non_max_suppression(bodyRects, probs=None, overlapThresh=0.65)

    # Draw the final bounding boxes on the clone.
    # DISABLED FOR SENIOR DESIGN SHOWCASE ON 09AUG2016.
    # for (xA, yA, xB, yB) in pick:
    #     cv2.rectangle(frameClone,
    #                   (xA, yA),
    #                   (xB, yB),
    #                   tuple(conf["tyrian"]),
    #                   2)
    #     text = 'Silhouette'

    # Populate the display feed with the time and relevant status information.
    # ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frameClone,
                "Sector: {}".format(text),
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                conf["font_sector"],
                tuple(conf["red"]),
                2)

    cv2.putText(frameClone,
                str(time_disp.utcnow(local_tz)),
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
            fps.stop()
            print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
            logger.debug('User terminated program. Exiting.')
            cv2.destroyAllWindows()
            camera.stop()
            break

    # Update FPS counter.
    fps.update()

    # Clear stream in preparation for the next frame.
    # Comment out for multithreaded implementation.
    # rawCapture.truncate(0)
