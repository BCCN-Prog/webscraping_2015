# -*- coding: utf-8 -*-
"""
<("<)
"""

import urllib
import json
import time
import pandas as pd
import numpy as np
#import bad

def build_url(city):
    '''
    input must be a string, containing the city name alone
    '''
    
    url = 'http://api.wunderground.com/api/'+return_wundergroud_key+\
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
            raise bad.city()
            
    forecasturl = 'http://api.wunderground.com/api/'+return_wundergroud_key+\
    '/forecast10day'+cityname+'.json'
    return forecasturl

def pandize(url,cityname):
    page = urllib.request.urlopen(url) 
    read = page.read()
    decoded = read.decode('utf8')
    data = json.loads(decoded)
    table = pd.DataFrame(columns = ['ref_date','city','pred_offset','Min Air Temp','Max Air Temp','avg_wind_speed',\
    'avg_wind_direction','max_wind_speed','max_wind_direction','avg_humidity'\
    ,'percp_total','percp_day','percp_night','snow_total','snow_day','snow_night'])
    for i in range(9):
        forecast = data["forecast"]["simpleforecast"]["forecastday"][i]
        table.loc[i] = [\
pd.to_datetime([\
str(data["forecast"]["simpleforecast"]["forecastday"][0]['date']['day'])+'.'+\
str(data["forecast"]["simpleforecast"]["forecastday"][0]['date']['month'])+'.'+\
str(data["forecast"]["simpleforecast"]["forecastday"][0]['date']['year'])\
], dayfirst=True)\
,cityname\
,int(i)\
,forecast["low"]['celsius']\
,forecast["high"]['celsius']\
,forecast["avewind"]['kph']
,forecast["avewind"]['degrees']\
,forecast["maxwind"]['kph']\
,forecast["maxwind"]['degrees']\
,forecast["avehumidity"]\
,forecast["qpf_allday"]["mm"]\
,forecast["qpf_day"]["mm"]\
,forecast["qpf_night"]["mm"]\
,forecast["snow_allday"]["cm"]\
,forecast["snow_day"]["cm"]\
,forecast["snow_night"]["cm"]]
    return table

###############################
################################

clocktesterarray = np.zeros(500)
def clocktester(n):
    ''' manual testing tool for clocker() function.'''
    for i in range(n):
        clocktesterarray[i] = time.time()
        clocker()
        
def clocker():
    '''Let the clocked function work at full speed while possibl, then wait
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
    global wunderground_keys_

    key_well_ = [\
    '3a8e74a2827886a1',\
    '8714d2a1dfc6e7a8',\
    '23e7a53f72f058ac',\
    '7b88114d03edd183',\
    '6392e7cab4ead3bf',\
    'e709118692e74123',\
    '15858ca917d7dfae',\
    'a930fdbbb56c3b59',\
    '3ef23167f819b269'\
    ]
    
    try:
        if len(wunderground_keys_) > 0:
            clocker()
            return wunderground_keys_.pop()
        else:
            wunderground_keys_ = key_well_.copy()
            clocker()
            return wunderground_keys_.pop()
    except:
        wunderground_keys_ = key_well_.copy()
        clocker()
        return wunderground_keys_.pop()        