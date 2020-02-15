#!/usr/bin/env python3
"""Example code for testing Foscam video"""

import argparse
import foscam
import cv2

def frame_callback(image, userdata):
    window_name = userdata
    cv2.imshow(window_name, image)
    cv2.waitKey(1)

if __name__ == "__main__":
    """Example code for testing Foscam video"""

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The IP address of the camera")
    parser.add_argument("user", help="The user account on the camera")
    parser.add_argument("password", help="The password of the user account")
    args = parser.parse_args()

    cam = foscam.Foscam(args.url, args.user, args.password)

    window_name = "Display {}".format(cam.url)
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    resolution = cam.RESOLUTION['640x480']
    rate = cam.RATE_FPS['2']
    cam.start_video(frame_callback, window_name, resolution, rate)
    cam.move_ptz("center", 2)
    cam.move_ptz("up", 2)
    cam.move_ptz("left", 2)
    cam.move_ptz("down", 2)
    cam.move_ptz("right", 2)
    cam.move_ptz("preset", 2)
    cam.stop_video()
    cv2.destroyAllWindows()
