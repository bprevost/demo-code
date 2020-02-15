#!/usr/bin/env python3
"""For Foscam IP Cameras, based on IP Camera CGI V1.21"""

from urllib.request import urlopen
import time
import threading
import numpy as np
import cv2
import argparse

class Foscam:
    """For Foscam IP Cameras, based on IP Camera CGI V1.21"""

    # For PTZ control
    PTZ = {
        "UP":0,
        "STOP_UP":1,
        "DOWN":2,
        "STOP_DOWN":3,
        "LEFT":6,
        "STOP_LEFT":7,
        "RIGHT":4,
        "STOP_RIGHT":5,
        "CENTER":25,
        "PRESET_1":31
    }

    # For video resolution and rate
    RESOLUTION = {"320x240":8, "640x480":32}
    RATE_FPS = {
        "full":0,
        "20":1,
        "15":3,
        "10":6,
        "5":11,
        "4":12,
        "3":13,
        "2":14,
        "1":15
    }

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.params = self.get_camera_params()
        self.params.update(self.get_misc_params())
        self.is_playing = False

    def send_command(self, cgi, param_dict, timeout=2):
        url = "http://{}/{}?user={}&pwd={}".format(
            self.url, cgi, self.user, self.password)
        for param in param_dict:
            url += "&{}={}".format(param, param_dict[param])
        return urlopen(url, timeout=timeout)

    def decode_params(self, f):
        param_dict = {}
        string_list = f.read().decode("utf-8").split("\n")
        for string in string_list:
            param = string.lstrip("var").lstrip().rstrip(";").split("=")
            if len(param) == 2:
                param_dict[param[0]] = param[1]
        return param_dict

    def get_camera_params(self):
        f = self.send_command("get_camera_params.cgi", {})
        return self.decode_params(f)

    def get_misc_params(self):
        f = self.send_command("get_misc.cgi", {})
        return self.decode_params(f)

    def move_ptz(self, direction, duration=1):
        flip = (self.params["flip"] == "3") # Is camera upside down?
        if (direction == "up" and not flip) or (direction == "down" and flip):
            self.send_command("decoder_control.cgi", {"command":self.PTZ["UP"]})
            time.sleep(duration)
            self.send_command("decoder_control.cgi", {"command":self.PTZ["STOP_UP"]})
        elif (direction == "down" and not flip) or (direction == "up" and flip):
            self.send_command("decoder_control.cgi", {"command":self.PTZ["DOWN"]})
            time.sleep(duration)
            self.send_command("decoder_control.cgi", {"command":self.PTZ["STOP_DOWN"]})
        elif (direction == "left" and not flip) or (direction == "right" and flip):
            self.send_command("decoder_control.cgi", {"command":self.PTZ["LEFT"]})
            time.sleep(duration)
            self.send_command("decoder_control.cgi", {"command":self.PTZ["STOP_LEFT"]})
        elif (direction == "right" and not flip) or (direction == "left" and flip):
            self.send_command("decoder_control.cgi", {"command":self.PTZ["RIGHT"]})
            time.sleep(duration)
            self.send_command("decoder_control.cgi", {"command":self.PTZ["STOP_RIGHT"]})
        elif (direction == "center"):
            self.send_command("decoder_control.cgi", {"command":self.PTZ["CENTER"]})
            time.sleep(duration)
        elif (direction == "preset"):
            self.send_command("decoder_control.cgi", {"command":self.PTZ["PRESET_1"]})
            time.sleep(duration)

    def snapshot_jpg(self, filename):
        f = self.send_command("snapshot.cgi", {})
        data = f.read()
        open(filename, "wb").write(data) # jpg

    def video_thread(self, f, callback, userdata):
        sequence = 0 # Counter
        while self.is_playing:
            line = f.readline().decode("utf-8")
            if line[:len("--ipcamera")] == "--ipcamera":
                f.readline()
                content_length = int(f.readline().decode("utf-8").split(":")[1].strip())
                f.readline()
                buffer = f.read(content_length)
                jpeg = np.frombuffer(buffer, dtype=np.uint8)
                image = cv2.imdecode(jpeg, cv2.IMREAD_COLOR)
                sequence = sequence + 1
                if callback is not None:
                    callback(image, userdata)
                else:
                    print(sequence)

    def start_video(self, callback=None, userdata=None, resolution=32, rate=0):
        if not self.is_playing:
            cmd = {"resolution":resolution, "rate":rate}
            f = self.send_command("videostream.cgi", cmd)
            self.videothread = threading.Thread(
                target=self.video_thread,
                args=(f, callback, userdata))
            self.is_playing = True
            self.videothread.start()

    def stop_video(self):
        if self.is_playing:
            self.is_playing = False
            self.videothread.join()

if __name__ == "__main__":
    """Example code for testing Foscam class"""
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The IP address of the camera")
    parser.add_argument("user", help="The user account on the camera")
    parser.add_argument("password", help="The password of the user account")
    args = parser.parse_args()

    cam = Foscam(args.url, args.user, args.password)
    print(cam.url, cam.user, cam.password)
    print(cam.params)
