import cv2
import numpy as np
import io
from ..util.img.img_detect import predict_image


def verify_img_file(file) -> dict:
    """
    Verify if the file extension is allowed.

    :param file:
    :param file_name: The file name.
    :return: True if the file extension is allowed, False otherwise.
    """
    allowed_extensions = ['png', 'jpg', 'jpeg']
    print(file.filename)
    if file.filename.split('.')[-1] in allowed_extensions:
        file_bytes = file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is not None:
            prediction = predict_image(image)
            print(prediction)
            if prediction > 0.5:
                prediction = 'AI Generated'
            else:
                prediction = 'Real'
            return {'prediction': prediction}
        else:
            return {'error': f'Invalid file: {file.filename}'}
    else:
        return {'error': f'Invalid file {file.filename}'}