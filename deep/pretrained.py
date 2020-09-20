#!/usr/bin/env python3

import os
import random
import glob
import numpy as np
import cv2

from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array

modelname = random.choice(['vgg16', 'vgg19', 'inception', 'xception', 'resnet'])
print('modelname', modelname)

if modelname == 'vgg16':
    from tensorflow.keras.applications import VGG16 as Network
    from tensorflow.keras.applications.imagenet_utils import preprocess_input as preprocess
    inputShape = (224, 224)
elif modelname == 'vgg19':
    from tensorflow.keras.applications import VGG19 as Network
    from tensorflow.keras.applications.imagenet_utils import preprocess_input as preprocess
    inputShape = (224, 224)
elif modelname == 'inception':
    from tensorflow.keras.applications import InceptionV3 as Network
    from tensorflow.keras.applications.inception_v3 import preprocess_input as preprocess
    inputShape = (299, 299)
elif modelname == 'xception':
    from tensorflow.keras.applications import Xception as Network
    from tensorflow.keras.applications.inception_v3 import preprocess_input as preprocess
    inputShape = (299, 299)
elif modelname == 'resnet':
    from tensorflow.keras.applications import ResNet50 as Network
    from tensorflow.keras.applications.imagenet_utils import preprocess_input as preprocess
    inputShape = (224, 224)
else:
    raise AssertionError('Bad model name')

filename = random.sample(glob.glob('images/*.jpg'), 1)[0]
print('filename', filename)

# Load and preprocess the image
image = load_img(filename, target_size=inputShape)
image = img_to_array(image)
image = np.expand_dims(image, axis=0)
image = preprocess(image)

# Classify the image
model = Network(weights='imagenet')
preds = model.predict(image)
P = imagenet_utils.decode_predictions(preds)

# Display the rank-5 predictions and probabilities
for (i, (imagenetID, label, prob)) in enumerate(P[0]):
    print('{}. {}: {:.2f}%'.format(i + 1, label, prob * 100))

# Display the image and the top prediction
orig = cv2.imread(filename)
(imagenetID, label, prob) = P[0][0]
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(orig, filename, (10, 30), font, 0.8, (0, 255, 0), 2)
cv2.putText(orig, modelname, (10, 60), font, 0.8, (0, 255, 0), 2)
cv2.putText(orig, label, (10, 90), font, 0.8, (0, 255, 0), 2)
cv2.imshow('Image', orig)
cv2.waitKey(5000)
