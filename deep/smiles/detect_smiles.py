#!/usr/bin/env python3

import numpy as np
import cv2
import imutils

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Load the face detector and smile detector
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = load_model('lenet.hdf5')

camera = cv2.VideoCapture(0)
while True:
    (grabbed, frame) = camera.read()
    frame = imutils.resize(frame, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_clone = frame.copy()
    # Detect faces
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(45, 45), flags=cv2.CASCADE_SCALE_IMAGE)
    # Loop over faces
    for (fX, fY, fW, fH) in rects:
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (28, 28))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        # Detect smiles
        (not_smiling, smiling) = model.predict(roi)[0]
        if smiling > not_smiling:
            label = 'Smiling'
            color = (255, 0, 0) # green
        else:
            label = 'Not Smiling'
            color = (0, 0, 255) # red
        cv2.rectangle(frame_clone, (fX, fY), (fX + fW, fY + fH), color, 2)
        cv2.putText(frame_clone, label, (fX, fY - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            
    # Display
    cv2.imshow("Face", frame_clone)
    if cv2.waitKey(100) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

