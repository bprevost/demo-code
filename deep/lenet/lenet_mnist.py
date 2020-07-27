#!/usr/bin/env python3

import sys
sys.path.append("..")

import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.datasets import mnist
from tensorflow.keras import backend as K
from lenet import LeNet

# Load the MNIST dataset
((trainData, trainLabels), (testData, testLabels)) = mnist.load_data()

if K.image_data_format() == "channels_first":
    # Use design matrix shape: num_samples x depth x rows x columns
    trainData = trainData.reshape((trainData.shape[0], 1, 28, 28))
    testData = testData.reshape((testData.shape[0], 1, 28, 28))
else:
    # Use design matrix shape: num_samples x rows x columns x depth
    trainData = trainData.reshape((trainData.shape[0], 28, 28, 1))
    testData = testData.reshape((testData.shape[0], 28, 28, 1))

# Scale data (image pixel intensities) to the range of [0, 1]
trainData = trainData.astype("float32") / 255.0
testData = testData.astype("float32") / 255.0

# Convert the labels from integers to one-hot vectors
lb = LabelBinarizer()
trainLabels = lb.fit_transform(trainLabels)
testLabels = lb.transform(testLabels)

# Initialize the optimizer and model
opt = SGD(lr=0.01) # Learning rate
model = LeNet.build(width=28, height=28, depth=1, classes=10) # Instantiate LeNet
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# Train the network
H = model.fit(trainData, trainLabels, validation_data=(testData, testLabels),
              batch_size=128, epochs=20, verbose=1)

# Evalute the performance of the network
predictions = model.predict(testData, batch_size=128)
print(classification_report(
    testLabels.argmax(axis=1),
    predictions.argmax(axis=1),
    target_names=[str(x) for x in lb.classes_]))

# Plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, 20), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, 20), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, 20), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, 20), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.show()
