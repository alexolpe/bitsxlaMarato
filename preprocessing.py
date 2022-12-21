import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from PIL import Image, ImageFilter


def preprocessing (img):

    kernel = np.ones((7,7),np.uint8)

    dilatacion = cv.dilate(img,kernel,iterations = 1)

    erosion = cv.erode(dilatacion,kernel,iterations = 1)

    gaussian_filter = cv.GaussianBlur(erosion, (5,5), 0)

    return gaussian_filter



