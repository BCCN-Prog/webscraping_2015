# -*- coding: utf-8 -*-
"""
<("<)
"""

import urllib
import json
import pandas as pd
#import bad

def build_url(city):
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
        cityname =  data["location"]["l"]
    else:                               # "Berlin" case (ambiguity)
        try:
            for cities in data["response"]["results"]:
                if cities["country"] == "DL":
                    cityname = cities["l"]
        except:
            raise bad.city()
            
    forecasturl = 'http://api.wunderground.com/api/3a8e74a2827886a1/forecast10day'\
    +cityname+'.json'
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