########## mnist.py ##########

# 7/28/2019

'''

This script implements a FFNW on the classic 
MNIST data set

'''
print('Running...'); print('\n')

#########
# Imports
#########

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
print(tf.__version__)

################
# Define dataset
################

'''
Initialize the dataset -->
Dataset of 60,000 28x28 pixel grayscale images of 
the 10 digits, along with a test set of 10,000 images.
'''
mnist = keras.datasets.mnist

'''
x_train, x_test: array of grayscale image data with 
shape (num_samples, 28, 28)

y_train, y_test: array of digit labels 
(integers in range 0-9) with shape 
'''
(train_images, train_labels),(test_images, test_labels) = mnist.load_data()

'''
Each image is mapped to a single label. Since the class 
names are not included with the dataset, store them here 
to use later when plotting the images
'''
class_names = ['0', '1', '2', '3', '4',
               '5', '6', '7', '8', '9']

####################
# Understand dataset
####################

# there are 60,000 images in the training set, with 
# each image represented as 28 x 28 pixels
print('Shape of train_images:', train_images.shape)

# likewise, there are 60,000 labels in the training set:
print('Length of training_labels:', len(train_labels))

# each label is an integer between 0 and 9
print('train_labels:', train_labels)

# there are 10,000 images in the test set. Again, 
# each image is represented as 28 x 28 pixels
print('Shape of test_images:', test_images.shape)

# and the test set contains 10,000 images labels
print('Length of test_labels:', len(test_labels))

# inspect the first image in the training set, you will 
# see that the pixel values fall in the range of 0 to 255
plt.figure()
plt.imshow(train_images[0], cmap = plt.cm.binary)
plt.colorbar()
plt.show()

'''
Scale these values to a range of 0 to 1 before feeding
to the neural network model. For this, we divide the 
values by 255. It's important that the training set and the 
testing set are preprocessed in the same way
'''
train_images = train_images / 255.0
test_images = test_images / 255.0

'''
Display the first 25 images from the training set and 
display the class name below each image. Verify that 
the data is in the correct format and we're ready to 
build and train the network
'''
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

#################
# Build the model
#################

'''
The basic building block of a neural network is the layer. 
Layers extract representations from the data fed into them. 
And, hopefully, these representations are more meaningful 
for the problem at hand
'''
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)), # input layer
    keras.layers.Dense(128, activation=tf.nn.relu), # fully connected hidden layer
    keras.layers.Dense(10, activation=tf.nn.softmax) # output layer
])

'''
 The model's compile step:
- Loss function —This measures how accurate the model 
is during training. We want to minimize this function 
to "steer" the model in the right direction
- Optimizer —This is how the model is updated based 
on the data it sees and its loss function.
- Metrics —Used to monitor the training and testing steps.
We want the accuracy, the fraction of the images that 
are correctly classified
'''
model.compile(optimizer = 'adam',
              loss = 'sparse_categorical_crossentropy',
              metrics = ['accuracy'])

#################
# Train the model
#################

'''
Training the neural network model requires the following steps:
1. Feed the training data to the model—in this example, 
the train_images and train_labels arrays.
2. The model learns to associate images and labels.
3. We ask the model to make predictions about a test set—in 
this example, the test_images array. We verify that the predictions 
match the labels from the test_labels array
4. To start training, call the model.fit method—the model 
is "fit" to the training data
'''
model.fit(train_images, train_labels, epochs=2)

####################
# Evaluate the model
####################

# Compare how the model performs on the test dataset
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test accuracy:', test_acc)

##################
# Make predictions
##################

# With the model trained, we can use it to make predictions 
# about some images.
predictions = model.predict(test_images)

# the model has predicted the label for each image in the 
# testing set. Let's take a look at the first prediction
print('Prediction of the first image in test_images', predictions[0])

'''
prediction is an array of 10 numbers. These describe the "confidence" 
of the model that the image corresponds to each of the 10 different 
digits. We can see which label has the highest confidence value
'''
print('Prediction label for the first image:', np.argmax(predictions[0]))

# We can check the test label to see this is correct
print('Actual label for the first image:', test_labels[0])

# We can graph this to look at the full set of 10 class predictions
def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  
  plt.imshow(img, cmap=plt.cm.binary)
  
  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'
  
  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)
  
  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

# Let's look at the 0th image, predictions, and prediction array
i = 0
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions, test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions,  test_labels)
plt.show()

'''
Let's plot several images with their predictions. Correct 
prediction labels are blue and incorrect prediction labels are 
red. The number gives the percent (out of 100) for the predicted 
label. Note that it can be wrong even when very confident.
'''
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, test_labels)
plt.show()

# Finally, use the trained model to make a prediction about a single image
img = test_images[0]
print('Shape of the test image:', img.shape)

'''
tf.keras models are optimized to make predictions on a 
batch, or collection,of examples at once. So even though 
we're using a single image, we need to add it to a list:
'''
img = (np.expand_dims(img,0)) # add the image to a batch where it's the only member.
print('Shape of the bactch test image:', img.shape)

# Now predict the image
predictions_single = model.predict(img)
print('The predicted confidence array for the image is:', predictions_single)

# display the confidence plot for the predicted image
plot_value_array(0, predictions_single, test_labels)
plt.xticks(range(10), class_names, rotation=45)
plt.show()

# model.predict returns a list of lists, one for each image in the 
# batch of data. Grab the predictions for our (only) image in the batch
prediction_result = np.argmax(predictions_single[0])
print('The predicted label for the image is:', prediction_result)