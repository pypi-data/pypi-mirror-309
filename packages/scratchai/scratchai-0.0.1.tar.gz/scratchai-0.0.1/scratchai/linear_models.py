import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class LinearRegression:
    def __init__(self):
        self.w = None
        self.b = None
        self.cost = None
        
    # metrics functions
    def calculate_cost(self, X, y, w, b):
        y_pred = self._predict(X, w, b)
        return (1 / len(y)) * np.sum((y_pred - y) ** 2)
      
    # ploting functions
    def plot_loss_curve(self, losses, epochs):
        plt.figure(figsize = [12, 5])
        plt.plot(epochs, losses)
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.show()
        
    def draw_model(self, X, y):
        y_pred = self._predict(X, self.w, self.b)
        
        plt.figure(figsize = [12, 5])
        plt.scatter(X, y)
        plt.plot(X, y_pred, color = 'red')
        plt.xlabel('X')
        plt.ylabel('y')
        plt.show()
        
    # Training functions
        
    def _predict(self, X, w, b):
        return np.dot(X, w) + b # X shape is (32, 4) - w shape is (4, 1) - resulting shape is (32, 1)
    
    def _gradient_descent(self, X, y, alpha, epochs, batch_size):
        # initialing model params
        w = np.zeros(X.shape[1])
        b = 0
        
        m = len(y)
        
        losses = []
        epochs_list = []
        
        for epoch in range(epochs):
            
            # shuffling the data before each epoch
            data = pd.DataFrame(X)
            data['y'] = y
            data = data.sample(frac = 1).reset_index(drop = True)
            X_shuffled = data.drop('y', axis = 1).values
            y_shuffled = data['y'].values
            
            for batch in range(0, m, batch_size):
                # set the X batch and y batch
                X_batch = X_shuffled[batch : batch + batch_size]
                y_batch = y_shuffled[batch : batch + batch_size]
                y_pred = self._predict(X_batch, w, b)
                
                if X_batch.shape[0] == 0 or y_batch.shape == 0:
                    continue
                
                if X_batch.shape[0] != y_batch.shape[0]:
                    raise ValueError('Mismatch between X_batch and y_batch sizes!')
                
                # calculate the gradient
                dw = (2 / X_batch.shape[0]) * np.dot(X_batch.T, (y_pred - y_batch))
                db = (2 / X_batch.shape[0]) * np.sum(y_pred - y_batch)
                
                # update the model parameters
                w -= alpha * dw
                b -= alpha * db
                
            # Storing the Loss and the epoch after each epoch to plot the loss curve
            loss = self.calculate_cost(X_shuffled, y_shuffled, w, b)
            losses.append(loss)
            epochs_list.append(epoch)
            
        traning_loss = self.calculate_cost(X, y, w, b)
        print(f'Traning completed succesfuly: Traning loss : {traning_loss}')
                
        return w, b, losses, epochs_list
    
    def fit(self, X, y, learning_rate, epochs, batch_size):
        w, b, losses, epochs_list = self._gradient_descent(X, y, learning_rate, epochs, batch_size)
        
        # update the model parameters
        self.w = w
        self.b = b
        
        # plot the loss curve
        self.plot_loss_curve(losses, epochs_list)
        
    def predict(self, X):
        return np.dot(X, self.w) + self.b