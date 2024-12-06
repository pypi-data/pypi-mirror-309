import numpy as np
# from Optimizers import GradientDescent, SGD, RMS_prop, ADAM
class NonLinearRegression:
  def __init__(self, degree: int, n_iter: int, optimizer ):
    self.n_iter = n_iter
    self.degree = degree
    self.optimizer = optimizer

  def  polynomial_features(self, x):
      for d in range(2, self.degree + 1):
           x = np.hstack((x, x**d))

      self.mean = np.mean(x, axis=0)
      self.std = np.std(x, axis=0)
      x = (x - self.mean) / self.std
      return x

  def fit(self,x,y):
      x_poly = self.polynomial_features(x)
      m, n = x_poly.shape
      self.theta = np.random.rand(1,n+1)
      X = np.hstack((np.ones((m, 1)), x_poly))
      y = y.reshape(1, -1)[0]
      for i in range(self.n_iter):
        y_pred = self._predict(X)
        self.theta = self.optimizer.update(self.theta, X, y)

      if i % 100 == 0:
        loss = self.optimizer.cost_function.loss(y, y_pred)
        print(f'Epoch {i}, Loss: {loss}')

      return self.theta, y_pred

  def _predict(self, x: np.ndarray):
      return np.dot(self.theta, x.T)

  def predict(self, x: np.ndarray):
    x_poly = self.polynomial_features(x)
    m= x_poly.shape[0]
    X = np.hstack((np.ones((m, 1)), x_poly))
    return self._predict(X)
