from sklearn.datasets import fetch_openml
import numpy as np
from neural_network import NeuralNetwork as NN
mnist = fetch_openml('mnist_784', version=1)

images = mnist.data.to_numpy()
y = mnist.target.astype(int).to_numpy()  # Convert to integers

# One-hot encoding
labels = np.eye(10)[y]

# Reshape to (n, 10, 1) if necessary

print(images.shape)  # Should be (70000, 784)
print(labels.shape)

my_nn = NN(784, 10, 15)
print(my_nn.hidden_layer_weights)
my_nn.initialize_data(images, labels, train_amount = .8)
my_nn.train(10)
my_nn.test()
print(my_nn.hidden_layer_weights)


