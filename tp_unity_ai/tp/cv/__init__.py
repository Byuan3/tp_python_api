from .cam_display import *


def downscale(image, factor):
    imageResize = cv2.resize(image, (image.shape[1] // factor, image.shape[0] // factor))
    return imageResize
