#关掉GPU
# import os
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"

import tensorflow as tf

#限制GPU使用内存
# physical_devices = tf.config.list_physical_devices('GPU')
# try:
#     tf.config.experimental.set_virtual_device_configuration(
#        physical_devices[0],
#        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*6)])
#     # tf.config.experimental.set_memory_growth(physical_devices[0], True)
# except:
#     # Invalid device or cannot modify virtual devices once initialized.
#     pass

minst = tf.keras.datasets.mnist
(x_train, y_train) , (x_test, y_test) = minst.load_data()

x_train = x_train / 255.0
x_test = x_test / 255.0

digit = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28)),
    tf.keras.layers.Dense(10, activation = tf.nn.softmax)
])

digit.compile(optimizer='adam', loss='sparse_categorical_crossentropy',metrics=['accuracy'])

digit.fit(x_train,y_train,epochs=100, batch_size=60000)

digit.evaluate(x_test,y_test)

