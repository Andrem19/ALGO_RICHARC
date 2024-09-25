import argparse
import pandas as pd
import tensorflow as tf
import io
import boto3
import os
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint

# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def train_model(file_path, model_dir, n_steps=84, epochs=50, batch_size=32):

    s3 = boto3.client('s3')
    bucket_name, key = file_path.replace("s3://", "").split("/", 1)
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    data = pd.read_csv(io.BytesIO(obj['Body'].read()), header=None)

    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))

    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(100, activation='relu', input_shape=(X_train.shape[1], 1)),
        tf.keras.layers.Dense(1)
    ])
    

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='mse')

    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size, verbose=2)

    model_local_path = '/tmp/my_model.h5'
    model.save(model_local_path)

    # Используем boto3 для загрузки модели в S3
    s3.upload_file(model_local_path, bucket_name, 'models/my_model.h5')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-path', type=str, required=True)
    parser.add_argument('--n-steps', type=int, default=84)
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch-size', type=int, default=32)
    args, unknown = parser.parse_known_args()  # Игнорируем неизвестные аргументы
    train_model(args.file_path, "s3://sagemodels1/models", args.n_steps, args.epochs, args.batch_size)
