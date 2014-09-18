#API test code

#2/place/pois/photos
#"https://api.weibo.com/2/place/pois/photos.json?access_token=2.00juYUmF0dYhVk4f50df99a8UEuKkD&poiid=B2094757DA6EA4FD4092&count=50&page=1"

#investigate structure of output json file
#if necessary use external parsing tool such as the one here: http://json.parser.online.fr/


#variable-based url generator

baseURL = "https://api.weibo.com/2/place/pois/photos.json"
access_token = "2.00juYUmF0dYhVk4f50df99a8UEuKkD"
poiid = "B2094757DA6EA4FD4092"
count = "50"
page = "1"

url = baseURL + "?" + "access_token=" + access_token + "&poiid=" + poiid + "&count=" + count + "&page=" + page
print url


#downloading result from web

import urllib2

response = urllib2.urlopen(url, timeout = 30)
data = response.read()
#print data


#parsing json for data

import json

parsedData = json.loads(data)
numPosts = parsedData["total_number"]
print "total number of posts: " + numPosts


#getting all posts as a list

posts = parsedData['statuses']
print len(posts)


#loop through data 

#for post in posts:
#    print post["user"]["id"]


#iterating through multiple pages
#create function for downloading page

import time

def fetch(url):
    response = urllib2.urlopen(url, timeout = 30)
    data = response.read()
    parsedData = json.loads(data)
    time.sleep(24) #delay after each download to ensure you don't exceed rate limits
                   #for weibo this should be (60 min * 60 sec) / 150 times per hour = 24 sec

    return parsedData


#loop through pages after finding out the total number of posts

import math

numPages = int(math.ceil(float(numPosts) / float(count)))
print "number of pages: " + str(numPages)


for i in range(numPages):
    page = str(i + 1) #remember i starts at 0
    url = baseURL + "?" + "access_token=" + access_token + "&poiid=" + poiid + "&count=" + count + "&page=" + page
    
    parsedData = fetch(url)
    posts = parsedData['statuses']
    
    for post in posts:
        print post["user"]["id"]
    
    print "-----"
    print "number of posts in page: " + str(len(posts))
    print "finished page " + page


#export data to file

workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 3\\demo\\"
fileName = workingDirectory + "data.txt"

with open( fileName, 'wb' ) as f:

    for i in range(numPages):
        page = str(i + 1) #remember i starts at 0
        url = baseURL + "?" + "access_token=" + access_token + "&poiid=" + poiid + "&count=" + count + "&page=" + page
        
        parsedData = fetch(url)
        posts = parsedData['statuses']
        
        for post in posts:
            try: #explain try/except statements, their advantages with messy data, and disadvantages for debugging
                f.write( post["user"]["id"] + "\n") #add "\n" for return
            except:
                print "no user information"
        
        print "number of posts in page: " + str(len(posts))
        print "finished page " + page


#export headings and multiple columns of data with delimitor

delim = ";"

with open( fileName, 'wb' ) as f:
    
    f.write(delim.join(["user_id", "comment"]) + "\n")

    for i in range(numPages):
        page = str(i + 1) #remember i starts at 0
        url = baseURL + "?" + "access_token=" + access_token + "&poiid=" + poiid + "&count=" + count + "&page=" + page
        
        parsedData = fetch(url)
        posts = parsedData['statuses']
    
        for post in posts:
            try:
                userID = str(post["user"]["id"]) #cast to string to make sure data does not come in as numbers
            except:
                userID = ""
            
            try:
                comment = post["text"]
            except:
                comment = ""
                
            entry = delim.join([userID, comment]) + "\n"
            f.write( entry.encode('utf-8') )
        
        print "number of posts in page: " + str(len(posts))
        print "finished page " + page
