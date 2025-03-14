import cv2
import numpy as np

def dct_2d(block):
    """
    Compute the 2D Discrete Cosine Transform (DCT) of a block.
    The block must be a 2D numpy array. cv2.dct expects input as float32.
    """
    block = np.float32(block)
    return cv2.dct(block)