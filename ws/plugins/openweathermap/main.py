from time import sleep
import pandas as pd
import numpy as np
import json
from datetime import timedelta
import urllib

def build_url(city):
    # check whether input is a string
    if type(city) != str:
        raise ValueError("The input city " + str(city) + " wasn't of type string")

    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' \
          + city \
          + '&mode=json' \
          + '&units=metric' \
          + '&cnt=16' # 'cnt = 16' means next 16 days

    return url

def pandize(str_data, cityname, date):
    '''      
    REMARK: I noticed that some forecasts include 'rain' and others don't. 
    Therefore, I used an if statement to verify if rain is a key or not. I am not 
    quite sure if rain is the only variable where this is the case. So if there is 
    an error while running this method, this could possibly be it.
    '''
    data = json.loads(str_data)
    table = pd.DataFrame(columns = ['Provider','ref_date','city','pred_offset',
'Station ID','Date','Quality Level','Air Temperature','Vapor Pressure', \
'Degree of Coverage','Air Pressure','Rel Humidity','Wind Speed','Max Air Temp', \
'Min Air Temp','Min Groundlvl Temp','Max Wind Speed','Precipitation', \
'Precipitation Ind','Hrs of Sun','Snow Depth'])
    if "list" in data.keys():
        for i in range(13):
            forecast = data["list"][i]
            table.loc[i] = [\
                            'openweathermap'\
                            ,date\
                            ,cityname\
                            ,date+timedelta(days=i)\
                            ,np.NaN\
                            ,np.NaN\
                            ,np.NaN\
                            ,forecast['temp']['day']\
                            ,np.NaN\
                            ,forecast['clouds']\
                            ,forecast['pressure']\
                            ,forecast['humidity']\
                            ,forecast['speed']\
                            ,forecast['temp']['max']\
                            ,forecast['temp']['min']\
                            ,np.NaN\
                            ,np.NaN\
                            ,forecast['rain'] if 'rain' in forecast.keys() else np.NaN\
                            ,np.NaN\
                            ,np.NaN\
                            ,np.NaN]
        return table
    else:
        return -1

