# -*- coding: utf-8 -*-
"""
Takes a city name string, and returns a string containing the index used on 
weather.com
"""



import urllib

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