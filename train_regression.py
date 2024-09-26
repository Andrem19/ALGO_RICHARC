import tensorflow as tf
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import json
import shared_vars as sv
import os
import pandas as pd
import numpy as np
from keras.models import Sequential
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from keras.layers import Input, LSTM, Dense, BatchNormalization, Dropout
from keras.models import Model
from keras.utils import to_categorical

class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        json_file_path = 'message.json'
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        if data['stop']:
            self.model.stop_training = True
        if logs.get('loss') < 0.00002:
            print("\nLoss is below 0.02, stopping training!")
            self.model.stop_training = True
        
        #data['message'] = f"Epoch {epoch + 1}:\nloss = {round(logs['loss'], 4)}\nval_loss = {round(logs['val_loss'], 4)}"
        data['message'] = f"Epoch {epoch + 1}:\nloss = {round(logs['loss'], 4)}\naccuracy = {round(logs['accuracy'], 4)}\nval_loss = {round(logs['val_loss'], 4)}\nval_accuracy = {round(logs['val_accuracy'], 4)}"
        data['is_new_message'] = True
        
        with open(json_file_path, 'w') as file:
            json.dump(data, file)

def parse_image(filename):
    parts = tf.strings.split(filename, '_')
    label_str = tf.strings.split(parts[-1], '.png')[0]
    label = tf.strings.to_number(label_str)
    image = tf.io.read_file(filename)
    image = tf.image.decode_png(image, channels=3)
    image = tf.image.resize(image, [340, 340])
    image = image / 255.0
    return image, label

def load_dataset(path):
    list_ds = tf.data.Dataset.list_files(os.path.join(path, '*.png'))
    labeled_ds = list_ds.map(parse_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    return labeled_ds

def train_2Dpic_model_regression(path: str):
    checkpoint = ModelCheckpoint(f'_models/my_model_{sv.mod_example}.h5', monitor='val_loss', save_best_only=True, mode='min')
    callbacks = [MyCallback(), tf.keras.callbacks.EarlyStopping(patience=24, restore_best_weights=True), checkpoint]
    train_dir = path
    batch_size = 32

    dataset = load_dataset(train_dir)
    val_size = int(0.1 * len(dataset))
    train_ds = dataset.skip(val_size).batch(batch_size).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    val_ds = dataset.take(val_size).batch(batch_size).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

    # data_augmentation = tf.keras.Sequential([
    #     tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
    #     tf.keras.layers.experimental.preprocessing.RandomTranslation(0.05, 0.05),
    # ])

    model = tf.keras.Sequential([
        # data_augmentation,
        tf.keras.layers.Conv2D(16, 3, activation='relu', input_shape=(340, 340, 3)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(2),
        
        tf.keras.layers.Flatten(),
        # tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        tf.keras.layers.Dense(1, activation='linear')
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                  loss='mean_squared_error')

    epochs = 100
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks
    )
    model.save(f'_models/my_model_{sv.mod_example}.keras')
    return model



def train_model(csv_file):
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=6, min_lr=0.00001)
    checkpoint = ModelCheckpoint(f'_models/my_model_{sv.mod_example}.h5', monitor='val_accuracy', save_best_only=True, mode='max')
    callbacks = [MyCallback(), checkpoint, reduce_lr]
    # 1. Чтение данных из CSV
    data = pd.read_csv(csv_file, header=None)

    # Допустим, у нас 200 столбцов для 50 свечей (OHLC) и 1 столбец для target
    n_features = 75  # 4 (OHLC) * 50 свечей
    X = data.iloc[:, :n_features].values  # Признаки (OHLC)
    y = data.iloc[:, n_features].values#:n_features+3].values   # Target (процент изменения закрытия)
    y = to_categorical(y, num_classes=5)
    # 2. Нормализация данных (очень важно для LSTM)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, 'scaler.pkl')

    # 3. Преобразуем данные в формат (samples, timesteps, features) для LSTM
    X_lstm = X_scaled.reshape(X_scaled.shape[0], 25, 3)  # 50 свечей, 4 значения на свечу (OHLC)

    # 4. Разделение на обучающие и валидационные данные
    X_train, X_val, y_train, y_val = train_test_split(X_lstm, y, test_size=0.15, random_state=42)

    # 5. Создание LSTM модели
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(128, return_sequences=True, input_shape=(25, 3)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(32, kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        tf.keras.layers.Dense(5, activation='softmax')
    ])
    # Компиляция модели
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])#loss='mse'

    # 6. Тренировка модели
    history = model.fit(
        X_train, 
        y_train, 
        epochs=1000, 
        batch_size=32, 
        validation_data=(X_val, y_val),
        callbacks=callbacks
        )

    # Возвращаем модель и историю обучения
    return model, history




def train_model_with_two_series(csv_file):
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=6, min_lr=0.00001)
    checkpoint = ModelCheckpoint(f'_models/my_model_{sv.mod_example}.h5', monitor='val_loss', save_best_only=True, mode='min')
    callbacks = [checkpoint, reduce_lr]

    # 1. Чтение данных из CSV
    data = pd.read_csv(csv_file, header=None)

    # Допустим, у нас 200 столбцов для 50 свечей (OHLC) и 1 столбец для target
    n_features = 150  # 2 временных ряда по 50 свечей (4 параметра на свечу)
    X1 = data.iloc[:, :75].values  # Первый временной ряд
    X2 = data.iloc[:, 75:150].values  # Второй временной ряд
    y = data.iloc[:, 150].values  # Таргет (класс)

    # Нормализация данных для каждого временного ряда
    scaler_1 = StandardScaler()
    scaler_2 = StandardScaler()

    X1_scaled = scaler_1.fit_transform(X1)
    X2_scaled = scaler_2.fit_transform(X2)

    joblib.dump(scaler_1, 'scaler_1.pkl')
    joblib.dump(scaler_2, 'scaler_2.pkl')

    # Преобразование в форму (samples, timesteps, features)
    X1_lstm = X1_scaled.reshape(X1_scaled.shape[0], 25, 3)
    X2_lstm = X2_scaled.reshape(X2_scaled.shape[0], 25, 3)

    # Преобразование меток классов
    y = to_categorical(y, num_classes=3)

    # Разделение на обучающие и валидационные данные
    X1_train, X1_val, X2_train, X2_val, y_train, y_val = train_test_split(X1_lstm, X2_lstm, y, test_size=0.2, random_state=42)

    # Вход для первого временного ряда
    input1 = Input(shape=(25, 3))
    x1 = LSTM(128, return_sequences=True)(input1)
    x1 = BatchNormalization()(x1)
    x1 = Dropout(0.2)(x1)
    x1 = LSTM(64)(x1)

    # Вход для второго временного ряда
    input2 = Input(shape=(25, 3))
    x2 = LSTM(128, return_sequences=True)(input2)
    x2 = BatchNormalization()(x2)
    x2 = Dropout(0.2)(x2)
    x2 = LSTM(64)(x2)

    # Объединение выходов
    combined = tf.keras.layers.concatenate([x1, x2])

    # Общие полносвязные слои для классификации
    x = Dense(64, activation='relu')(combined)
    x = Dropout(0.2)(x)
    output = Dense(3, activation='softmax')(x)

    # Создание модели
    model = Model(inputs=[input1, input2], outputs=output)

    # Компиляция модели
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Тренировка модели
    history = model.fit(
        [X1_train, X2_train],  # Два входа
        y_train,               # Целевой класс
        epochs=1000,
        batch_size=32,
        validation_data=([X1_val, X2_val], y_val),
        callbacks=callbacks
    )

    # Возвращаем модель и историю обучения
    return model, history
