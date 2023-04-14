from tp_unity_ai.tp.cv.cam_display import cam_display
import cv2


def downscale(image, factor):
    imageResize = cv2.resize(image, (image.shape[1] // factor, image.shape[0] // factor))
    return imageResize
