import numpy as np
# from .Optimizers import GradientDescent, SGD, RMS_prop, ADAM

class LinearRegression:
  def __init__(self, n_iter: int, optimizer):
    self.n_iter = n_iter
    self.optimizer = optimizer

  def fit(self, x: np.ndarray, y: np.ndarray):
        n_samples, n_features = x.shape
        self.theta = np.random.rand(1, n_features+1)
        X = np.hstack((np.ones((n_samples, 1)), x))
        y = y.reshape(1, -1)[0]
        for i in range(self.n_iter):
          y_pred = self._predict(X)
          self.theta = self.optimizer.update(self.theta, X, y)

          if i % 100 == 0:
            loss = self.optimizer.cost_function.loss(y, y_pred)
            print(f'Epoch {i}, Loss: {loss}')
        return self.theta

  def _predict(self, x: np.ndarray):
    return np.dot(self.theta, x.T)

  def predict(self, x: np.ndarray):
    n_samples= x.shape[0]
    X = np.hstack((np.ones((n_samples, 1)), x))
    return self._predict(X)
