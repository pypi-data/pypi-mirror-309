import numpy as np
from .CostFunctions import MSE, MAE, CrossEntropy
class Optimizer:
  def __init__(self,learning_rate: int, cost_function: str = "MSE, MAE"):
    self.learning_rate = learning_rate
    if cost_function == "MSE":
      self.cost_function = MSE()
    elif cost_function == "MAE":
      self.cost_function = MAE()
    elif cost_function == "CrossEntropy":
      self.cost_function = CrossEntropy()
    else :
      raise ValueError(f"Unknown cost function: {cost_function}")

  def update(theta,x,y):
    pass

class GradientDescent(Optimizer):
  def __init__(self,learning_rate: int, cost_function: str ="MSE, MAE"):
    super().__init__(learning_rate ,cost_function)

  def update(self, theta, x,y):
    theta = theta - self.learning_rate * self.cost_function.gradient(x,y,np.dot(theta, x.T))
    return theta

class SGD(Optimizer):
  def __init__(self,learning_rate: int, momentum: float, cost_function: str ="MSE, MAE"):
    super().__init__(learning_rate, cost_function)
    self.momentum = momentum

  def update(self,theta,x,y):
      n_features = x.shape[1]
      self.V = np.zeros((1, n_features))
      for i in range(len(x)):
        self.V = self.momentum * self.V + (1 - self.momentum) * self.cost_function.gradient(x[i,:].reshape(1,-1), y[i], np.dot(theta, x[i,:].reshape(1,-1).T))
        theta = theta - self.learning_rate * self.V
      return theta

class RMS_prop(Optimizer):
  def __init__(self, learning_rate: int, beta: float = 0.99, epsilon: float = 1e-8, cost_function: str="MSE, MAE"):
    super().__init__(learning_rate, cost_function)
    self.beta = beta
    self.epsilon = epsilon

  def update(self,theta,x,y):
    n_features = x.shape[1]
    self.S = np.zeros((1, n_features))
    for i in range(len(x)):
      self.S = self.beta * self.S + (1 - self.beta) * self.cost_function.gradient(x, y, np.dot(theta,x.T))**2
      theta = theta - self.learning_rate * self.cost_function.gradient(x, y, np.dot(theta,x.T)) / (np.sqrt(self.S) + self.epsilon)
    return theta

class ADAM(Optimizer):
  def __init__(self,learning_rate: int, beta1: float = 0.9, beta2: float=0.99, epsilon: float = 1e-8, cost_function: str ="MSE, MAE"):
    super().__init__(learning_rate, cost_function)
    self.beta1 = beta1
    self.beta2 = beta2
    self.epsilon = epsilon

  def update(self,theta,x,y):
    n_features = x.shape[1]
    self.V = np.zeros((1, n_features))
    self.S = np.zeros((1, n_features))
    
    t=0
    for i in range(len(x)):
      t+=1
      self.V = self.beta1 * self.V + (1 - self.beta1) * self.cost_function.gradient(x, y, np.dot(theta,x.T))
      self.S = self.beta2 * self.S + (1 - self.beta2) * self.cost_function.gradient(x, y, np.dot(theta,x.T))**2
      V_hat = self.V / (1 - self.beta1**t)
      S_hat = self.S / (1 - self.beta2**t)
      theta = theta - self.learning_rate * V_hat / (np.sqrt(S_hat) + self.epsilon)
    return theta