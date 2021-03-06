#!/usr/bin/env python3

import numpy as np
import cv2

# Initialize the class labels
labels = ["dog", "cat", "panda"]

# Set the seed of the pseudorandom number generator
np.random.seed(1) # Rigged example...

# Randomly initialize the weight matrix and bias vector
W = np.random.randn(3, 3072)
b = np.random.randn(3)

# Load image, resize, and flatten into feature vector
filename = 'images/beagle.png'
orig = cv2.imread(filename)
image = cv2.resize(orig, (32, 32)).flatten()

# Compute the output class label scores by applying the scoring function
scores = W.dot(image) + b

# Loop over the scores & labels and display them
for (label, score) in zip(labels, scores):
    print("{}: {:.2f}".format(label, score))

# Draw the label with the highest score on the image as the prediction
cv2.putText(orig, "Label: {}".format(labels[np.argmax(scores)]),
    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the input image
cv2.imshow("Image", orig)
cv2.waitKey(5000)
