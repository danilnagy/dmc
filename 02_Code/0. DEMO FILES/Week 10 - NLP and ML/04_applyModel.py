zipFileName = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\DMC\\03_Data\\Weibo\\20140830\\02_users.zip"
workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 10 - ML Classification\\demo_final\\data\\"

writeFile = workingDirectory + "predictedPOIID.txt"
Predict_file = workingDirectory + "OCT_data.txt"

import zipfile
import random

import pickle
from sklearn import preprocessing
from sklearn import svm
import sys

import numpy as np

random.seed(0)

Predict_List = []

with open(Predict_file, 'r') as f:
    data = f.read()
    entries = data.splitlines()
    entries.pop(0)
    
    random.shuffle(entries)
    
    for entry in entries:
        Predict_List.append(entry)
        
print len(Predict_List)


model = pickle.load(open(workingDirectory + "model.p", "rb"))
scaler = pickle.load(open(workingDirectory + "scaler.p", "rb"))

inList = pickle.load(open(workingDirectory + "inList.p", "rb"))
bothList = pickle.load(open(workingDirectory + "bothList.p", "rb"))
outList = pickle.load(open(workingDirectory + "outList.p", "rb"))

c1 = 0
c0 = 0

with zipfile.ZipFile(zipFileName) as zf:
    
    with open(writeFile, 'w') as wf:
        
        wf.write("POIID;ratio\n")
    
        numFiles = int(len(zf.infolist()))
        
        random.shuffle(zf.infolist())
        
        for i, f in enumerate(zf.infolist()):
            
            if i != 0 and i % (numFiles/10) == 0:
                print str(i / (numFiles/100)) + "% processed"
                    
            try:
                poiid = f.filename.split('_')[2].split('.')[0]
            except:
                continue
            
            if poiid in Predict_List:
            
                data = zf.read(f)
                entries = data.splitlines()
                entries.pop(0)
                
                posCount = 0
                count = 0
                
                if entries == 0:
                    continue
            
                for entry in entries:
                    text = entry.split(';')[2].split("http")[0].decode('utf8')
                    
                    if text == "":
                        continue
                    
                    featList = []
                    
                    feat = 0
                    for word in inList:
                        if word in text:
                            feat += 1
                    featList.append(feat)
                    
                    feat = 0
                    for word in outList:
                        if word in text:
                            feat += 1
                    featList.append(feat)
                    
                    feat_scaled = scaler.transform(np.asarray([featList], dtype='float'))
                    p = model.decision_function(feat_scaled)

                    posCount += p
                    count += 1
                    
                        
                try:
                    ratio = float(posCount)/float(count)
                    wf.write(poiid + ";" + str(ratio) + "\n")
                except:
                    continue
                    
                