import numpy as np
from louay_ml_library.base import Model
from louay_ml_library.utils import xavier_init_normal
from louay_ml_library.utils import create_batches

class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input):
        raise NotImplementedError
    
    def backward(self, output_gradient):
        raise NotImplementedError
    
class DenseLayer(Layer):
    def __init__(self, input_size, output_size):
        self.weights = xavier_init_normal(input_size, output_size)
        self.bias = np.zeros((output_size, 1))
        self.grad_weights = None
        self.grad_bias = None

        self.v_w = np.zeros_like(self.weights)
        self.v_b = np.zeros_like(self.bias)

        self.s_w = np.zeros_like(self.weights)
        self.s_b = np.zeros_like(self.bias)

    def forward(self, input):
        self.input = input
        return np.dot(self.weights, self.input) + self.bias
    
    def backward(self, output_gradient):
        self.grad_weights = np.dot(output_gradient, self.input.T)
        self.grad_bias = output_gradient
        return np.dot(self.weights.T, output_gradient)
    
class ActivationLayer(Layer):
    def __init__(self, activation_fn):
        self.activation_fn = activation_fn

    def forward(self, input):
        self.input = input
        return self.activation_fn.activation(self.input)
    
    def backward(self, output_gradient):
        return self.activation_fn.gradient(self.input) * output_gradient

class Network(Model):
    def __init__(self, optimizer, batch_size=1, epochs=1000):
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.epochs = epochs
        self.layers = []
        self.loss_fn = None

    def add(self, layer):
        self.layers.append(layer)

    def use(self, loss_fn):
        self.loss_fn = loss_fn

    def forward(self, input):
        output = input
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def backward(self, grad):
        for layer in reversed(self.layers):
            grad = layer.backward(grad)

    def predict(self, X):
        predictions = []
        for x in X:
            output = x
            for layer in self.layers:
              output = layer.forward(output)
            predictions.append(output)
        return predictions
    
    def fit(self, X, Y):
        batches = create_batches(X, Y, self.batch_size)
        for epoch in range(self.epochs):
          error = 0
          for batch in batches:
            x_batch, y_batch = batch
            x_batch, y_batch = x_batch[0], y_batch[0]
            output = self.forward(x_batch)

            batch_error = self.loss_fn.compute_loss(y_batch, output)
            error += batch_error
        
            grad = self.loss_fn.gradient(y_batch, output)
            self.backward(grad)
            self.optimizer.step(self._parameters())

          # Average error over the entire epoch
          error /= len(batches)

          if epoch % 10 == 0:
              print(f"Epoch {epoch}, error {error}")
    
    def _parameters(self):
        return [layer for layer in self.layers if isinstance(layer, DenseLayer)]