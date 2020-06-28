# Tool Usage Instructions

First user needs python script for training the model with datasets.

## Example code for usps and cifar :
```python
from __future__ import print_function
import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
import os
from pprint import pprint
import tensorflow as tf
import numpy as np
from keras.models import Model
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

import h5py 
from functools import reduce



batch_size = 32
num_classes = 10
epochs = 100
num_predictions = 20
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'keras_cifar10_trained_model.h5'


(x_train, y_train), (x_test, y_test) = cifar10.load_data()


y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)



x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

x_train /= 255
x_test /= 255



model = Sequential()

conv_layer = Conv2D(6, kernel_size=(5,5), input_shape=(32,32,3),use_bias = False)
model.add(conv_layer)

conv_layer_2 = Conv2D(6, kernel_size=(5,5), input_shape=(28,28,6),use_bias = False)
model.add(conv_layer_2)


conv_layer_3 = Conv2D(6, kernel_size=(5,5), input_shape=(24,24,6),use_bias = False)
model.add(conv_layer_4)

max_pooling_layer = MaxPooling2D(pool_size=(2,2), strides=(1,1))
model.add(max_pooling_layer)

model.add(Flatten()) # Flattening the 2D arrays for fully connected layers


dense_layer= Dense(num_classes,activation="linear",use_bias = False)
model.add(dense_layer)





# initiate RMSprop optimizer
opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

# Let's train the model using RMSprop
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

print(model.summary())

model.fit(x=x_train,y=y_train, epochs=1)
model.evaluate(x_test, y_test)


model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")


```

Then you need to copy this output .h5 and .json file to project file and run below code.

```
python3 oto_generator.py --precision 30
```
This operation will produce test c files for error generation. You can pick precision value for compiling c files. 
İf you have test dataset for prediction error control. You can use test_dataset.py for formatting this network input images for compiling.
