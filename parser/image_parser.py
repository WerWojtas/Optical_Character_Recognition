from PIL import Image, ImageOps
import cv2
import numpy as np
import os
from scipy.ndimage import convolve
from math import sqrt
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon


class ImageParser():
    def __init__(self):
        pass


    def rotation(self, image_path):
        image = Image.open(image_path)
        image = np.array(image)
        image_bef = np.copy(image)
        image = cv2.bitwise_not(image)
        points_cords = np.array(list(map(tuple, np.argwhere(image >0))))
        rect = cv2.minAreaRect(points_cords)
        angle = rect[2]
        if angle < -45:
            angle = 90 + angle
        angle = -angle
        image = Image.fromarray(image_bef)
        image = image.rotate(angle, expand=1, fillcolor='white',resample=Image.BILINEAR)
        image = ImageOps.invert(image)
        image = image.crop(image.getbbox())
        image = ImageOps.invert(image)
        image = ImageOps.expand(image, border=10, fill='white')
        return image
    
    def remove_noise(self,image_path, file_path = True):
        if file_path:
            image = Image.open(image_path)
        else:
            image = image_path
        image = np.array(image)
        return Image.fromarray(cv2.fastNlMeansDenoising(image, None, 40, 7, 21))