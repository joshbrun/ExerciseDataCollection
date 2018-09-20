from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, GRU
from keras.utils import to_categorical
from keras.optimizers import SGD
import pandas as pd 
import numpy as np
from os import getcwd, listdir
from os.path import join, isfile
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from matplotlib import pyplot as plt
import matplotlib
from keras.models import load_model
import tensorflow as tf

def load_dir(f_name):
    data_set = pd.read_csv(f_name, header=None)
    data_set = data_set.drop(data_set.columns[2::3], axis=1)
    # data_set = data_set.values.astype('float32')
    data_set = data_set.values
    x, y = data_set[:,:-1], data_set[:,-1:]
    y = to_categorical(y)
    return x, y

def get_model():
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model = Sequential()
    model.add(Dense(units=10, activation='relu', input_dim=50))
    model.add(Dense(units=5, activation='relu', input_dim=50))
    model.add(Dense(2, activation='relu'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
    return model


x, y = load_dir("./data/output_training/hcs_squat_front.csv")
val_x, val_y = load_dir("./data/output_testing/hcs_squat_front.csv")
x_test, y_test = load_dir("./data/output_testing/hcs_squat_front.csv")
test_accs = []

model = get_model()
for i in range(10):
    epochs = 20

    checkpoint = ModelCheckpoint("model.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
    early = EarlyStopping(monitor='val_acc', min_delta=0, patience=20, verbose=1, mode='auto')
    board = TensorBoard(log_dir='./tb', histogram_freq=0, write_graph=True, write_images=True)
    history = model.fit(x, y, validation_data=(val_x, val_y), epochs=epochs*(i+1), initial_epoch=i*epochs, batch_size=16, callbacks=[checkpoint, board])

    evaluation = model.evaluate(x_test, y_test)
    print(evaluation)
    print(model.metrics_names)
