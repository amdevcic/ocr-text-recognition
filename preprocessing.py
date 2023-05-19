import cv2
import skimage.io
from scipy.ndimage import *
from skimage import transform
from scipy.fft import *
from scipy.signal import *
from scipy.stats import *
from skimage.filters import *
from skimage.feature import *
import numpy as np


def calculateRotationValue(img, angle):
    data = transform.rotate(img, angle, resize=True)
    rotatedHistogram = np.sum(data, axis=1)
    value = np.sum((rotatedHistogram[1:] - rotatedHistogram[:-1]) ** 2)
    return rotatedHistogram, value


def unrotate(img):
    binImg = np.uint8(img) * 255

    results = []
    angleDelta = 1
    limit = 20
    angles = np.arange(-limit, limit + angleDelta, angleDelta)
    for angle in angles:
        hist, value = calculateRotationValue(binImg, angle)
        results.append([angle, value])

    maxValue = 0
    actualAngle = 0
    for result in results:
        if result[1] > maxValue:
            maxValue = result[1]
            actualAngle = result[0]

    return transform.rotate(img, actualAngle, resize=True)


def skeletonize(img, size=5, iterations=1):
    kernel = np.ones((size, size), np.uint8)
    erodedImage = cv2.erode(img, kernel, iterations=iterations)
    return erodedImage


def preprocessing():

    img = cv2.imread("sample/image1.jpg")

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV,401 ,2)

    binary = unrotate(binary)

    erosion = skeletonize(binary, 3, 2)


    img = cv2.resize(erosion, (img.shape[1]//10, img.shape[0]//10))
    cv2.imshow("Thresholding", img)
    cv2.waitKey()


if __name__ == "__main__":
    preprocessing()
