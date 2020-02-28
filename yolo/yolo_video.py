#!/usr/bin/env python3

import cv2
from yolo import Yolo

yolo = Yolo()
vs = cv2.VideoCapture('overpass.mp4')
prop = cv2.CAP_PROP_FRAME_COUNT
total = int(vs.get(prop))
print('{} total frames in video'.format(total))
count = 0
while True:
    (grabbed, frame) = vs.read()
    if not grabbed: # End of video
        break
    count = count + 1
    print('Searching frame {} of {}'.format(count, total))
    yolo.run(frame)
    cv2.imshow('Image', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: # Escape to quit
        break
