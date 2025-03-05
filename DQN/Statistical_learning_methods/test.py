from sklearn.datasets import fetch_openml
import numpy as np
from neural_network import NeuralNetwork as NN
mnist = fetch_openml('mnist_784', version=1)

images = mnist.data.to_numpy()
labels = mnist.target.to_numpy()
my_nn = NN(images, labels, 30, 10)
my_nn.train(100)


