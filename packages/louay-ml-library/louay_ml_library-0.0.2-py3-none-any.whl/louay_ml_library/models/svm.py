import numpy as np
from louay_ml_library.base import Model

class SVM(Model):
    """
    Support Vector Machine (SVM) Classifier.

    This implementation is based on the Sequential Minimal Optimization (SMO) algorithm.
    It supports both linear and RBF (Gaussian) kernels for binary classification.
    """
    def __init__(self, C=1.0, tol=1e-3, max_passes=5, kernel='linear', gamma=1):
        """
        Initializes the SVM classifier.

        Parameters:
            C : float, optional (default=1.0)
                Regularization parameter controlling the trade-off between margin size and classification error.
            kernel : str, optional (default='linear')
                Kernel function type, either 'linear' or 'rbf'.
            tol : float, optional (default=1e-4)
                Tolerance for convergence.
            max_passes: int, optional (default=1000)
                Maximum number of iterations for the SMO algorithm.
            gamma : ('scale', 'auto', or float value), optional (default='scale') 
                Kernel coefficient for 'rbf'.
        """
        self.C = C
        self.tol = tol
        self.max_passes = max_passes
        self.kernel = kernel
        self.gamma = gamma
        self.b = 0
        self.alphas = None
        self.X = None
        self.y = None

    def _kernel_function(self, x1, x2):
        if self.kernel == 'linear':
            return np.dot(x1, x2)
        elif self.kernel == 'rbf':
            return np.exp(-self.gamma * np.linalg.norm(x1 - x2) ** 2)
        else:
            raise ValueError("Unsupported kernel")

    def fit(self, X, y):
        """
        Trains the SVM model using the Sequential Minimal Optimization (SMO) algorithm.

        Parameters:
            X (numpy.ndarray): Input data, where each row is a data point.
            y (numpy.ndarray): Labels corresponding to the data points, where values should be either -1 or 1.

        Returns:
            self: The fitted SVM model.
        """
        self.X = X
        self.y = y
        n_samples, n_features = X.shape
        self.alphas = np.zeros(n_samples)
        if self.gamma == 'scale':
            self.gamma = 1 / (n_features * X.var())
        elif self.gamma == 'auto':
            self.gamma = 1 / n_features
        passes = 0

        while passes < self.max_passes:
            num_changed_alphas = 0

            for i in range(n_samples):
                E_i = self._calculate_error(i)

                if (self.y[i] * E_i < -self.tol and self.alphas[i] < self.C) or (self.y[i] * E_i > self.tol and self.alphas[i] > 0):
                    j = self._select_second_alpha(i, n_samples)
                    E_j = self._calculate_error(j)

                    alpha_i_old, alpha_j_old = self.alphas[i], self.alphas[j]

                    if self.y[i] != self.y[j]:
                        L = max(0, alpha_j_old - alpha_i_old)
                        H = min(self.C, self.C + alpha_j_old - alpha_i_old)
                    else:
                        L = max(0, alpha_i_old + alpha_j_old - self.C)
                        H = min(self.C, alpha_i_old + alpha_j_old)

                    if L == H:
                        continue

                    eta = 2 * self._kernel_function(self.X[i], self.X[j]) - \
                          self._kernel_function(self.X[i], self.X[i]) - \
                          self._kernel_function(self.X[j], self.X[j])

                    if eta >= 0:
                        continue

                    self.alphas[j] -= self.y[j] * (E_i - E_j) / eta
                    self.alphas[j] = np.clip(self.alphas[j], L, H)

                    if abs(self.alphas[j] - alpha_j_old) < 1e-5:
                        continue

                    self.alphas[i] += self.y[i] * self.y[j] * (alpha_j_old - self.alphas[j])

                    b1 = self.b - E_i - \
                         self.y[i] * (self.alphas[i] - alpha_i_old) * self._kernel_function(self.X[i], self.X[i]) - \
                         self.y[j] * (self.alphas[j] - alpha_j_old) * self._kernel_function(self.X[i], self.X[j])

                    b2 = self.b - E_j - \
                         self.y[i] * (self.alphas[i] - alpha_i_old) * self._kernel_function(self.X[i], self.X[j]) - \
                         self.y[j] * (self.alphas[j] - alpha_j_old) * self._kernel_function(self.X[j], self.X[j])

                    if 0 < self.alphas[i] < self.C:
                        self.b = b1
                    elif 0 < self.alphas[j] < self.C:
                        self.b = b2
                    else:
                        self.b = (b1 + b2) / 2

                    num_changed_alphas += 1

            passes = passes + 1 if num_changed_alphas == 0 else 0

    def _calculate_error(self, i):
        return self._decision_function(self.X[i]) - self.y[i]

    def _select_second_alpha(self, i, m):
        j = np.random.randint(0, m)
        while j == i:
            j = np.random.randint(0, m)
        return j

    def _decision_function(self, X):
        return np.sum(self.alphas * self.y * [self._kernel_function(x, X) for x in self.X]) + self.b

    def predict(self, X):
        """
        Predicts the class labels for the input samples.

        Parameters:
            X (numpy.ndarray): Input data of shape (n_samples, n_features).

        Returns:
            numpy.ndarray: Predicted class labels of shape (n_samples,).
        """
        return np.sign([self._decision_function(x) for x in X])