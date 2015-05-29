

##### This is weather.com ###

import urllib
import ws.bad as bad
import json

def weathercom_get_city_index(city): 
    '''
    input must be a string, containing the city name alone
    '''
    
    url = 'http://wxdata.weather.com/wxdata/ta/' \
    + city +',germany' \
    + '.js?locType=1&cb=twctacb_575661617_4&' \
    + 'key=2227ef4c-dfa4-11e0-80d5-0022198344f4&max=20&locale=en_US'
    

    page = urllib.request.urlopen(url) 
    index = page.readlines()[1]
    index = index[19:-3]
    return index.decode(encoding='UTF-8')

def build_url(city):
    '''
    input must be a string, containing the city name alone
    '''
    city_index = weathercom_get_city_index(city)
    url = 'http://dsx.weather.com/%28wxd/v2/MORecord;wxd/v2/wwir;wxd/'\
    +'v2/PastFlu;wxd/v2/SkiResorts;wxd/v2/DIRecord;wxd/v2/DFRecord;wxd/'\
    +'v2/DHRecord;wxd/v2/BERecord;wxd/v2/Pollen;wxd/v2/airportDelays;wxd/v2/'\
    +'TIRecord;wxd/v2/WMRecord%29/%28en_US/'+city_index\
    +':1:GM%29?api=01119904-40b2-4f81-94a0-57867d0fd22c'
    return url
    
