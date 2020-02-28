#!/usr/bin/env python3

import os
import os.path
import time
import numpy as np
import cv2

class Yolo(object):

    labels_path = 'coco.names'
    weights_path = 'yolov3.weights'
    config_path = 'yolov3.cfg'
    confidence = 0.5 # Minimum probability to filter out detections
    threshold = 0.3 # Threshold when applying non-maxima suppression

    def __init__(self):

        if not os.path.isfile(self.weights_path):
            print("Assembling {} file...".format(self.weights_path))
            os.system('cat {0}.* > {0}'.format(self.weights_path))

        # Load the COCO class labels that the YOLO model was trained on
        self.labels = open(self.labels_path).read().strip().split('\n')

        # Initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype='uint8')

        # Load the YOLO object detector trained on the COCO dataset (80 classes)
        self.net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)

        # Determine the output layer names that are needed from YOLO
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def run(self, image):

        # Construct a blob from the image and perform a forward pass of the object detector
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(self.ln)
        end = time.time()
        print('YOLO took {:.6f} seconds'.format(end - start))

        # Initialize lists of detected bounding boxes, confidences, and class IDs
        boxes = []
        confidences = []
        classIDs = []

        (H, W) = image.shape[:2]
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > self.confidence:
                    # Scale the bounding box coordinates back relative to the size of the image
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype('int')
                    # Derive the top left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # Update the list of bounding box coordinates, confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.threshold)

        # Ensure at least one detection exists and loop over the indexes we are keeping
        if len(idxs) > 0:
            for i in idxs.flatten():
                # Extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                # Draw a bounding box rectangle and label on the image
                color = [int(c) for c in self.colors[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = '{}: {:.4f}'.format(self.labels[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

if __name__ == '__main__':
    yolo = Yolo()

    # Load and run the input image
    image = cv2.imread('baggage_claim.jpg')
    yolo.run(image)

    # Display the output image
    cv2.imshow('Image', image)
    cv2.waitKey(10000)
