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

def build_url(city):
    '''
    input must be a string, containing the city name alone
    '''

    url = 'http://api.wunderground.com/api/'+return_wundergroud_key()+\
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

    forecasturl = 'http://api.wunderground.com/api/'+return_wundergroud_key()+\
    '/forecast10day'+cityname+'.json'
    return forecasturl

def pandize(str_data, cityname, date):
    page = urllib.request.urlopen(str_data)
    read = page.read()
    decoded = read.decode('utf8')
    data = json.loads(decoded)
    table = pd.DataFrame(columns = ['ref_date','city','pred_offset','Station ID', \
'Date', 'Quality Level', 'Air Temperature', 'Vapor Pressure', 'Degree of Coverage', \
'Air Pressure', 'Rel Humidity', 'Wind Speed', 'Max Air Temp', 'Min Air Temp', \
'Min Groundlvl Temp', 'Max Wind Speed', 'Precipitation', 'Precipitation Ind', \
'Hrs of Sun', 'Snow Depth','realfeelhigh','realfeellow','winddirection','maxuv', \
'snowamount', 'tstormprob'])
    for i in range(9):
        forecast = data["forecast"]["simpleforecast"]["forecastday"][i]
        table.loc[i] = [\
date\
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
,forecast["snow_allday"]["cm"]\
,np.NaN\
,np.NaN\
,np.NaN\
,np.NaN\
,np.NaN\
,np.NaN]
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
    time.sleep(0.0112) # = ~ 1/85 (there are 90 keys)

def clocker_old():
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
    wunderground_keys_ = pickle.load(open('wunderground_keys_', "rb"))
                

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
            pop = wunderground_keys_.pop()
            pickle.dump(wunderground_keys_, open( 'wunderground_keys_', "wb" ))
            return pop
        else:
            wunderground_keys_ = key_well_.copy()
            clocker()
            pop = wunderground_keys_.pop()
            pickle.dump(wunderground_keys_, open( 'wunderground_keys_', "wb" ))
            return pop
    except:
        wunderground_keys_ = key_well_.copy()
        clocker()
        pop = wunderground_keys_.pop()
        pickle.dump(wunderground_keys_, open( 'wunderground_keys_', "wb" ))
        return pop
