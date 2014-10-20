workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\DMC\\03_Data\\Weibo\\20140830\\"

import sys
import pickle

poiidDict = pickle.load( open( workingDirectory + "SZHKpoiidDict.p", "rb" ) )

print len(poiidDict)

matchDict = {}

for key in poiidDict.keys():
    
    curr = poiidDict.pop(key)
    
    matchDict[key] = {}
    
    for uid in curr['uid']:
        for ref in poiidDict:
            if uid in poiidDict[ref]['uid']:
                #print "match found: " + key + ", " + ref
                
                if ref in matchDict[key]:
                    matchDict[key][ref] += 1
                else:
                     matchDict[key][ref] = 1
     
    if len(matchDict) % 1000 == 0:        
        print len(matchDict)
    
print len(poiidDict)

pickle.dump( matchDict, open( workingDirectory + "matchDict.p", "wb" ) )