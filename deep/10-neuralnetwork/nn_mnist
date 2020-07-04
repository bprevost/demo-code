#!/usr/bin/env python3

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import datasets
from neuralnetwork import NeuralNetwork

print("Load MNIST (sample) dataset...")
# Load the MNIST dataset and scale the pixel intensity values to the range [0, 1]
# Each image is represented by an 8 x 8 = 64-dim feature vector
digits = datasets.load_digits()
data = digits.data.astype("float")
data = (data - data.min()) / (data.max() - data.min())
print("Samples: {}, dim: {}".format(data.shape[0], data.shape[1]))

# Training and testing splits
(trainX, testX, trainY, testY) = train_test_split(data, digits.target, test_size=0.25)

# Convert the labels from integers to vectors
trainY = LabelBinarizer().fit_transform(trainY)
testY = LabelBinarizer().fit_transform(testY)

print("Train network...")
nn = NeuralNetwork([trainX.shape[1], 32, 16, 10])
print("{}".format(nn))
nn.fit(trainX, trainY, epochs=1000)

print("Evaluate network...")
predictions = nn.predict(testX)
predictions = predictions.argmax(axis=1)
print(classification_report(testY.argmax(axis=1), predictions))
