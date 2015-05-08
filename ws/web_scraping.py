# -*- coding: utf-8 -*-

''' WARNING: for some reason it only works with Python 2.7!
    This is the actual scraping file that will be executed
    on a server and query openweathermap.org for forecasts
    every day at the same time '''

from datetime import datetime
import time
import urllib3
import pickle
import urllib
import urllib.request
import json


#### FUNCTION DEFINITIONS #####################################################

def get_xml_openweathermap(city, http):
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' \
          + city \
          + '&mode=xml' \
          + '&units=metric' \
          + '&cnt=16' # 'cnt = 16' means next 16 days
    r = http.request('GET', url)
    
    print('I queried openweathermap for %s' %city)
    forecast = str(r.data)
    
    current_time = str(datetime.now())
    text_file = open(city + '_' + current_time + \
		     '_openweathermap_16_days' + '.forecast', "w")
    text_file.write(forecast)
    text_file.close()
    
    return forecast

def wundergrund_get_city_index(city):
    '''
    input must be a string, containing the city name alone
    python3!!!!!
    '''

    url = 'http://api.wunderground.com/api/3a8e74a2827886a1/geolookup/'\
    'conditions/q/DL/'+'Berlin'+'.json'
    page = urllib.request.urlopen(url)
    read = page.read()
    decoded = read.decode('utf8')
    data = json.loads(decoded)

    if "location" in data.keys():     # "location" case (ambiguity)
        return data["location"]["l"]
    else:                               # "Berlin" case (ambiguity)
        for cities in data["response"]["results"]:
            if cities["country"] == "DL":
                return cities["l"]

def wundergrund_get_10days(city):
    '''
    input must be a string, containing the city name alone
    python3!!!
    city should be in English :)
    '''

    index = wundergrund_get_city_index(city)
    url = 'http://api.wunderground.com/api/3a8e74a2827886a1/forecast10day'\
    +index+'.json'
    page = urllib.request.urlopen(url)
    read = page.read()
    decoded = read.decode('utf8')
    data = json.loads(decoded)

    print('I queried weatherunderground for %s' %city)
    current_time = str(datetime.now())
    out_file = city + '_' + current_time + \
		     '_weatherunderground_10_days' + '.forecast'
    with open( out_file, 'w') as outfile:
        json.dump(data, outfile)

# This script will essentially run forever. Every minute it checks whether
# it is currently 03:00 o'clock, and if so, it performs the scraping task.

while True:
    if time.strftime("%H") == "03" and time.strftime("%M") == "00":
        for city in cities_only:
            print city
            get_xml_openweathermap(city)
            #wundergrund_get_10days(city)
    time.sleep(55)



#### IMPLEMENTATION ###########################################################

citylist = pickle.load(open('cityfile_checked.dump','rb'))
# get the second substring from every string
cities_only          = [item[1] for item in citylist] 


http = urllib3.PoolManager()
forecast = get_xml_openweathermap('Berlin', http)