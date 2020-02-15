#!/usr/bin/env python3
"""Example code for testing Foscam snapshot"""

import argparse
import foscam

parser = argparse.ArgumentParser()
parser.add_argument("url", help="The IP address of the camera")
parser.add_argument("user", help="The user account on the camera")
parser.add_argument("password", help="The password of the user account")
args = parser.parse_args()

cam = foscam.Foscam(args.url, args.user, args.password)

print("Moving to center...")
cam.move_ptz("center", 2)
cam.snapshot_jpg("center.jpg")

print("Moving up...")
cam.move_ptz("up", 2)
cam.snapshot_jpg("up.jpg")

print("Moving left...")
cam.move_ptz("left", 2)
cam.snapshot_jpg("left.jpg")

print("Moving down...")
cam.move_ptz("down", 2)
cam.snapshot_jpg("down.jpg")

print("Moving right...")
cam.move_ptz("right", 2)
cam.snapshot_jpg("right.jpg")

print("Moving to preset...")
cam.move_ptz("preset", 2)
cam.snapshot_jpg("preset.jpg")
