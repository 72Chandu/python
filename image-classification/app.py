import cv2 as cv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import datasets, models, layers

(training_images, training_labels), (testing_images, testing_labels) = datasets.cifar10.load_data()
training_images, testing_images = training_images / 255.0, testing_images / 255.0

class_names = ['Plane', 'Car','Bird','cat','Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

for i in range(16):
    plt.subplot(4, 4, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(training_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[training_labels[i][0]])
plt.show()  # when run the file it will show the images with labels & low resolution

# # Comment these lines if you want to use the full dataset:
# #Reducing the dataset size , train faster, especially on limited hardware,
# training_images=training_images[:20000] #Selects the first 20,000 training images from the original 50,000.
# training_labels=training_labels[:20000] #Selects the first 20,000 training labels (matching the above images)
# testing_images=testing_images[:4000] # Selects the first 4,000 test images from the original 10,000.
# testing_labels=testing_labels[:4000] #Selects the first 4,000 test labels

# # Create a simple CNN model
# model= models.Sequential()
# model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.Flatten())
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(10, activation='softmax'))

# # Compile and train the model
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels))
# test_loss, test_acc = model.evaluate(testing_images, testing_labels)
# print('accuracy:', test_acc) #accuracy:0.7146000266075134
# print('loss:', test_loss) #loss: loss: 0.883826494216919

# # Save the model
# model.save('image_classifier.keras')

# Load the model
model = tf.keras.models.load_model('image_classifier.keras')

img= cv.imread('deer.jpg')
img= cv.resize(img, (32, 32))  # Resize the image to match the input shape of the model
img= cv.cvtColor(img, cv.COLOR_BGR2RGB)
plt.imshow(img,cmap=plt.cm.binary)
prediction = model.predict(np.array([img / 255.0]))  # Ensure division inside the array
index=np.argmax(prediction)  # Get the index of the highest predicted probability
print('Prediction is :', class_names[index])
plt.show()  # Display the image with the prediction label