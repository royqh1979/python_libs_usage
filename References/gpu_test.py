import tensorflow as tf

#让tf不要一次性分配所有显存（性能会有影响，但是不容易出现无内存错误）
# physical_devices = tf.config.list_physical_devices('GPU')
# try:
#     tf.config.experimental.set_virtual_device_configuration(
#        physical_devices[0],
#        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*6)])
#     # tf.config.experimental.set_memory_growth(physical_devices[0], True)
# except:
#     # Invalid device or cannot modify virtual devices once initialized.
#     pass

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5, verbose=2)
model.evaluate(x_test, y_test, verbose = 2)
