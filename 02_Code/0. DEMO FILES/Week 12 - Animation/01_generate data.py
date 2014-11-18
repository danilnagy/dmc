import zipfile
from dateutil import parser

#location of all checkin zip file
zipFileName = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\DMC\\03_Data\\Weibo\\20140830\\02_users.zip"
#location of working directory
workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 12 - Python Viz\\class demo\\data\\"

#name of file containing poiid's of places you want to visualize
poiidFile = workingDirectory + "SZHK_data.txt"

#read through poiid data file and create list of poiid's
poiid_list = []
with open(poiidFile, 'r') as f:
    data = f.read()
    entries = data.splitlines()
    entries.pop(0)
    
    for entry in entries:
        poiid_list.append(entry)
        
#location of data set containing lat/lon data for all poiid's
poiidFileName = workingDirectory + "weibo_PRD_20140830_allEntries.txt"

#generate dictionary of lat/lon information for all poiid's
poiidDict = {} 
with open(poiidFileName, 'r') as f:
    data = f.read()
    entries = data.splitlines()
    entries.pop(0)
   
    for entry in entries:
        data = entry.split(";")
        poiidDict[data[0]] = {'lat': data[3], 'lon': data[4]}

#set starting time of analysis
minTime = parser.parse('Jan 1 0:0:0 +0800 2014')

#generate dictionary of checkins with an empty dictionary entry for each minute in 24 hour period
checkins = {}
cat_n = 24 * 60
for c in range(cat_n):
    checkins[c] = {}

#open zip file for reading
with zipfile.ZipFile(zipFileName) as zf:

    numFiles = int(len(zf.infolist()))
    
    #iterate through all files in zipfile
    for i, f in enumerate(zf.infolist()):
        
        #print feedback about processes through zipfile
        if i != 0 and i % (numFiles/10) == 0:
            print str(i / (numFiles/100)) + "% processed"
      
        #try to get poiid from file name, otherwise continue to next file      
        try:
            poiid = f.filename.split('_')[2].split('.')[0]
        except:
            continue
        
        #if poiid is in list of poiids to visualize
        if poiid in poiid_list:
            
            #read in all checkins within poiid
            data = zf.read(f)
            entries = data.splitlines()
            entries.pop(0)
            
            #posCount = 0
            #count = 0
            
            #if there are no entries, continue to next file
            if entries == 0:
                continue
                
            #iterate through all checkins
            for entry in entries:
                
                #get time of current checkin
                try:
                    #uid = entry.split(";")[3]
                    time = parser.parse(entry.split(";")[0])
                    #if uid == "":
                    #    continue
                except:
                    continue
                
                #if time older than minimum, break out of loop and continue to next file
                if time < minTime:
                    break
                    
                #generate checkin dictionary key (minute in 24 time period)
                key = int(time.hour * 60 + time.minute)
                
                #if poiid not already in dictionary for that minute, 
                #add it to dictionary with lat/lon information and an initial weight of 1
                if poiid not in checkins[key]:
                    checkins[key][poiid] = [poiidDict[poiid]['lat'], poiidDict[poiid]['lon'], 1]
                #if already in dictionary, increment value by 1
                else:
                    checkins[key][poiid][2] += 1
                
                        
#export checkin dictionary to file
import pickle
pickle.dump( checkins, open( workingDirectory + "checkins.p", "wb" ) )
                    
                