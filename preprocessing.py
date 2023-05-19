import cv2
import skimage.io
from scipy.ndimage import *
from scipy.fft import *
from scipy.signal import *
from scipy.stats import *
from skimage.filters import *
from skimage.feature import *
import numpy as np
from skimage.filters.thresholding import threshold_minimum


def preprocessing():
    url = "http://sipi.usc.edu/database/download.php?vol=misc&img=4.2.07"
    img = skimage.io.imread(url)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # cv2.imshow("Image", img)
    # cv2.waitKey()

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray image", gray_img)
    # cv2.waitKey()

    thresh_min = threshold_minimum(gray_img)
    print(thresh_min)
    binary_min = gray_img > thresh_min
    binary_min = np.uint8(binary_min) * 255

    cv2.imshow("Thresholding", binary_min)
    cv2.waitKey()


if __name__ == "__main__":
    preprocessing()
