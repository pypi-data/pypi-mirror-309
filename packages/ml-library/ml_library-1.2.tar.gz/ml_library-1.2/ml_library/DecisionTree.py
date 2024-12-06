import numpy as np

class ImpurityMeasure:
  def __init__(self):
    pass

  def update(self, y):
    pass


class Entropy(ImpurityMeasure):
  def __init__(self):
    super().__init__()

  def update(self, y):
    unique_counts = np.bincount(y)
    probabilities = unique_counts / len(y)
    entropy_value = np.sum([p * np.log2(1/p) for p in probabilities if p > 0])
    return entropy_value


class Gini(ImpurityMeasure):
  def __init__(self):
    super().__init__()

  def update(self, y):
    unique_counts = np.bincount(y)
    probabilities = unique_counts / len(y)
    gini_value = np.sum([p * (1-p) for p in probabilities if p > 0])
    return gini_value



class DecisionTreeClassifier:
    def __init__(self, max_depth: int, impurity_measurment, tree=None):
        self.max_depth = max_depth
        self.impurity_measurment = impurity_measurment
        self.tree = None

    def information_gain(self, y, left_y, right_y):
        H_y = self.impurity_measurment.update(y)
        weight_left = len(left_y) / len(y)
        weight_right = len(right_y) / len(y)
        H_y_after_split = weight_left * self.impurity_measurment.update(left_y) + weight_right * self.impurity_measurment.update(right_y)
        return H_y - H_y_after_split

    def score_split(self, X, y, threshold):
        # Calculate the score (information gain) for a given split threshold.

        left_mask = X < threshold
        right_mask = ~left_mask
        left_y, right_y = y[left_mask], y[right_mask]
        return self.information_gain(y, left_y, right_y)

    def split_data(self, X, y, feature_idx, threshold):
        # Split data into left and right branches based on feature and threshold.

        left_mask = X[:, feature_idx] < threshold
        right_mask = X[:, feature_idx] >= threshold
        left_X, left_y = X[left_mask], y[left_mask]
        right_X, right_y = X[right_mask], y[right_mask]
        return left_X, left_y, right_X, right_y

    def find_best_split(self, X, y):
        # Find the best split by checking all features and thresholds.

        best_score = -1
        best_feature, best_threshold = None, None
        for feature_idx in range(X.shape[1]):
            # thresholds = np.unique(X[:, feature_idx]) # Feature by feature
            thresholds = np.unique(X[:, feature_idx][:-1] + X[:, feature_idx][1:]) / 2  # Midpoints
            for threshold in thresholds:
                score = self.score_split(X[:, feature_idx], y,threshold)
                if score > best_score:
                    best_score, best_feature, best_threshold = score, feature_idx, threshold
        return best_feature, best_threshold, best_score

    def decision_tree(self, X, y, depth=1):

        # Stopping condition
        if depth > self.max_depth or len(set(y)) == 1:
            return np.bincount(y).argmax()  # Majority class

        # Find the best split
        feature_idx, threshold, score = self.find_best_split(X, y)

        if feature_idx is None:
            return np.bincount(y).argmax()  # Return majority class if no split improves information gain

        # Split data
        left_X, left_y, right_X, right_y = self.split_data(X, y, feature_idx, threshold)

        # Recursive splitting
        left_branch = self.decision_tree(left_X, left_y, depth + 1)
        right_branch = self.decision_tree(right_X, right_y, depth + 1)

        # Create tree structure
        return {
            'feature_index': feature_idx,
            'threshold': threshold,
            'left': left_branch,
            'right': right_branch
        }

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.tree = self.decision_tree(X, y)

    def predict_one(self, x, tree):
        # Predict the class for a single sample.
        if not isinstance(tree, dict):
            return tree
        feature_idx, threshold = tree['feature_index'], tree['threshold']
        if x[feature_idx] < threshold:
            return self.predict_one(x, tree['left'])
        else:
            return self.predict_one(x, tree['right'])

    def predict(self, X: np.ndarray):
        # Predict classes for multiple samples.
        return np.array([self.predict_one(x, self.tree) for x in X])




class DecisionTreeRegressor:
    def __init__(self, max_depth: int, tree=None):
        self.max_depth = max_depth
        self.tree = None

    def variance_reduction(self, y, left_y, right_y):
        variance_y = np.var(y)
        weight_left = len(left_y) / len(y)
        weight_right = len(right_y) / len(y)
        variance_after_split = (weight_left * np.var(left_y)) + (weight_right * np.var(right_y))
        return variance_y - variance_after_split

    def score_split(self, X, y, threshold):
        left_mask = X < threshold
        right_mask = ~left_mask
        left_y, right_y = y[left_mask], y[right_mask]
        return self.variance_reduction(y, left_y, right_y)

    def split_data(self, X, y, feature_idx, threshold):
        left_mask = X[:, feature_idx] < threshold
        right_mask = X[:, feature_idx] >= threshold
        left_X, left_y = X[left_mask], y[left_mask]
        right_X, right_y = X[right_mask], y[right_mask]
        return left_X, left_y, right_X, right_y

    def find_best_split(self, X, y):
        best_score = -1
        best_feature, best_threshold = None, None
        for feature_idx in range(X.shape[1]):
            thresholds = np.unique(X[:, feature_idx][:-1] + X[:, feature_idx][1:]) / 2  # Midpoints
            for threshold in thresholds:
                score = self.score_split(X[:, feature_idx], y, threshold)
                if score > best_score:
                    best_score, best_feature, best_threshold = score, feature_idx, threshold
        return best_feature, best_threshold, best_score

    def decision_tree(self, X, y, depth=1):
        # Stopping condition
        if depth > self.max_depth or len(y) <= 1:
            return np.mean(y)  # Return the mean value at the leaf node

        # Find the best split
        feature_idx, threshold, score = self.find_best_split(X, y)

        if feature_idx is None or score <= 0:
            return np.mean(y)  # Return the mean value if no split improves variance reduction

        # Split data
        left_X, left_y, right_X, right_y = self.split_data(X, y, feature_idx, threshold)

        # Recursive splitting
        left_branch = self.decision_tree(left_X, left_y, depth + 1)
        right_branch = self.decision_tree(right_X, right_y, depth + 1)

        # Create tree structure
        return {
            'feature_index': feature_idx,
            'threshold': threshold,
            'left': left_branch,
            'right': right_branch
        }

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.tree = self.decision_tree(X, y)

    def predict_one(self, x, tree):
        if not isinstance(tree, dict):
            return tree  # Return the mean value (real number) at the leaf node
        feature_idx, threshold = tree['feature_index'], tree['threshold']
        if x[feature_idx] < threshold:
            return self.predict_one(x, tree['left'])
        else:
            return self.predict_one(x, tree['right'])

    def predict(self, X: np.ndarray):
        return np.array([self.predict_one(x, self.tree) for x in X])



