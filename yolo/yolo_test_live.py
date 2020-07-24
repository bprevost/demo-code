#!/usr/bin/env python3

import numpy as np
import cv2

from yolo import Yolo

yolo = Yolo()
cap = cv2.VideoCapture(0)

while(True):
    # Capture image from camera
    ret, image = cap.read()

    # Run yolo on the image
    yolo.run(image)

    # Display the output image
    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
