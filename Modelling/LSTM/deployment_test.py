from keras.models import load_model
import tensorflow as tf
import numpy as np
from LSTMv2 import load_dir

model = load_model("./model.h5")
graph = tf.get_default_graph()

x_test, y_test = load_dir("./data/terran/")

# train_eval    
evaluation = model.evaluate(x_test, y_test)

print(evaluation)
print(model.metrics_names)

# input = 
  # 
# prediction = model.predict(input)
# 
# print(prediction)