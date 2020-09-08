#!/usr/bin/env python3

from lenet import LeNet
from tensorflow.keras.utils import plot_model

# Initialize LeNet
model = LeNet.build(28, 28, 1, 10)

# Write the network architecture visualization grpah to disk
plot_model(model, to_file="lenet.png", show_shapes=True)
