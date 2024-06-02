# 실습과제#11-1my_mnist_model.py
# Python ≥3.5 is required
import sys
assert sys.version_info >= (3, 5)
# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"
# TensorFlow ≥2.0 is required
import tensorflow as tf
from tensorflow import keras
assert tf.__version__ >= "2.0"
# Common imports
import numpy as np
import os
# to make this notebook's output stable across runs
np.random.seed(42)
tf.random.set_seed(42)
# To plot pretty figures
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)
# Where to save the figures
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "deploy"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID)
os.makedirs(IMAGES_PATH, exist_ok=True)
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
 path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
 print("Saving figure", fig_id)
 if tight_layout:
    plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)
print("\n\n##########################################################")
print("Save/Load a SavedModel")
(X_train_full, y_train_full), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train_full = X_train_full[..., np.newaxis].astype(np.float32) / 255.
X_test = X_test[..., np.newaxis].astype(np.float32) / 255.
X_valid, X_train = X_train_full[:5000], X_train_full[5000:]
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
np.random.seed(42)
tf.random.set_seed(42)
model = keras.models.Sequential([
 keras.layers.Flatten(input_shape=[28, 28, 1]),
 keras.layers.Dense(100, activation="relu"),
 keras.layers.Dense(10, activation="softmax")
])
model.summary()
model.compile(loss="sparse_categorical_crossentropy",
 optimizer=keras.optimizers.SGD(learning_rate=1e-2),
 metrics=["accuracy"])
# X_train의 정의를 model.fit() 메서드 바로 다음에 배치합니다.
model.fit(X_train, y_train, epochs=10, validation_data=(X_valid, y_valid))
X_new = X_test[:3]
print("\nnp.round(model.predict(X_new), 2): \n",
 np.round(model.predict(X_new), 2))
print("\nExporting SavedModels: ")
model_version = "0001"
model_name = "my_mnist_model"
model_path = os.path.join(model_name, model_version)
print("\nmodel_path: \n", model_path)
tf.saved_model.save(model, model_path)
for root, dirs, files in os.walk(model_name):
 indent = ' ' * root.count(os.sep)
 print('{}{}/'.format(indent, os.path.basename(root)))
 for filename in files:
    print('{}{}'.format(indent + ' ', filename))
print("\nLet's write the new instances to a npy file so we can pass them easily to our model:")
np.save("my_mnist_tests.npy", X_new)
input_layer = model.layers[0]  # 첫 번째 레이어가 입력 레이어일 것으로 예상됩니다.
input_name = input_layer.name
print("\ninput_name: \n", input_name)