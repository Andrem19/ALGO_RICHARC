import tensorflow as tf
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import json
import shared_vars as sv
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
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

def custom_loss(y_true, y_pred):
    # Матрица штрафов
    penalty_matrix = tf.constant([
        [0.0, 1.0, 2.0, 3.0, 4.0],  # Штрафы для ошибки в классе 0
        [1.0, 0.0, 1.0, 3.0, 3.0],  # Штрафы для ошибки в классе 1
        [2.0, 1.0, 0.0, 1.0, 2.0],  # Штрафы для ошибки в классе 2
        [3.0, 3.0, 1.0, 0.0, 1.0],  # Штрафы для ошибки в классе 3
        [4.0, 3.0, 2.0, 1.0, 0.0],  # Штрафы для ошибки в классе 4
    ], dtype=tf.float32)
    
    # Получение индексов реальных классов
    true_idx = tf.argmax(y_true, axis=-1)

    # Применение softmax к предсказаниям
    y_pred_softmax = tf.nn.softmax(y_pred)

    # Использование индексов для нахождения штрафов для каждого предсказанного класса
    penalties = tf.tensordot(y_pred_softmax, penalty_matrix, axes=1)
    
    # Выбор штрафа в зависимости от правильного класса
    true_penalties = tf.gather_nd(penalties, tf.expand_dims(true_idx, axis=-1), batch_dims=1)

    # Среднее значение штрафов для всех примеров в батче
    penalty_loss = tf.reduce_mean(true_penalties)

    # Основная функция потерь - categorical crossentropy
    cross_entropy_loss = tf.reduce_mean(tf.keras.losses.categorical_crossentropy(y_true, y_pred))

    # Совмещение штрафов и crossentropy
    return cross_entropy_loss + 0.1 * penalty_loss

import tensorflow as tf

class CustomModelCheckpoint(tf.keras.callbacks.Callback):
    def __init__(self, save_path, monitor='val_accuracy', save_best_only=True, min_accuracy=0.60, mode='max'):
        super(CustomModelCheckpoint, self).__init__()
        self.save_path = save_path
        self.monitor = monitor
        self.save_best_only = save_best_only
        self.min_accuracy = min_accuracy
        self.best_val = -float('inf') if mode == 'max' else float('inf')
        self.mode = mode

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get(self.monitor)
        
        # Проверяем, что val_accuracy превышает порог
        if current is not None and current > self.min_accuracy:
            if self.save_best_only:
                if (self.mode == 'max' and current > self.best_val) or (self.mode == 'min' and current < self.best_val):
                    self.best_val = current
                    # Формируем имя файла с точностью
                    filepath = f'{self.save_path}/model_{current:.4f}.h5'
                    self.model.save(filepath)
                    print(f'Saving model at {current:.4f} accuracy as {filepath}')
            else:
                # Сохраняем каждую модель, если save_best_only=False
                filepath = f'{self.save_path}/model_{current:.4f}.h5'
                self.model.save(filepath)
                print(f'Saving model at {current:.4f} accuracy as {filepath}')

# Использование





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
    # checkpoint = ModelCheckpoint(f'_models/my_model_{sv.mod_example}.h5', monitor='val_accuracy', save_best_only=True, mode='max')
    save_path = f'_models/1h3_trend'
    checkpoint = CustomModelCheckpoint(save_path=save_path, monitor='val_accuracy', save_best_only=True, min_accuracy=0.65)
    callbacks = [MyCallback(), checkpoint, reduce_lr]
    # 1. Чтение данных из CSV
    data = pd.read_csv(csv_file, header=None)

    # Допустим, у нас 200 столбцов для 50 свечей (OHLC) и 1 столбец для target
    n_features = 500  # 4 (OHLC) * 50 свечей
    X = data.iloc[:, :n_features].values  # Признаки (OHLC)
    y = data.iloc[:, n_features].values#:n_features+3].values   # Target (процент изменения закрытия)
    y = to_categorical(y, num_classes=3)
    # 2. Нормализация данных (очень важно для LSTM)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, 'scaler_1h.pkl')

    # 3. Преобразуем данные в формат (samples, timesteps, features) для LSTM
    X_lstm = X_scaled.reshape(X_scaled.shape[0], 100, 5)  # 50 свечей, 4 значения на свечу (OHLC)

    # 4. Разделение на обучающие и валидационные данные
    X_train, X_val, y_train, y_val = train_test_split(X_lstm, y, test_size=0.15, random_state=42)

    # 5. Создание LSTM модели
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(128, return_sequences=True, input_shape=(100, 5), dropout=0.2, recurrent_dropout=0.1),
        tf.keras.layers.BatchNormalization(),
        # tf.keras.layers.Dropout(0.3),
        tf.keras.layers.LSTM(64, dropout=0.2, recurrent_dropout=0.1),
        tf.keras.layers.BatchNormalization(),
        # tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(32, kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        # tf.keras.layers.Dropout(0.2),
        # tf.keras.layers.Dense(32),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    # Компиляция модели
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])#loss='mse''categorical_crossentropy'
    # class_weights = {0: 1, 1: 2, 2: 2}
    # 6. Тренировка модели
    history = model.fit(
        X_train, 
        y_train, 
        epochs=1000, 
        batch_size=32, 
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        # class_weight=class_weights
        )

    # Возвращаем модель и историю обучения
    return model, history

# Функция для создания блока внимания
def attention_block(inputs):
    attention = tf.keras.layers.Dense(1, activation='tanh')(inputs)
    attention = tf.keras.layers.Flatten()(attention)
    attention = tf.keras.layers.Activation('softmax')(attention)
    attention = tf.keras.layers.RepeatVector(inputs.shape[-1])(attention)
    attention = tf.keras.layers.Permute([2, 1])(attention)
    output_attention = tf.keras.layers.Multiply()([inputs, attention])
    return output_attention

# # Основная функция для тренировки модели
# def train_model(csv_file):
#     reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=6, min_lr=0.00001)
#     checkpoint = ModelCheckpoint(f'_models/my_model.h5', monitor='val_accuracy', save_best_only=True, mode='max')
#     callbacks = [checkpoint, reduce_lr]
    
#     # 1. Чтение данных из CSV
#     data = pd.read_csv(csv_file, header=None)

#     # 2. Допустим, у нас 75 столбцов для 25 свечей (OHLC) и 1 столбец для target
#     n_features = 75  # 3 (различия) * 25 свечей
#     X = data.iloc[:, :n_features].values  # Признаки (OHLC)
#     y = data.iloc[:, n_features].values   # Target (классы 0-4)
#     y = to_categorical(y, num_classes=5)
    
#     # 3. Нормализация данных (очень важно для LSTM)
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)
#     joblib.dump(scaler, 'scaler.pkl')

#     # 4. Преобразуем данные в формат (samples, timesteps, features) для LSTM
#     X_lstm = X_scaled.reshape(X_scaled.shape[0], 25, 3)  # 25 свечей, 3 значения на свечу (различия open-close, open-high, open-low)

#     # 5. Разделение на обучающие и валидационные данные
#     X_train, X_val, y_train, y_val = train_test_split(X_lstm, y, test_size=0.15, random_state=42)

#     # 6. Создание LSTM модели с блоком внимания
#     inputs = tf.keras.Input(shape=(25, 3))  # Входные данные: 25 свечей, 3 признака
#     lstm_out = tf.keras.layers.LSTM(64, return_sequences=True, dropout=0.2, recurrent_dropout=0.01)(inputs)
    
#     # Применяем attention_block
#     attention_out = attention_block(lstm_out)
    
#     # Продолжаем слои LSTM и Dense
#     lstm_out = tf.keras.layers.LSTM(32, dropout=0.2, recurrent_dropout=0.1)(attention_out)
#     lstm_out = tf.keras.layers.BatchNormalization()(lstm_out)
    
#     dense_out = tf.keras.layers.Dense(16, kernel_regularizer=tf.keras.regularizers.l2(0.01))(lstm_out)
#     outputs = tf.keras.layers.Dense(5, activation='softmax')(dense_out)

#     # Создание модели
#     model = tf.keras.Model(inputs=inputs, outputs=outputs)

#     # Компиляция модели
#     optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
#     model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

#     # 7. Тренировка модели
#     history = model.fit(
#         X_train, 
#         y_train, 
#         epochs=1000, 
#         batch_size=64, 
#         validation_data=(X_val, y_val),
#         callbacks=callbacks
#     )

#     # Возвращаем модель и историю обучения
#     return model, history


def train_model_with_two_series(csv_file):
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=6, min_lr=0.00001)
    checkpoint = ModelCheckpoint(f'_models/my_model_{sv.mod_example}.h5', monitor='val_loss', save_best_only=True, mode='min')
    callbacks = [MyCallback(), checkpoint, reduce_lr]

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
    y = to_categorical(y, num_classes=5)

    # Разделение на обучающие и валидационные данные
    X1_train, X1_val, X2_train, X2_val, y_train, y_val = train_test_split(X1_lstm, X2_lstm, y, test_size=0.2, random_state=42)

    # Вход для первого временного ряда
    input1 = Input(shape=(25, 3))
    x1 = LSTM(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.2)(input1)
    x1 = BatchNormalization()(x1)
    x1 = LSTM(64, dropout=0.3, recurrent_dropout=0.2)(x1)
    x1 = Dropout(0.2)(x1)

    # Вход для второго временного ряда
    input2 = Input(shape=(25, 3))
    x2 = LSTM(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.2)(input2)
    x2 = BatchNormalization()(x2)
    x2 = LSTM(64, dropout=0.3, recurrent_dropout=0.2)(x2)
    x2 = Dropout(0.2)(x2)

    # Объединение выходов
    combined = tf.keras.layers.concatenate([x1, x2])

    # Общие полносвязные слои для классификации
    x = Dense(64, activation='relu')(combined)
    x = Dropout(0.2)(x)
    x = Dense(32, activation='relu')(x)
    output = Dense(5, activation='softmax')(x)

    # Создание модели
    model = Model(inputs=[input1, input2], outputs=output)

    # Компиляция модели
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    class_weights = {0: 1.5, 1: 1.2, 2: 1.0, 3: 1.2, 4: 1.5}
    # Тренировка модели
    history = model.fit(
        [X1_train, X2_train],  # Два входа
        y_train,               # Целевой класс
        epochs=1000,
        batch_size=32,
        validation_data=([X1_val, X2_val], y_val),
        callbacks=callbacks,
        class_weight=class_weights
    )

    # Возвращаем модель и историю обучения
    return model, history



def train_model_with_three_series(csv_file):
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=6, min_lr=0.00001)
    checkpoint = ModelCheckpoint(f'_models/my_model_{sv.mod_example}.h5', monitor='val_loss', save_best_only=True, mode='min')
    callbacks = [MyCallback(), checkpoint, reduce_lr]

    # 1. Чтение данных из CSV
    data = pd.read_csv(csv_file, header=None)

    # Допустим, у нас 300 столбцов для 75 свечей (OHLC) и 1 столбец для target
    n_features = 225  # 3 временных ряда по 75 свечей (4 параметра на свечу)
    X1 = data.iloc[:, :75].values  # Первый временной ряд
    X2 = data.iloc[:, 75:150].values  # Второй временной ряд
    X3 = data.iloc[:, 150:225].values  # Третий временной ряд
    y = data.iloc[:, 225].values  # Таргет (класс)

    # Нормализация данных для каждого временного ряда
    scaler_1 = StandardScaler()
    scaler_2 = StandardScaler()
    scaler_3 = StandardScaler()

    X1_scaled = scaler_1.fit_transform(X1)
    X2_scaled = scaler_2.fit_transform(X2)
    X3_scaled = scaler_3.fit_transform(X3)

    joblib.dump(scaler_1, 'scaler_1.pkl')
    joblib.dump(scaler_2, 'scaler_2.pkl')
    joblib.dump(scaler_3, 'scaler_3.pkl')

    # Преобразование в форму (samples, timesteps, features)
    X1_lstm = X1_scaled.reshape(X1_scaled.shape[0], 25, 3)
    X2_lstm = X2_scaled.reshape(X2_scaled.shape[0], 25, 3)
    X3_lstm = X3_scaled.reshape(X3_scaled.shape[0], 25, 3)

    # Преобразование меток классов
    y = to_categorical(y, num_classes=5)

    # Разделение на обучающие и валидационные данные
    X1_train, X1_val, X2_train, X2_val, X3_train, X3_val, y_train, y_val = train_test_split(X1_lstm, X2_lstm, X3_lstm, y, test_size=0.2, random_state=42)

    # Вход для первого временного ряда
    input1 = Input(shape=(25, 3))
    x1 = LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.1)(input1)
    # x1 = BatchNormalization()(x1)
    x1 = attention_block(x1)
    # x1 = Dropout(0.2)(x1)
    x1 = LSTM(64, dropout=0.3, recurrent_dropout=0.1)(x1)
    x1 = BatchNormalization()(x1)

    # Вход для второго временного ряда
    input2 = Input(shape=(25, 3))
    x2 = LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.1)(input2)
    # x2 = BatchNormalization()(x2)
    x2 = attention_block(x2)
    # x2 = Dropout(0.2)(x2)
    x2 = LSTM(64, dropout=0.3, recurrent_dropout=0.1)(x2)
    x2 = BatchNormalization()(x2)

    # Вход для третьего временного ряда
    input3 = Input(shape=(25, 3))
    x3 = LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.1)(input3)
    # x3 = BatchNormalization()(x3)
    x3 = attention_block(x3)
    # x3 = Dropout(0.2)(x3)
    x3 = LSTM(64, dropout=0.3, recurrent_dropout=0.1)(x3)
    x3 = BatchNormalization()(x3)

    # Объединение выходов
    combined = tf.keras.layers.concatenate([x1, x2, x3])

    # Общие полносвязные слои для классификации
    x = Dense(128, activation='relu')(combined)
    x = Dropout(0.2)(x)
    x = Dense(64, activation='relu')(combined)
    x = Dropout(0.2)(x)
    x = Dense(32, activation='relu')(combined)
    output = Dense(5, activation='softmax')(x)

    # Создание модели
    model = Model(inputs=[input1, input2, input3], outputs=output)

    # Компиляция модели
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])#'categorical_crossentropy'
    class_weights = {0: 1.5, 1: 1.2, 2: 1.0, 3: 1.2, 4: 1.5}
    # Тренировка модели
    history = model.fit(
        [X1_train, X2_train, X3_train],  # Три входа
        y_train,                         # Целевой класс
        epochs=1000,
        batch_size=32,
        validation_data=([X1_val, X2_val, X3_val], y_val),
        callbacks=callbacks,
        class_weight=class_weights
    )

    # Возвращаем модель и историю обучения
    return model, history

# def train_model_XGBoost(path: str):
#     data = pd.read_csv(path, header=None)
#     # random.shuffle(data)
#     # data = data.iloc[:, 10:] # delete first columns
#     X = data.iloc[:, :-1]
#     y = data.iloc[:, -1]


#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     xgb_model = XGBClassifier(n_estimators=1000, random_state=42)

#     xgb_model.fit(X_train, y_train, eval_metric="logloss", verbose=True)

#     y_pred = xgb_model.predict(X_test)

#     accuracy = accuracy_score(y_test, y_pred)

#     feature_importance = xgb_model.feature_importances_
#     print('Feature Importances:')
#     for i, importance in enumerate(feature_importance):
#         print(f'Feature {i+1}: {importance:.4f}')

#     class_report = classification_report(y_test, y_pred)
#     print('Classification Report:')
#     print(class_report)
#     save_path = f'_models/my_model_{sv.mod_example}.h5'
#     joblib.dump(xgb_model, save_path)
#     return xgb_model