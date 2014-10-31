from sklearn import datasets
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import random

random.seed(3)

plt.close('all') 

boston = datasets.load_boston()
print boston.DESCR

X = boston.data[:, [5,7]]

y = boston.target
val = y.mean()

np.putmask(y, y<val, -1)
np.putmask(y, y>=val, 1)


r = range(X.shape[0])
num = int(X.shape[0] * .7)
train_set = sort(random.sample(r,num))
val_set = [i for i in r if i not in train_set]

X_train = X[train_set]
X_val = X[val_set]

y_train = y[train_set]
y_val = y[val_set]

cm = plt.get_cmap('bwr') 

####TRAINING

from sklearn import svm
from sklearn import preprocessing

scaler = preprocessing.StandardScaler().fit(X)
X_scaled = scaler.transform(X)

count = 1
mse_val = []

for C_var in [1, 50, 500]:
    
    for e_var in [.01,.1,1]:
        
        figure(num=count, figsize = (10,8), dpi=150)

        svr = svm.SVC(kernel='rbf', C=C_var, gamma=e_var, cache_size=2000)   
        
        svr.fit(X_train, y_train)
        
        h = .02
        
        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                                np.arange(y_min, y_max, h))
        
        Z = svr.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        
        plt.contourf(xx, yy, Z, 8, cmap=cm, alpha=.25)
        C = contour(xx, yy, Z, 2, colors='black', linewidth=.1)
        
        y_val_p = [svr.predict(i) for i in X_val]
        
        plt.scatter(X_train[:, [0]], X_train[:, [1]], c='k', marker=u'+')
        
        plt.scatter(X_val[:, [0]], X_val[:, [1]], c=y_val, lw=.1, cmap=cm)
    
    
        s_v = X_train[svr.support_]
        plt.scatter(s_v[:, [0]], s_v[:, [1]], s=40, facecolors='none', edgecolors='k', lw=.5)
        
        mse = np.sum(y_val != np.asarray(y_val_p).flatten())
        mse_val.append(mse)
    
        plt.xlim(5, 9)
        plt.ylim(1, 8)
        
        plt.title('Boston house prices')
        plt.xlabel('number of rooms')
        plt.ylabel('distance to center (mi)')
        
        plt.text(8, 7.6, 'C=' + str(C_var))
        plt.text(8, 7.35, 'g=' + str(e_var))
        plt.text(8, 7.1, 'mse=' + str(mse))
        
        count += 1
    

plt.show()

print mse_val