workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\DMC\\03_Data\\Weibo\\20140830\\"
zipFileName = workingDirectory + "02_users.zip"
poiidFileName = workingDirectory + "weibo_PRD_20140830_allEntries.txt"

with open(poiidFileName, 'r') as f:
    data = f.read()
    entries = data.split("\n")
    entries.pop(0)
   
poiidDict = {} 
      
for entry in entries:
    data = entry.split(";")
    poiidDict[data[0]] = {'lat': data[3], 'lon': data[4]}

import zipfile
  
from dateutil import parser
maxTime = parser.parse('Jun 1 0:0:0 +0800 2014')
  
with zipfile.ZipFile(zipFileName) as zf:
    
    numFiles = int(len(zf.infolist()))
    
    for i,f in enumerate(zf.infolist()):
        
        if i % (numFiles/10) == 0:
            print str(i / (numFiles/100)) + "% processed"
        
        #print f.filename, f.file_size
        
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
        entries = data.split("\n")
        entries.pop(0)
        
        for entry in entries:
            try:
                uid = entry.split(";")[3]
                time = parser.parse(entry.split(";")[0])
                if uid == "":
                    continue
            except:
                #print "uid entry error!"
                continue
            #print uid
            
            #BREAK AT MAX TIME
            if time < maxTime:
                #print "less"
                break
            
            #ONLY ADD UNIQUE UID
            if uid not in poiidDict[poiid]['uid']:
                poiidDict[poiid]['uid'].append(uid)


print len(poiidDict) 

    
##CULL ENTRIES FROM DICTIONARY BY POIID LIST FILE
    
selectPoiidFileName = workingDirectory + "SZHKfood_poiid.txt"

with open(selectPoiidFileName, 'rb') as f:
    data = f.read()
    entries = data.split("\r")
    entries.pop(0)

SZHKDict = {}

for i,entry in enumerate(entries):
    
    if i % (len(entries)/10) == 0:
        print str(i / (len(entries)/100)) + "% processed"
    
    SZHKDict[entry] = poiidDict[entry]
print len(SZHKDict) 

poiidDict.clear()
                   
import pickle

pickle.dump( SZHKDict, open( workingDirectory + "SZHKpoiidDict.p", "wb" ) )
