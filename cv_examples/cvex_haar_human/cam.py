# USAGE
# python cam.py --face cascades/haarcascade_frontalface_default.xml

# import the necessary packages
# sys added to access default site packages folder.
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

# 05MAR2016
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from picamera.array import PiRGBArray
from picamera import PiCamera
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from pyimagesearch.facedetector import FaceDetector
from pyimagesearch import imutils
#import imutils
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required = True,
	help = "path to where the face cascade resides")
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())

# construct the face detector
fd = FaceDetector(args["face"])

# if a video path was not supplied, grab the reference
# to the gray
if not args.get("video", False):
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#camera = cv2.VideoCapture(0)

	# initialize the camera and grab a reference to the raw camera capture
	camera = PiCamera()
	camera.resolution = (1280, 720)
	camera.framerate = 30

	# ADDED ROTATION FUNCTION.
	camera.rotation = 270
	rawCapture = PiRGBArray(camera, size = (1280, 720))
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# otherwise, load the video
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a
	# frame, then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame and convert it to grayscale
	frame = imutils.resize(frame, width = 300)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the image and then clone the frame
	# so that we can draw on it
	faceRects = fd.detect(gray, scaleFactor = 1.1, minNeighbors = 5,
		minSize = (30, 30))
	frameClone = frame.copy()

	# loop over the face bounding boxes and draw them
	for (fX, fY, fW, fH) in faceRects:
		cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 2)

	# show our detected faces
	cv2.imshow("Face", frameClone)

	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
