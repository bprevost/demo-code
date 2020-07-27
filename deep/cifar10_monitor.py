#!/usr/bin/env python3

import sys
sys.path.append("..")

import os
import matplotlib

from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.datasets import cifar10
from minivggnet import MiniVGGNet
from trainingmonitor import TrainingMonitor

# Load the CIFAR-10 dataset
((trainX, trainY), (testX, testY)) = cifar10.load_data()

# Scale data (image pixel intensities) to the range of [0, 1]
trainX = trainX.astype("float") / 255.0
testX = testX.astype("float") / 255.0

# Convert the labels from integers to one-hot vectors
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

# Initialize the label names for the CIFAR-10 dataset
labelNames = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

# Initialize the optimizer and model (but without any learning rate decay)
opt = SGD(lr=0.01, momentum=0.9, nesterov=True)
model = MiniVGGNet.build(width=32, height=32, depth=3, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# Construct the set of callbacks
figPath = "{}.png".format(os.getpid())
jsonPath = "{}.json".format(os.getpid())
callbacks = [TrainingMonitor(figPath, jsonPath=jsonPath)]

# train the network
model.fit(trainX, trainY, validation_data=(testX, testY), batch_size=64, epochs=100, callbacks=callbacks, verbose=1)
