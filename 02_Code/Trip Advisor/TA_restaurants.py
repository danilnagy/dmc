import time, csv, math, re, urllib2, sys
from bs4 import BeautifulSoup
import json

def fetch(url):

    fetchFail = True
    failCount = 0
    while fetchFail:
        try:
            response = urllib2.urlopen(url)
            data = response.read()
                
            fetchFail = False
        except Exception as e:
            failCount += 1
            print "attempt " + str(failCount) + " failed"
            print "sleeping for 1 seconds before retrying..."
            
            if failCount >= 5:
                return ""
            
            time.sleep(1)
    
    return data

def extract_data(data):

    global L

    L = ""

    baseUrl = "http://www.tripadvisor.com/"
    website = baseUrl + data.findChildren('a')[0]['href']
    title = data.findChildren('a')[0].string.strip()

    try:
        category = data.findChildren('div', 'information cuisine')[0].text.strip()[10:]
    except Exception as e:
        category = ""

    try:
        mapString = data.findChildren('div', 'resources')[0].findChildren()[0]['onclick']
        strIndexes = [(a.start(), a.end()) for a in list(re.finditer(',', mapString))]
        latitude = mapString[strIndexes[3][1]+2:strIndexes[4][0]-1]
        longitude = mapString[strIndexes[4][1]+2:strIndexes[5][0]-1]
    except Exception as e:
        latitude = '0'
        longitude = '0'

    if latitude == 'hi':
        latitude = '0'
        longitude = '0'



    try:
        ratingString = data.findChildren('div', 'rs rating')[0].findChildren('img')[0]['alt']
        rating = ratingString
    except Exception as e:
        rating = '0'


    print("restaurant name: " + title)
    print("cuisine: " + category)
    print("site latitude: " + latitude)
    print("site longitude: " + longitude)
    print("site rating: " + rating + " of 5 stars")

    L = L + title + delim
    L = L + category + delim
    L = L + rating + delim

    reviews_wrapper(website, latitude, longitude)

    L = L + "\n"

    print("_______")

    #print L
    #sys.exit()

    try:
        f.write(L)
    except Exception as e:
        L = L.encode('utf-8')
        f.write(L)
    return L

    
def extract_review(data):

    global L

    try:
        name = data.findChildren('div', 'username mo')[0].text.strip()
        print name
        L = L + name + delim

        location = data.findChildren('div', 'location')[0].text.strip()
        print location
        L = L + location + delim
        
        return name
    
    except Exception as e:
        #print "unrecognized member"
        return None

def reviews_wrapper(url, latitude, longitude):

    global L

    page = fetch(url)
    soup = BeautifulSoup(page)

    try:
        street_address = soup.findAll('span', 'street-address')[0].text.strip()
    except:
        street_address = ""
    try:
        locality = soup.findAll('span', 'locality')[0].text.strip()
    except:
        locality = "Shenzhen"
    try:
        country = soup.findAll('span', 'country-name')[0].text.strip()
    except:
        locality = "China"
    address = street_address + ', ' + locality + ', ' + country
    
    print("site address: " + address)

    
    if latitude == '0':
        
        #generate request URL from components
        requestURL = "http://maps.googleapis.com/maps/api/geocode/json?address="+address+"&sensor=false"
        requestURL = requestURL.replace(" ","%20")
        
        print requestURL

        encoded = fetch(requestURL)
        decoded = json.loads(encoded)

        try:
            coords = decoded['results'][0]['geometry']['location']
        except Exception as e:
            coords = {'lat':0, 'lng':0}

        latitude = str(coords['lat'])
        longitude = str(coords['lng'])

        print 'glat: ', latitude
        print 'glng: ', longitude

    
    
    try:
        reviewsNum = soup.findAll('label', attrs={'for': 'sortOrder'})[0].string.strip()[:-18]
    except:
        reviewsNum = '1'

    print(reviewsNum + " reviews for site")

    L = L + address + delim
    L = L + reviewsNum + delim
    
    L = L + latitude + delim
    L = L + longitude + delim

    return ""   #escape out of reviews

    keepLooking = True

    while keepLooking:
        url = fetch_reviews(url)
        if url == None:
            keepLooking = False
    

def fetch_reviews(url):

    page = fetch(url)
    #print url

    soup = BeautifulSoup(page)
    reviews = soup.findAll('div', 'reviewSelector')
    reviews = [x for x in reviews if x.findChildren()]

    if len(reviews) == 0:
        print "end of range"
        return None

    noReview = True
    for s in reviews:
        review = extract_review(s)
        if review != None:
            noReview = False

    time.sleep(1)
    
    baseUrl = "http://www.tripadvisor.com"

    try:
        nextLink = soup.findAll('a', 'guiArw sprite-pageNext ')[0]['href'].strip()
        print nextLink
        return baseUrl + nextLink
        
    except Exception as e:
        print 'end of reviews'
        return None

    

def fetch_items(url):

    global keepLooking

    page = fetch(url)
    soup = BeautifulSoup(page)
    listings = soup.findAll('div', 'listing')
    listings = [x for x in listings if x.findChildren()]

    attraction_listings = []
    
    if len(listings) == 0:
        print "end of range"
        keepLooking = False
        return None

    noListings = True
    for s in listings:
        listing = extract_data(s)
        if listing != None:
            noListings = False

    if noListings:
        keepLooking = False

    time.sleep(1)
    

#START COLLECTION CODE


delim = ";"
city_name = 'BJ'
date = '20140710'

workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Trip Advisor Data\\data\\"+city_name+"\\"+date+"\\"
file_name = "TA_" + city_name + "_" + date + ".txt"
local_file = workingDirectory + file_name

urlList = [
"http://www.tripadvisor.com/Restaurants-g294212-oa{0}-Beijing.html"
    ]

for urlBase in urlList:

    f = open(local_file, 'w')

    categories = "Name;Category;Rating;Location;Number of Reviews;lat;lng\n"
    #f.write(categories)

    attraction_listings = []

    L = ""

    j = 0

    url = urlBase.format(0)
    
    page = fetch(url)
    soup = BeautifulSoup(page)
    
    resultNum = soup.findAll('span', 'pgCount')[0].findAll('i')[0].string.strip()
    resultNum = re.sub("[^0-9]", "", resultNum)
    
    print "number of results in section: ", resultNum

    keepLooking = True

    numTimes = int(math.floor(float(resultNum) / 30)) + 1

    print "number of pages: ", numTimes

    #j += 3900
    
    for k in range(numTimes):
        
        url = urlBase.format(j)
        fetch_items(url)
        
        print "page ", J/30, " out of ", numTimes, "completed"
        f.close()
        f = open(local_file, 'a')

        j += 30

        
    f.close()


