#!/usr/bin/env python
"""
OpenCV pre-processing functions.

Part of ELEC4500 Senior Electronic Design I, Spring 2016
Dept. of Electrical Engineering and Technology
Wentworth Institute of Technology.
"""
import cv2


def grayscale(frame):
    '''Convert a frame to grayscale.'''
    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame


def gauss(frame, kern_size, std_deviation):
    '''Pre-process a frame through Gausiann blur.
    Provide a tuple for kernel size followed by an int for sigma.'''
    cv2.GaussianBlur(frame, kern_size, std_deviation)
    return frame
