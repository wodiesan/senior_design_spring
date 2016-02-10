"""
@author:     Sze "Ron" Chau
@e-mail:     chaus3@wit.edu
@source:     https://github.com/wodiesan/sweet-skoomabot
@desc        Night sensor-->RPi for Senior Design 1
"""

import logging
import os
import RPi.GPIO as GPIO
import serial
import subprocess
import sys
import time
import traceback

# GPIO pins. Uses the BCM numbering system based on RPi B+ board.
IR1 = 26
IR2 = 19
IR3 = 13
IR4 = 6

def init_serial():
    """Initialize the serial connection to the light sensor."""
    ser = serial.Serial()
    #ser.port = "\\.\COM4"       # Windows
    ser.port = "/dev/ttyUSB0"  # Linux
    ser.baudrate = 57600
    try:
        ser.open()
    except Exception, e:
        logger.info("Possible open serial port: " + str(e))
        print 'Check the serial USB port.'
        exit()
    return ser


def init_leds():
    """Initial setup for light sensor and IR LEDs. Currently uses the BCM
     numbering system based on RPi B+ board."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR1, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IR2, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IR3, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IR4, GPIO.OUT, initial=GPIO.HIGH)
    thread = threading.Thread(target=warnings)
    thread.daemon = False
    thread.start()
    return thread
