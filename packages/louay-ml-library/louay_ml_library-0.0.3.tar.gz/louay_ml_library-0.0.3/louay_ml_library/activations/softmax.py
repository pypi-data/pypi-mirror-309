import numpy as np
from louay_ml_library.base import ActivationFunction

class Softmax(ActivationFunction):
    def activation(self, x):
        return np.exp(x - np.max(x, axis=1, keepdims=True)) / np.sum(np.exp(x - np.max(x, axis=1, keepdims=True)), axis=1, keepdims=True)

    def gradient(self, x):
        s = np.exp(x - np.max(x, axis=1, keepdims=True)) / np.sum(np.exp(x - np.max(x, axis=1, keepdims=True)), axis=1, keepdims=True)
        return s * (1 - s)