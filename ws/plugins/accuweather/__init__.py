import numpy as np
import pickle
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
