import unittest
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from tests import test_model
from louay_ml_library.models.mlp import Network 

class TestMLP(unittest.TestCase):
    def setUp(self):
        # Create synthetic classification data
        X, y = make_classification(n_samples=100, n_features=2, n_classes=2, random_state=42)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    def test_neural_network(self):
        model = Network(hidden_layer_sizes=(10,), max_iter=1000)
        accuracy = test_model(model, self.X_train, self.X_test, self.y_train, self.y_test, problem_type='classification')
        self.assertGreater(accuracy, 0.85)
