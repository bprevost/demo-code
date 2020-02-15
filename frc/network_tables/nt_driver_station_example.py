#!/usr/bin/env python3
'''This is a NetworkTables client (driver station or coprocessor side).'''

import time
from networktables import NetworkTables
import logging

# To see messages from networktables, you must setup logging
logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize(server='192.168.1.21')
sd = NetworkTables.getTable("SmartDashboard")

dsTime = 0
while True:
    sd.putNumber("dsTime", dsTime)
    dsTime += 1

    robotTime = sd.getNumber("robotTime", "N/A")
    print("robotTime:", robotTime)

    time.sleep(1)
