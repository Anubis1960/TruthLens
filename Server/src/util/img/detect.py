import cv2
import numpy as np
import tensorflow as tf
from cv2.typing import MatLike

def load_model() -> tf.keras.Model:
    return tf.keras.models.load_model("ai_gen_detector.keras")

def prepare_image(img: MatLike) -> MatLike:
    image = cv2.resize(img, (32, 32))
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image

def predict_image(image: MatLike) -> int:
    model = load_model()
    prepared_image = prepare_image(image)
    return model.predict(prepared_image)

