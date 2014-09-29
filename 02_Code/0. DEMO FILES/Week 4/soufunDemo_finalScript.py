#Web Scraping demo code

#Danil Nagy, 2014
#Data Mining the City, Fall 2014
#Columbia University GSAPP

import urllib
import gzip
import time
from bs4 import BeautifulSoup
import math

def fetch(url):
    print url #print url to console for debugging
    
    urllib.urlretrieve(url, 'myfile')
    data = gzip.open('myfile', 'rb').read()
    
    time.sleep(1)
    return data.decode('gbk')
    

#start main code

baseURL = "http://zu.sz.fang.com/house/c2{0}-d2{1}-i3{2}/" #click on next pages to show url structure
newURL = baseURL.format(0, 250, 1)

page = fetch(newURL)
soup = BeautifulSoup(page)

items = soup.findAll('span','org bold')[0].string.strip() #final query
print "number of listing in filtered selection: " + items


listingsPerPage = 36
numPages = int(math.ceil(float(items) / listingsPerPage))

print "number of pages in filtered selection: " + str(numPages)


workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\Fall, 2014\\Week 3\\demo\\"
fileName = workingDirectory + "data_soufun.txt"

delim = ";"

with open( fileName, 'wb' ) as f:
    
    f.write(delim.join(["name", "price"]) + "\n")

    
    for i in range(numPages):
        newURL = baseURL.format(0, 250, i+1) #remember i starts at 0
        
        page = fetch(newURL)
        soup = BeautifulSoup(page)
        
        listings = soup.find('div', 'houseList').findAll('dl')
        print "number of listing on page: " + str(len(listings))
        
        for listing in listings:
            name = listing.findChildren('p', 'title')[0].findChildren()[0].string.strip() #name
            price = listing.findChildren('span', 'price')[0].string.strip() #name
            
            entry = delim.join([name, price]) + "\n"
            f.write( entry.encode('utf-8') )



#EXERCISE: adapt this code to store the address of each listing
#EXTRA CHALLENGE: adapt this code to automatically loop through different filters to capture all of Shenzhen's listings




