import numpy as py
import pandas as pd
import tensorflow as tf
# from tensorflow import feature_column # reformats structured data fro ease in calculations
# from tensorflow.keras import layers # to create the layer in the neural network
# from sklearn.model_selection import train_test_split # splits the data for us
from sklearn.metrics import confusion_matrix # calculates the confusion matrix
from sklearn.metrics import accuracy_score # calculates the accuracy score

import matplotlib.pyplot as plt

physical_devices = tf.config.list_physical_devices('GPU')
try:
    tf.config.experimental.set_virtual_device_configuration(
       physical_devices[0],
       [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*5)])
    # tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
    # Invalid device or cannot modify virtual devices once initialized.
    pass

Number_of_features = 2
Number_of_units = 1 # number of neurons

weight = tf.Variable(tf.zeros([Number_of_features,Number_of_units])) # initializing to zero
bias = tf.Variable(tf.zeros([Number_of_units])) # Initializing to zero

def perceptron(x):
    I = tf.add(tf.matmul(x,weight),bias)
    output = tf.sigmoid(I)
    return output

individual_loss = lambda : abs(tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y,logits=perceptron(x))))

optimizer = tf.keras.optimizers.Adam(.01)

dataframe = pd.read_csv("data.csv")
print(dataframe.head())
# plt.scatter(dataframe.x1, dataframe.x2, c= dataframe.label)
# plt.show()

x_input = dataframe[['x1','x2']].to_numpy()
y_label = dataframe[['label']].to_numpy()

x=tf.Variable(x_input)
x=tf.cast(x, tf.float32)

y = tf.Variable(y_label)
y = tf.cast(y, tf.float32)

for i in range(1000):
    optimizer.minimize(individual_loss,[weight,bias])
print("weight,bias")
print(weight,bias)

print("final loss")
final_loss = individual_loss()
print(final_loss)

y_pred = perceptron(x)
y_pred = tf.round(y_pred)

print("accuracy score:")
print(accuracy_score(y,y_pred))

print("confusion matrix:")
print(confusion_matrix(y,y_pred))



