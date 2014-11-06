workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 10 - ML Classification\\demo_final\\data\\"

import pickle
from sklearn import preprocessing
from sklearn import svm
from sklearn.decomposition import RandomizedPCA

import matplotlib.pyplot as plt
from pylab import *

import numpy as np
import sys
import random

random.seed(0)

plt.close('all') 
cm = plt.get_cmap('bwr') 

features = pickle.load( open(workingDirectory + "features.p", "rb"))
target = pickle.load( open(workingDirectory + "target.p", "rb"))

data = zip(features, target)
random.shuffle(data)

features[:], target[:] = zip(*data)



X = np.asarray(features, dtype='float')
y = np.asarray(target, dtype='float')

num = int(len(target) * .7)

X_train = X[:num]
X_val = X[num:]

y_train = y[:num]
y_val = y[num:]

#mean 0, variance 1
scaler = preprocessing.StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)


figure(1)
jitter = .2
plt.scatter([i + random.uniform(-jitter, jitter) for i in X_train_scaled[:, [0]]], [i + random.uniform(-jitter, jitter) for i in X_train_scaled[:, [-1]]], c=y_train, lw=0, cmap=cm, s=10, alpha=.1)
plt.show()

#VALIDATION

mse_val = []

for C_var in [10]:

    model = svm.SVC(C=C_var, kernel='linear', cache_size=2000)
    model.fit(X_train_scaled, y_train)
    
    X_val_scaled = scaler.transform(X_val)
    
    p = [model.predict(i) for i in X_val_scaled]
    e = np.sum(y_val != np.asarray(p).flatten())
    
    print 'C=' + str(C_var)
    print 'e=' + str(e)
    print '-----'
    
    
figure(2)

plt.scatter([i + random.uniform(-jitter, jitter) for i in X_val_scaled[:, [0]]], [i + random.uniform(-jitter, jitter) for i in X_val_scaled[:, [-1]]], c=p, lw=0, cmap=cm, s=5, alpha=.1)
plt.show()

pickle.dump( model, open(workingDirectory + "model.p", "wb"))
pickle.dump( scaler, open(workingDirectory + "scaler.p", "wb"))