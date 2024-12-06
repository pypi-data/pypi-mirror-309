import numpy as np
from louay_ml_library.base import ActivationFunction

class Tanh(ActivationFunction):
    def activation(self, x):
        return np.tanh(x)

    def gradient(self, x):
        return 1 - np.tanh(x) ** 2