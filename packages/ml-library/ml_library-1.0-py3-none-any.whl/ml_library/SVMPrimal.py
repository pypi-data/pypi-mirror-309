import numpy as np

class SVM_Primal:
    def __init__(self, learning_rate: float = 0.01, lambda_param: float = 0.01, n_iters: int = 1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        y_ = np.where(y <= 0, -1, 1)

        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    self.w -= self.lr * (2 * self.lambda_param * self.w) #L2 regularization

                else:
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx]))
                    self.b -= self.lr * y_[idx]

    def predict(self, X):
        approx = np.dot(X, self.w) - self.b     #linear decision function: w * X - b
        return np.sign(approx)

    def hinge_loss(self, X, y):

        distances = 1 - y * (np.dot(X, self.w) + self.b)
        hinge_loss = np.maximum(0, distances)
        return np.mean(hinge_loss) + self.lambda_param * np.dot(self.w, self.w)  # Soft margin loss with regularization