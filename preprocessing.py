import cv2
import skimage.io
from skimage import transform
import numpy as np


def calculateRotationValue(img, angle):
    data = transform.rotate(img, angle, resize=True)
    rotatedHistogram = np.sum(data, axis=1)
    value = np.sum((rotatedHistogram[1:] - rotatedHistogram[:-1]) ** 2)
    return rotatedHistogram, value


def unrotate(img, limit):
    binImg = np.uint8(img) * 255

    results = []
    angleDelta = 1
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


def preview(img_name, block_size, erode_size, erode_iterations):
    img = skimage.io.imread(img_name)
    max_dim = np.argmax(img.shape)
    dim = [720, 720]
    dim[1-max_dim] = int((img.shape[1-max_dim] / img.shape[max_dim]) * 720)
    img = cv2.resize(img, (dim[1], dim[0]))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, block_size, 2)

    display = skeletonize(binary, erode_size, erode_iterations)

    return display

def preprocess(img_name, block_size, angle, erode_size, erode_iterations):
    img = skimage.io.imread(img_name)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV,block_size ,2)

    binary = unrotate(binary, angle)
    erosion = skeletonize(binary, erode_size, erode_iterations)

    display = cv2.resize(erosion, (img.shape[1]//10, img.shape[0]//10))
    return erosion, display


if __name__ == "__main__":
    url = "https://api.time.com/wp-content/uploads/2015/10/california.jpg"
    pr = preview(url, 1001, 3, 2)
    cv2.imshow("display", pr)
    cv2.waitKey()
    preprocess(url, 1001, 5, 3, 2)

