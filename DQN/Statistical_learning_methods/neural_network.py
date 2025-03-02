
import matplotlib.pyplot as plt
import numpy as np
import math
class NeuralNetwork:
    def __init__(self, data, prediction, hidden_layer_size, output_layer_size):
        x_rows, x_cols = data.shape
        y_rows, y_cols = prediction.shape
        sample_size = round(x_cols * .8)
        self.x_train, self.x_test = data[:sample_size, :], data[sample_size:, :]
        self.y_train, self.y_test = prediction[:sample_size, :], prediction[sample_size:, :]
        self.hidden_layer_weights = self.create_weights(x_rows, hidden_layer_size)
        self.output_layer_weights = self.create_weights(y_rows, output_layer_size)


    """Creates matrix for weights not transposed, where x: p x N, hidden layer: p x M"""
    def create_weights(self, dim, size):
        return np.random.randint(0, 1, size=(dim + 1,size))

    def sigmoid(self,v):
        return 1 / (1 + (1/(math.e ** v)))

    def train_neural_network(self, r):
        R = []

        for j in range(1,r +1):
            R = []

            for i in range(self.x_train.shape[1]):
                X = self.x_train[:, i]

                Y = self.y_train[:, i]
                Z = self.input_to_hidden(X)
                T = self.hidden_to_output(Z)
                g = self.output_vector(T)
                ga_h = (Y, Z, T, g, X, [])
                R.append(ga_h)
            self.gradient_descent(R)

    def gradient_descent(self, R):

        sum_e = sum(e_T)
        for i in range(len(R)):
            Y, Z, T, g, X = R[i][0], R[i][1], R[i][2], R[i][3], R[i][4]
            e_T = [math.e ** T[i] for i in range(T.shape[0])]

            for l in range(self.output_layer_weights.shape[0]):
                Y, Z, T, g, X = R[i][0], R[i][1], R[i][2], R[i][3], R[i][4]
                e_T = [math.e ** T[i] for i in range(T.shape[0])]
                C = sum(e_T) - e_T[j]
                self.output_layer_weights[l][i] -= -2 * (Y[j] - g[j]) *((C * e_T[j])/((e_T[j] + C)**2)) * self.hidden_layer_weights.shape[j][i] * X[l]

            for j in range(self.hidden_layer_weights.shape[0]):
                C = sum(e_T) - e_T[j]
                self.hidden_layer_weights.shape[j][i] -= -2 * (Y[j] - g[j]) *((C * e_T[j])/((e_T[j] + C)**2)) * Z[j]


    def input_to_hidden(self, X):
        size = self.hidden_layer_weights.shape[1]
        w = self.hidden_layer_weights
        Z = np.zeros((size, 1))
        for i in range(size):
            Z[i] = self.sigmoid(w[0][i] + np.matmul(w[1:, :].transpose(), X))
        return Z

    def hidden_to_output(self, Z):
        size = self.output_layer_weights.shape[1]
        w = self.output_layer_weights
        T = np.zeros((size, 1))
        for i in range(size):
            T[i] = w[0][i] + np.matmul(w[1:, :].transpose(), Z)
        return T
    def output_vector(self, T):
        size = T.shape[0]
        e_T = [math.e ** T[i] for i in range(size)]
        sum_e = sum(e_T)
        g = np.zeros((size, 1))
        for i in range(size):
            g[i] = e_T[i]/sum_e
        return g

    def sum_diff_squared(self, Y, g):
        accum = 0
        for i in range(Y.shape[0]):
            accum += (Y[i] - g[i]) ** 2
        return accum