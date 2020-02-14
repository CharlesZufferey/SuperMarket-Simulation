# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 09:43:15 2020

@author: Charles
"""

# Gradient Boosting
#1. Get Data
#2. Get initial prediction first ("bad first guess")
#3. We need a loss function (mean square error for example)
#4. Visualize the loss (recap of gradients)
#5. Calculate the gradient (derivative of the loss function)
#6. Calculate the pseudo-residuals (its basically the gradient)
#7. Train our first weak tree
#8. make next prediction
#9. put it all in a loop / function
#10. Make final prediction

#%%

#1. Get Data
from sklearn.datasets import load_boston
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%%
boston = load_boston()
x = boston.data
y = boston.target

#%% 2. Bad First Guess
y_hat = np.array([y.mean()]*len(y)) #predicting the mean for every single value
#%%
plt.figure(figsize=(12,8))
plt.plot(y)
plt.plot(y_hat)
#%% 3. Loss function
def compute_loss(y,y_hat):
    """y and y_hate are single points"""
    return (y-y_hat)**2/2

loss = compute_loss(y,y_hat).mean() # the loss is around root(42*2) = around 9k
    
#%% 4. Visualize loss
plt.scatter(y_hat[0],compute_loss(y[0],y_hat[0])) #loss for first point
# plot a curve that will calculate the loss from 2 and -2 of that point:
losses = []
for i in range(-200,200):
    losses.append(compute_loss(y[0],y_hat[0]+i/100))

plt.plot(y_hat[0] + np.arange(-2,2,0.01),losses) # we want now to calculate the slope 
# of the point, so lets put another point:
plt.scatter(y_hat[0]+1,compute_loss(y[0],y_hat[0]+1)) #small step
plt.scatter(y_hat[0]+0.5,compute_loss(y[0],y_hat[0]+0.5)) #smaller step
plt.scatter(y_hat[0]+0.1,compute_loss(y[0],y_hat[0]+0.1)) #even smaller step
#%% calculation of the slope
delta_x = 0.1
delta_y = compute_loss(y[0],y_hat[0]+0.1) - compute_loss(y[0],y_hat[0] )

slope = delta_y / delta_x


#%% 5. In order to have this for every point we will use the derivative
def loss_gradient(y,y_hat):
    return y_hat-y

grad = loss_gradient(y,y_hat)
#%% 6. Pseudo Residuals - basically the negative of the gradient
pseudo_residuals = -loss_gradient(y,y_hat)

#%% 7 train first tree
from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor(max_depth = 1)
#%%
ft = regressor.fit(x,pseudo_residuals)
print(ft)
#%%
from sklearn.tree import export_graphviz
import graphviz 
tree = export_graphviz(regressor, impurity = False, filled = True)
open("boston.jpg","w").write(tree)
graph = graphviz.Source(tree)
print(graph)
#%%
y1 = y_hat + regressor.predict(x)
plt.figure(figsize = (12,8))
plt.plot(y)
plt.plot(y_hat)
plt.plot(y1)
plt.legend(['real values','mean','newest prediction'])
#%% check the new loss
cl = compute_loss(y,y1).mean() #around 23
#%% Second iteration of the tree
pseudo_residuals = -loss_gradient(y,y1) # not y_hat, but y1
regressor.fit(x,pseudo_residuals)
y2 = y1+regressor.predict(x)
cl = compute_loss(y,y2).mean() #around 16
#%% lets put this into a loop
def gradient_boosted_mse(X,y,n):
    
    """gradient boosted tree algorythm """
    regressors = []
    y_hat = np.array([y.mean()] * len(y))
    y0 = y_hat[0]
    for i in range(n):
        #calculate pseudo residual
        pseudo_residuals = -loss_gradient(y,y_hat)
        #train a tree
        regressor = DecisionTreeRegressor(max_depth = 100)
        # fit it
        regressor.fit(X,pseudo_residuals)
        #add latest tree to a list
        regressors.append(regressor)
        y_hat = y_hat + regressor.predict(X)
        print(compute_loss(y,y_hat).mean())
    
    return regressors,y0


#%%

#%%10.  make final prediction, use train test split
from sklearn.model_selection import train_test_split
X_train, X_test,y_train,y_test = train_test_split(x,y,random_state=42)
#%%
#%%
def gb_predict(regressors,y0,X_test):
    y_hat = np.array([y0]*len(X_test))
    for r in regressors:
        y_hat = y_hat + r.predict(X_test)
    return y_hat # the final predicted array of housing prices

#%% train
r,y0 = gradient_boosted_mse(X_train,y_train,100)
#predict
y_final = gb_predict(r,y0,X_test)
#%%
print(compute_loss(y_test,y_final).mean())
#
