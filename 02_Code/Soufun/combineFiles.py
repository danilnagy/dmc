from os import walk

workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\03_Data\\Soufun\\PRD\\housing\\20140908\\coded\\"

fileNames = []
for (dirpath, dirnames, filenames) in walk(workingDirectory):
    fileNames.extend(filenames)
    break
    
culledEntries = ""

for fileName in fileNames:

    with open(workingDirectory + fileName, 'r') as f:
        with open(workingDirectory + "allEntries" + "_combined" + ".txt", 'a') as wf:
            wf.write(f.read())

    print '.'
