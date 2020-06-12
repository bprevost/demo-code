#!/usr/bin/env python3

import os

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from simplepreprocessor import SimplePreprocessor
from simpledatasetloader import SimpleDatasetLoader
from imutils import paths

DATASET = os.path.join(os.getenv('HOME'), 'books/DL4CV/SB_Code/datasets/animals')
NEIGHBORS = 1 # Number of nearest neighbors (k) for classification
JOBS = 1 # Number of jobs for k-NN distance (-1 uses all available cores)

# Load images
imagePaths = list(paths.list_images(DATASET))

# Initialize the image preprocessor
sp = SimplePreprocessor(32, 32)
sdl = SimpleDatasetLoader(preprocessors=[sp])

# Load the dataset from disk
(data, labels) = sdl.load(imagePaths, verbose=500)

# Reshape the data matrix
data = data.reshape((data.shape[0], 3072))

# Encode the labels as integers
le = LabelEncoder()
labels = le.fit_transform(labels)

# Partition the data into training and testing splits (75% for training and 25% for testing)
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)

# Train and evaluate the k-NN classifier on the raw pixel intensities
model = KNeighborsClassifier(n_neighbors=NEIGHBORS, n_jobs=JOBS)
model.fit(trainX, trainY)
print(classification_report(testY, model.predict(testX), target_names=le.classes_))
