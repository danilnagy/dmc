workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 9 - ML\\demo\\data\\"
dataFileName = workingDirectory + "soufun_20141006_SZ.txt"

from sklearn import preprocessing
from sklearn import svm

import numpy as np
import random

random.seed(0)

with open(dataFileName, 'r') as f:
    data = f.read()
    entries = data.splitlines()
    entries.pop(0)
    
    featureData = []
    targetData = []
    
    random.shuffle(entries)
    
    for entry in entries[:1000]:
        data = entry.split(';')
        
        try:
            featureData.append([data[1], data[2]])
            targetData.append(data[0])
        except:
            continue
        

X = np.asarray(featureData, dtype='float')
y = np.asarray(targetData, dtype='float')

num = int(len(targetData) * .7)

X_train = X[:num]
X_val = X[num:]

y_train = y[:num]
y_val = y[num:]

#mean 0, variance 1
scaler = preprocessing.StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)


'''
#VALIDATION

mse_val = []

for C_var in [10000, 100000, 200000]:
    for e_var in [.00000001, .000001, .001]:

        model = svm.SVR(C=C_var, epsilon=e_var, kernel='rbf', cache_size=2000)
        model.fit(X_train_scaled, y_train)
        
        y_val_p = [model.predict(i) for i in X_val]
        
        mse = ((np.asarray(y_val_p).flatten() - np.asarray(y_val).flatten())**2).mean()
        
        print 'C=' + str(C_var)
        print 'e=' + str(e_var)
        print 'mse=' + str(mse)
        print '-----'

'''

model = svm.SVR(C=100000, epsilon=.00001, kernel='rbf', cache_size=2000)
model.fit(X_train_scaled, y_train)


testFileName = workingDirectory + "testSet.txt"

with open(testFileName, 'r') as f:
    data = f.read()
    entries = data.splitlines()
    entries.pop(0)
    
    testFeatureData = []
    IDData = []
    
    for entry in entries:
        data = entry.split(';')
        
        try:
            testFeatureData.append([data[1], data[2]])
            IDData.append(data[0])
        except:
            continue
            
            
X_test = np.asarray(testFeatureData, dtype='float')

X_test_scaled = scaler.transform(X_test)


prediction = model.predict(X_test_scaled)


trainedFileName = workingDirectory + "trainedSet.txt"

with open(trainedFileName, 'w') as wf:
    wf.write('id;lat;lon;prediction\n')
    
    for i in range(len(prediction)):
        wf.write(IDData[i] + ';' + testFeatureData[i][0] + ';' + testFeatureData[i][1] + ';' + str(prediction[i]) + '\n')




        