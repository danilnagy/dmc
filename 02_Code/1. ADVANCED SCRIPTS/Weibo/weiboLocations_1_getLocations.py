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

#data = data[8500:]

accessTokens = ("2.00Oe8rnCG3bvrCca5471c55cLiZmSB",
"2.00Oe8rnC5_oFaCf9813055d4bxYhPD",
"2.00Oe8rnCpd_DCD12bb182aab1YDQRD",
"2.00FhBWDEbsi2hCa58289cd311mC6bD",
"2.00scObXC0ICwnR09bd41b21e0SQJgk",
"2.00Oe8rnCaG2JvC0e38bea444BonZME",
"2.00Oe8rnCYAliJE612e6edc8e0xe7Qg",
"2.00Oe8rnC0I_FiWe739a5364bTvJcaB",
"2.00Oe8rnCJpLoFDd5316a36f9IcImwC",
"2.00Oe8rnC23bgxC8d96ad7dbaULDhTB",
"2.00Oe8rnC1MhkwB6de53faa4dmqMMND",
"2.00kFI9gFwppZqD7a8d0cd57cid756D", #fetcho
"2.00WdYTgF0lC74Z92e9e27742Fjf9BE", #fetcho
"2.00hwXTgF0mqzb62fdf71880dZgVlfB", #fetcho
"2.00aYDYgFYGZf9Da7a2531e67wA2KyC", #fetcho
"2.00HfEYgFZbsjXB3f305b2e04AoQ7DE", #fetcho
"2.00yvFYgFlB42XBfd98ddf6f0bY4H5B", #fetcho
"2.00oRRZgFjYiyaB8367d184d50W_hj3", #fetcho
"2.00n1HYgFVYSoeD2ec7f5fdb5dK8olC", #fetcho
"2.00MwxWgF8MkYDD3a2c474670K_zMtD", #fetcho
"2.00dxIYgF0AkoCc852244291eWGoyJE", #fetcho
"2.00iI7ZgFOEnO4D72e055314d3c1msC", #fetcho
"2.00fiPYgFlIpsDC5c6cb6a2910xX5nY", #fetcho
"2.00g8FXgF4JV3VB4e71d25b33KIBy4B", #fetcho
"2.007GGXgFmekRkC0332e52313xfvAGD", #fetcho
"2.00NIJXgFfVZFuB75d40f65de0MF9Gr", #fetcho
"2.00Q4UagFMi2dyDc5506f2c1708WLlw", #fetcho
"2.002SCdgFkanLZC5a38d96a5eCnKBcC", #fetcho
"2.00g7jggF8Q66QE246be290a3UFQOLC", #fetcho
"2.009BafgFXkzLlC9cce59ff287N3UUD", #fetcho
"2.00M3kggF0roYO4808b32662c0q5WiG", #fetcho
"2.00nx6egFUY8RCC0cbd110ff4gXtDIC", #fetcho
"2.005S9ZgFilzN_Ca950937ea0S8tAhD", #fetcho
"2.00elXUgF0IVe_vfa28588d0ehAfsfB") #tianran

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

