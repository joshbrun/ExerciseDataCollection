from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, GRU
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

def load_dir(set_dir):
    # set_dir = "./data/output_training/"
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
                                    length=48, sampling_rate=4,
                                    batch_size=1)

        for i in range(len(data_gen)):
            # print(data_gen[i][0][0])
            x_data_sets.append(data_gen[i][0][0])
            # print(data_gen[i][0][0])
            y_data_sets.append(data_gen[i][1][0])

    x_data_sets = np.array(x_data_sets)
    y_data_sets = np.array(y_data_sets)

    return x_data_sets, y_data_sets

def get_model():
    model = Sequential()
    model.add(GRU(500, input_shape=(12, 50)))
    # model.add(LSTM(250, return_sequences=True))
    # model.add(LSTM(250))
    model.add(Dense(1, activation='relu'))
    model.compile(loss='binary_crossentropy', optimizer='adam')
    return model


x, y = load_dir("./data/output_training/")
val_x, val_y = load_dir("./data/output_validation/")
x_test, y_test = load_dir("./data/output_test/")
test_accs = []

for j in range(1):
    model = get_model()
    for i in range(1):
        epochs = 20

        checkpoint = ModelCheckpoint("model1.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
        early = EarlyStopping(monitor='val_acc', min_delta=0, patience=20, verbose=1, mode='auto')
        board = TensorBoard(log_dir='./tb', histogram_freq=0, write_graph=True, write_images=True)
        history = model.fit(x, y, validation_data=(val_x, val_y), epochs=epochs*(i+1), initial_epoch=i*epochs, batch_size=16, callbacks=[checkpoint, board])


        plt.rcParams.update({'font.size': 25})
        axes = plt.gca()
        axes.set_ylim([0,1])  

        plt.plot(history.history['acc'], color='blue')
        plt.plot(history.history['val_acc'], color='green')

        val_eval = model.evaluate(val_x, val_y)
        evaluation = model.evaluate(x_test, y_test)

        test_accs.append(evaluation[1])

a = pd.DataFrame(test_accs)
a.to_csv('./ss_16_me.csv')

plt.ylabel('Score')
plt.xlabel('epoch')
    
plt.legend(['Train Accuracy', 'Validation Accuracy'], loc='lower left')
plt.show()

# train_eval    
val_eval = model.evaluate(val_x, val_y)
evaluation = model.evaluate(x_test, y_test)

print(evaluation)
print(model.metrics_names)

model = load_model("./model1.h5")
graph = tf.get_default_graph()
# train_eval    
val_eval = model.evaluate(val_x, val_y)
evaluation = model.evaluate(x_test, y_test)

print(evaluation)
print(model.metrics_names)