import numpy as np

class ActivationFunction:
  def __init__(self):
    pass

  def activation(self, x):
    pass

  def activation_prime(self, x):
    pass

  def predict(self, x):
    pass

class Sigmoid(ActivationFunction):
  def __init__(self):
    super().__init__()

  def activation(self, x):
    return 1 / (1 + np.exp(-x))
  
  def activation_prime(self, x):
    sigmoid_output = self.activation(x)
    return sigmoid_output * (1 - sigmoid_output)
  
  def predict(self, x):
    return  1 if self.activation(x) >= 0.5 else -1

class Sign(ActivationFunction):
  def __init__(self):
    super().__init__()

  def activation(self, x):
    return x

  def predict(self, x):
    return 1 if x >= 0 else 0

class Tanh(ActivationFunction):
  def __init__(self):
    super().__init__()

  def activation(self, x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

  def activation_prime(self, x):
    return 1 - self.activation(x)**2

  def predict(self, x):
    return 1 if self.activation(x) >= 0 else -1

class Softmax(ActivationFunction):
  def __init__(self):
    super().__init__()

  def activation(self, x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x, axis=0)
  
  def activation_prime(self, x):
    s = self.activation(x)
    return s * (1 - s)
  
  def predict(self, x):
    return np.argmax(self.activation(x))

class ReLU(ActivationFunction):
  def __init__(self):
    super().__init__()

  def activation(self, x):
    return np.maximum(0, x)
  
  def activation_prime(self, x):
        return np.where(x > 0, 1, 0)

  def predict(self, x):
    return self.activation(x)

class LeakyReLU(ActivationFunction):
  def __init__(self, alpha= 0.01):
    super().__init__()
    self.alpha = alpha

  def activation(self, x):
    return np.maximum(self.alpha * x, x)

  def activation_prime(self, x):
    return np.where(x > 0, 1, self.alpha)

  def predict(self, x):
    return self.activation(x)
