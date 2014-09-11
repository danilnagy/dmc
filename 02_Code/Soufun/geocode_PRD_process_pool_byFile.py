import multiprocessing
import time
import random
import sys
import json

import urllib2
import urllib

from os import walk

def calculate(func, args):
    result = func(args)
    return result

def geocode(entry):
    data = entry.split(";")
    
    try:
        address = data[3]+data[2]+data[1]
    except:
        return ""
    
    geo = extract_address(address)
	
    entry = entry + delim + str(geo['lat']) + delim + str(geo['lng']) + delim + str(geo['precision']) + delim + str(geo['confidence'])
    entry = entry + "\n"
    
    return entry
    
###

def fetchURL(url):
	try:
	    response = urllib2.urlopen(url)
	    return response
	except:
	    return ""
	    
	
#Baidu Geocode
def urlEncoder(a):
	try:
		encoded = urllib.urlencode({'':a})
		return encoded[1:]
	except Exception as e:
		print "not encoded"

def extract_address(street):	

    #cities = {'SZ':"%E6%B7%B1%E5%9C%B3",
    # 'GZ':"%E5%B9%BF%E5%B7%9E",
    # 'DG':"%E4%B8%9C%E8%8E%9E",
    # 'FS':"%E4%BD%9B%E5%B1%B1",
    # 'HZ':"%E6%83%A0%E5%B7%9E",
    # 'JM':"%E6%B1%9F%E9%97%A8",
    # 'SD':"%E9%A1%BA%E5%BE%B7",
    # 'ZH':"%E7%8F%A0%E6%B5%B7",
    # 'ZS':"%E4%B8%AD%E5%B1%B1",
    # 'ZQ':"%E8%82%87%E5%BA%86"}

    #cities.get(cityName, "%E6%B7%B1%E5%9C%B3")
    #city = cities.get('FS')

    #city = "%E4%BD%9B%E5%B1%B1" #FS
	
    #city = "%E5%8C%97%E4%BA%AC" # BJ
    
    baseURL = "http://api.map.baidu.com/geocoder?"
    apikey = "0Ad9502dc64485a3e583adbb3112ec90"
    
    request = baseURL + "address="+ urlEncoder(street) +"&output=json"+"&key="+apikey #+"&city="+urlEncoder(city)
    response = fetchURL(request)
    
    try:
        data = response.read()
        decoded = json.loads(data)
        
        coords = decoded['result']['location']
        coords["precision"] = decoded['result']['precise']
        coords["confidence"] = decoded['result']['confidence']
    except Exception as e:
        coords = {'lat' : 0, 'lng' : 0,  'precision': 0,  'confidence': 0}

    print coords
    sys.exit()
            
    return coords

###

delim = ';'

def run():

    workingDirectory = 'C:\\Users\\Danil\\Documents\\Teaching\\DMC\\China Creative City\\03_Data\\Soufun\\PRD\\housing\\20140831\\'
    scanDirectory = workingDirectory + 'raw data\\HZ\\'

    fileNames = []
    for (dirpath, dirnames, filenames) in walk(scanDirectory):
        fileNames.extend(filenames)
        break
    
    first = True
    
    for fileName in fileNames:

        cityName = fileName[7:9]
    
        with open(scanDirectory + fileName, 'r') as f:
            data = f.read()
            entries = data.split("\n")
    
        file_name = "geocoded_" + fileName
        local_file = workingDirectory + "coded\\" + file_name
        
        with open(local_file, 'wb') as f:
            
            if first:
                f.write(entries.pop(0)+'\n')
                first = False
        
        
            #for entry in entries:

            # Create pool
        
            PROCESSES = 16
            
            print 'Creating pool with %d processes' % PROCESSES
            pool = multiprocessing.Pool(PROCESSES)
            print 'pool = %s' % pool
            print

            #e = entries.pop(0) + delim + cityName
            
            TASKS = [(geocode, entries.pop(0) ) for i in range(len(entries))]
            results = [pool.apply_async(calculate, t) for t in TASKS]
        
            #print 'Ordered results using pool.apply_async():'
            for r in results:
                try:
                    line = r.get(timeout=20)
                    if line is not None:
                        f.write(line)
                    else:
                        print "None Object"
                except:
                    print "exception"
                #print '\t', line
               	                
            pool.terminate()
            pool.join()
        
            for worker in pool._pool:
                assert not worker.is_alive()
        
            print 'terminate() succeeded\n'
            print fileName + " finished"

            #sys.exit()

    print "job complete"
    
    
if __name__ == '__main__':
    multiprocessing.freeze_support()

    assert len(sys.argv) in (1, 2)

    if len(sys.argv) == 1 or sys.argv[1] == 'processes':
        print ' Using processes '.center(79, '-')
    elif sys.argv[1] == 'threads':
        print ' Using threads '.center(79, '-')
        import multiprocessing.dummy as multiprocessing
    else:
        print 'Usage:\n\t%s [processes | threads]' % sys.argv[0]
        raise SystemExit(2)

    run()
