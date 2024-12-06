import numpy as np
from louay_ml_library.base import ActivationFunction

class Sigmoid(ActivationFunction):
    def activation(self, x):
        return 1 / (1 + np.exp(-x))

    def gradient(self, x):
        return (1 / (1 + np.exp(-x))) * (1 - self.output)