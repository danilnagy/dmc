from pylab import *
import matplotlib.pyplot as pyplot
import math
import random
import numpy
random.seed(3)
import sys

def f(x):
    y = math.pow(x,3) + 3
    return y
    
def f_r(x):
    y = math.pow(x,3) + 3
    y = y + (random.random() - .5) * 15
    return y
 
close('all')   

figure(1)

numPoints = 20
          
X = numpy.linspace(-3,3,num=numPoints)

r = range(numPoints)
train_set = sort(random.sample(r,10))
val_set = [i for i in r if i not in train_set]

print r
print train_set
print val_set


X_train = X[train_set]
X_validate = X[val_set]

Y_train = [f_r(i) for i in X_train]

scatter(X_train,Y_train, color="blue")

Y_validate = [f_r(i) for i in X_validate]

scatter(X_validate,Y_validate, color="red")




####TRAINING

from sklearn import svm
from sklearn import preprocessing

scaler = preprocessing.StandardScaler().fit(X_train)
X_scaled = scaler.transform(X_train)

numTrials = 11

mse_train = []
mse_val = []

for i in range(numTrials):
    
    deg = i

    svr_poly = svm.SVR(kernel='poly', C=1, epsilon=.1, degree=deg, coef0=3, cache_size=2000)
    svr_poly.fit(np.reshape(X_train, (X_train.shape[0], 1)), Y_train)

    line_x = numpy.linspace(-3,3,num=100)
    line_y = [svr_poly.predict(i) for i in line_x]
    
    lw = .2
        
    plt.plot(line_x, line_y, color="black", linestyle="-", linewidth=lw)
    
    #predict on training set
    Y_train_p = [svr_poly.predict(i) for i in X_train]
    
    #predict on validation set
    Y_validate_p = [svr_poly.predict(i) for i in X_validate]
    
    #check error values
    mse_train.append(((np.asarray(Y_train_p).flatten() - np.asarray(Y_train).flatten())**2).mean())
    mse_val.append(((np.asarray(Y_validate_p).flatten() - np.asarray(Y_validate).flatten())**2).mean())


svr_poly = svm.SVR(kernel='poly', C=1, epsilon=.1, degree=3, coef0=3, cache_size=2000)
svr_poly.fit(np.reshape(X_train, (X_train.shape[0], 1)), Y_train)

line_x = numpy.linspace(-3,3,num=100)
line_y = [svr_poly.predict(i) for i in line_x]
    
plt.plot(line_x, line_y, color="black", linestyle="-", linewidth=1.5)


xlim(-3.5, 3.5)
ylim(-20, 35)

figure(2)

semilogy(range(numTrials), mse_train, color="blue")
semilogy(range(numTrials), mse_val, color="red")

title('Model Validation')
xlabel('degree')
ylabel('mean squared error')

show()

