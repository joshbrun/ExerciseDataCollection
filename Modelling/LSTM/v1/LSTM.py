from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, GRU
import pandas as pd 
import numpy as np
from keras.preprocessing.sequence import TimeseriesGenerator

data_set = pd.read_csv("input.csv", header=None)
data_set = data_set.drop(data_set.columns[2::3], axis=1)
print(data_set.shape)
print(data_set)
data_set = data_set.values.astype('float32')

print(data_set.shape)

train_size = int(len(data_set) * 0.8)
test_size = len(data_set) - train_size
train, test = data_set[0:train_size,:], data_set[train_size:len(data_set),:]
print(len(train), len(test))

X_train, y_train = train[:,:-1], train[:,-1:]
X_test, y_test = test[:,:-1], test[:,-1:]
print(X_test.shape, y_test.shape)

data_train = TimeseriesGenerator(X_train, y_train,
                               length=10, sampling_rate=1,
                               batch_size=1)
data_test = TimeseriesGenerator(X_test, y_test,
                               length=10, sampling_rate=1,
                               batch_size=1)

# i = 0
# for x in data_train:
#     i += 1
#     print(i)

print(len(data_train))
model = Sequential()
model.add(LSTM(250, input_shape=(10, 50), dropout=0.10, return_sequences=True))
model.add(LSTM(250, dropout=0.10, return_sequences=True))
model.add(LSTM(250))
# model.add(Dense(50, activation='relu'))
model.add(Dense(1, activation='relu'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.fit_generator(data_train, validation_data=data_test, epochs=50)
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3, batch_size=64)
