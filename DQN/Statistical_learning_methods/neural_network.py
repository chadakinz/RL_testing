import matplotlib.pyplot as plt
import numpy as np
import math
from tqdm import tqdm
class NeuralNetwork:
    """Neural Network with one hidden layer"""
    def __init__(self, data_size, classification_size, hidden_layer_size, dec_rate = 1):
        """
        Initialize the weights and hyperparameters of the neural network using arbitrary data size
        """
        self.hidden_layer_weights = np.random.uniform(0, 1, size=(data_size + 1, hidden_layer_size))
        self.output_layer_weights = np.random.uniform(0, 1, size=(hidden_layer_size + 1, classification_size))
        self.dec_rate = dec_rate

    def initialize_data(self, data, classification, train_amount):
        """
        Gives the neural network the data to create the training and testing sets
        """
        x_cols, x_rows = data.shape
        sample_size = round(x_cols * train_amount)
        self.x_train, self.x_test = data[:sample_size, :], data[sample_size:, :]
        self.y_train, self.y_test = classification[:sample_size, :], classification[sample_size:, :]
        self.x_train = self.x_train.T
        self.x_test = self.x_test.T
        self.y_train = self.y_train.T
        self.y_test = self.y_test.T

    def train(self, r):


        for j in tqdm(range(r)):
            for i in range(self.x_train.shape[1]):
                X = self.x_train[:, i]
                Y = self.y_train[:, i]
                Z, A = self.input_to_hidden(X)
                T = self.hidden_to_output(Z)
                g = self.softmax(T)

                dg_dT = np.diag(g/T) - np.outer(g, g/T)
                drel_dA = np.array([1 if x > 0 else 0 for x in A])
                dR_dg = -2/10 * (Y - g)
                S = dg_dT @ dR_dg
                L = np.matmul(self.output_layer_weights[1:], S) * drel_dA

                self.output_layer_weights[1:] -=  (self.dec_rate) * np.matmul(Z[:, np.newaxis], (S[:, np.newaxis].T))
                self.output_layer_weights[0] -= (self.dec_rate) * S

                self.hidden_layer_weights[0] -= (self.dec_rate) * L
                self.hidden_layer_weights[1:] -= (self.dec_rate) * np.matmul(X[:, np.newaxis], L[:, np.newaxis].T)


    def input_to_hidden(self, X):
        """
        Applies weights and biases to the input vector X and returns vector Z = vector reLU(A)
        Returns both Z and A for partial derivative calculations in gradient descent.
        :param X:
        :return: Z, A
        """
        biases = self.hidden_layer_weights[0]
        weights = self.hidden_layer_weights[1:]
        A = biases + (weights.T @ X)
        reLU = np.vectorize(lambda x: np.maximum(0, x))
        Z = reLU(A)
        return Z, A

    def hidden_to_output(self, Z):
        """
        Takes vector Z output from the hidden layer, and outputs vector T.
        """
        biases = self.output_layer_weights[0]
        weights = self.output_layer_weights[1:]
        T = biases + (weights.T @ Z)
        normalize = np.vectorize(lambda x: np.maximum(1, x))
        return normalize(T)
    def softmax(self, T):
        """
        Apply softmax activation to our output vector T and get the distribution of our classification predictions
        as probabilities from [0, 1]. Apply the log function to vector T in order to prevent divergence and
        return vector g.
        """
        exp_T = np.exp(np.log(T))
        return exp_T / np.sum(exp_T)

    def test(self):
        count = 0
        #classifications = [x for x in range(10)]
        for i in range(self.x_test.shape[1]):
            X = self.x_test[:, i]
            Y = self.y_test[:, i]
            Z, A = self.input_to_hidden(X)
            T = self.hidden_to_output(Z)
            g = self.softmax(T)

            #if np.random.choice(classifications, p = g, size = 1)[0] == np.argmax(Y):
            if np.argmax(g) == np.argmax(Y):

                count += 1

        print(f"Accuracy: {count/self.x_test.shape[1]}")