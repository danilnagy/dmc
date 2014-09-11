import sys
import math

workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\03_Data\\Soufun\\PRD\\housing\\20140908\\coded\\"
fileName = 'allEntries_combined.txt'
writeFile = workingDirectory + "allEntries" + "_culled_shifted_precision" + ".txt"

delim = ';'

culledEntries = ""

with open(workingDirectory + fileName, 'r') as f:
    data = f.read()
    entries = data.split("\n")
    
print "ORIGINAL ENTRIES: ", len(entries)

with open(writeFile, 'w') as f:
    f.write(entries.pop(0) + delim + 'gglat' + delim + 'gglng' + "\n")
    

for entry in entries:
    
    try:
        ##for office:
        #bd_lat = float(entry.split(delim)[7])
        #bd_lon = float(entry.split(delim)[8])
        #precision = entry.split(delim)[9]
        #confidence = entry.split(delim)[10]

        ##for housing
        bd_lat = float(entry.split(delim)[8])
        bd_lon = float(entry.split(delim)[9])
        precision = entry.split(delim)[10]
        confidence = entry.split(delim)[11]
        
        x_pi = 3.14159265358979324 * 3000.0 / 180.0
        x = bd_lon - 0.0065 
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)  
        theta = math.atan2(x,y) - 0.000003 * math.cos(x * x_pi) 
        gg_lat = z * math.cos(theta)
        gg_lon = z * math.sin(theta)
        
        #print precision
        #print confidence
        
        #if int(confidence) >= 40:
        if int(precision) > 0:
            culledEntries += entry + delim + str(gg_lat) + delim + str(gg_lon) + "\n"
            
    except:
       continue
        
print "FINAL ENTRIES: ", len(culledEntries.split("\n"))

with open(writeFile, 'a') as f:
    f.write(culledEntries)
