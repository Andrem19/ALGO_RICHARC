import tensorflow as tf
import numpy as np
import helpers.vizualizer as viz
from keras.preprocessing import image
import shared_vars as sv

def predict_image_class(data: np.ndarray) -> int:
    # Загрузка модели
    viz.save_candlesticks_pic(data, '_temp_pic/sample.png')
    
    # Загрузка и предобработка изображения
    img = image.load_img('_temp_pic/sample.png', target_size=(340, 340))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Нормализация изображения

    # Предсказание класса
    predictions = sv.model_1.predict(img_array, verbose=0)
    predicted_class = np.argmax(predictions, axis=1)[0]
    # if predictions[0][-1]> predictions[0][0]:
    print(predictions)
    
    if predicted_class == 0:
        return 3
    elif predicted_class == 1:
        return 2
    
    return predicted_class