#!/usr/bin/env python
"""
Utility module to handle the time being displayed on security feed.

Part of ELEC4500 Senior Electronic Design I, Spring 2016
Dept. of Electrical Engineering and Technology
Wentworth Institute of Technology.
"""
#import sys
# Path added to access default site packages (cv2) on RPi2.
#sys.path.append('/usr/local/lib/python2.7/site-packages')
from datetime import datetime
import pytz
import time
from tzlocal import get_localzone


def utcnow(local_tz):
    '''Take the local timezone, convert a utc timestamp into local time.'''
    ts = time.time()
    utc_ts = datetime.utcfromtimestamp(ts)
    local_now = utc_ts.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_now
