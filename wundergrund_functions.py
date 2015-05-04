# -*- coding: utf-8 -*-
"""
Functions to retrive info from wundergrund.
"""

import urllib
import json
import pandas as pd

def wundergrund_get_city_index(city): 
    '''
    input must be a string, containing the city name alone
    '''
    
    url = 'http://api.wunderground.com/api/3a8e74a2827886a1/geolookup/'\
    'conditions/q/DL/'+city+'.json'
    page = urllib.request.urlopen(url) 
    read = page.read()
    decoded = read.decode('utf8')
    data = json.loads(decoded)
    
    if "location" in data.keys():     # "location" case
        return data["location"]["l"]
    else:                               # "Berlin" case (ambiguity)
        for cities in data["response"]["results"]:
            if cities["country"] == "DL":
                return cities["l"]
                
def wundergrund_get_10days(index): 
    '''
    input a valid city index, return a pandas dataframe containing 
    10-day forecast in 10 rows (days ahead day of get) and a column for every
    weather parameter.
    '''
    
    url = 'http://api.wunderground.com/api/3a8e74a2827886a1/forecast10day'\
    +index+'.json'
    page = urllib.request.urlopen(url) 
    read = page.read()
    decoded = read.decode('utf8')
    data = json.loads(decoded)
    table = pd.DataFrame(columns = ['mintemp','hightemp','avg_wind_speed',\
    'avg_wind_direction','max_wind_speed','max_wind_direction','avg_humidity'\
    ,'percp_total','percp_day','percp_night','snow_total','snow_day','snow_night'])
    for i in range(9):
        forecast = data["forecast"]["simpleforecast"]["forecastday"][i]
        table.loc[i] = [forecast["low"]['celsius'], forecast["high"]['celsius'], forecast["avewind"]['kph'], forecast["avewind"]['degrees']\
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