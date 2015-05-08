# -*- coding: utf-8 -*-
"""
Takes weather.com index and returns data.
"""

import urllib
import json

def weathercom_get_data(index): 
    '''
    input must be a string, containing the city name alone
    '''
    
    url = 'http://dsx.weather.com/%28wxd/v2/MORecord;wxd/v2/wwir;wxd/v2/'\
    +'PastFlu;wxd/v2/SkiResorts;wxd/v2/DIRecord;wxd/v2/DFRecord;wxd/v2/'\
    +'DHRecord;wxd/v2/BERecord;wxd/v2/Pollen;wxd/v2/airportDelays;wxd/v2/'\
    +'TIRecord;wxd/v2/WMRecord%29/%28en_US/'\
    +index+':1:GM%29?api=01119904-40b2-4f81-94a0-57867d0fd22c'
    

    page = urllib.request.urlopen(url) 
    read = page.read()
    decoded = read.decode('utf8')
    data = json.loads(decoded)
    return data