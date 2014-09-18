baseURL = "http://zu.sz.fang.com/house/" #explore the website's structure in Chrome's developoer tools

#download website's HTML using python

import urllib
import gzip
import time

def fetch(url):
    print url #print url to console for debugging
    
    urllib.urlretrieve(url, 'myfile')
    data = gzip.open('myfile', 'rb').read()
    
    time.sleep(1)
    return data.decode('gbk')
'''  
page = fetch(baseURL)

#print page


#parse HTML structure using Beautiful Soup
'''
from bs4 import BeautifulSoup
'''
soup = BeautifulSoup(page)

#show where to locate identifiers in Chrome
print soup.findAll('span','org bold') #parse HTML for tag, this returns a list
print "-----"
print soup.findAll('span','org bold')[0] #get first item in list
print "-----"
print soup.findAll('span','org bold')[0].string #get text contents from item
print "-----"
print soup.findAll('span','org bold')[0].string.strip() #strip item of all leading and trailing spaces (cleanup)
print "-----"

items = soup.findAll('span','org bold')[0].string.strip() #final query
print "number of listing in city: " + items


#extract listings from page

listings = soup.find('div', 'houseList').findAll('dl')
print "number of listing on page: " + str(len(listings))


#loop through listings and extract information

for listing in listings:
    name = listing.findChildren('p', 'title')[0].findChildren()[0].string.strip() #name
    price = listing.findChildren('span', 'price')[0].string.strip() #name
    
    print "name: " + name + "; price: " + price
'''

#generating new URL with filtering to reduce total listings below maximum pages allowed

baseURL = "http://zu.sz.fang.com/house/c2{0}-d2{1}/" #click through website to show changing format
newURL = baseURL.format(0, 250) #build new url from format
print newURL


#getting new number of listings in filtered set

page = fetch(newURL)
soup = BeautifulSoup(page)

items = soup.findAll('span','org bold')[0].string.strip() #final query
print "number of listing in filtered selection: " + items


#calculating number of pages

import math

listingsPerPage = 36
numPages = int(math.ceil(float(items) / listingsPerPage))

print "number of pages in filtered selection: " + str(numPages)


#looping through pages and building dynamic url addresses

baseURL = "http://zu.sz.fang.com/house/c2{0}-d2{1}-i3{2}/" #click on next pages to show url structure
'''
for i in range(numPages):
    newURL = baseURL.format(0, 250, i+1) #remember i starts at 0
    
    page = fetch(newURL)
    soup = BeautifulSoup(page)
    
    listings = soup.find('div', 'houseList').findAll('dl')
    print "number of listing on page: " + str(len(listings))
    
    for listing in listings:
        name = listing.findChildren('p', 'title')[0].findChildren()[0].string.strip() #name
        price = listing.findChildren('span', 'price')[0].string.strip() #name
        
        print "name: " + name + "; price: " + price
'''    
        
#export data to file

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






