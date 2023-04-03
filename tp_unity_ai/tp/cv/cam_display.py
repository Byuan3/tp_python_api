import requests
import numpy as np
import cv2


def cam_display(cameraID=0):
    while True:
        # Make a GET request to retrieve the image data
        response = requests.get('http://localhost:7000/display')

        # Convert the raw image data to a NumPy array
        if response.status_code == 200:
            image_data = np.frombuffer(response.content, np.uint8)
            print(response)

            # Decode the NumPy array into an OpenCV image
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            # Display the image using OpenCV
            cv2.imshow(f'Unity Camera {cameraID}', image)
            if cv2.waitKey(1) == 27:
                break
        else:
            print("Bad request")

