# -*- coding: utf-8 -*-
import time, urllib2
import urllib
from urllib import urlretrieve
import gzip
from bs4 import BeautifulSoup
import json
import sys
import re
import math

import socket
socket.setdefaulttimeout(60)

delim = ';'
city_name = 'SD'
date = '20140831'

def fetch(url):
    
    fetchFail = True
    failCount = 0
    while fetchFail:
        try:
            urlretrieve(url, 'myfile')
            data = gzip.open('myfile', 'rb').read()
            
            try:
                data_decoded = data.decode('gbk')
            except Exception as e:
                data_decoded = data
                print("error decoding")
                
            fetchFail = False
        except Exception as e:
            failCount += 1
            print "attempt " + str(failCount) + " failed"
            print "sleeping for 1 seconds before retrying..."
            
            if failCount >= 20:
                return ""
            
            time.sleep(1)
    
    return data_decoded
    
    
def extract_data(data):
    global i
    
    d = {}
        
    try:
        d['title'] = data.findChildren('p', 'title')[0].findChildren()[0].string.strip().replace(delim,'-') #title 
    except:
        d['title'] = ""
    try:
        d['region'] = data.findChildren('p', 'gray6 mt10')[0].findChildren('a')[0].text.strip().replace(delim,'-')  #region
    except:
        d['region'] = ""
    try:
        d['location'] = data.findChildren('p', 'gray6 mt10')[0].findChildren('a')[1].text.strip().replace(delim,'-')  #location
    except:
        d['location'] = ""
    try:
        d['building'] = data.findChildren('p', 'gray6 mt10')[0].findChildren('a')[2].text.strip().replace(delim,'-')   #development
    except:
        d['building'] = ""
    try:
        d['address'] = data.findChildren('p', 'gray6 mt10')[0].findChildren('span','iconAdress ml10')[0].text.replace(delim,'-') #address
    except:
        d['address'] = ""
    try:
        d['details'] = data.findChildren('p', 'gray6 mt5')[0].text.strip().replace(delim,'-') #details
    except:
        d['details'] = ""
    try:
        d['description'] = data.findChildren('p', 'gray6 mt5')[1].text.strip().replace(delim,'-') #details
    except:
        d['description'] = ""
    try:
        d['price'] = data.findChildren('span', 'price')[0].string.strip().replace(delim,'-')
    except:
        d['price'] = ""
    
    
    L = d['title'] + delim + d['region'] + delim + d['location'] + delim + d['building'] + delim + d['address'] + delim + d['details'] + delim + d['description'] + delim + d['price']
    L = L + "\n"
    
    encoded = L.encode('utf-8')
    f.write(encoded)
    
    i += 1
    return d


def fetch_items(soup):
    global keepLooking

    houses = soup.find('div', 'houseList').findAll('dl')
    houses = [x for x in houses if x.findChildren()]
    
    if len(houses) == 0:
        print "end of range"
        keepLooking = False
        return None

    noListings = True
    for house in houses:
        listing = extract_data(house)
        if listing != None:
            noListings = False

    if noListings:
        keepLooking = False

    return house_listings
    
    

#START COLLECTION CODE

house_listings = []
i = 0
minStep = 50
resultsPerPage = 35
maxPages = 100
startNum = 0
maxNum = 200000

maxStep = minStep * 100
step = minStep * 10

workingDirectory = "C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\03_Data\\Soufun\\PRD\\housing\\"+date+"\\raw data\\"
file_name = "soufun_" + city_name + "_" + date + "_" + str(startNum) + ".txt"
local_file = workingDirectory + file_name

f = open(local_file, 'wb')
    
categories = "Title;Region;Location;Building;Address;Details;Description;Price;Lat;Lng;Precision;Confidence\n"
f.write(categories)
         
baseURL = "http://zu.shunde.fang.com/house{0}/c2{1}-d2{2}-h34-i3{3}/"

while startNum < maxNum:

    upperRange = (startNum+step) % (maxNum+step)
    print "starting range: " + str(startNum+1) + " to " + str(upperRange)
    url = baseURL.format("", startNum+1, upperRange, 1)
    
    print url

    try:
        page = fetch(url)
        soup = BeautifulSoup(page)
        
        items = soup.findAll('span','org bold')[0].string.strip()
        pages = math.ceil(float(items) / resultsPerPage)
        print "number of pages in range: " + str(pages)
    except:
        print "no results in range"
        startNum = startNum + step
        if step < maxStep:
            print 'increasing step size to: ' + str(step * 10)
            step = step * 10
            
        continue
    
    if int(pages) >= maxPages:
        

        print 'decreasing step size to: ' + str(step/10)
        step = step/10
        continue
                

    else:
        
        fetch_items(soup)
        
        for j in range(2,int(pages)+1):
            
            url = baseURL.format("", startNum+1, upperRange, j)
            print url
            page = fetch(url)
            soup = BeautifulSoup(page)
            
            fetch_items(soup)
            
            print "page number completed: " + str(j)
        
    startNum = startNum + step
    
    if int(pages) < 5:
        if step < maxStep:
            print 'increasing step size to: ' + str(step * 10)
            step = step * 10
    
    f.close()
    
    file_name = "soufun_" + city_name + "_" + date + "_" + str(startNum) + ".txt"
    local_file = workingDirectory + file_name
    
    f = open(local_file, 'wb')
    

f.close()


print "job complete"




