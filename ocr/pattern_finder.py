import numpy as np
from skimage import measure


class PatternFinder:
    def __init__(self):
        pass

    def calc_correlation(self, image, pattern):
        pattern = np.rot90(pattern, 2)
        pattern_fft = np.fft.fft2(pattern, image.shape)
        image_fft = np.fft.fft2(image)
        return np.real(np.fft.ifft2(np.multiply(pattern_fft, image_fft)))
    
    def find_pattern(self, image, pattern, threshold=0.6):
        correlation = self.calc_correlation(image, pattern)
        correlation = np.where(correlation > np.max(correlation)* threshold, correlation, 0)
        return correlation
