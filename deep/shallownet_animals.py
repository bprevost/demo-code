#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.optimizers import SGD

from imutils import paths
from simplepreprocessor import SimplePreprocessor
from simpledatasetloader import SimpleDatasetLoader
from imagetoarraypreprocessor import ImageToArrayPreprocessor
from shallownet import ShallowNet

DATASET = os.path.join(os.getenv('HOME'), 'books/DL4CV/SB_Code/datasets/animals')

print("Loading images...")
image_paths = list(paths.list_images(DATASET))
print(len(image_paths), "images found.")

# Initialize the image preprocessors
sp = SimplePreprocessor(32, 32)
iap = ImageToArrayPreprocessor()

# Load the dataset from disk
sdl = SimpleDatasetLoader(preprocessors=[sp, iap])
(data, labels) = sdl.load(image_paths, verbose=500)

# Scale the raw pixel intensities to the range [0, 1]
data = data.astype("float") / 255.0

# Partition the data into training (75%) and testing (25%) splits
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)

# Convert the labels from integers to vectors (one-hot encoding)
trainY = LabelBinarizer().fit_transform(trainY)
testY = LabelBinarizer().fit_transform(testY)

# Initialize the SGD optimizer using a learning rate of 0.005
opt = SGD(lr=0.005)

# Initialize the model
model = ShallowNet.build(width=32, height=32, depth=3, classes=3)

# Compile the model using cross-entropy as the loss function and SGD as the optimizer
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# Train the network
H = model.fit(trainX, trainY, validation_data=(testX, testY), batch_size=32, epochs=100, verbose=1)

# Evalute the performance of the network
predictions = model.predict(testX, batch_size=32)
print(classification_report(
    testY.argmax(axis=1),
    predictions.argmax(axis=1),
    target_names=["cat", "dog", "panda"]))

# Plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, 100), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, 100), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, 100), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, 100), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.show()
