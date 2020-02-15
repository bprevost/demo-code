#!/usr/bin/env python3
'''This is a NetworkTables server (the robot side).'''

import time
from networktables import NetworkTables
import logging

# To see messages from networktables, you must setup logging
logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

robotTime = 0
while True:
    sd.putNumber("robotTime", robotTime)
    robotTime += 1

    dsTime = sd.getNumber("dsTime", "N/A")
    print("dsTime:", dsTime)

    time.sleep(1)
