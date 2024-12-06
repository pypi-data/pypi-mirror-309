import numpy as np
class MLPOptimizer:
  def __init__(self,learning_rate):
    self.learning_rate = learning_rate

  def update(weights_error, output_error, weights, bias, V, S, t = None ):
    pass

class SGD(MLPOptimizer):
  def __init__(self, learning_rate: int, momentum: float = 0.9):
    super().__init__(learning_rate)
    self.momentum = momentum


  def update(self, weights_error, output_error, weights, bias, V, S, t= None ):
        V = self.momentum * V + (1 - self.momentum) * weights_error
        weights -= self.learning_rate * V
        bias -= self.learning_rate * output_error
        return weights, bias, V, S


class RMS_prop(MLPOptimizer):
  def __init__(self, learning_rate: int, beta: float = 0.99, epsilon: float = 1e-8):
    super().__init__(learning_rate)
    self.beta = beta
    self.epsilon = epsilon

  def update(self, weights_error, output_error, weights, bias, V, S, t=None):
          S = self.beta * S + (1 - self.beta) * weights_error**2
          weights -= self.learning_rate * weights_error / (np.sqrt(S) + self.epsilon)
          bias -= self.learning_rate * output_error
          return weights, bias, V, S

class ADAM(MLPOptimizer):
  def __init__(self, learning_rate: int, beta1: float = 0.9, beta2: float = 0.99, epsilon: float = 1e-8):
    super().__init__(learning_rate)
    self.learning_rate = learning_rate
    self.beta1 = beta1
    self.beta2 = beta2
    self.epsilon = epsilon

  def update(self, weights_error, output_error, weights, bias, V, S, t ):
          V = self.beta1 * V + (1 - self.beta1) * weights_error
          S = self.beta2 * S + (1 - self.beta2) * weights_error**2
          V_hat = V / (1 - self.beta1**t)
          S_hat = S / (1 - self.beta2**t)
          weights -= self.learning_rate * V_hat / (np.sqrt(S_hat) + self.epsilon)
          bias -= self.learning_rate * output_error
          return weights, bias, V, S