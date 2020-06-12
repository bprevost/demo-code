import numpy as np

class Perceptron:
    def __init__(self, N, alpha=0.1):
        # Initialize the weight matrix with N + 1 entries
        # One for each of the N inputs in the feature vector plus one for the bias
        self.W = np.random.randn(N + 1) / np.sqrt(N)
        # Store the learning rate
        self.alpha = alpha

    def step(self, x):
        # Apply the step function
        return 1 if x > 0 else 0

    def fit(self, X, y, epochs=10):
        # Insert a column of 1's as the last entry in the feature matrix (bias)
        X = np.c_[X, np.ones((X.shape[0]))]

        # Loop over the epochs
        for epoch in np.arange(0, epochs):
            # Loop over the data points
            for (x, target) in zip(X, y):
                # Take the dot product between the input features and the weight matrix
                # Pass this value through the step function to obtain the prediction
                p = self.step(np.dot(x, self.W))
                # Update the weights if the prediction does not match the target
                if p != target:
                    error = p - target
                    self.W += -self.alpha * error * x

    def predict(self, X, addBias=True):
        # Ensure input is a matrix
        X = np.atleast_2d(X)

        # Check to see if the bias column should be added
        if addBias:
            # Insert a column of 1's as the last entry in the feature matrix (bias)
            X = np.c_[X, np.ones((X.shape[0]))]

        # Take the dot product between the input features and the weight matrix
        # Pass this value through the step function
        return self.step(np.dot(X, self.W))
