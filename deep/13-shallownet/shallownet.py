from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras import backend as K

class ShallowNet:
    @staticmethod
    def build(width, height, depth, classes):

        # Initialize the model
        model = Sequential()

        # Channel order
        inputShape = (height, width, depth) # Channels last
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)

        # CONV layer
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=inputShape))

        # RELU layer
        model.add(Activation("relu"))

        # Softmax classifier
        model.add(Flatten())
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        # Return the constructed network architecture
        return model
