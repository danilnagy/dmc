workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\DMC\\03_Data\\Weibo\\20140830\\"


import pickle

poiidDict = pickle.load( open( workingDirectory + "poiidDict.p", "rb"))

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
        

pickle.dump( matchDict, open(workingDirectory + "matchDict.p", "wb"))
        
                    
