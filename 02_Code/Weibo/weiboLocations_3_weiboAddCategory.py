import time
import csv
import sys
import urllib2
import json
import math

delim = ';'

workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\"
codeDirectory = workingDirectory + "02_Code\\Weibo\\"
fileName = "category"
fileExt = ".csv"

categoryData = {}

with open( codeDirectory+fileName+fileExt, 'rb' ) as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        categoryData[row[0].strip()] = row[1:]
        
dataDirectory = workingDirectory + "03_Data\\Weibo\\PRD\\20140830\\01_locations\\"
dataFileName = "weibo_PRD_20140830_allEntries_culled_ampFixed"
fileExt = ".txt"

failCount = 0
failList = []

with open(dataDirectory + dataFileName + fileExt, 'r') as f:
    data = f.read()
    entries = data.strip().split("\n")

    print "Number of Entries: " + str(len(entries))
    
    with open(dataDirectory + dataFileName + "_categorized" + fileExt, 'w') as wf:
        wf.write(entries.pop(0) + delim + "cat_1" + delim + "cat_2" + "\n")
    
        for entry in entries:
            try:
                categoryName = entry.split(";")[7].strip()
            except:
                print entry,  ": ENTRY ERROR"
                continue
            
            try:
                cat_1 = categoryData[categoryName][0]
                cat_2 = categoryData[categoryName][1]
            except:
                cat_1 = ""
                cat_2 = ""
                failCount += 1
                if categoryName not in failList:
                    failList.append(categoryName)
                    
                print categoryName, ": CATEGORY ERROR"
                print entry
                print '-----'
            
            wf.write(entry + delim + cat_1 + delim + cat_2 + "\n")
    
with open(dataDirectory + dataFileName + "_failedCategorized" + fileExt, 'w') as wf:
    for fail in failList:
        wf.write(fail + "\n")

print failCount
print "JOB COMPLETE"

