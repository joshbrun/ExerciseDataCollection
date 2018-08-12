from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, GRU
import pandas as pd 
import numpy as np
from os import getcwd, listdir
from os.path import join, isfile
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping

def load_dir(set_dir):
    set_dir = "./data/output_training/"
    files = [f for f in listdir(set_dir) if isfile(join(set_dir, f))]
    x_data_sets = []
    y_data_sets = []
    for f in files:
        data_set = pd.read_csv(set_dir + f, header=None)
        data_set = data_set.drop(data_set.columns[2::3], axis=1)
        # print(data_set.shape)
        # print(data_set)
        data_set = data_set.values.astype('float32')

        x, y = data_set[:,:-1], data_set[:,-1:]

        # generate sequences with windows
        data_gen = TimeseriesGenerator(x, y,
                                    length=48, sampling_rate=8,
                                    batch_size=1)

        for i in range(len(data_gen)):
            # print(data_gen[i][0][0])
            x_data_sets.append(data_gen[i][0][0])
            # print(data_gen[i][0][0])
            y_data_sets.append(data_gen[i][1][0])

    x_data_sets = np.array(x_data_sets)
    y_data_sets = np.array(y_data_sets)

    return x_data_sets, y_data_sets

x, y = load_dir("./data/output_training/")
val_x, val_y = load_dir("./data/output_validation/")
print(x)

model = Sequential()
model.add(LSTM(250, input_shape=(6, 50), dropout=0.50, return_sequences=True))
model.add(LSTM(250, dropout=0.40, return_sequences=True))
model.add(LSTM(250, dropout=0.30))
model.add(Dense(1, activation='relu'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

checkpoint = ModelCheckpoint("model.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='val_acc', min_delta=0, patience=20, verbose=1, mode='auto')
board = TensorBoard(log_dir='./tb', histogram_freq=0, write_graph=True, write_images=True)

model.fit(x, y, validation_data=(val_x, val_y), epochs=1000, batch_size=64, callbacks=[checkpoint, early, board])
