#!/usr/bin/env python3

import numpy as np
import cv2

from yolo import Yolo

yolo = Yolo()

# Load and run the input image
image = cv2.imread('traffic.jpg')
yolo.run(image)

# Display the output image
cv2.imshow('Image', image)
cv2.waitKey(10000)
