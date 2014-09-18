import time
import csv
import sys
import urllib2
import json
import math

workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\"
fileName = "02_Code\\Weibo\\PRD_grids_500"
fileExt = ".csv"

data = []

with open( workingDirectory+fileName+fileExt, 'rb' ) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        data.append(row)

authCodeDirectory = "C:\\Users\\Danil\\Documents\\GIT\\dmc\\02_Code\\1. ADVANCED SCRIPTS\\Weibo\\"
fileName = authCodeDirectory + "authCodes.txt"

#GET ACCESS TOKENS FROM FILE
accessTokens = []

with open( fileName, 'rb' ) as f:
    data = f.read()
    codes = data.split("\n")
    
    for code in codes:
        accessTokens.append( code.strip() )
    

### FUNCTIONS ###

def checkRate(accessToken):
	global tokenRates

	count = tokenRates[accessToken]['counter']
	timePrev = tokenRates[accessToken]['record'][(count + 1) % rateLimit]

	if timePrev != 0:
		timeElapsed = time.time() - timePrev
		print "time elapsed: " + str(timeElapsed)
		if timeElapsed < maxTime:
			print "limit reached, delaying " + str(maxTime-timeElapsed) + " seconds."
			time.sleep(maxTime-timeElapsed)

def addTime(accessToken):
        global tokenRates
        
	count = (tokenRates[accessToken]['counter'] + 1) % rateLimit
	tokenRates[accessToken]['counter'] = count
	
	tokenRates[accessToken]['record'][count] = time.time()


def fetch(url, accessToken):
        global currentToken
        global accessTokens

	failLength = 0
	fetchFail = True

	while fetchFail:
		try:
			checkRate(currentToken)
			response = urllib2.urlopen(url, timeout = 30)
			data = response.read()
			fetchFail = False
		except:
			failLength += 1
			if failLength > 5:
				print "FAILED PERMANENTLY!!"
				return None
			print "failed to fetch data"
			addTime(currentToken)
			indx = accessTokens.index(currentToken)
	                currentToken = accessTokens[(indx+1) % len(accessTokens)]

	addTime(currentToken)
	
	indx = accessTokens.index(currentToken)
	currentToken = accessTokens[(indx+1) % len(accessTokens)]

	return data

	
def searchLocation(j, data, accessToken):

	lat = str(data[1])
	lng = str(data[2])

	request = baseUrlLoc + '&access_token=' + accessToken + '&lat=' + lat + '&long=' + lng + '&range=' + rng + '&page=' + str(j+1) + '&count=' + str(count)
    
	print request
	print '------'
	print 'page: ' + str(j)

	encodedPage = fetch(request, accessToken)
	decodedPage = json.loads(encodedPage)

	if len(decodedPage) == 0:
		print 'no results'
		return ""
	else:
		try:
			number = decodedPage['total_number']
			print 'total number of listings: ' + str(number)
		except Exception as e:
			print 'ERROR IN RESULTS'
			return ""

	pois = decodedPage['pois']

	results = ""

	for k in range(len(pois)):
		item = pois[k]

		try:
 			entry = (item['poiid'] + delim + 
			item['title'] + delim + 
			item['address'] + delim + 
			item['lat'] + delim + 
			item['lon'] + delim + 
			item['city'] + delim + 
			item['category'] + delim + 
			item['category_name'] + delim + 
			item['categorys'] + delim + 
			str(item['checkin_num']) + delim + 
			str(item['checkin_user_num']) + delim + 
			str(item['herenow_user_num']) + delim + 
			str(item['photo_num']) + delim + 
			str(time.strftime('%c')) + delim + 
			str(time.time()) + "\n")
					
		except Exception as e:
			print "location fail"
			entry = ""

		print "found location: " + item['poiid']
		
		results += entry.encode('utf-8')
		
	pages = int(math.ceil(float(number) / float(count)))
	print 'total pages: ' + str(pages) + ' page number: ' + str(j)
	
	#recurse through remaining pages
	if j < pages - 1:
		results += searchLocation(j+1, data, accessToken)
		
	print 'done page: ' + str(j)
	return results

	
rng = "400"
count = 50
delim = ";"

baseUrlLoc = "https://api.weibo.com/2/place/nearby/pois.json?"

rateLimit = 5
maxTime = 150

tokenRates = {}
for token in accessTokens:
	tokenRates[token] = {}
	tokenRates[token]['record'] = [0] * rateLimit
	tokenRates[token]['counter'] = 0
	
currentToken = accessTokens[0]

results = ""

local_files = []

cityName = "PRD"
date = "20140830"

saveDirectory = workingDirectory + "03_Data\\Weibo\\" + cityName + "\\" + date + "\\01_locations\\"

fileCount = 0
filePrefix = "weibo_" + cityName + "_" + date + "_"
fileName = saveDirectory + filePrefix + str(fileCount) + ".txt"
f = open( fileName, 'wb' )
f.write("poiid;title;address;lat;lon;city;category;category_name;categorys;checkin_num;checkin_user_num;herenow_user_num;photo_num;time;time_standard\n")

results = ""

data.pop(0)

iter_count = 0
fileMod = 500

#for entry in data[fileCount:]:
for entry in data:

		iter_count += 1
		
		print 'starting location: ' + entry[0] + " at: " + entry[2] + " " + entry[1] + " on token: " + currentToken
		results += searchLocation(0, entry, currentToken)
		print "-----"

		if iter_count % fileMod == 0:
				f.write(results)
				f.close()

				print "writing file: " + fileName
				
				fileCount += fileMod
				fileName = saveDirectory + filePrefix + str(fileCount) + ".txt"
				f = open( fileName, 'wb' )
				
				results = ""

		if len(data) == 0:
			keepRunning = False
			break
			

f.write(results)
f.close()

print "writing file: " + fileName

print " "
print "JOB COMPLETE"

