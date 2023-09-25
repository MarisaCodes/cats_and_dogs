import keras
import numpy as np
import cv2
from pprint import pprint

LABELS = ["Dog", "Cat"]
IMG_SIZE = 100
model = keras.models.load_model("cats_and_dogs.keras")


def process_img(data):
    '''Take data buffer and return image array using cv2'''
    try:
        img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, dsize=(IMG_SIZE, IMG_SIZE))
    except Exception as e:
        print(f"Exception: {e}")
        pass
    img = np.array(img).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    img = keras.utils.normalize(img, axis=1)
    return img


def cat_or_dog(img) -> str:
    '''Take image array (img=img_arr) and return string cat or dog as prediction'''
    confidence = model.predict(img)[0][0]
    pred = round(confidence)
    return (confidence, LABELS[pred])
