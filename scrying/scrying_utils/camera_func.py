#!/usr/bin/env python
"""
Functions related to the camera module.

Part of ELEC4500 Senior Electronic Design I, Spring 2016
Dept. of Electrical Engineering and Technology
Wentworth Institute of Technology.
"""
from threading import Thread

from picamera.array import PiRGBArray
from picamera import PiCamera


class Scrying_Stream:
    '''Utilize multi-threading for capturing and processing frames.'''
    def __init__(self, resolution=(640, 480), framerate=15, rotation=270):
        # Init camera module and stream.
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.rotation = rotation
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="bgr",
                                                     use_video_port=True)

        # Init frame and a var to indicate the thread stopping point.
        self.frame = None
        self.stopped = False

    def start(self):
        '''Start a thread to intercept incoming frames.'''
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        '''Continuously loop until the thread is stopped.'''
        for f in self.stream:
            # Grab frame and clear stream in preparation for the next frame.
            self.frame = f.array
            self.rawCapture.truncate(0)

            # If the thread indicator is set, stop thread and camera resources.
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        '''Return the last frame that was analyzed.'''
        return self.frame

    def stop(self):
        '''Indicate the stopping point for a thread.'''
        self.stopped = True
