# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:27:00 2015

@author: tabea
"""

import xml.etree.ElementTree as ET
import pandas
import numpy as np
from scipy.constants.constants import F2C
        
# Station ID needed here!!
columns = ['ref_date','city','pred_offset','Station ID', 'Date', 'Quality Level', 'Air Temperature', \
'Vapor Pressure', 'Degree of Coverage', 'Air Pressure', 'Rel Humidity', \
'Wind Speed', 'Max Air Temp', 'Min Air Temp', 'Min Groundlvl Temp', \
'Max Wind Speed', 'Precipitation', 'Precipitation Ind', 'Hrs of Sun', \
'Snow Depth','realfeelhigh','realfeellow','winddirection','maxuv','snowamount', \
'tstormprob']

# for 7 days
index = range(7)

df_ = pandas.DataFrame(index=index, columns=columns)
#df_ = df_.fillna(np.NaN)
#df_['Date'] = index


tree = ET.parse('accuweather_exampleXML_berlin.xml')
root = tree.getroot()
#root.find('{http://www.accuweather.com}forecast')
# observation: elementname include the url
forecast = root.find('{http://www.accuweather.com}forecast')


# difference precipitation and precipitation ind??
columns_acc = ['hightemperature','lowtemperature','realfeelhigh','realfeellow', \
'windspeed','winddirection','maxuv','rainamount','snowamount','tstormprob']
# columns_dat contains the column names that match the names from accuweather:
columns_dat = ['Max Air Temp','Min Air Temp','realfeelhigh','realfeellow', \
'Wind Speed','winddirection','maxuv','Precipitation','snowamount','tstormprob']

# get weather params from xml
url = '{http://www.accuweather.com}'
for idx, param_name in enumerate(columns_acc):
    values = [element.text for element in forecast.iter() if element.tag==url+param_name]
    if param_name == 'rainamount':
        tempValues = [float(values[i]) + float(values[i+1]) for i in np.arange(0,14,2)]
    else:
        tempValues = values[1::2]
    if param_name == 'hightemperature' or param_name == 'lowtemperature'\
    or param_name == 'realfeelhigh' or param_name == 'realfeellow' :
        tempValues = F2C(np.array([int(i) for i in values]))
    df_[columns_dat[idx]]=pandas.Series(tempValues)

# fill reference date into df
dates = [element.text for element in forecast.iter() if element.tag==url+'obsdate']
# i take intentionally the same date because the refdate is the same
refdate = [pandas.Timestamp(dates[0]) for i in range(7)] 
df_['ref_date'] = pandas.Series(refdate)

# pred_offset is just the number of the day in future with respect to the reference date
df_['pred_offset'] = pandas.Series(np.arange(7))

# get city name and fill into df
local = root.find(url+'local')
city = [elem.text for elem in local.iter() if elem.tag==url+'city']
city = [city[0] for i in np.arange(7)]
df_['city'] = pandas.Series(city)


