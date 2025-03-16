import tempfile

import numpy as np
import cv2
from io import BytesIO
from pydub import AudioSegment
import assemblyai as aai
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


def verify_video(file):
    """
    Verify the file, extract audio, and transcribe it.

    :param file: The uploaded file object.
    :return: The transcribed text.
    """
    # Allowed file extensions
    allowed_extensions = ['mp4', 'avi', 'mov', 'wav', 'mp3']

    # Check if the file extension is allowed
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        return {'error': f'Invalid file extension: {file_extension}'}

    try:
        # Read the file bytes
        file_bytes = file.read()

        # Create a file-like object in memory
        file_like = BytesIO(file_bytes)

        # Write the video bytes to a temporary file
        with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(file_bytes)

    except Exception as e:
        return {'error': f'Error during transcription: {str(e)}'}