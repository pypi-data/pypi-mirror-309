import unittest
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from tests import test_model
from louay_ml_library.models.linear_regression import LinearRegression

class TestLinearRegression(unittest.TestCase):
    def setUp(self):
        # Create synthetic regression data
        X, y = make_regression(n_samples=100, n_features=2, noise=0.1)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    def test_linear_regression(self):
        model = LinearRegression(degree=1)  # Adjust if your model uses different params
        mse = test_model(model, self.X_train, self.X_test, self.y_train, self.y_test, problem_type='regression')
        self.assertLess(mse, 10)  # Adjust this threshold based on expected performance

