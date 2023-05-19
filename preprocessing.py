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
from skimage.filters.thresholding import threshold_minimum


def calculateRotationValue(img, angle):
    data = transform.rotate(img, angle, resize=True)
    rotatedHistogram = np.sum(data, axis=1)
    value = np.sum((rotatedHistogram[1:] - rotatedHistogram[:-1]) ** 2)
    return rotatedHistogram, value


def unrotate(img):
    binImg = np.uint8(img) * 255

    results = []
    angleDelta = 1
    limit = 45
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
    url = "http://sipi.usc.edu/database/download.php?vol=misc&img=4.2.07"
    img = skimage.io.imread(url)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # cv2.imshow("Image", img)
    # cv2.waitKey()

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray image", gray_img)
    # cv2.waitKey()

    img = cv2.imread("/Users/davidcemeljic/Downloads/skeletonizeTest.png", cv2.IMREAD_GRAYSCALE)

    thresh_min = threshold_minimum(img)
    print(thresh_min)
    img = img > thresh_min
    img = np.uint8(img) * 255

    img = skeletonize(img, 5, 15)
    cv2.imshow("Skeletonization", img)
    cv2.waitKey()


if __name__ == "__main__":
    preprocessing()
