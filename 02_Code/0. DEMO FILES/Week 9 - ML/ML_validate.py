workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 9 - ML\\demo\\data\\"
dataFileName = workingDirectory + "soufun_20141006_SZ.txt"

import numpy as np
from sklearn import svm
from sklearn import preprocessing
import random
import sys

random.seed(0)

with open(dataFileName, 'r') as f:
    data = f.read()
    entries = data.split("\n")
    entries.pop(0) #remove first (header) line
    
    #generate feature array (samples X features)
    featureData = []
    
    #generate target array
    targetData = []
    
    random.shuffle(entries)
      
    for entry in entries[:]:
        data = entry.split(";")
        
        #try for missing values
        try:
            featureData.append([data[1], data[2]])
            targetData.append(data[0])
        except:
            continue


#convert data to numpy.ndarray format
X = np.asarray(featureData, dtype='float')
y = np.asarray(targetData, dtype='float')


r = range(X.shape[0])
num = int(X.shape[0] * .7)

X_train = X[:num]
X_val = X[num:]

y_train = y[:num]
y_val = y[num:]

#scale features to mean 0 variance 1
scaler = preprocessing.StandardScaler().fit(X_train)
X_scaled = scaler.transform(X_train)

count = 1
mse_val = []

#for C_var in [10000, 100000, 200000]:
for C_var in [100000]:
    
    #for e_var in [.00000001, .000001, .001]:
    for e_var in [.000001]:

        #set cache size depending on RAM available on machine
        model = svm.SVR(C=C_var, cache_size=2000, epsilon=e_var, gamma=0.0, kernel='rbf')
        model.fit(X_scaled, y_train)
        
        y_val_p = [model.predict(i) for i in X_val]
    
        #check error values
        mse = ((np.asarray(y_val_p).flatten() - np.asarray(y_val).flatten())**2).mean()/1000000
        mse_val.append(mse)
        
        print 'C = ' + str(C_var)
        print 'e = ' + str(e_var)
        print 'mse = ' + str(mse)
        print '-----'
        
print mse_val

sys.exit()


testFileName = workingDirectory + "testSet.txt"

with open(testFileName, 'r') as f:
    data = f.read()
    entries = data.split("\n")
    entries.pop(0) #remove first (header) line
    
    #generate feature array (samples X features)
    testFeatureData = []
    
    #generate ID (matching) array
    IDData = []
      
    for entry in entries:
        data = entry.split(";")
        
        #try for missing values
        try:
            testFeatureData.append([data[1], data[2]])
            IDData.append(data[0])
        except:
            continue
            
#convert data to numpy.ndarray format
X_test = np.asarray(testFeatureData, dtype='float')

#scale features to mean 0 variance 1
X_test_scaled = scaler.transform(X_test)   

prediction = model.predict(X_test_scaled)

trainedFileName = workingDirectory + "trainedSet.txt"

with open(trainedFileName, 'w') as wf:
    
    wf.write('id;lat;lon;prediction\n')
    
    for i in range(len(prediction)):
        wf.write(IDData[i] + ";" + testFeatureData[i][0] + ";" + testFeatureData[i][1] + ";" + str(prediction[i]) + "\n")