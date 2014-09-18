from os import walk

workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\03_Data\\Weibo\\PRD\\20140830\\01_locations\\"

fileNames = []
for (dirpath, dirnames, filenames) in walk(workingDirectory):
    fileNames.extend(filenames)
    break
    
culledEntries = ""
entryList = []

for fileName in fileNames:

    with open(workingDirectory + fileName, 'r') as f:
        data = f.read()
        entries = data.split("\n")

    print "Original Entries: " + str(len(entries))
    
    for entry in entries:
        entryID = entry.split(";")[0]
        if entryID not in entryList:
            entryList.append(entryID)
            culledEntries += entry + "\n"
    
    print "Final Entries: " + str(len(culledEntries.split("\n")))

with open(workingDirectory + "allEntries" + "_culled" + ".txt", 'w') as f:
    f.write(culledEntries)
    f.close()