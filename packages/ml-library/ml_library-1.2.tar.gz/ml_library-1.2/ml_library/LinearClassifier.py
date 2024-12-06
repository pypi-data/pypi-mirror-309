import numpy as np
# from ActivationFunctions import Sigmoid, Sign, Tanh, Softmax
class LinearClassifier:
  def __init__(self, learning_rate: float, n_iter: int , activation_function):
    self.learning_rate = learning_rate
    self.n_iter = n_iter
    self.activation_function = activation_function
    self.theta= None

  def fit(self, x: np.ndarray, y: np.ndarray):
    m, n_features = x.shape
    X = np.hstack((np.ones((m, 1)), x))
    self.theta = np.random.rand(1,n_features+1)
    for _ in range(self.n_iter):
        for i in range(m):
            z = np.dot(self.theta,X[i].T)
            y_pred = self.activation_function.predict(z)
            self.theta = self.theta + (self.learning_rate * (y[i] - y_pred) * X[i]) 
    return self.theta
  
  def predict (self, x):
    X = np.hstack((np.ones((x.shape[0], 1)), x))  
    predictions = []  
    for i in range(x.shape[0]):
        z = np.dot(self.theta, X[i].T)  
        prediction = self.activation_function.predict(z)  
        predictions.append(prediction)  
    return predictions

  

