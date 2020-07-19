#!/usr/bin/env python3

import sys
sys.path.append("..")

import os
import numpy as np
import cv2

from tensorflow.keras.models import load_model
from imutils import paths
from simpledatasetloader import SimpleDatasetLoader
from simplepreprocessor import SimplePreprocessor
from imagetoarraypreprocessor import ImageToArrayPreprocessor

DATASET = os.path.join(os.getenv('HOME'), 'books/DL4CV/SB_Code/datasets/animals')

# Initialize the class labels
classLabels = ["cat", "dog", "panda"]

# Randomly sample images from the dataset
image_paths = np.array(list(paths.list_images(DATASET)))
idxs = np.random.randint(0, len(image_paths), size=(10,))
image_paths = image_paths[idxs]

# Initialize the image preprocessors
sp = SimplePreprocessor(32, 32)
iap = ImageToArrayPreprocessor()

# Load the dataset from disk
sdl = SimpleDatasetLoader(preprocessors=[sp, iap])
(data, labels) = sdl.load(image_paths, verbose=500)

# Scale the raw pixel intensities to the range [0, 1]
data = data.astype("float") / 255.0

# Load the pre-trained network
model = load_model("shallownet_weights.hdf5")

# Make predictions on the images
preds = model.predict(data, batch_size=32).argmax(axis=1)

# Loop over the sample images
for (i, image_path) in enumerate(image_paths):
    image = cv2.imread(image_path)
    cv2.putText(image, "Label: {}".format(classLabels[preds[i]]),
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
