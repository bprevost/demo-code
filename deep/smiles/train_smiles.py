#!/usr/bin/env python3

import sys
sys.path.insert(0, '../lenet')

import os
import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt

from imutils import paths
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from lenet import LeNet

folder = '/home/bprevost/brad2/book/datasets/SMILEsmileD'

data = []
labels = []
for image_path in sorted(list(paths.list_images(folder))):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = imutils.resize(image, width=28)
    image = img_to_array(image)
    data.append(image)
    label = image_path.split(os.path.sep)[-3]
    label = "smiling" if label == "positives" else "not_smiling"
    labels.append(label)

data = np.array(data, dtype="float") / 255.0 # Scale to [0, 1]
labels = np.array(labels)

# Apply one-hot encoding to the labels
le = LabelEncoder().fit(labels)
labels = to_categorical(le.transform(labels), 2)

# Account for class imbalance in the labeled data
class_totals = labels.sum(axis=0)
class_weight = class_totals.max() / class_totals

# Split the data into training and testing sets
(trainX, testX, trainY, testY) = train_test_split(data,
    labels, test_size=0.20, stratify=labels, random_state=42)

# Initialize the model
model = LeNet.build(width=28, height=28, depth=1, classes=2)
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the network
H = model.fit(trainX, trainY, validation_data=(testX, testY),
    class_weight=class_weight, batch_size=64, epochs=15, verbose=1)

# Save the model to disk
model.save('lenet.hdf5')

# Evaluate the network
predictions = model.predict(testX, batch_size=64)
print(classification_report(testY.argmax(axis=1),
    predictions.argmax(axis=1), target_names=le.classes_))

# Plot the loss and accuracy
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, 15), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, 15), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, 15), H.history["accuracy"], label="acc")
plt.plot(np.arange(0, 15), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.show()

