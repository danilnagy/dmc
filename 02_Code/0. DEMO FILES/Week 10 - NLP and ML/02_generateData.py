workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 10 - ML Classification\\demo_final\\data\\"

import pickle
import random

inList = pickle.load(open(workingDirectory + "inList.p", "rb"))
bothList = pickle.load(open(workingDirectory + "bothList.p", "rb"))
outList = pickle.load(open(workingDirectory + "outList.p", "rb"))

textList_Target = pickle.load(open(workingDirectory + "textList_Target.p", "rb"))
textList_notTarget = pickle.load(open(workingDirectory + "textList_notTarget.p", "rb"))


features = []
target = []

random.shuffle(textList_Target)
random.shuffle(textList_notTarget)

for text in textList_Target[:4000]:
    
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
    
    features.append(featList)
    target.append(1)
    
    
for text in textList_notTarget[:4000]:
    
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
    
    features.append(featList)
    target.append(-1)


pickle.dump( features, open(workingDirectory + "features.p", "wb"))
pickle.dump( target, open(workingDirectory + "target.p", "wb"))
