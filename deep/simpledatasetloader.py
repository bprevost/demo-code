import numpy as np
import cv2
import os

class SimpleDatasetLoader:
    def __init__(self, preprocessors=None):
        # Store the image preprocessors
        self.preprocessors = preprocessors

        # If the preprocessors are None then initialize them as an empty list
        if self.preprocessors is None:
            self.preprocessors = []

    def load(self, imagePaths, verbose=-1):
        # Initialize the list of features and labels
        data = []
        labels = []

        # Loop over the input images
        for (i, imagePath) in enumerate(imagePaths):
            # Load the image and extract the class label
            # Assume that the path has the following format:
            # /path/to/dataset/{class}/{image}.jpg
            image = cv2.imread(imagePath)
            label = imagePath.split(os.path.sep)[-2]

            # Check to see that the preprocessors are not None
            if self.preprocessors is not None:
                # Loop over the preprocessors and apply each to the image
                for p in self.preprocessors:
                    image = p.preprocess(image)

            # Treat the processed image as a feature vector
            # Update the data list followed by the labels
            data.append(image)
            labels.append(label)

            # Show an update every few images
            if verbose > 0 and i > 0 and (i + 1) % verbose == 0:
                print("Processed {}/{}".format(i + 1, len(imagePaths)))

        # Return a tuple of the data and labels
        return (np.array(data), np.array(labels))
