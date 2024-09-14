import tensorflow as tf
import numpy as np
import helpers.vizualizer as viz
from keras.preprocessing import image
import shared_vars as sv

def predict_image_class(data: np.ndarray, sample_2: np.ndarray, sample_3: np.ndarray) -> int:
    # Загрузка модели
    viz.save_candlesticks_pic_2(data, sample_2, '_temp_pic/sample.png')
    
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

    zero = predictions[0][0]
    one = predictions[0][1]

    # if zero > 0.70:
    #     return False
    # else:
    #     return True
    
    if predicted_class == 0:
        return False
    elif predicted_class == 1:
        return True
    
    return predicted_class