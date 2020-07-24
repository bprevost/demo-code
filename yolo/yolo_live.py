#!/usr/bin/env python3

import numpy as np
import cv2

from yolo import Yolo

print("Start")

cap = cv2.VideoCapture(0)
yolo = Yolo()

while(True):
    # Capture image from camera
    ret, image = cap.read()

    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)

    # Run yolo on the image
    yolo.run(image)

    # Display the resulting image
    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
