#!/usr/bin/env python3

from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.callbacks import ModelCheckpoint
from minivggnet import MiniVGGNet

# Load the CIFAR-10 dataset
((trainX, trainY), (testX, testY)) = cifar10.load_data()

# Scale data (image pixel intensities) to the range of [0, 1]
trainX = trainX.astype("float") / 255.0
testX = testX.astype("float") / 255.0

# Convert the labels from integers to one-hot vectors
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

# Initialize the optimizer and model
opt = SGD(lr=0.01, decay=0.01 / 40, momentum=0.9, nesterov=True)
model = MiniVGGNet.build(width=32, height=32, depth=3, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# Construct the callback to save only the best model to disk based on the validation loss

#filename = "weights-{epoch:03d}-{val_loss:.4f}.hdf5"
#checkpoint = ModelCheckpoint(filename, monitor="val_loss", mode="min", save_best_only=True, verbose=1)

filename = 'cifar10_best_weights.hdf5'
checkpoint = ModelCheckpoint(filename, monitor="val_loss", save_best_only=True, verbose=1)

callbacks = [checkpoint]

# Train the network
H = model.fit(trainX, trainY, validation_data=(testX, testY), batch_size=64, epochs=40, callbacks=callbacks, verbose=2)
