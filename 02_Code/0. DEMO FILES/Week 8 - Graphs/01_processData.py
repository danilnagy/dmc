workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\DMC\\03_Data\\Weibo\\20140830\\"

poiidFileName = workingDirectory + "SZHKfood_poiid.txt"


poiidDict = {}

with open(poiidFileName, 'r') as f:
    data = f.read()
    entries = data.splitlines()
    entries.pop(0)
    
    for entry in entries:
        data = entry.split(';')
        poiidDict[data[0]] = {'lat': data[1], 'lon': data[2]}
        

zipFileName = workingDirectory + "02_users.zip"

import zipfile

from dateutil import parser
d = "Jun 01 0:0:0 +0800 2014"
maxTime = parser.parse(d)

with zipfile.ZipFile(zipFileName) as zf:
    numFiles = int(len(zf.infolist()))
    
    for i, f in enumerate(zf.infolist()):
        
        if i % (numFiles/10) == 0:
            print str(i / (numFiles/100)) + "% processed"
                
        try:
            poiid = f.filename.split('_')[2].split('.')[0]
            #print poiid
        except:
            #print "poiid entry error!"
            continue
        
        try:
            poiidDict[poiid]['uid'] = []
        except:
            #print "poiid entry error!"
            continue
        
        data = zf.read(f)
        entries = data.splitlines()
        entries.pop(0)
        
        
        for entry in entries:
            uid = entry.split(';')[3]
            if uid == '':
                continue
            time = parser.parse(entry.split(';')[0])
            
            if time < maxTime:
                break
            
            if uid not in poiidDict[poiid]['uid']:
                poiidDict[poiid]['uid'].append(uid)


import pickle

pickle.dump( poiidDict, open(workingDirectory + "poiidDict.p", "wb"))
