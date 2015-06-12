import numpy as np
import pickle
import xml.etree.ElementTree as ET
import pandas
import numpy as np
from scipy.constants.constants import F2C
from datetime import timedelta
import os
import sys

mydir = os.path.abspath(os.path.dirname(__file__))
lookupmatrix = pickle.load(open(os.path.join(mydir, 'accuweather_location_codes.dump'), 'rb'))
lookuplist = lookupmatrix.tolist()

def build_url(city):
    # check whether input is a string
    if type(city) != str:
        raise ValueError("The input city " + str(city) + " wasn't of type string")

    index = lookuplist[1].index(city)
    accuweather_index = lookuplist[0][index]

    url = 'http://realtek.accu-weather.com/widget/realtek/weather-data.asp' \
          + '?location=cityId:' \
          + str(accuweather_index)

    return url
    
def pandize(data, city, date):
    
    columns = ['Provider','ref_date','city','pred_offset','Station ID', 'Date', 'Quality Level', 'Air Temperature', \
    'Vapor Pressure', 'Degree of Coverage', 'Air Pressure', 'Rel Humidity', \
    'Wind Speed', 'Max Air Temp', 'Min Air Temp', 'Min Groundlvl Temp', \
    'Max Wind Speed', 'Precipitation', 'Precipitation Ind', 'Hrs of Sun', \
    'Snow Depth']
    
    # for 7 days
    index = range(7)
    
    df_ = pandas.DataFrame(index=index, columns=columns)
    
    
    root = ET.fromstring(data)
    #root = tree.getroot()
    #root.find('{http://www.accuweather.com}forecast')
    # observation: elementname include the url
    forecast = root.find('{http://www.accuweather.com}forecast')
    
    
    # difference precipitation and precipitation ind??
    columns_acc = ['hightemperature','lowtemperature', \
    'windspeed','rainamount']
    # columns_dat contains the column names that match the names from accuweather:
    columns_dat = ['Max Air Temp','Min Air Temp', \
    'Wind Speed','Precipitation']
    
    # get weather params from xml
    url = '{http://www.accuweather.com}'
    for idx, param_name in enumerate(columns_acc):
        values = [element.text for element in forecast.iter() if element.tag==url+param_name]
        if param_name == 'rainamount':
            tempValues = [float(values[i]) + float(values[i+1]) for i in np.arange(0,14,2)]
        else:
            tempValues = values[1::2]
        if param_name == 'hightemperature' or param_name == 'lowtemperature':
            tempValues = F2C(np.array([int(i) for i in values]))
        df_[columns_dat[idx]]=pandas.Series(tempValues)
    
    '''
    # fill reference date into df
    dates = [element.text for element in forecast.iter() if element.tag==url+'obsdate']
    # i take intentionally the same date because the refdate is the same
    '''
    refdate = [date for i in range(7)] 
    dates = [date+timedelta(days=i) for i in range(7)] 
    
    df_['ref_date'] = pandas.Series(refdate)
    df_['Date'] = pandas.Series(dates)
    # pred_offset is just the number of the day in future with respect to the reference date
    df_['pred_offset'] = pandas.Series(np.arange(7))
    
    city = [city for i in np.arange(7)]
    df_['city'] = pandas.Series(city)
    
    provider = ['accuweather' for i in range(7)]
    df_['Provider'] = pandas.Series(provider)
    return df_
    
def pandize_advanced(data, city, date):
    
    columns = ['Provider','ref_date','city','pred_offset','Station ID', 'Date', 'Quality Level', 'Air Temperature', \
    'Vapor Pressure', 'Degree of Coverage', 'Air Pressure', 'Rel Humidity', \
    'Wind Speed', 'Max Air Temp', 'Min Air Temp', 'Min Groundlvl Temp', \
    'Max Wind Speed', 'Precipitation', 'Precipitation Ind', 'Hrs of Sun', \
    'Snow Depth','realfeelhigh','realfeellow','winddirection','maxuv','snowamount', \
    'tstormprob']
    
    # for 7 days
    index = range(7)
    
    df_ = pandas.DataFrame(index=index, columns=columns)
    
    
    root = ET.fromstring(data)
    #root = tree.getroot()
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
    
    '''
    # fill reference date into df
    dates = [element.text for element in forecast.iter() if element.tag==url+'obsdate']
    # i take intentionally the same date because the refdate is the same
    '''
    refdate = [date for i in range(7)] 
    dates = [date+timedelta(days=i) for i in range(7)] 
    
    df_['ref_date'] = pandas.Series(refdate)
    df_['Date'] = pandas.Series(dates)
    # pred_offset is just the number of the day in future with respect to the reference date
    df_['pred_offset'] = pandas.Series(np.arange(7))
    
    city = [city for i in np.arange(7)]
    df_['city'] = pandas.Series(city)
    
    provider = ['accuweather' for i in range(7)]
    df_['Provider'] = pandas.Series(provider)
    return df_
