import numpy as np
from louay_ml_library.activations import Sign
from louay_ml_library.base import Model

class Perceptron(Model):
    def __init__(self, epochs=500, learning_rate=0.01, activation=Sign()):
        self.epochs = epochs
        self.activation = activation
        self.learning_rate = learning_rate
        self.w = None
    
    def predict(self, x, threshold):
        return self.activation.activation(np.dot(self.w, x.T))
    
    def fit(self, x, y):
        N, features_nb = x.shape
        self.w = np.random.rand(1, features_nb + 1)
        x = np.hstack((np.ones((N, 1)), x))
        y = y.reshape(1, -1)[0]
        for epoch in range(self.epochs):
            for i in range(N):
                y_pred = self.predict(x[i], self.activation)
                self.w += (self.learning_rate*(y[i] - y_pred)*x[i])
        return self.w    