

##### This is weather.com ###

import urllib
import ws.bad

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
    
    url = 'http://api.wunderground.com/api/3a8e74a2827886a1/geolookup/'\
    'conditions/q/DL/'+\
    weathercom_get_city_index(city)\
    +'.json'
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