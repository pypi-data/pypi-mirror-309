from abc import ABC, abstractmethod

class ActivationFunction(ABC):
    @abstractmethod
    def activation(self, x):
        """
        Compute the activation output for the input.
        """
        pass

    @abstractmethod
    def gradient(self, x):
        """
        Compute the derivative of the activation function.
        """
        pass
