import numpy as np

class CostFunction:
  def __init__(self):
    pass

  def loss(self, y, y_pred):
    pass

  def loss_prime(self, y, y_pred):
    pass

  def gradient(self, x, y, y_pred):
    pass

class MSE(CostFunction):
  def __init__(self):
    super().__init__()

  def loss(self, y, y_pred):
    return np.mean((y-y_pred)**2)

  def loss_prime(self, y, y_pred):
    return 2*(y_pred-y)/y.size


  def gradient(self, x, y, y_pred):
    m = x.shape[0]
    return -(2/m) * np.dot((y.T - y_pred), x)

class MAE(CostFunction):
  def __init__(self):
    super().__init__()

  def loss(self, y, y_pred):
    return np.mean(np.abs(y-y_pred))

  def loss_prime(self, y, y_pred):
    return np.sign(y_pred - y) / y.size


  def gradient(self, x, y, y_pred):
    m = x.shape[0]
    return -(1/m) * np.dot((y.T - y_pred), x)


class CrossEntropy(CostFunction):
  def __init__(self):
    super().__init__()

  def loss(self, y, y_pred):
    y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
    loss = -np.mean(np.sum(y * np.log(y_pred), axis=1))
    return loss

  def loss_prime(self, y, y_pred):
    y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
    return (y_pred - y) / y.shape[0]

  def gradient(self, x, y, y_pred):
    y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
    gradient = -np.dot(x.T, (y - y_pred)) / y.shape[0]  
    return gradient
