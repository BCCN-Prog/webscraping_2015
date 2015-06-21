# -*- coding: utf-8 -*-
"""
<("<)
"""

import pickle
import urllib
import json
import time
import pandas as pd
import numpy as np
import ws.bad as bad
from datetime import timedelta
import os
mydir = os.path.abspath(os.path.dirname(__file__))

wug_urls_book = pickle.load(open(os.path.join(mydir, 'cities_urls'), 'rb'))

def build_url(city):
    '''
    assumes cities are called only from the city list, existing on 20.6.15
    '''
    city_dex = np.where(wug_urls_book[:,0]== city)[0][0]
    if wug_urls_book[city_dex,1] == '0':
        raise bad.City()
    else:
        static_url = list(wug_urls_book[city_dex,1])
        dynamic_key = list(return_wundergroud_key())
        static_url[32:48] = dynamic_key
        return ''.join(static_url)

def pandize(str_data, cityname, date):
    data = json.loads(str_data)
    table = pd.DataFrame(columns = ['Provider','ref_date','city','pred_offset', \
'Station ID','Date','Quality Level','Air Temperature','Vapor Pressure', \
'Degree of Coverage','Air Pressure', 'Rel Humidity', 'Wind Speed', 'Max Air Temp', \
'Min Air Temp','Min Groundlvl Temp', 'Max Wind Speed', 'Precipitation', \
'Precipitation Ind','Hrs of Sun', 'Snow Depth'])
    for i in range(9):
        forecast = data["forecast"]["simpleforecast"]["forecastday"][i]
        table.loc[i] = [\
'wunderground'
,date\
,cityname\
,int(i)\
,np.NaN\
,date+timedelta(days=i)\
,np.NaN\
,np.NaN\
,np.NaN\
,np.NaN\
,np.NaN\
,forecast["avehumidity"]\
,forecast["avewind"]['kph']\
,forecast["high"]['celsius']\
,forecast["low"]['celsius']\
,np.NaN\
,forecast["maxwind"]['kph']\
,forecast["qpf_allday"]["mm"]\
,np.NaN\
,np.NaN\
,forecast["snow_allday"]["cm"]]
    return table

###############################
################################    

def url_builder(city):
    '''
    input must be a string, containing the city name alone
    '''
    key= return_wundergroud_key()
    url = 'http://api.wunderground.com/api/'+key+\
    '/geolookup/conditions/q/DL/'+city+'.json'
    page = urllib.request.urlopen(url)
    read = page.read()
    decoded = read.decode('utf8')
    data = json.loads(decoded)

    if "location" in data.keys():     # "location" case
        cityname =  data["location"]["l"]
    else:                               # "Berlin" case (ambiguity)
        try:
            for cities in data["response"]["results"]:
                if cities["country"] == "DL":
                    cityname = cities["l"]
        except:
            raise bad.City()

    forecasturl = 'http://api.wunderground.com/api/'+key+\
    '/forecast10day'+cityname+'.json'
    return forecasturl
    
def temp_debugging_helper_function(url):
    page = urllib.request.urlopen(url)
    read = page.read()
    data = read.decode('utf8')
    return data


def url_storage_function():
    city_list = pickle.load(open(os.path.join(mydir, 'citylist.dump'), 'rb'))
    #rank = len(city_list)
    cities = []
    urls= []
    failures =[]
    i = 0
    
    for city in city_list:
        print("doing "+str(i))
        try:
            url = build_url(city)
        except bad.City:
            url = '0'
            failures.append(city)
        except:
            url = '1'
            failures.append(city)
        urls.append(url)
        cities.append(city)
        i += 1
    storage = np.array([cities,urls])
    dropped = np.array(failures)
    return storage.T, dropped
            
            
    

def clocker(key_well_):
    arg = 12.2 / len(key_well_)
    time.sleep(arg) # 2 seconds at the moment

def clocker_legacy_function(): # defunk and non-working but beautifully conceived 
    '''Let the clocked function work at full speed while possible, then wait
    until the period ends that allows it to go again.'''

    global wunderground_keys_time_ticks_
    if 'wunderground_keys_time_ticks_' not in globals():
        wunderground_keys_time_ticks_ = np.zeros(90)
    if wunderground_keys_time_ticks_[-1] == 0:
        wunderground_keys_time_ticks_ = np.roll(wunderground_keys_time_ticks_, 1)
        wunderground_keys_time_ticks_[0] = time.time()
    else:
        deltatee = wunderground_keys_time_ticks_[0] - wunderground_keys_time_ticks_[-1]
        if deltatee < 61:
            time.sleep(61-deltatee)
            wunderground_keys_time_ticks_ = np.roll(wunderground_keys_time_ticks_, 1)
            wunderground_keys_time_ticks_[0] = time.time()
        else:
            wunderground_keys_time_ticks_ = np.roll(wunderground_keys_time_ticks_, 1)
            wunderground_keys_time_ticks_[0] = time.time()



def return_wundergroud_key():
    wunderground_keys_ = pickle.load(open(os.path.join(mydir, 'wunderground_keys_'), 'rb'))
                

    key_well_ = [\
    '3a8e74a2827886a1',\
    '8714d2a1dfc6e7a8',\
    '23e7a53f72f058ac',\
    '7b88114d03edd183',\
    '6392e7cab4ead3bf',\
    'e709118692e74123',\
    '15858ca917d7dfae',\
    'a930fdbbb56c3b59',\
    'c64c1dd8e5350991',\
    '3ef23167f819b269'\
    ]

    try:
        if len(wunderground_keys_) > 0:
            clocker(key_well_)
            pop = wunderground_keys_.pop()
            pickle.dump(wunderground_keys_, open(os.path.join(mydir, 'wunderground_keys_'), "wb" ))
            return pop
        else:
            wunderground_keys_ = key_well_.copy()
            clocker(key_well_)
            pop = wunderground_keys_.pop()
            pickle.dump(wunderground_keys_, open(os.path.join(mydir, 'wunderground_keys_'), "wb" ))
            return pop
    except:
        wunderground_keys_ = key_well_.copy()
        clocker(key_well_)
        pop = wunderground_keys_.pop()
        pickle.dump(wunderground_keys_, open(os.path.join(mydir, 'wunderground_keys_'), "wb" ))
        return pop
