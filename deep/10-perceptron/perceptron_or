#!/usr/bin/env python3

import numpy as np
from perceptron import Perceptron

# Construct the OR dataset
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [1]])

print("Training perceptron...")
p = Perceptron(X.shape[1], alpha=0.1)
p.fit(X, y, epochs=20)

print("Testing perceptron...")
for (x, target) in zip(X, y):
    # Make a prediction on the data point and display the result
    pred = p.predict(x)
    print("data={}, ground-truth={}, pred={}".format(x, target[0], pred))
