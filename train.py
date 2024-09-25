import tensorflow as tf
from tensorflow import keras
import shared_vars as sv
from imblearn.over_sampling import SMOTE
import numpy as np
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
from joblib import dump
from keras.regularizers import L1L2
from keras.layers import BatchNormalization
from keras.layers import GaussianNoise
from sklearn.utils import resample
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, Dropout, Conv1D, Flatten, MaxPooling1D
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from catboost import CatBoostClassifier
from keras.utils import to_categorical
from keras import optimizers
from sklearn.decomposition import PCA
from pyts.image import GramianAngularField
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, LSTM
import json
import pandas as pd
import numpy as np

class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        json_file_path = 'message.json'
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        if data['stop']:
            self.model.stop_training = True
        if logs.get('accuracy') > 0.99 and logs.get('loss') < 0.02:
            print("\nReached 99% accuracy so cancelling training!")
            self.model.stop_training = True
        
        data['message'] = f"Epoch {epoch + 1}:\nloss = {round(logs['loss'], 4)}\naccuracy = {round(logs['accuracy'], 4)}\nval_loss = {round(logs['val_loss'], 4)}\nval_accuracy = {round(logs['val_accuracy'], 4)}"
        data['is_new_message'] = True
        
        with open(json_file_path, 'w') as file:
            json.dump(data, file)

class MCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        json_file_path = 'message.json'
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        if data['stop']:
            self.model.stop_training = True

def train_2Dpic_model_2(softmsax: int, path: str, start: bool):
    checkpoint = ModelCheckpoint(f'_models/my_model_{sv.mod_example}.h5', monitor='val_loss', save_best_only=True, mode='min')
    callbacks = [MyCallback(), tf.keras.callbacks.EarlyStopping(patience=12, restore_best_weights=True), checkpoint]
    train_dir = path
    batch_size = 32
    img_height = 340
    img_width = 340

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.1,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.1,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

    normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

    # data_augmentation = tf.keras.Sequential([
    #     # tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
    #     tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
    #     tf.keras.layers.experimental.preprocessing.RandomZoom(0.1),
    #     tf.keras.layers.experimental.preprocessing.RandomTranslation(0.1, 0.1),
    # ])
    if start:
        model = keras.Sequential([
            # data_augmentation,
            keras.layers.Conv2D(64, 3, activation='relu', input_shape=(img_height, img_width, 3)),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D(2),
            # keras.layers.Dropout(0.2),
            keras.layers.Conv2D(128, 3, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D(2),
            # keras.layers.Dropout(0.2),
            keras.layers.Conv2D(256, 3, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D(2),
            keras.layers.Dropout(0.3),
            keras.layers.Flatten(),
            # tf.keras.layers.GlobalAveragePooling2D(),
            # keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            
            keras.layers.Dense(softmsax, activation='softmax')
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                    metrics=['accuracy'])
    else:
        model = tf.keras.models.load_model(f'_models/my_model_{sv.mod_example}.h5')

    epochs = 100
    history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks=callbacks
    )
    model.save(f'_models/my_model_{sv.mod_example}.keras')
    return model

def train_2Dpic_model(softmsax: int, path: str, min_sample: int):
    callbacks = MyCallback()
    # Загрузка и предобработка данных
    train_dir = path # путь к папке с тренировочными данными
    batch_size = 32 # размер батча
    img_height = 240 # высота изображений
    img_width = 240 # ширина изображений

    # Создание объекта tf.data.Dataset из изображений в подпапках 0, 1 и 2
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.2, # доля валидационных данных
    subset="training", # выбор подмножества для обучения
    seed=123, # случайное зерно для перемешивания данных
    image_size=(img_height, img_width), # размер изображений
    batch_size=batch_size) # размер батча

    # Создание объекта tf.data.Dataset для валидационных данных
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

    # Нормализация значений пикселей от 0 до 1
    normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

    # Создание и компиляция модели CNN
    model = keras.Sequential([
    # Слой свертки с 32 фильтрами размера 3x3 и функцией активации ReLU
    keras.layers.Conv2D(32, 3, activation='relu', input_shape=(img_height, img_width, 3)),
    # Слой макс-пулинга с размером окна 2x2
    keras.layers.MaxPooling2D(2),
    # Слой свертки с 64 фильтрами размера 3x3 и функцией активации ReLU
    keras.layers.Conv2D(64, 3, activation='relu'),
    # Слой макс-пулинга с размером окна 2x2
    keras.layers.MaxPooling2D(2),
    # Слой свертки с 128 фильтрами размера 3x3 и функцией активации ReLU
    keras.layers.Conv2D(128, 3, activation='relu'),
    # Слой макс-пулинга с размером окна 2x2
    keras.layers.MaxPooling2D(2),
    #Dropout
    keras.layers.Dropout(0.5),
    # Слой, который преобразует двумерный тензор в одномерный
    keras.layers.Flatten(),
    # Полносвязный слой с 128 нейронами и функцией активации ReLU
    keras.layers.Dense(128, activation='relu'),
    # Выходной слой с 3 нейронами и функцией активации softmax
    keras.layers.Dense(softmsax, activation='softmax')
    ])

    # Компиляция модели с оптимизатором Adam, функцией потерь категориальной кросс-энтропии и метрикой точности
    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                metrics=['accuracy'])

    # Обучение модели на тренировочных данных и проверка на валидационных данных
    epochs = 500 # количество эпох обучения
    history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks=[callbacks]
    )

    # Визуализация кривых обучения
    # Получение значений потерь и точности на каждой эпохе
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    accuracy = history.history['accuracy']
    val_accuracy = history.history['val_accuracy']

    # # Создание фигуры с двумя подграфиками
    # plt.figure(figsize=(10, 5))
    # # Подграфик для потерь
    # plt.subplot(1, 2, 1)
    # # Построение кривой потерь для обучающей выборки
    # plt.plot(range(epochs), loss, label='Training Loss')
    # # Построение кривой потерь для валидационной выборки
    # plt.plot(range(epochs), val_loss, label='Validation Loss')
    # # Добавление заголовка, легенды и меток осей
    # plt.title('Loss')
    # plt.legend()
    # plt.xlabel('Epoch')
    # plt.ylabel('Loss')
    # # Подграфик для точности
    # plt.subplot(1, 2, 2)
    # # Построение кривой точности для обучающей выборки
    # plt.plot(range(epochs), accuracy, label='Training Accuracy')
    # # Построение кривой точности для валидационной выборки
    # plt.plot(range(epochs), val_accuracy, label='Validation Accuracy')
    # # Добавление заголовка, легенды и меток осей
    # plt.title('Accuracy')
    # plt.legend()
    # plt.xlabel('Epoch')
    # plt.ylabel('Accuracy')
    # Показать фигуру
    # plt.show()

    # Сохранение модели в формате HDF5
    model.save('_models/my_model_3.keras')
    return model
    # Загрузка модели из файла
    # model = tf.keras.models.load_model('_models/my_model.keras')

def load_model(path: str):
    model = tf.keras.models.load_model(path)
    return model

def train_1D_model(softmax: int, path: str):
    callbacks = MyCallback()
    # Load and preprocess the data
    data = pd.read_csv(path, header=None)
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Reshape the data to be 3D as required by Conv1D
    X_train = np.expand_dims(X_train, axis=2)
    X_test = np.expand_dims(X_test, axis=2)

    # Define the model
    model = Sequential()
    model.add(Conv1D(32, 3, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(MaxPooling1D(2))
    model.add(Conv1D(64, 3, activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(softmax, activation='softmax'))

    # Compile the model
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    # Train the model
    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=200, callbacks=[callbacks])

    # Save the model
    model.save('_models/my_model_3.keras')

    return model

def train_GAF_model(softmax: int, path: str):
    callbacks = MyCallback()
    df = pd.read_csv(path, header=None)

    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values 

    # scaler = MinMaxScaler()
    # X = scaler.fit_transform(X)
    # dump(scaler, 'scaler.joblib')
    # sv.scaler = scaler

    n_components = min(X.shape[0], X.shape[1])
    print(f'n_componwents: {n_components}')

    # pca = PCA(n_components=n_components)
    # X = pca.fit_transform(X)
    # dump(pca, 'pca.joblib')
    # sv.pca = pca

    # # Encode target variable
    # label_encoder = LabelEncoder()
    # y = label_encoder.fit_transform(y)
    y = to_categorical(y)
    # GAF Transformation
    gaf = GramianAngularField(image_size=20, method='summation')
    X_gaf = gaf.fit_transform(X)
    dump(gaf, 'gaf.joblib')
    sv.gaf = gaf

    # Reshape the data for CNN
    X_gaf = X_gaf.reshape(-1, 20, 20, 1)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_gaf, y, test_size=0.2, random_state=42)

    # Build the CNN model
    model = Sequential()
    # model.add(GaussianNoise(0.1, input_shape=(7, 7, 1)))
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(20, 20, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(16, activation='relu'))
    # , kernel_regularizer=keras.regularizers.l2(0.01)
    model.add(Dense(softmax, activation='softmax'))

    opt = optimizers.Adam(learning_rate=0.001)
    # Compile the model
    model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, epochs=20000, batch_size=32, callbacks=[callbacks])

    # Evaluate the model on test data
    evaluation = model.evaluate(X_test, y_test)
    print("Accuracy:", evaluation[1])
    model.save('_models/my_model_3.keras')

    return model

def train_LSTM_neuron_network(softmax: int, path):
    callbacks = MyCallback()
    # Load the dataset
    data = pd.read_csv(path, header=None)  # Replace 'data.csv' with the actual filename

    # Split data into features and labels
    features = data.iloc[:, :-1].values
    labels = data.iloc[:, -1].values

    # Convert labels to one-hot encoding
    num_classes = len(np.unique(labels))
    labels = pd.get_dummies(labels).values

    # Reshape features and labels for LSTM
    features = np.reshape(features, (features.shape[0], features.shape[1], 1))
    opt = optimizers.Adam(learning_rate=0.01)
    # Create the LSTM model
    model = Sequential()
    model.add(LSTM(units=32, input_shape=(features.shape[1], 1), return_sequences=True))
    model.add(LSTM(units=64))
    model.add(Dense(units=128, activation='relu'))
    model.add(Dense(units=64, activation='relu'))
    model.add(Dense(units=softmax, activation='softmax'))

    # Compile and train the model with adjusted hyperparameters
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(features, labels, epochs=20000, batch_size=32, callbacks=[callbacks])  # Increase epochs to 20 and batch_size to 128

    # Evaluate the model on the training data
    loss, accuracy = model.evaluate(features, labels)
    print('Training loss:', loss)
    print('Training accuracy:', accuracy)
    model.save('_models/my_model_3.keras')

    return model

def train_model_CatBoost(path: str):
    data = pd.read_csv(path, header=None)
    # data = data[~data.map(lambda x: x > 1 or x < -1).any(axis=1)]

    # data = data.iloc[:, col_to_del:] # delete first columns
    
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    # data_majority = data[data.iloc[:, -1] == 0]
    # data_minority1 = data[data.iloc[:, -1] == 1]
    # data_minority2 = data[data.iloc[:, -1] == 2]

    # # Андерсемплинг мажоритарного класса
    # data_majority_downsampled = resample(data_majority, replace=False, n_samples=len(data_minority1)*10, random_state=42)

    # # Объединение миноритарных классов с андерсемплированным мажоритарным классом
    # data_downsampled = pd.concat([data_majority_downsampled, data_minority1, data_minority2])

    # X = data_downsampled.iloc[:, :-1]
    # y = data_downsampled.iloc[:, -1]

    class_counts = y.value_counts()
    print(class_counts)
    class_weights = [1, 2, 2] #TODO add third class

    params = {
    # # 'depth': 10,
    # 'grow_policy': 'Lossguide',
    # 'max_leaves': 128,
    'learning_rate': 0.1,
    'iterations': 15000,
    'depth': 7,
    'loss_function':'MultiClass', #TODO uncoment this
    'early_stopping_rounds': 100,
    'l2_leaf_reg': 5,
    'class_weights': class_weights
}
    # scaler = MinMaxScaler()
    # X = scaler.fit_transform(X)
    # dump(scaler, 'scaler.joblib')
    # sv.scaler = scaler
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = CatBoostClassifier(random_state=42, **params) #categorical_feature=categorical_indexes
    
    model.fit(X_train, y_train, eval_set=(X_test, y_test))
    print(model.get_all_params())
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, y_pred))

    feature_importance = model.feature_importances_
    print('Feature Importances:')
    for i, importance in enumerate(feature_importance):
        print(f'Feature {i+1}: {importance:.4f}')
    
    model.save_model('_models/my_model_3.keras')

    return model

def early_stop_callback(error, best_error):
    # Остановить обучение, если ошибка меньше 0.05
    if best_error < 0.05:
        return True
    else:
        return False
    
def train_LSTM_classif(path: str):
    callbacks = [MyCallback(), tf.keras.callbacks.EarlyStopping(patience=5)]
    data = pd.read_csv(path, header=None)

     # Разделение данных на мажоритарный и миноритарные классы
    data_majority = data[data.iloc[:, -1] == 0]
    data_minority1 = data[data.iloc[:, -1] == 1]
    data_minority2 = data[data.iloc[:, -1] == 2]

    # Андерсемплинг мажоритарного класса
    data_majority_downsampled = resample(data_majority, replace=False, n_samples=len(data_minority1)*3, random_state=42)

    # Объединение миноритарных классов с андерсемплированным мажоритарным классом
    data_downsampled = pd.concat([data_majority_downsampled, data_minority1, data_minority2])

    X = data_downsampled.iloc[:, :-1]
    y = data_downsampled.iloc[:, -1]

    # class_weights = {0: 1., 1: 10., 2: 10.}
    # X = data.iloc[:, :-1]
    # y = data.iloc[:, -1]

    # Предполагается, что X и y уже определены
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # smote = SMOTE(sampling_strategy='minority')
    # X_train, y_train = smote.fit_resample(X_train, y_train)
    # Преобразование y в категориальный формат
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    # Создание модели
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(32))
    model.add(Dropout(0.2))
    model.add(Dense(3, activation='softmax'))
    opt = optimizers.Adam(learning_rate=0.01)
    # Компиляция модели
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

    # Обучение модели
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, callbacks=[callbacks])

    y_pred = model.predict(X_test)
    y_pred = np.argmax(y_pred, axis=1)
    y_test = np.argmax(y_test, axis=1)
    print(classification_report(y_test, y_pred, target_names=['Class 0', 'Class 1', 'Class 2']))

    # loss, accuracy = model.evaluate(X_test, y_test)
    # print('Training loss:', loss)
    # print('Training accuracy:', accuracy)
    model.save('_models/my_model_3.keras')

    return model



# Определение и тренировка модели LSTM
def train_lstm_model(file_path, n_steps=84, epochs=50, batch_size=32):
    data = pd.read_csv(file_path, header=None)
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    # Разделение данных на тренировочный и валидационный наборы
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Форматирование данных для LSTM
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))

    # Создание модели
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)),
        BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.LSTM(256, activation='relu', return_sequences=True),
        BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.LSTM(128, activation='relu'),
        BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, kernel_regularizer=tf.keras.regularizers.l2(0.01))
    ])
    checkpoint = ModelCheckpoint('_models/my_model_5.h5', monitor='val_loss', save_best_only=True, mode='min')
    callbacks = [MCallback(), checkpoint]

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='mse')

    # Тренировка модели с валидационными данными
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size, verbose=1, callbacks=callbacks)

    return model

def train_lstm_model_2(file_path, n_steps=84, epochs=50, batch_size=32):
    data = pd.read_csv(file_path, header=None)
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    # Разделение данных на тренировочный и валидационный наборы
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Форматирование данных для LSTM
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))

    # Создание модели
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(128, activation='tanh', return_sequences=True, input_shape=(X_train.shape[1], 1)),
        BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.LSTM(256, activation='tanh', return_sequences=True),
        BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.LSTM(128, activation='tanh'),
        BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='sigmoid', kernel_regularizer=tf.keras.regularizers.l2(0.01))
    ])
    checkpoint = ModelCheckpoint('_models/my_model_5.h5', monitor='val_loss', save_best_only=True, mode='min')
    callbacks = [MCallback(), checkpoint]

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    # Тренировка модели с валидационными данными
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size, verbose=1, callbacks=callbacks)

    return model
