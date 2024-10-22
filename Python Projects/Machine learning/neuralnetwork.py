import tensorflow as tf
from tensorflow import keras
(train_images,train_labels),(test_images,test_labels) = keras.datasets.mnist.load_data()
train_images=train_images.reshape((60000,784)).astype('float32')/255
test_images=test_images.reshape((10000,784)).astype('float32')/255
model = keras.Sequential([
    keras.layers.Dense(128, activation= 'relu', input_shape=(784,)),
    keras.layers.Dense(10, activation = 'softmax')
])
model.compile(optimizer='adam',
              loss = 'sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_images,train_labels, epochs=5)
test_loss,test_accuracy = model.evaluate(test_images,test_labels)
print(f"Test accuracy:{test_accuracy:.4f}")
