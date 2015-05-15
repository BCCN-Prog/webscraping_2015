
import numpy as np
import pickle
import os
import sys
#import ws.bad

mydir = os.path.abspath(os.path.dirname(__file__))

print(mydir)

lookupmatrix = pickle.load(open( \
                               mydir +'/accuweather_location_codes.dump','rb'))

lookuplist = lookupmatrix.tolist()

def build_url(city):
    
    # check whether input is a string
    if type(city) != str:
        raise(bad.type('input is not string'))
        
    
    index = lookuplist[1].index(city)
    accuweather_index = lookuplist[0][index]
    
    url = 'http://realtek.accu-weather.com/widget/realtek/weather-data.asp' \
          + '?location=cityId:' \
          + str(accuweather_index)
          
    
          
    return url
    

#print(build_url('babelsberg'))