import os

import cv2
import numpy as np

from src.util.scrape import get_total_frames, analyze_frames, transcript
from ..util.img.img_detect import predict_image
from ..util.news.news_detect import predict_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "..", "temp")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


def verify_img_file(file) -> dict:
    """
    Verify if the file extension is allowed.

    :param file:
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

        # Write the video bytes to a temporary file

        # Random generated file name
        file_name = os.urandom(8).hex()

        # Saving path
        out_path = os.path.join(TEMP_DIR, file_name)

        with open(out_path + '.mp4', 'wb') as f:
            f.write(file_bytes)
        total_frames = get_total_frames(out_path + '.mp4')
        frames = np.random.randint(0, total_frames, 5)
        print(frames)

        pred = analyze_frames(out_path + '.mp4', frames)
        print(pred)

        ts = transcript(out_path + '.mp4')

        title = ""

        verdict = predict_text(title, ts)

        if pred[0] > 0.5:
            pred = 'AI Generated'
        else:
            pred = 'Real'

        return {'video': pred, 'audio': verdict}

    except Exception as e:
        return {'error': f'Error during transcription: {str(e)}'}
