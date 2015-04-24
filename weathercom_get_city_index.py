# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:31:34 2015

@author: Mark
"""

# Written for python 2. Supposedly one can uncommet the lines that contain
# the <<<<<<<<<<<< marking and delete one line above these to make it 
# work with python 3.


import urllib2      # Python 2 
# import urllib2  # <<<<<<<<<<<<<<<<<<

def weathercom_get_city_index(city): 
    '''
    input must be a string, containing the city name alone
    '''
    
    url = 'http://wxdata.weather.com/wxdata/ta/' \
    + city +',germany' \
    + '.js?locType=1&cb=twctacb_575661617_4&' \
    + 'key=2227ef4c-dfa4-11e0-80d5-0022198344f4&max=20&locale=en_US'
    
    page = urllib2.urlopen(url)
#    page = urllib.request.urlopen(url) #<<<<<<<<<<
    index = page.readlines()[1]
    index = index[19:-2]
    return index