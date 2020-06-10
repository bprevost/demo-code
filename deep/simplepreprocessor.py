import cv2

class SimplePreprocessor:
    def __init__(self, width, height, inter=cv2.INTER_AREA):
        # Target width, height, and interpolation method used when resizing images
        self.width = width
        self.height = height
        self.inter = inter

    def preprocess(self, image):
        # Resize the image to a fixed size but ignore the aspect ratio
        return cv2.resize(image, (self.width, self.height), interpolation=self.inter)
