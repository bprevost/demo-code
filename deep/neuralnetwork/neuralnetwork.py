import numpy as np

class NeuralNetwork:
    def __init__(self, layers, alpha=0.1):
        self.W = [] # List of weights matrices
        self.layers = layers # Network architecture, eg [2,2,1]
        self.alpha = alpha # Learning rate

        # Initialize the list of weights matrices
        # Loop from the first layer but not the last two layers
        # For each layer, add an extra node for the bias
        for i in np.arange(0, len(layers) - 2):
            w = np.random.randn(layers[i] + 1, layers[i + 1] + 1)
            # Scale w to normalize the variance of each neuron’s output
            self.W.append(w / np.sqrt(layers[i]))
        # For the last two layers, the inputs need a bias term but the output does not
        w = np.random.randn(layers[-2] + 1, layers[-1])
        # Scale w to normalize the variance of each neuron’s output
        self.W.append(w / np.sqrt(layers[-2]))

    def __repr__(self):
        # Return a string that represents the network architecture
        return "NeuralNetwork: {}".format("-".join(str(l) for l in self.layers))

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1.0 / (1 + np.exp(-x))

    def sigmoid_deriv(self, x):
        # Derivative of the sigmoid function
        # Assume that x has already been passed through the sigmoid function
        return x * (1 - x)

    def fit(self, X, y, epochs=1000, displayUpdate=100):
        # Insert a column of 1's as the last entry in the feature matrix (bias)
        X = np.c_[X, np.ones((X.shape[0]))]

        # Loop over the epochs
        for epoch in np.arange(0, epochs):
            # Loop over the data points and train the network
            for (x, target) in zip(X, y):
                self.fit_partial(x, target)

            # Display a training update occasionally
            if epoch == 0 or (epoch + 1) % displayUpdate == 0:
                loss = self.calculate_loss(X, y)
                print("epoch={}, loss={:.7f}".format(epoch + 1, loss))

    def fit_partial(self, x, y):
        # Construct the list of output activations for each layer
        # The first activation is just the input feature vector itself
        A = [np.atleast_2d(x)]

        # FEEDFORWARD
        for layer in np.arange(0, len(self.W)):
            # Compute the net input to the current layer
            net = A[layer].dot(self.W[layer]) # The 'net input'
            out = self.sigmoid(net) # The 'net output'
            A.append(out) # Add the net output to the list of activations

        # BACKPROPAGATION
        # Compute the difference between the predicted label and the ground-truth label
        error = A[-1] - y
        # Apply the chain rule to build the list of deltas
        D = [error * self.sigmoid_deriv(A[-1])]
        for layer in np.arange(len(A) - 2, 0, -1):
            delta = D[-1].dot(self.W[layer].T)
            delta = delta * self.sigmoid_deriv(A[layer])
            D.append(delta)
        # Reverse the deltas since we looped in reverse
        D = D[::-1]

        # WEIGHT UPDATE PHASE
        for layer in np.arange(0, len(self.W)):
            # This is where the actual "learning" takes place
            self.W[layer] += -self.alpha * A[layer].T.dot(D[layer])

    def predict(self, X, addBias=True):
        # Initialize the output prediction as the input features
        p = np.atleast_2d(X)

        # Check to see if the bias column should be added
        if addBias:
            # Insert a column of 1's as the last entry in the feature matrix (bias)
            p = np.c_[p, np.ones((p.shape[0]))]

        # Loop over the network layers to compute the output prediction
        for layer in np.arange(0, len(self.W)):
            p = self.sigmoid(np.dot(p, self.W[layer]))

        # Return the predicted value
        return p

    def calculate_loss(self, X, targets):
        # Make predictions for the input data points then compute the loss
        targets = np.atleast_2d(targets)
        predictions = self.predict(X, addBias=False)
        loss = 0.5 * np.sum((predictions - targets) ** 2)
        return loss
