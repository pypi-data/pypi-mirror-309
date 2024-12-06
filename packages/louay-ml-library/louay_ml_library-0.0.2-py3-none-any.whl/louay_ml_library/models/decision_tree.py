import numpy as np
from louay_ml_library.base import Model

class DecisionTree(Model):
    def __init__(self, max_depth):
        """
        Initializes the decision tree model with a specified max depth.
        Parameters:
            max_depth (int): The maximum depth of the tree.
        """
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        """
        Fit the decision tree model to the training data.
        Parameters:
            X (np.ndarray): The input features (2D array where each row is a sample).
            y (np.ndarray): The target labels (1D array with corresponding labels).
        """
        self.tree = self._build_tree(X, y, depth=0)
        return self

    def _build_tree(self, X, y, depth: int):
        n_labels = len(np.unique(y))
        if depth == self.max_depth or n_labels == 1:
            leaf_value = np.bincount(y).argmax()
            return leaf_value

        best_feature, best_threshold = self._find_best_split(X, y)
        left_indices = X[:, best_feature] < best_threshold
        right_indices = ~left_indices
        
        left_subtree = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_subtree = self._build_tree(X[right_indices], y[right_indices], depth + 1)
        
        return (best_feature, best_threshold, left_subtree, right_subtree)                    

    def _find_best_split(self, X, y):
        best_gain = -1
        best_feature = None
        best_threshold = None
        n_features = X.shape[1]
        
        for i in range(n_features):
            thresholds = np.unique(X[:, i]) 
            for t in range(len(thresholds)-1):
                threshold = np.mean([thresholds[t], thresholds[t+1]])
                left_indices = X[:, i] < threshold
                right_indices = ~left_indices
                gain = self._information_gain(y, y[left_indices], y[right_indices])
                if gain > best_gain:
                    best_gain = gain
                    best_feature = i
                    best_threshold = threshold
        
        return best_feature, best_threshold
    
    def _entropy(self, y):
        _, counts = np.unique(y, return_counts=True)
        prob = counts / len(y)
        return np.sum(-prob * np.log2(prob + 1e-9))
    
    def _information_gain(self, y, left_y, right_y):
        return self._entropy(y) - (len(left_y) / len(y)) * self._entropy(left_y) - (len(right_y) / len(y)) * self._entropy(right_y)
    
    def predict(self, X):
        """
        Predicts the target labels for the input data.
        Parameters:
            X (np.ndarray): The input data to make predictions on.
        Returns:
            predictions (np.ndarray): The predicted labels.
        """
        predictions = [self._predict_one(sample, self.tree) for sample in X]
        return np.array(predictions)

    def _predict_one(self, x, tree):
        if isinstance(tree, int):
            return tree
        
        feature, threshold, left_subtree, right_subtree = tree
        
        if x[feature] < threshold:
            return self._predict_one(x, left_subtree)
        else:
            return self._predict_one(x, right_subtree)
