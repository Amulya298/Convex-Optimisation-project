# -*- coding: utf-8 -*-
"""cvxy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e4YDklQyEzlgXdYJYVBnV6eA1BsDCRpj
"""

import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

# Generate some random points
points = np.random.rand(20, 2)

# Compute the convex hull of the points
hull = ConvexHull(points)

# Plot the points and the convex hull
fig, ax = plt.subplots()
ax.scatter(points[:, 0], points[:, 1])
for simplex in hull.simplices:
    ax.plot(points[simplex, 0], points[simplex, 1], 'r-')
plt.show()

plt.plot(X[y == 1][:, 0], X[y == 1][:, 1], "ro")
plt.plot(X[y == -1][:, 0], X[y == -1][:, 1], "bo")
plt.grid()

import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
from scipy.spatial import ConvexHull # this is used only for plotting the convex hulls only. 

# Note: This is done using the linearly separable data. 
np.random.seed(52)
X1 = np.random.randn(50, 2) + [2, 2]
X2 = np.random.randn(50, 2) + [-2, -2]
X = np.concatenate((X1, X2), axis=0)
y = np.concatenate((np.ones(50), -np.ones(50)), axis=0)

# Plot the data and the convex hulls
plt.scatter(X[:, 0], X[:, 1], c=y)
hull1 = ConvexHull(X[y == 1])
plt.plot(X[y == 1][:, 0], X[y == 1][:, 1], "ro")
for simplex in hull1.simplices:
    plt.plot(X[y == 1][simplex, 0], X[y == 1][simplex, 1], "r--", linewidth=2)
hull2 = ConvexHull(X[y == -1])
plt.plot(X[y == -1][:, 0], X[y == -1][:, 1], "bo")
for simplex in hull2.simplices:
    plt.plot(X[y == -1][simplex, 0], X[y == -1][simplex, 1], "b--", linewidth=2)
plt.grid()
plt.show()

# Compute the convex hulls of the two classes
CH1 = np.concatenate((hull1.points[hull1.vertices], np.ones((hull1.vertices.shape[0], 1))), axis=1)
CH2 = np.concatenate((hull2.points[hull2.vertices], np.ones((hull2.vertices.shape[0], 1))), axis=1)

# Define the variables
w = cp.Variable(X.shape[1])
b = cp.Variable()

# Define the constraints
constraints = []
for i in range(X.shape[0]):
    constraints.append(y[i] * (X[i].reshape((1,-1)) @ w + b) >= 1)

# Define the objective function
obj = cp.Minimize(cp.norm(w))

# Define the problem
problem = cp.Problem(obj, constraints)

# Solve the problem
problem.solve()

# Get the optimal values of w and b
w_opt = w.value
b_opt = b.value

# Compute the support vectors
SV = np.where(np.abs(X @ w_opt + b_opt - 1) < 1e-5)[0]

# Plot the SVM and the support vectors
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.plot(X[:, 0], -w_opt[0]/w_opt[1] * X[:, 0] - b_opt/w_opt[1], "k-")
plt.scatter(X[SV, 0], X[SV, 1], facecolors='none', s=80)
plt.grid()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

# Generate three classes of data
np.random.seed(0)
X1 = np.random.randn(20, 2) + np.array([2, 2])
X2 = np.random.randn(20, 2) + np.array([-2, -2])
X3 = np.random.randn(20, 2) + np.array([2, -2])

# Concatenate data and labels
X = np.zeros((len(X1) + len(X2) + len(X3), 2))
X[:len(X1), :] = X1
X[len(X1):(len(X1) + len(X2)), :] = X2
X[(len(X1) + len(X2)):, :] = X3
y = np.zeros(len(X))
y[:len(X1)] = 1
y[len(X1):(len(X1) + len(X2))] = 2
y[(len(X1) + len(X2)):] = 3

# Create a scatter plot for each class
colors = ['b', 'r', 'g']
labels = ['Class 1', 'Class 2', 'Class 3']
for i in range(len(colors)):
    plt.scatter(X[y == i + 1, 0], X[y == i + 1, 1], color=colors[i], label=labels[i])

# Compute the convex hull for each class and plot it
for i in range(len(colors)):
    X_class = X[y == i + 1, :]
    hull = ConvexHull(X_class)
    plt.plot(X_class[hull.vertices, 0], X_class[hull.vertices, 1], color=colors[i])

# Set plot title and legend
plt.title('Multiple Class Scatter Plot with Convex Hull')
plt.legend()

# Show the plot
plt.show()

x = np.linspace(-20, 20) # the range of x vector.

import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

# Generate some sample data
np.random.seed(1)
X1 = np.random.randn(200, 2) + np.array([2, 2]) # the first data 
X2 = np.random.randn(200, 2) + np.array([-2, -2]) # the second data. 
X3 = np.random.randn(200, 2) + np.array([2, -2]) # the third data. 
X = np.vstack([X1, X2, X3]) # stack the total datasets. 
y = np.concatenate([np.ones(200), 2 * np.ones(200), 3 * np.ones(200)]) # this creates the labels. 

num_classes = len(np.unique(y)) # find the number of classes. 
w = [] # empty list of w variable.
b = [] # empty list of b variable. 
for i in range(num_classes):
    y_i = np.where(y == i+1, 1, -1) # find the list of the labels for one to many. 
    w_i = cp.Variable(2)
    b_i = cp.Variable()
    objective_i = cp.Minimize(0.5 * cp.norm(w_i)**2 + cp.sum(cp.pos(1 - cp.multiply(y_i, X @ w_i + b_i)))) # the objective function 
    prob_i = cp.Problem(objective_i) # the problm
    prob_i.solve()
    w.append(w_i.value) # append the w values. 
    b.append(b_i.value) # append the b values. 

# the function for drawing out the contours. 
def predict(x):
    scores = []
    for i in range(num_classes):
        score_i = w[i].T @ x + b[i]
        scores.append(score_i)
        #print(np.argmax(scores)+1)
    return (np.argmax(scores) + 1)


plt.scatter(X1[:,0], X1[:,1], color='blue') # class 1 scatter
plt.scatter(X2[:,0], X2[:,1], color='red') # class 2 scatter
plt.scatter(X3[:,0], X3[:,1], color='green') # class 3 scatter
x1_min, x1_max = X[:,0].min() - 1, X[:,0].max() + 1 # take the minimum and the maximum points. 
x2_min, x2_max = X[:,1].min() - 1, X[:,1].max() + 1
xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, 0.1), np.arange(x2_min, x2_max, 0.1)) # meshgrid 
Z = np.zeros(xx1.shape)
for i, x1 in enumerate(xx1[0]):
    for j, x2 in enumerate(xx2[:,0]):
        Z[j,i] = predict(np.array([x1, x2])) # predict the regions in which of the field it would come at. 
plt.contourf(xx1, xx2, Z, alpha=0.2, levels=np.arange(0, num_classes+1))
plt.plot(x, (w[0][0]*x - b[0])/(w[0][1]),'b' )
plt.plot(x, (w[1][0]*x - b[1])/(w[1][1]),'r' )
plt.plot(x, (w[2][0]*x - b[2])/(w[2][1]),'g' )
plt.xlim(x1_min, x1_max)
plt.ylim(x2_min, x2_max)
plt.show()

plt.scatter(X1[:,0], X1[:,1], color='blue') # class 1 scatter
plt.scatter(X2[:,0], X2[:,1], color='red') # class 2 scatter
plt.scatter(X3[:,0], X3[:,1], color='green') # class 3 scatter
plt.grid()

np.random.seed(1)
X1 = np.random.randn(200, 2) + np.array([2, 2]) # the first data 
X2 = np.random.randn(200, 2) + np.array([-2, -2]) # the second data. 
X3 = np.random.randn(200, 2) + np.array([2, -2]) # the third data. 
X4 = np.random.randn(200, 2) + np.array([-2, 2]) # the fourth data 
X = np.vstack([X1, X2, X3, X4]) # stack the total datasets. 
y = np.concatenate([np.ones(200), 2 * np.ones(200), 3 * np.ones(200), 4 * np.ones(200)]) # this creates the labels. 

num_classes = len(np.unique(y)) # find the number of classes. 
w = [] # empty list of w variable.
b = [] # empty list of b variable. 
for i in range(1):
    y_i = np.where(y == i+1, 1, -1) # find the list of the labels for one to many. 
    w_i = cp.Variable(2)
    b_i = cp.Variable()
    objective_i = cp.Minimize(0.5 * cp.norm(w_i)**2 + cp.sum(cp.pos(1 - cp.multiply(y_i, X @ w_i + b_i)))) # the objective function 
    prob_i = cp.Problem(objective_i) # the problm
    prob_i.solve()
    w.append(w_i.value) # append the w values. 
    b.append(b_i.value) # append the b values.

x = np.linspace(-5, 5)

plt.scatter(X1[:,0], X1[:,1], color='blue') # class 1 scatter
plt.scatter(X2[:,0], X2[:,1], color='red') # class 2 scatter
plt.scatter(X3[:,0], X3[:,1], color='green') # class 3 scatter
plt.scatter(X4[:,0], X4[:,1], color='purple') # class 4 scatter
plt.plot(x, (w[0][0]*x - b[0])/(w[0][1]),'b' )
#plt.plot(x, (w[1][0]*x - b[1])/(w[1][1]),'r' )
#plt.plot(x, (w[2][0]*x - b[2])/(w[2][1]),'g' )
#plt.plot(x, (w[3][0]*x - b[3])/(w[3][1]),'violet' )

import cvxpy as cp
import numpy as np

# Generate some sample data
np.random.seed(1)
X1 = np.random.randn(200, 2) + np.array([2, 2])
X2 = np.random.randn(200, 2) + np.array([-2, -2])
X3 = np.random.randn(200, 2) + np.array([2, -2])
X = np.vstack([X1, X2, X3])
y = np.concatenate([np.ones(200), 2 * np.ones(200), 3 * np.ones(200)])

# Define the first hyperplane as a constraint
a, b, c = 1, 1, 0
constraint = lambda x: a*x[0] + b*x[1] + c

# Define the SVM problem
w = cp.Variable((2, 3))
b = cp.Variable(3)
xi = cp.Variable(len(X), nonneg=True)
objective = cp.Minimize(cp.sum_squares(w) + cp.sum(xi))
constraints = []
for i in range(len(X)):
    for j in range(3):
        if j == 0:
            constraints.append(y[i]*((w[:, j].T @ X[i]) + b[j]) >= 1 - xi[i])
        else:
            constraints.append(y[i]*((w[:, j].T @ X[i]) + b[j]) >= 1 - xi[i] - constraint(X[i]))
problem = cp.Problem(objective, constraints)
problem.solve()

# Print the results
print("status:", problem.status)
print("optimal value:", problem.value)
print("w:", w.value)
print("b:", b.value)

import cvxpy as cp # for convex problems and operations. 
import numpy as np # for array operations
import matplotlib.pyplot as plt # for plotting purposes
from sklearn import datasets # for importing the datasets. 

# Generate some sample data
np.random.seed(1)
X1 = np.random.randn(200, 2) + np.array([2, 2])
X2 = np.random.randn(200, 2) + np.array([-2, -2])
X3 = np.random.randn(200, 2) + np.array([2, -2])
X4 = np.random.randn(200, 2) + np.array([-2, 2])
X = np.vstack([X1, X2, X3, X4])
y = np.concatenate([np.ones(200), 2 * np.ones(200), 3 * np.ones(200), 4 * np.ones(200)])

num_classes = len(np.unique(y))
w = []
b = []
for i in range(num_classes):
    y_i = np.where(y == i+1, 1, -1)
    w_i = cp.Variable(2)
    b_i = cp.Variable()
    if i != 0: # if it is not the first class then dont add the constraints. 
        constraint = [w_i.T @ X1[0] + b_i <= 1]
    else:
        constraint = []
    objective_i = cp.Minimize(0.5 * cp.norm(w_i)**2 + cp.sum(cp.pos(1 - cp.multiply(y_i, X @ w_i + b_i))))
    prob_i = cp.Problem(objective_i, constraint)
    prob_i.solve()
    w.append(w_i.value)
    b.append(b_i.value)

# the function for drawing out the contours
def predict(x):
    scores = []
    for i in range(num_classes):
        score_i = w[i].T @ x + b[i]
        scores.append(score_i)
    return (np.argmax(scores) + 1)

plt.scatter(X1[:,0], X1[:,1], color='blue')
plt.scatter(X2[:,0], X2[:,1], color='red')
plt.scatter(X3[:,0], X3[:,1], color='green')
plt.scatter(X4[:,0], X4[:,1], color='purple')
x1_min, x1_max = X[:,0].min() - 1, X[:,0].max() + 1
x2_min, x2_max = X[:,1].min() - 1, X[:,1].max() + 1
xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, 0.1), np.arange(x2_min, x2_max, 0.1))
Z = np.zeros(xx1.shape)
for i, x1 in enumerate(xx1[0]):
    for j, x2 in enumerate(xx2[:,0]):
        Z[j,i] = predict(np.array([x1, x2]))
#plt.contourf(xx1, xx2, Z, alpha=0.2, levels=np.arange(0, num_classes+1))
x1 = np.linspace(-5, 5)
plt.plot(x1, (w[0][0]*x1 - b[0])/(w[0][1]),'b' )
plt.plot(x1, (w[1][0]*x1 - b[1])/(w[1][1]),'r' )
plt.plot(x1, (w[2][0]*x1 - b[2])/(w[2][1]),'g' )
plt.xlim(x1_min, x1_max)
plt.ylim(x2_min, x2_max)
plt.show()

plt.scatter(X1[:,0], X1[:,1], color='blue')
plt.scatter(X2[:,0], X2[:,1], color='red')
plt.scatter(X3[:,0], X3[:,1], color='green')
plt.scatter(X4[:,0], X4[:,1], color='purple')
plt.plot(x, (w[0][0]*x - b[0])/(w[0][1]),'b' )

# Importing libraries here. Note: The straight forward libraries are used in situations where the main part of 
# analysis isnt of much importance. 
import numpy as np # for array operations
import cvxpy as cp # for convex problem related operations. 
import matplotlib.pyplot as plt # for plotting purposes. 
# The Sklearn library in python is used to load data and split it to training and testing data. 
from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split

# define a function for the confusion matrix.
def conf_matr(n_classes):
  cm = np.zeros((n_classes,n_classes)) # an empty array 
  for true_label, pred_label in zip(y_test, y_pred): # for the particular GT and the predicted label. 
    cm[true_label,pred_label] += 1 # increment at those locations. 
  return cm

# define accuracy function here. 
def acc(y_test,y_pred):
  ct = np.sum(y_test==y_pred) # the sum of correctly predicted labels.
  accr = ct/len(y_test) # divide the above with the length of the test labels. 
  return accr

# define the function for the One Versus One approach using the IRIS Dataset here. 
def train_ovo(X_train, y_train, X_test, y_test):
    num_samples, num_features = X_train.shape # the samples is the height here and the total features are the labels. 
    num_classes = len(np.unique(y_train)) # the total features 
    classifiers = []

    # One-vs-One approach: train a binary classifier for each pair of classes
    for i in range(num_classes):
        for j in range(i+1, num_classes):
            # Extract samples and labels for the current pair of classes
            idx = np.logical_or(y_train == i, y_train == j)
            X_pair = X_train[idx] # taking the data here
            y_pair = y_train[idx] # taking the corrsponding labels. 
            y_pair = np.where(y_pair == i, 1, -1) # the label comparison is done in a one to one fashion.

            w = cp.Variable(num_features) # the weight parameter.
            b = cp.Variable() # the bias parameter
            loss = cp.sum(cp.pos(1 - cp.multiply(y_pair, X_pair @ w + b))) # the loss function for miss classifications 
            reg = cp.norm(w, 2) # the regularization is taken here. (the norm is to be minimized)
            C = 6 # take an arbitrary C value here. 
            prob = cp.Problem(cp.Minimize(loss/C + reg), [cp.sum(w) == 0]) # the objective is to minimize the sum of both the misclassification and the norm. 
            prob.solve() # solve for the above. 

            classifiers.append((w.value, b.value, i, j)) # append he value of w,b and at the particular stage. 

    num_test_samples = X_test.shape[0] # the test samples. 
    num_classifiers = len(classifiers) # the labels are selected here. 
    scores = np.zeros((num_test_samples, num_classes)) # score each of the sample here. 
    for i in range(num_test_samples):
        for j in range(num_classifiers):
            w, b, c1, c2 = classifiers[j] # find the 'w' and 'b' from the appended list. 
            score = np.sign(X_test[i] @ w + b) # score it accordingly. 
            if score == 1: 
                scores[i, c1] += 1
            else:
                scores[i, c2] += 1
    y_pred = np.argmax(scores, axis=1) # find the maximum value of the argmax. 
    return y_pred, scores


iris = load_iris() # load the dataset here. 
X = iris.data # the input that contains the height and the width of the petal and sepal respectively. 
y =  iris.target # this contains the labels here. 

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # split the dataset here. 

# Train and test using One-vs-One approach
y_pred,scores = train_ovo(X_train, y_train, X_test, y_test) # this finds out the predicted label. 
cm = conf_matr(len(np.unique(y_test))) # find the confusion matrix; a function is created here. (sklearn can also be used for verification.)
ctp = np.sum(y_pred==y_test) # the count of correctly predicted labels. 
accuracy =  ctp/len(y_pred) # the number of correctly predicted labels by the total length of the prediction. 
print('Accuracy:', accuracy)
print('The Confusion Matrix:\n',cm)

plt.figure()
plt.imshow(cm) # plot the confusion matrix. 
plt.colorbar()

import numpy as np #
import cvxpy as cp
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


def train_ova(X_train, y_train, X_test, y_test):
    num_samples, num_features = X_train.shape # takes the shape here. 
    num_classes = len(np.unique(y_train)) # the total number of classes
    classifiers = [] # empty list to include all the parameters here. 

    for i in range(num_classes):

        y_class = np.where(y_train == i, 1, -1) # the main difference is the label is separated from the rest here (unlike the previous one. )

        w = cp.Variable(num_features) # define the weight vector. 
        b = cp.Variable() # define the bias vector here. 
        loss = cp.sum(cp.pos(1 - cp.multiply(y_class, X_train @ w + b))) # define the loss here (miss classification is done here.)
        reg = cp.norm(w, 2) # the regularization is used here which is the L2 norm of the weight vector. 
        C = 1 # the constant parameter is taken here. more this value, the lesser concentration is done in the miss classification here. 
        prob = cp.Problem(cp.Minimize(loss/C + reg), [cp.sum(w) == 0]) # formulate the problem here. 
        prob.solve()

        classifiers.append((w.value, b.value)) # append all the values in the empty list. 

    num_test_samples = X_test.shape[0] # the length is taken here. 
    num_classifiers = len(classifiers) # labels 
    scores = np.zeros((num_test_samples, num_classes)) # score around each, gives the probability. 
    for i in range(num_test_samples):
        for j in range(num_classifiers):
            w, b = classifiers[j] # take the w and b values. 
            score = X_test[i] @ w + b # compute it and get the corresponding score. 
            scores[i, j] = score
    y_pred = np.argmax(scores, axis=1) # the likely one is the one that has max probability. 
    return y_pred

iris = load_iris() # load the data here. 
X, y = iris.data, iris.target # load the data along with the corresponding labels. 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # the data is split here (70-30 scenario)

# Train and test using One-vs-All approach
y_pred = train_ova(X_train, y_train, X_test, y_test) # run the above defined code. 
accuracy = acc(y_test,y_pred) # find the accuracy of correct detection 
cm = conf_matr(len(np.unique(y_test))) # the confusion matrix is observed
print('Accuracy:', accuracy)
print('Confusion Matrix:\n',cm)

# representing the confusion matrix 
plt.figure()
plt.imshow(cm) # plot the confusion matrix.
plt.colorbar(); # for the visual range of variation