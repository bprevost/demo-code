from tensorflow.keras.preprocessing.image import img_to_array

class ImageToArrayPreprocessor:
    def __init__(self, dataFormat=None):
        self.dataFormat = dataFormat # Image data format

    def preprocess(self, image):
        # Rearrange the dimensions of the image using Keras
        return img_to_array(image, data_format=self.dataFormat)
