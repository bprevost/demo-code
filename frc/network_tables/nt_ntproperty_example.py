#!/usr/bin/env python3
'''This NetworkTables client demonstrates the use of classes to access values.'''

import time
from networktables import NetworkTables
from networktables.util import ntproperty
import logging

# To see messages from networktables, you must setup logging
logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize(server='192.168.1.21')

class SomeClient(object):
    robotTime = ntproperty("/SmartDashboard/robotTime", 0)
    dsTime = ntproperty("/SmartDashboard/dsTime", 0)

c = SomeClient()

while True:
    print("robotTime:", c.robotTime)
    print("dsTime:", c.dsTime)
    time.sleep(1)
