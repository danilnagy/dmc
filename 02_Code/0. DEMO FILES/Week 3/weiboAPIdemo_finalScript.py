#API demo code

#Danil Nagy, 2014
#Data Mining the City, Fall 2014
#Columbia University GSAPP

import urllib2
import json
import time
import math

#function for downloading result data from web
def fetch(url):
    print url #print url to console for debugging
    
    response = urllib2.urlopen(url, timeout = 30)
    data = response.read()
    parsedData = json.loads(data)
    #time.sleep(24) #delay after each download to ensure you don't exceed rate limits
                   #for weibo this should be (60 min * 60 sec) / 150 times per hour = 24 sec

    return parsedData

#function for getting specific entry from data
def getEntry(data):
    try:
        userID = str(post["user"]["id"]) #get user id
    except:
        userID = "" #or if error return empty string
    
    #try:
    comment = post["text"] #get comment
    #except:
    #    comment = "" #or if error return empty string
    
    entry = delim.join([userID, comment]) + "\n"
    return entry

#start main code

#specify all required parameters for API call
baseURL = "https://api.weibo.com/2/place/pois/photos.json" #specify base url of API call
access_token = "2.00juYUmF0dYhVk4f50df99a8UEuKkD" #fill in you access token
poiid = "B2094757DA6EA4FD4092" #specify point of interest
count = "50" #specify count (should be 50 which is the maximum per page)
page = "1" #specify page number

url = baseURL + "?access_token=" + access_token + "&poiid=" + poiid + "&count=" + count + "&page=" + page #build url

parsedData = fetch(url) #get data from web
numPosts = parsedData["total_number"] #parse for specific data
print "total number of posts: " + numPosts

numPages = int(math.ceil(float(numPosts) / float(count))) #calculate number of pages in set
print "number of pages: " + str(numPages)

workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 3\\demo\\"
fileName = workingDirectory + "data.txt"

delim = ";"

with open( fileName, 'wb' ) as f: #open file for writing
    
    f.write(delim.join(["user_id", "comment"]) + "\n") #write initial heading line

    for i in range(numPages): #iterate through all pages
        page = str(i + 1) #remember i starts at 0
        url = baseURL + "?" + "access_token=" + access_token + "&poiid=" + poiid + "&count=" + count + "&page=" + page
        
        parsedData = fetch(url) #get data from web
        posts = parsedData['statuses'] #generate list of all posts
    
        for post in posts: #iterate through all posts on page
            
            entry = getEntry(post) #run function to generate entry
            f.write( entry.encode('utf-8') ) #write entry to file
        
        print "number of posts in page: " + str(len(posts)) #print status messages
        print "finished page " + page


#EXERCISE: adapt this code to store the url for the photo in the post
#EXTRA CHALLENGE: use Python to automatically download the photo to your computer