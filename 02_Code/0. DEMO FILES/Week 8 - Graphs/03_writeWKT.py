workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\DMC\\03_Data\\Weibo\\20140830\\"

import pickle

matchDict = pickle.load( open( workingDirectory + "matchDict.p", "rb"))

poiidFileName = workingDirectory + "SZHKfood_poiid.txt"

poiidDict = {}

with open(poiidFileName, 'r') as f:
    data = f.read()
    entries = data.splitlines()
    entries.pop(0)
    
    for entry in entries:
        data = entry.split(';')
        poiidDict[data[0]] = {'lat': data[1], 'lon': data[2]}
        

#create WKT file

writeFileName = workingDirectory + "poiidGraph.txt"

with open(writeFileName, 'w') as f:
    
    f.write('Geom;originPOIID;destPOIID;weight\n')
    
    s = "LINESTRING ({0} {1}, {2} {3});{4};{5};{6}\n"
    
    for key in matchDict:
        y1 = poiidDict[key]['lat']
        x1 = poiidDict[key]['lon']
        
        for ref in matchDict[key]:
            y2 = poiidDict[ref]['lat']
            x2 = poiidDict[ref]['lon']
            
            w = int(matchDict[key][ref])
            
            if w > 1:
                f.write(s.format(x1, y1, x2, y2, key, ref, w))
    
    
    