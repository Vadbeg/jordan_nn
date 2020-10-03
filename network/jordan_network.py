"""Module with neural network code"""

from typing import List, Union

import numpy as np

from network.utils import sigmoid, sigmoid_der, log, log_der


class Jordan:
    """Jordan network"""

    def __init__(self, lr: float, momentum: float, shape: List[int]):
        self.lr = lr
        self.momentum = momentum

        self.shape = shape

        self.n_layers = len(shape)

        self.layers = self.__init_layers__()
        self.weights = self.__init_weights__()

        self.dw = [0] * len(self.weights)

    def __init_layers__(self) -> List[np.ndarray]:
        """
        Initialize layers of NN

        :return: list of initialized layers
        """

        layers = list()

        layers.append(np.ones(self.shape[0] + self.shape[-1] + 1))

        for i in range(1, self.n_layers):
            layers.append(np.ones(self.shape[i]))

        return layers

    def __init_weights__(self) -> List[np.ndarray]:
        """
        Neural networks he initialization

        :url: https://medium.com/@prateekvishnu/xavier-and-he-normal-he-et-al-initialization-8e3d7a087528
        :return: list of weights
        """

        if len(self.layers) == 0:
            raise ValueError('Before weight initialization, initialize layers!')

        weights = list()

        for i in range(self.n_layers - 1):
            curr_weights = np.random.randn(self.layers[i].size,
                                           self.layers[i + 1].size) + np.sqrt(2 / self.layers[i].size)

            weights.append(curr_weights)

        return weights

    def propagate_forward(self, x: Union[np.ndarray, List]) -> np.ndarray:
        """
        Propagate data in network forward. Forward pass

        :param x: data to propagate
        :return: result of neural network
        """

        self.layers[0][0: self.shape[0]] = x
        self.layers[0][self.shape[0]: -1] = self.layers[-1]

        for i in range(1, len(self.shape)):
            self.layers[i][...] = log(
                np.dot(self.layers[i - 1], self.weights[i - 1])
            )

        return self.layers[-1]

    def propagate_backward(self, target) -> float:
        """
        Performs backpropagation on neural network.

        :param target: desired result
        :param lr: learning rate
        :param momentum: momentum of the NN optimizer
        :return: error of the network
        """

        deltas = list()

        error = target - self.layers[-1]

        last_layer_delta = error * log_der(self.layers[-1])
        deltas.append(last_layer_delta)

        # TODO: add try catch clause here for negative len(self.shape) - 2
        for i in range(len(self.shape) - 2, 0, -1):
            curr_delta = np.dot(deltas[0],
                                self.weights[i].T * log_der(self.layers[i]))

            deltas.insert(0, curr_delta)

        for i in range(len(self.weights)):
            layer = np.atleast_2d(self.layers[i])
            curr_delta = np.atleast_2d(deltas[i])

            curr_dw = np.dot(layer.T, curr_delta)

            self.weights[i] += self.lr * curr_dw + self.momentum * self.dw[i]
            self.dw[i] = curr_dw

        return (error ** 2).sum()


if __name__ == '__main__':
    network = Jordan(lr=0.01, momentum=0.1, shape=[10, 15, 15, 1])

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = network.propagate_forward(x=x)
    error = network.propagate_backward(target=1, )

    print(f'Result: {result}')
    print(f'Error: {error}')
    # print(f'Result dw: {network.dw}')

    # print(x[-2])
    # print(x[len(x) - 2])

