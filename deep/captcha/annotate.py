#!/usr/bin/env python3

from imutils import paths
import imutils
import cv2

folder = 'downloads'
path_list = list(paths.list_images(folder))
for (i, image_path) in enumerate(path_list):
    print("Processing image {}/{} {}".format(i+1, len(path_list), image_path))
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:4] # Keep 4 largest
    for c in cnts:
        # Bounding box
        (x, y, w, h) = cv2.boundingRect(c)
        roi = gray[y-5:y+h+5, x-5:x+w+5]
        # Display
        cv2.imshow("ROI", imutils.resize(roi, width=28))
        key = cv2.waitKey(250)
