workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\DMC\\03_Data\\Weibo\\20140830\\"

import sys
import pickle

matchDict = pickle.load( open( workingDirectory + "matchDict.p", "rb" ) )


poiidFileName = workingDirectory + "weibo_PRD_20140830_allEntries.txt"

poiidDict = {} 

with open(poiidFileName, 'r') as f:
    data = f.read()
    entries = data.split("\n")
    entries.pop(0)
   
    for entry in entries:
        data = entry.split(";")
        poiidDict[data[0]] = {'lat': data[3], 'lon': data[4]}
    

writeFileName = workingDirectory + "poiidGraph.txt"

with open(writeFileName, 'w') as f:
    f.write('Geom;originPOIID;destPOIID;weight\n')
    s = "LINESTRING ({0} {1}, {2} {3});{4};{5};{6}\n"
    
    for key in matchDict:
        
        x1 = poiidDict[key]['lat']
        y1 = poiidDict[key]['lon']
        
        for ref in matchDict[key]:
            
            x2 = poiidDict[ref]['lat']
            y2 = poiidDict[ref]['lon']
        
            w = int(matchDict[key][ref])
            
            if w > 1:
                f.write(s.format(y1,x1,y2,x2,key,ref,w))
        