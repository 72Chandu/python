creating virtual enviroment
(base) D:\python training\image-classification>python -mvenv myenv

# Steps to Select Python Interpreter in VS Code:
Open your project folder in VS Code.
Press Ctrl + Shift + P (or F1) to open the Command Palette.
Type:Python: Select Interpreter
and press Enter.
VS Code will show a list of available Python environments on your system (including conda envs like base, img-env, etc.).

# now activate the enviroment 
(base) D:\python training\image-classification>myenv\Scripts\activate

(myenv) (base) D:\python training\image-classification>
now then install 
pip install matplotlib
pip install tensorflow
pip install opencv-python

# come to original environment: conda deactivate
model = models.Sequential(): you're stacking layers one after the other, in order.

Layer 1 – Conv2D
Conv2D: Applies 32 filters (feature detectors), each of size 3x3, to the input.
activation='relu': ReLU introduces non-linearity.
input_shape=(32, 32, 3): Each input image is 32x32 pixels, with 3 color channels (RGB).

This layer extracts low-level features like edges or colors.

Layer 2 – MaxPooling2D :
model.add(layers.MaxPooling2D((2, 2)))
Reduces the size of the feature map by taking the maximum value in each 2×2 region.
This helps downsample the image, reducing computation and overfitting.
Makes the network more translation-invariant and reduces dimensions.

Layer 3 – Conv2D:
Learns more complex features (like corners or textures).

Layer 4 – MaxPooling2D :
Again reduces feature map size, just like before.

Layer 5 – Conv2D
Layer 6 – Flatten
Converts the 3D feature map (from convolution layers) into a 1D vector so it can be passed to dense (fully connected) layers.

 Layer 7 – Dense (Hidden Layer)
 Fully connected layer with 64 neurons.

Learns non-linear combinations of the features extracted.
Layer 8 – Dense (Output Layer) : model.add(layers.Dense(10, activation='softmax'))

Output layer with 10 neurons, one for each class in CIFAR-10.

Softmax activation converts raw scores into probabilities summing to 1.

| Layer Type   | Output Shape | Purpose                             |
| ------------ | ------------ | ----------------------------------- |
| Conv2D (32)  | (30, 30, 32) | Feature extraction                  |
| MaxPooling2D | (15, 15, 32) | Downsampling                        |
| Conv2D (64)  | (13, 13, 64) | Deeper feature extraction           |
| MaxPooling2D | (6, 6, 64)   | Downsampling                        |
| Conv2D (64)  | (4, 4, 64)   | High-level feature extraction       |
| Flatten      | (1024)       | Flatten to vector                   |
| Dense (64)   | (64)         | Fully connected layer               |
| Dense (10)   | (10)         | Final class probabilities (softmax) |

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

optimizer='adam': Popular optimizer that adapts learning rates during training.

loss='sparse_categorical_crossentropy': Used for integer-labeled multi-class classification.

metrics=['accuracy']: Measures the accuracy during training and validation.

model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels))
Trains the model for 10 epochs on the training data.

validation_data: Data to evaluate model performance after each epoch (but not used for training).


test_loss, test_acc = model.evaluate(testing_images, testing_labels, verbose=2)
Evaluates the final trained model on the testing dataset.

Returns test accuracy and test loss.


model.save('image_classifier.model')
Saves the trained model in a file/folder named 'image_classifier.model'