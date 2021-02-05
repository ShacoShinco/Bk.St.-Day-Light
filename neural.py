import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from grabber import ChatBoxGrabber
import pickle
import numpy as np

inputs = keras.Input(shape=(784,), name="message")
x = layers.Dense(64, activation="relu", name="dense_1")(inputs)
x = layers.Dense(64, activation="relu", name="dense_2")(x)
outputs = layers.Dense(10, activation="softmax", name="user")(x)

model = keras.Model(inputs=inputs, outputs=outputs)


a = ChatBoxGrabber()
a.dataSet = pickle.load(open('data.pickle', 'rb'))

x_train = [data.message for data in a.dataSet.values()]
y_train = [data.user for data in a.dataSet.values()]

# Reserve 10,000 samples for validation
x_val = x_train[-10000:]
y_val = y_train[-10000:]
x_train = x_train[:-10000]
y_train = y_train[:-10000]

train = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(64).shuffle(buffer_size=1024)
test = tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(64)

model.compile(
    optimizer=keras.optimizers.RMSprop(),  # Optimizer
    # Loss function to minimize
    loss=keras.losses.SparseCategoricalCrossentropy(),
    # List of metrics to monitor
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)


print("Fit model on training data")
history = model.fit(
    x_train,
    epochs=2,
    batch_size=64,
    steps_per_epoch=100,
    # We pass some validation for
    # monitoring validation loss and metrics
    # at the end of each epoch
    validation_data=(x_val, y_val),
)

# You can also evaluate or predict on a dataset.
print("Evaluate")
result = model.evaluate(test)
dict(zip(model.metrics_names, result))
