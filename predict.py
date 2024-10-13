import tensorflow as tf
import numpy as np
import helpers.vizualizer as viz
from keras.preprocessing import image
from sklearn.preprocessing import StandardScaler
import shared_vars as sv


def predict_image_class(model, variant: int, data: np.ndarray, sample_2: np.ndarray, sample_3: np.ndarray = None, var: int = 2) -> int:
    # Загрузка модели
    path = f'_temp_pic/{sv.image_ident}{variant}_sample.png'
    if var == 1:
        viz.save_candlesticks_pic_1(data, path)
    elif var == 2:
        viz.save_candlesticks_pic_2(data, sample_2, path)
    elif var == 3:
        viz.save_candlesticks_pic_3(sample_2, data, sample_3, path)
    elif var == 4:
        viz.save_candlesticks_pic_2BB(data, sample_2, path)
    
    # Загрузка и предобработка изображения
    img = image.load_img(path, target_size=(340, 340))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Нормализация изображения

    # Предсказание класса
    predictions = model.predict(img_array, verbose=0)
    predicted_class = np.argmax(predictions, axis=1)[0]
    # if predictions[0][-1]> predictions[0][0]:
    print(predictions)
    return predictions[0]
    if variant == 1:
        if predictions[0][1] > 0.85:
            return True
        else:
            return False
    elif variant == 2:
        if predicted_class == 0:
            return False
        elif predicted_class == 1:
            return True
    elif variant == 3:
        if predictions[0][0] > 0.70:
            return False
        else:
            return True
    elif variant == 4:
        return predictions[0][1], predicted_class
        
    else:
        return predicted_class


# def make_predictions(data_list):
#     data_list = np.array(data_list).reshape((1, len(data_list), 1))
#     prediction = sv.model_1.predict(data_list, verbose=1)
#     return prediction[0][0]


import numpy as np
from keras.models import Model

def make_prediction(model: Model, input_data: list, scaler: StandardScaler, variant: int, shape_1: int, shape_2: int) -> float:
    # Проверяем, что входные данные имеют правильный размер
    
    # input_array = np.array(input_data).reshape(-1, 4)
    scaled_input = scaler.transform([input_data])#np.array(input_data)#
    # Преобразуем входные данные в нужную форму (50, 4)
    scaled_input = scaled_input.reshape(1, shape_1, shape_2)
    
    # Делаем предсказание
    prediction = model.predict(scaled_input, verbose=0)
    predicted_class = np.argmax(prediction, axis=1)[0]
    # print(prediction[0])
    return predicted_class, prediction[0]
    # Возвращаем первое (и единственное) предсказанное значение
    # if variant == 1:
    #     if prediction[0][1] > 0.70:    
    #         return True
    #     else:
    #         return False
    # elif variant == 2:
    #     return predicted_class
    # elif variant == 3:
    #     if prediction[0][2] > 0.50 and prediction[0][1]<0.20:
    #         return True
    #     else:
    #         return False
    # return predicted_class

def make_prediction_2(model: Model, input_data: list, scaler1: StandardScaler, scaler2: StandardScaler, scaler3: StandardScaler, variant: int) -> int:
    # Проверяем, что входные данные имеют правильный размер
    if len(input_data) != 225:
        print(len(input_data))
        raise ValueError("input_data должно содержать 150 значений (2 временных ряда по 25 свечей с 3 параметрами).")
    
    # Разделяем данные на две части: первые 75 для первого временного ряда, вторые 75 для второго
    input1 = input_data[:75]  # Данные для первого временного ряда
    input2 = input_data[75:150]  # Данные для второго временного ряда
    input3 = input_data[150:225]
    # Преобразуем списки в numpy массивы и масштабируем данные
    # input1 = np.array(input1).reshape(-1, 3)  # Преобразование в форму (25, 3)
    # input2 = np.array(input2).reshape(-1, 3)
    
    # Масштабируем данные для каждого временного ряда с использованием соответствующих scaler'ов
    scaled_input1 = scaler1.transform([input1])
    scaled_input2 = scaler2.transform([input2])
    scaled_input3 = scaler3.transform([input3])
    # Преобразуем данные в нужную форму (1, 25, 3) для модели
    scaled_input1 = scaled_input1.reshape(1, 25, 3)
    scaled_input2 = scaled_input2.reshape(1, 25, 3)
    scaled_input3 = scaled_input3.reshape(1, 25, 3)
    
    # Делаем предсказание, передавая два временных ряда
    prediction = model.predict([scaled_input1, scaled_input2, scaled_input3], verbose=0)
    # print(prediction)
    # Получаем класс с наивысшей вероятностью
    predicted_class = np.argmax(prediction, axis=1)[0]
    return predicted_class, prediction[0]
    # Возвращаем предсказанный класс
    if variant == 1:
        if prediction[0][1] > 0.55 and prediction[0][2]<0.15:    
            return True
        else:
            return False
    elif variant == 2:
        return predicted_class
    elif variant == 3:
        if prediction[0][2] > 0.50 and prediction[0][1]<0.20:
            return True
        else:
            return False

    