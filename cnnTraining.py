import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from glob import glob
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


IMG_H = 28
IMG_W = 28
IMG_C = 1

np.random.seed(1)


def preprocess(dataset, batch_size=32):
    dataset = dataset.shuffle(buffer_size=10000)
    dataset = dataset.batch(batch_size)
    dataset = dataset.cache().prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    return dataset


def load_image(path):
    img = tf.io.read_file(path)
    img = tf.io.decode_png(img)
    img = tf.image.resize_with_crop_or_pad(img, IMG_H, IMG_W)
    img = tf.cast(img, tf.float32)
    return img


def make_dataset(paths, label):
    paths = glob(paths + "/*")
    paths = tf.convert_to_tensor(paths, dtype=tf.string)
    paths = tf.data.Dataset.from_tensor_slices(paths)

    img = paths.map(load_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    label = tf.convert_to_tensor(label, dtype=tf.float32)
    label = tf.data.Dataset.from_tensor_slices(label)
    dataset = tf.data.Dataset.zip((img, label))
    return dataset


def CNN(size):
    model = keras.Sequential(
        [
            layers.InputLayer(input_shape=(IMG_H, IMG_W, IMG_C)),
            layers.Conv2D(24, 9),
            layers.ReLU(),
            layers.MaxPool2D(),
            layers.Flatten(),
            layers.Dense(size),
            layers.Softmax(),
        ]
    )

    model.compile(
        loss=keras.losses.CategoricalCrossentropy(),
        optimizer="adam",
        metrics=["accuracy"],
    )
    return model


image_path = glob("dataForTrainingbn/upper/*")
labels = [i.split("\\")[-1] for i in image_path]
one_hot = []
for i in range(len(labels)):
    a = np.zeros((len(labels),))
    a[i] = 1
    one_hot.append(a)
Labels = {i: j for i, j in zip(labels, one_hot)}


dataset = make_dataset(image_path[0], np.array([Labels[labels[0]]] * 714))
# print(len(list(dataset.as_numpy_iterator())))

for i, path in enumerate(image_path[1:]):
    tmp = make_dataset(path, np.array([Labels[labels[i + 1]]] * 714))
    dataset = dataset.concatenate(tmp)

# print(len(list(dataset.as_numpy_iterator())))
dataset = preprocess(dataset)
baseBottom = 38 * 714
upper = 14 * 714

split = 0.9
size = int(upper / 32 * split)

train_data, valid_data = dataset.take(size), dataset.skip(size)

model = CNN(len(labels))
model.summary()
print(len(list(dataset.as_numpy_iterator())))
history = model.fit(train_data, epochs=5, validation_data=valid_data)


model.save("convnetUpper.h5")
