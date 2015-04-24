''' WARNING: for some reason it only works with Python 2.7!
    This is the actual scraping file that will be executed
    on a server and query openweathermap.org for forecasts
    every day at the same time '''

from datetime import datetime
import time
import urllib
import pickle



#### FUNCTION DEFINITIONS #####################################################

def get_xml_openweathermap(city):
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' \
          + city \
          + '&mode=xml' \
          + '&units=metric' \
          + '&cnt=16' # 'cnt = 16' means next 16 days
    r = http.request('GET', url)
    
    print('I queried openweathermap for %s' %city)
    forecast = str(r.data)
    
    current_time = str(datetime.now())
    text_file = open(city + '_' + current_time + \
		     '_openweathermap_16_days' + '.forecast', "w")
    text_file.write(forecast)
    text_file.close()


# This script will essentially run forever. Every minute it checks whether
# it is currently 03:00 o'clock, and if so, it performs the scraping task.
while True:
    if time.strftime("%H") == "03" and time.strftime("%M") == "00":
        for city in cities_only:
            get_xml_openweathermap(city)
    time.sleep(55)



#### IMPLEMENTATION ###########################################################

citylist = pickle.load(open('cityfile_checked.dump','rb'))
# get the second substring from every string
cities_only          = [item[1] for item in citylist] 
http = urllib3.PoolManager()