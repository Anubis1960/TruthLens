import cv2
import numpy as np
from cv2.typing import MatLike
import tensorflow as tf
import os
from dotenv import load_dotenv

load_dotenv()

m_path = os.getenv('IMG_MODEL')

def load_modell():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the model file
    model_path = os.path.join(script_dir, "ai_gen_detector.keras")
    model = tf.keras.models.load_model(model_path)
    return model

def new_load_modell():
    model = tf.keras.models.load_model(m_path)
    return model

def prepare_image(img: MatLike) -> MatLike:
    image = cv2.resize(img, (32, 32))
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image

def new_prep_img(img: MatLike) -> MatLike:
    image = cv2.resize(img, (64, 64))
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image

def predict_image(image: MatLike) -> int:
    print("Predicting")
    model = new_load_modell()
    # prepared_image = prepare_image(image)
    prepared_image = new_prep_img(image)
    prediction = model.predict(prepared_image)
    print("Prediction:", prediction)
    return prediction

if __name__ == "__main__":
    img = cv2.imread('/home/anubis/Downloads/archive/test/REAL/0000.jpg')
    print(predict_image(img))