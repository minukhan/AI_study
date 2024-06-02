import tensorflow as tf
from tensorflow import keras
assert tf.__version__ >= "2.0"

import tensorflowjs as tfjs

# VGG16 모델 로드 및 저장
vgg16 = keras.applications.VGG16()
tfjs.converters.save_keras_model(vgg16, './public/tfjs-models/VGG16')

# MobileNetV2 모델 로드 및 저장
mobileNetv2 = keras.applications.MobileNetV2()
tfjs.converters.save_keras_model(mobileNetv2, './public/tfjs-models/MobileNetV2')
