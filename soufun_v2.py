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
import datetime
import requests

import socket
socket.setdefaulttimeout(60)

delim = ';'
date = '20160314'

summary = []

def fetch(url):
    
    fetchFail = True
    failCount = 0
    while fetchFail:
        try:
            #data = urlretrieve(url, 'myfile')
            
            
            #data = gzip.open('myfile', 'rb').read()
            
            # try:
            # data = urlretrieve(url, 'myfile')
            # data = gzip.open('myfile', 'rb').read()
            # data_decoded = data.decode('gbk')
            r = requests.get(url, timeout=20.0)
            data_decoded = r.text
                
            #data = urllib.urlopen(url)
            #text = data.read()
                
            
            # except:
            #     #data_decoded = data
            #     print("error decoding")
                
            #     response = urllib2.urlopen(url, timeout = 15)
            #     data = response.read()
            #     data_decoded = data.decode('gbk')
                
            fetchFail = False
        except Exception as e:
            failCount += 1
            print "attempt " + str(failCount) + " failed: " + url
        #    #print e
            print "sleeping for 1 seconds before retrying..."
        #    
            if failCount >= 20:
                return ""
        #    
            time.sleep(1)
    
    return data_decoded


def stringReplacer(toReplace, string, replaceWith):
    for s in toReplace:
        string = string.replace(s, replaceWith)
    return string

toReplace = [delim, '\\', '\'', '\"']
replaceWith = '-'
    
def extract_data(data, cityNameChinese):
    
    d = {}
        
    try:
        s = data.findChildren('p', 'title')[0].findChildren()[0].string.strip() #title 
        d['title'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['title'] = ""
    try:
        s = '-'.join([i.string.strip() for i in data.findChildren('p', 'gray6 mt20')[0].findChildren('a')])  #development
        d['development'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['development'] = ""
    try:
        s = data.findChildren('p', 'gray6 mt12')[0].findChildren('span')[-1]['title'] #address
        d['address'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['address'] = ""
    try:
        s = data.findChildren('p', 'gray6 mt15')[1].findChildren('span', 'gray9 pr10')[0].text.strip() #details
        d['details'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['details'] = ""
    try:
        s = data.findChildren('p', 'font16 mt20 bold')[0].text.strip() #description
        d['description'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['description'] = ""
    try:
        s = data.findChildren('span', 'price')[0].string.strip() #price
        d['price'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['price'] = ""
    try:
        s = data.findChildren('p', 'title')[0].findChildren()[0].get('href') #link
        d['link'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['link'] = ""
    try:
        s = data.findChildren('p', 'gray6 mt10')[1].findChildren('span', 'pr10')[0].findChildren('a')[0].text.strip() #realtor
        d['realtor'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['realtor'] = ""
    try:
        s = data.findChildren('span', 'iconPerson')[0].text.strip() #renter
        d['renter'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['renter'] = ""

    try:
        s = data.findChildren('span', 'gray9 pr10')[0].text.strip() #updated
        d['updated'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['updated'] = ""
    
    try:
        s = data.findChildren('span', 'note colorGreen')[0].text.strip() #notes-green
        d['notes1'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['notes1'] = ""
    
    try:
        s = data.findChildren('span', 'note colorRed')[0].text.strip() #notes-red
        d['notes2'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['notes2'] = ""
    
    try:
        s = data.findChildren('span', 'note colorBlue')[0].text.strip() #notes-blue
        d['notes3'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['notes3'] = ""
    
    try:
        s = data.findChildren('span', 'note subInfor')[0].text.strip() #notes-sub
        d['notes4'] = stringReplacer(toReplace, s, replaceWith)
    except:
        d['notes4'] = ""
        
    t1 = str(time.time())
    t2 = str(datetime.datetime.now().isoformat())
    
    L = cityNameChinese + delim + d['title'] + delim + d['development'] + delim + d['address'] + delim + d['details'] + delim + d['description'] + delim + d['price'] + delim + d['link'] + delim + t1 + delim + t2 + delim + d['realtor'] + delim + d['renter'] + delim + d['updated'] + delim + d['notes1'] + delim + d['notes2'] + delim + d['notes3'] + delim + d['notes4']

    L = L + "\n"
    
    encoded = L.encode('utf-8')
    return encoded


def fetch_items(page, house_listings, cityNameChinese):
    #global keepLooking

    try:
        soup = BeautifulSoup(page.split('<!--houseList star-->', 1)[1].split('<!--houseList end-->', 1)[0])
        houses = soup.findAll('dl')
        houses = [x for x in houses if x.findChildren()]
    except:
        print "error getting houses"
        return house_listings
    
    if len(houses) == 0:
        print "no items found"
        return house_listings

    for house in houses:
        house_listings.append(extract_data(house, cityNameChinese))

    return house_listings
    

def fetchPages(page, house_listings, cityNameChinese, pages, baseURL, startNum, upperRange, city):
    
    house_listings = fetch_items(page, house_listings, cityNameChinese)
            
    for j in range(2,int(pages)+1):
        
        url = baseURL.format(city, startNum+1, upperRange, j)
        print url
        page = fetch(url)
        #soup = BeautifulSoup(page)
        
        house_listings = fetch_items(page, house_listings, cityNameChinese)
        
        print "page number completed: " + "(" + city + ") " + str(j)
        
    return house_listings



workingDirectory = "D:\\DMC\\03_Data\\"+date+"\\"
# workingDirectory = "C:\\Users\\danil\\Desktop\\DMC\\03_Data\\"+date+"\\"

def main(city_name, coreURL, cityNameChinese):
    
    minStep = 10
    resultsPerPage = 30
    maxPages = 100
    startNum = 0
    # startNum = 1920
    maxNum = 200000
    
    maxStep = minStep * 10000
    step = minStep * 1
    
    gotItems = 0
                
    baseURL = coreURL + "house{0}/c2{1}-d2{2}-i3{3}-l310/"
    
    while startNum < maxNum:

        file_name = "soufun_" + city_name + "_" + date + "_" + str(startNum) + ".txt"
        local_file = workingDirectory + file_name
        
        #house_listings = []
    
        upperRange = (startNum+step) % (maxNum+step)
        print "starting range: " + str(startNum+1) + " to " + str(upperRange)
        url = baseURL.format("", startNum+1, upperRange, 1)
        
        print url
    
        # try:
        page = fetch(url)
                
        try:
            pageCut = page.split('<!--fenye star-->')[1].split('<!--fenye end-->')[0]
            soup = BeautifulSoup(pageCut)
            pages = soup.findChildren('div', 'fanye')[0].findChildren('span', 'txt')[0].text.strip()[1:-1]

        except:
            soup = BeautifulSoup(page)
            try:
                pages = soup.findChildren('div', 'fanye')[0].findChildren('span', 'txt')[0].text.strip()[1:-1]
            except IndexError:
                print "error in page numbers..."
                pages = 1
                # continue
        
        # pages = math.ceil(float(items) / resultsPerPage)
        print "number of pages in range: " + str(pages)
        # except:
        #     print "no results in range"
        #     startNum = startNum + step
        #     if step < maxStep:
        #         step = step * 10
        #         print 'increasing step size to: ' + str(step)
        #         #step = step * 10
                
            # continue
        
        if int(pages) >= maxPages:
            
            if step <= minStep:
                
                print "starting city-based search" 
                
                try:
                    soup = BeautifulSoup(page.split("<dl class=\"search-list clearfix\">")[1].split("</dl>")[0])
                except IndexError:
                    #sometimes
                    soup = BeautifulSoup(page.split("<div class=\"qxName\">")[1].split("</div>")[0])
                cities = ['-' + link.get('href').split('/')[1].split('-')[1] for link in soup.findAll('a')[1:]]
                
                print cities
                
                house_listings = []
                
                for city in cities:
                    print "starting city: " + city
                    
                    try:
                        url = baseURL.format(city, startNum+1, upperRange, 1)
                        print url
                        page = fetch(url)
                        soup = BeautifulSoup(page)
                    
                        pagesCity = soup.findChildren('div', 'fanye')[0].findChildren('span', 'txt')[0].text.strip()[1:-1]
                        
                        # pagesCity = math.ceil(float(items) / resultsPerPage)
                        # pagesCity = min(pagesCity, 100)
                        print "number of pages in range: " + str(pagesCity)
                        
                        print 'getting {} pages'.format(str(pagesCity))
                        
                    except:
                        print "no results in range"
                        continue
                
                    
                    house_listings = fetchPages(page, house_listings, cityNameChinese, pagesCity, baseURL, startNum, upperRange, city)
                    gotItems += float(len(house_listings))
                
            else:
                step = step / 10
                print 'decreasing step size to: ' + str(step)
                #step = step/10
                continue
                    
    
        else:
            
            print 'getting {} pages'.format(str(pages))
            # gotItems += float(resultsPerPage * pages)
            
            house_listings = fetchPages(page, [], cityNameChinese, pages, baseURL, startNum, upperRange, "")  
            gotItems += float(len(house_listings))
                            
        startNum = startNum + step
        
        if int(pages) < 2:
            if step < maxStep:
                step = step * 10
                print 'increasing step size to: ' + str(step)
                #step = step * 10
      
        if len(house_listings) > 0:  
            with open(local_file, 'wb') as f:
                categories = "City;Title;Development;Address;Details;Description;Price;link;time;timeFormat;Realtor;Renter;Updated;notes1;notes2;notes3;notes4\n"
                f.write(categories)
                
                for listing in house_listings:
                    f.write(listing)

    print "got {} items from {}".format(int(gotItems), city_name)
    print "job complete: " + city_name
    summary.append( "got {} items from {}".format(int(gotItems), city_name) )

#sys.exit()

url = 'http://zu.fang.com/cities.aspx'
page = fetch(url)
soup = BeautifulSoup(page)

links = soup.findAll('div','onCont')[0].findAll('a', class_='red')
        
cities = [link.get('href') for link in links]
cityNamesChinese = [link.string for link in links]
cityNames = [link.split('.')[1] for link in cities]

#SH 81
cities = cities[:]
cityNamesChinese = cityNamesChinese[:]
cityNames = cityNames[:]

for i, cityName in enumerate(cityNames):
    main(cityName, cities[i], cityNamesChinese[i])

with open(workingDirectory + "summary.txt", 'wb') as f:
    for s in summary:
        f.write(s + "\n")


