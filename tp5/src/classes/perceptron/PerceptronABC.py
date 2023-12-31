import random
import sys
from abc import ABC, abstractmethod

import numpy as np

from src.utils.DatasetUtils import DatasetUtils


class PerceptronABC(ABC):
    """
    **IMPORTANT!** In case of using an ``optimization method`` which takes more than one constant coefficient, it MUST
    be configured from the outside. Eg: MomentumO
    """

    def __init__(self, weight_qty: int, learning_rate: float, optimization_method, weights=None, **kwargs):
        self.learning_rate = learning_rate
        if weights is None:
            self.weights = np.array(np.random.uniform(-1, 1, size=(1, weight_qty)))
        else:
            self.weights = np.array(weights)
        self.optimization_method = optimization_method
        self.optimization_method.configure(learning_rate)

    def excitement(self, training_value):
        return np.dot(self.weights, training_value)

    @abstractmethod
    def activation(self, excitement):
        pass

    @abstractmethod
    def error(self, training_set, expected_set):
        pass

    def update_weights(self, diff):
        self.weights = self.weights + diff
        return self.weights

    @abstractmethod
    def compute_deltaw(self, activation_value, training_value, expected_value):
        pass

    def k_cross_validation(self, training_set, expected_set, k, epoch, epsilon):
        if k <= 1 or k >= len(training_set):
            raise ValueError('k must be greater than 1 and lower than the length of the training set')
        # Initialization
        previous_weights = np.array(self.weights)
        training_errors = []
        test_errors = []
        min_error = sys.maxsize
        w_min = None
        i = 0
        j = 0

        # Iterations
        while min_error > epsilon and i < epoch:
            training_copy = np.array(training_set.copy())
            expected_copy = expected_set.copy()

            training_copy, expected_copy, test_set_copy, test_expected_copy = \
                DatasetUtils.k_split_dataset(np.array(training_copy), expected_copy, k, j)
            expected_copy = expected_copy.tolist()
            delta_w = [0.0 for i in range(len(self.weights[0]))]
            for _ in range(0, k):
                mu = random.randint(0, len(training_copy) - 1)
                training_value = training_copy[mu]
                training_copy = np.delete(training_copy, mu, 0)
                expected_value = expected_copy.pop(mu)
                excitement_value = self.excitement(training_value)
                activation_value = self.activation(excitement_value)
                delta_w += self.compute_deltaw(activation_value, np.array(training_value), expected_value)
            w = self.update_weights(delta_w)
            error = self.error(training_set, expected_set)
            if error < min_error:
                min_error = error
                w_min = w

            if j == k-1:
                j = 0
            else:
                j += 1
            i += 1
            previous_weights = np.append(previous_weights, w, axis=0)
            training_errors.append(error)
            test_errors.append(self.error(test_set_copy, test_expected_copy))
        return w_min, i, previous_weights, training_errors, test_errors

    def train(self, training_set, expected_set, test_set, test_expected, batch_amount, epoch, epsilon):
        """ Trains the perceptron until error < epsilon or epoch amount is reached"""
        training_set = np.array(training_set)
        previous_weights = np.array(self.weights)
        training_errors = []
        test_errors = []
        min_error = sys.maxsize
        w_min = None
        i = 0
        while min_error > epsilon and i < epoch:
            training_copy = np.array(training_set.copy())
            expected_copy = expected_set.copy()
            delta_w = [0.0 for i in range(len(self.weights[0]))]
            for _ in range(0, batch_amount):
                mu = random.randint(0, len(training_copy)-1)
                training_value = training_copy[mu]
                training_copy = np.delete(training_copy, mu, 0)
                expected_value = expected_copy.pop(mu)
                excitement_value = self.excitement(training_value)
                activation_value = self.activation(excitement_value)
                delta_w += self.compute_deltaw(activation_value, np.array(training_value), expected_value)
            w = self.update_weights(delta_w)
            error = self.error(training_set, expected_set)
            if error < min_error:
                min_error = error
                w_min = w
            i += 1
            previous_weights = np.append(previous_weights, w, axis=0)
            training_errors.append(error)
            test_errors.append(self.error(test_set, test_expected))
        return w_min, i, previous_weights, training_errors, test_errors

    def test(self, test_set, weights):
        """ Calculates outputs from a test_set using custom weights parameter"""
        original_weights = self.weights.copy()
        self.weights = weights
        activation_values = np.array([])

        for i in range(0, len(test_set)):
            excitement = self.excitement(test_set[i])
            activation_values = np.append(activation_values, self.activation(excitement))

        self.weights = original_weights
        return activation_values
