zipFileName = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\DMC\\03_Data\\Weibo\\20140830\\02_users.zip"
workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 10 - ML Classification\\demo_final\\data\\"

Target_file = workingDirectory + "OCT_data.txt"

import random

random.seed(0)

Target_List = []

with open(Target_file, 'r') as f:
    data = f.read()
    entries = data.splitlines()
    entries.pop(0)
    
    random.shuffle(entries)
    
    for entry in entries:
        Target_List.append(entry)
        
print len(Target_List)

import zipfile
  
from dateutil import parser
maxTime = parser.parse('Jan 1 0:0:0 +0800 2014')

listOfWords_Target = []
listOfWords_notTarget = []

textList_Target = []
textList_notTarget = []

inCount = 0
outCount = 0

with zipfile.ZipFile(zipFileName) as zf:
    numFiles = int(len(zf.infolist()))
    
    random.shuffle(zf.infolist())
    
    for i, f in enumerate(zf.infolist()):
        
        if i % (numFiles/10) == 0:
            print str(i / (numFiles/100)) + "% processed"
                
        try:
            poiid = f.filename.split('_')[2].split('.')[0]
        except:
            continue
            
        if poiid in Target_List:
            
            data = zf.read(f)
            entries = data.splitlines()
            entries.pop(0)
            
            for entry in entries:
                
                time = parser.parse(entry.split(";")[0])
                if time < maxTime:
                    break
                
                text = entry.split(';')[2].split("http")[0]
                
                l1 = list(unicode(text.decode('utf8')))
                
                charNum = range(1,5)
                for char in charNum:
                    for j in range(len(l1)-(char-1)):
                        word = "".join(l1[j:j+char])
                        listOfWords_Target.append(word)
                        
                textList_Target.append(text.decode('utf8'))
                        
                        
        elif random.random() < .01:
            
            data = zf.read(f)
            entries = data.splitlines()
            entries.pop(0)
            
            for entry in entries:
                
                time = parser.parse(entry.split(";")[0])
                if time < maxTime:
                    break
                    
                text = entry.split(';')[2].split("http")[0]
                
                
                l1 = list(unicode(text.decode('utf8')))
                
                charNum = range(1,5)
                for char in charNum:
                    for j in range(len(l1)-(char-1)):
                        word = "".join(l1[j:j+char])
                        listOfWords_notTarget.append(word)
                        
                textList_notTarget.append(text.decode('utf8'))
                        
                                    
        else:
            continue



import collections

collection = collections.Counter(listOfWords_Target)
coll_Target = [row[0] for row in collection.most_common(2000)]

collection = collections.Counter(listOfWords_notTarget)
coll_notTarget = [row[0] for row in collection.most_common(2000)]

inList = [i for i in coll_Target if i not in coll_notTarget]
bothList = [i for i in coll_Target if i in coll_notTarget]
outList = [i for i in coll_notTarget if i not in coll_Target]

import pickle

pickle.dump( inList, open(workingDirectory + "inList.p", "wb"))
pickle.dump( bothList, open(workingDirectory + "bothList.p", "wb"))
pickle.dump( outList, open(workingDirectory + "outList.p", "wb"))

pickle.dump( textList_Target, open(workingDirectory + "textList_Target.p", "wb"))
pickle.dump( textList_notTarget, open(workingDirectory + "textList_notTarget.p", "wb"))

with open(workingDirectory + "inList.txt", "w") as f:
    for i in inList:
        f.write(i.encode('utf8') + "\n")
        
with open(workingDirectory + "bothList.txt", "w") as f:
    for i in bothList:
        f.write(i.encode('utf8') + "\n")
        
with open(workingDirectory + "outList.txt", "w") as f:
    for i in outList:
        f.write(i.encode('utf8') + "\n")
