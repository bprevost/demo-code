#!/usr/bin/env python3

import numpy as np
import cv2
from skimage.exposure import rescale_intensity

def convolve(image, K):
    (iH, iW) = image.shape[:2] # Image
    (kH, kW) = K.shape[:2] # Kernel

    # Pad the input image
    pad = (kW - 1) // 2
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REPLICATE)

    # Allocate the output image
    output = np.zeros((iH, iW), dtype="float")

    # Apply convolution
    for y in np.arange(pad, iH + pad):
        for x in np.arange(pad, iW + pad):
            # Extract the ROI of the image
            roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]
            # Perform the actual convolution
            k = (roi * K).sum()
            # Store the convolved value
            output[y - pad, x - pad] = k

    # Rescale the output image to the range [0, 255]
    output = rescale_intensity(output, in_range=(0, 255))
    output = (output * 255).astype("uint8")
    return output

IMAGEFILE = "images/beagle.png"

# Construct averaging kernels for smoothing an image
smallBlur = np.ones((7, 7), dtype="float") * (1.0 / (7 * 7))
largeBlur = np.ones((21, 21), dtype="float") * (1.0 / (21 * 21))

# Construct a sharpening filter
sharpen = np.array((
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]), dtype="int")

# Construct a Laplacian kernel for detecting edges
laplacian = np.array((
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0]), dtype="int")

# Construct the Sobel X-axis kernel
sobelX = np.array((
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]), dtype="int")

# Construct the Sobel Y-axis kernel
sobelY = np.array((
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]), dtype="int")

# Construct an emboss kernel
emboss = np.array((
    [-2, -1, 0],
    [-1, 1, 1],
    [0, 1, 2]), dtype="int")

# Construct the kernel bank
kernelBank = (
    ("small_blur", smallBlur),
    ("large_blur", largeBlur),
    ("sharpen", sharpen),
    ("laplacian", laplacian),
    ("sobel_x", sobelX),
    ("sobel_y", sobelY),
    ("emboss", emboss))

# Load the input image and convert it to grayscale
image = cv2.imread(IMAGEFILE)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Loop over the kernels
for (kernelName, K) in kernelBank:
    print("Applying {} kernel".format(kernelName))
    convolveOutput = convolve(gray, K)
    opencvOutput = cv2.filter2D(gray, -1, K)
    cv2.imshow("Original", gray)
    cv2.imshow("{} - convole".format(kernelName), convolveOutput)
    cv2.imshow("{} - opencv".format(kernelName), opencvOutput)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
