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

page = fetch(baseURL)

#print page


#parse HTML structure using Beautiful Soup

from bs4 import BeautifulSoup

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
