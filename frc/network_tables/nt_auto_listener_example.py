#!/usr/bin/env python3
'''This NetworkTables client will monitor an automatically updated value.'''

import time
from networktables import NetworkTables
import logging

# To see messages from networktables, you must setup logging
logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize(server='192.168.1.21')
sd = NetworkTables.getTable("SmartDashboard")
auto_value = sd.getAutoUpdateValue("robotTime", 0)

while True:
    robotTime = auto_value.value
    print("robotTime:", robotTime)
    time.sleep(1)
