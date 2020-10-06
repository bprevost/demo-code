from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense

def build(height, width, depth, classes):

    if K.image_data_format() != "channels_last":
        raise AssertionError("Channels need to be last")
    input_shape = (height, width, depth)

    # Initialize the model
    model = Sequential()

    # First set of CONV => RELU => POOL layers
    # CONV layer will learn 20 filters, each of size 5×5
    model.add(Conv2D(20, (5, 5), padding="same", input_shape=input_shape))
    # ReLU activation function
    model.add(Activation("relu"))
    # 2×2 pooling with 2×2 stride, decreasing input volume size by 75%
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    # Second set of CONV => RELU => POOL layers
    # CONV layer will learn 50 filters, each of size 5×5
    model.add(Conv2D(50, (5, 5), padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    # First (and only) set of FC => RELU layers
    # Flatten the input volume and apply a fully-connected layer with 500 nodes
    model.add(Flatten())
    model.add(Dense(500))
    model.add(Activation("relu"))

    # Softmax classifier
    model.add(Dense(classes))
    model.add(Activation("softmax"))

    # Return the constructed network architecture
    return model
