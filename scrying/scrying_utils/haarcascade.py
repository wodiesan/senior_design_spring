#!/usr/bin/env python
"""
OpenCV Haar Detector Class.

Part of ELEC4500 Senior Electronic Design I, Spring 2016
Dept. of Electrical Engineering and Technology
Wentworth Institute of Technology.
"""
import cv2
# from threading import Thread


class HaarDetect:
    def __init__(self, haarPath):
        # Path to the classifier.
        self.haarPath = cv2.CascadeClassifier(haarPath)
        # Thread(target=self.detect).start()

    def detect(self, image, scaleFac, minNbrs, minSize):
        # Detect objects in frame.
        rects = self.haarPath.detectMultiScale(image,
                scaleFactor=scaleFac, minNeighbors=minNbrs,
                minSize=minSize, flags = cv2.CASCADE_SCALE_IMAGE)

        # Return bounding rects.
        return rects

