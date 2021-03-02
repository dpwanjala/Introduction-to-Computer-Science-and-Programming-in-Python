# Final Project CP
# Name: David Paul Wanjala
# Collaborators:
# Time Spent:
# PROJECT - image classification with an artificial neural network


# 1. we first import tensorflow and keras
import os
import tensorflow as tf
from tensorflow import keras

# we will use matplotlib to give us a visual insight into our datasets
# -> % matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


root_logdir = os.path.join(os.curdir, "my_logs")
def get_run_logdir():
    import time
    run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return os.path.join(root_logdir, run_id)

run_logdir = get_run_logdir()

# 2. we will utilize keras utility function to fetch and load common datasets. this project
# will work with the popular fashion MNIST database. This dataset includes 70,000 grayscale
# images of 28 × 28 pixels each, with 10 classes ranges from Trousers to Boots and T-shirts

fashion_mnist_dataset = keras.datasets.fashion_mnist

# This is a dataset of 60,000 28x28 grayscale images of 10 fashion categories, along with a test set of 10,000 images
# Returns a tuple of numpy array that we assign to variables X_train_full, y_train_full, x_test, and y_test
# Note that each pixel intensity is represented as a byte (0 to 255)

(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist_dataset.load_data()
# each image is represented as a 28 by 28 array rather than a 1D array of size 784
# the pixel intensities are represented as integers from 0 to 255 rather than floats.


# we are further going to split the provided X_train_full into a smaller training set (55k) and a
# validation set (5K) (these will be useful later when we measure the performance of our model)
# we will be using gradient descent approach to train our model and thus must also pixel intensities
# down to the 0-1 range by dividing them by 255.0 which also converts them into floats

X_valid, X_train = X_train_full[:5000] / 255., X_train_full[5000:] / 255.
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.

# fashion_class_names associated with different label indices for our fashion items in the dataset
fashion_class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

# Let us look at one of the examples in our training set by plotting it using imshow() from matplotlib library
plt.imshow(X_train[3], cmap="binary")
# we can see the corresponding fashion_class_name / label by indexing the fashion_class_namess list
# with the label value for a given example this way:
# fashion_class_names[y_train[3]]
plt.axis('off')
plt.show()

# let us look at a sample of the images in the dataset
n_rows = 4
n_cols = 10
plt.figure(figsize=(n_cols * 1.2, n_rows * 1.2))
for row in range(n_rows):
    for col in range(n_cols):
        index = n_cols * row + col
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(X_train[index], cmap="binary", interpolation="nearest")
        plt.axis('off')
        plt.title(fashion_class_names[y_train[index]], fontsize=12)
plt.subplots_adjust(wspace=0.2, hspace=0.5)
# save_fig('fashion_mnist_plot', tight_layout=False)
plt.show()


# we can create a classification mlp with two hidden layers as follows

# strategy 1. first, we create a Sequential model which is basically creating an object of the class Sequential that
# is provided by keras. This model consists of a single stack of layers connected sequentially, a sequential API 2.
# we build a first layer of our neural network and add it to the model. this is a Flatten layer whose role is to
# convert each input image into a 1D array: if it receives input data X, it computes X.reshape(-1, 1) and has no
# parameters. input_shape tells it the shape of the instances to use as it does the preprocessing
# 3. we add a dense layer with 300 neurons, it will use the relu activation function. the layer manages
# its own weight matrix, containing all the connection weights between the neurons and their inputs. it also manages
# vector of bias terms (one per neuron). and computes ...-> this function when it receives some
# input data.
# 4. a second dense layer with 100 neurons with a relu activation function
# 5. we add an output dense layer with 10 neurons (one per class i.e "Coat", and softmax activation
# function because the classes are exclusive.

# 1.
model = keras.models.Sequential()
# 2.
model.add(keras.layers.Flatten(input_shape=[28, 28]))
# 3.
model.add(keras.layers.Dense(300, activation="relu"))
# 4.
model.add(keras.layers.Dense(100, activation="relu"))
# 5.
model.add(keras.layers.Dense(10, activation="softmax"))

# model.summary()
# hidden1 = model.layers[1]
# weights, biases = hidden1.get_weights()
# weights
# biases

# after we have created the model, we now call its compile() to specify a loss function and the
# optimizer to use.

# a) first we use the "sparse_categorical_crossentropy" loss because we have sparse labels and the classes are
# exclusive as opposed to to other such as "categorical_crossentropy", or "binary_crossentropy" which would have been
# useful if we were doing binary classification
# b) we are using a simple stochastic gradient descent algorithm to train the model. this will enable keras to perform
# the backpropagation algorithm (i.e., reverse-mode autodiff plus Gradient Descent).
# c) we will measure the accuracy of this model during training and evaluation
model.compile(loss="sparse_categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])


tensorboard_cb = keras.callbacks.TensorBoard(run_logdir)

# the model is ready to train
# fit we need to call its fit() method and pass it the input features (X_train) and target classes (y_train),
# number of epochs to train, optional validation set,

history = model.fit(X_train, y_train, epochs=30, validation_data=(X_valid, y_valid), callbacks=[tensorboard_cb])
#
# neural network is now trained.

# let us save our model
model.save("fashion_classifier_keras_model.h5")

# let us plot the learning curves
pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1) # set the vertical range to [0-1]
plt.show()

# let us evaluate our model on training set to estimate the generalization error
# we will do this using the evaluate() method

model.evaluate(X_test, y_test)

# let us use the model to make a prediction
# we will do this using the predict() method
# since we don't have actual new instances, we will just use first 3 instances of test data
# for each instance, our model estimates one probability per class, from class 0 to 9.
X_new = X_test[:3]
y_probability = model.predict(X_new)
y_probability.round(2)

# if we only care about the class with highest estimated probability even if that is quite low,
# we will use predict_class() method

# y_pred = model.predict_classes(X_new)
# y_pred

#visualize the predictions
plt.imshow(X_test[0], cmap="binary")
plt.axis('off')
plt.show()




# when needing to use later
# model = keras.models.load_model("my_keras_model.h5")


