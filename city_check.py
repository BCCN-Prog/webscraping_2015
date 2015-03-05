''' This script checks which cities are available from the weather
    providers '''


import pickle
import urllib3
import time
import string


citylist = pickle.load(open('current_cityfile.dump','rb'))
# get the second substring from every string
cities_only          = [item[1] for item in citylist] 
http = urllib3.PoolManager()
    
def check_cities(citylist, weatherprovider):
    indices_to_be_deleted = []
    
    for idx, city in enumerate(citylist):
        print('Doing query nr %d to %s for %s' % (idx, weatherprovider, city))
        if 'ü' in city or 'ö' in city or 'ä' in city or 'ß' in city:
            print('Cityname (%s) contained illegal character, skipping' %city)
            indices_to_be_deleted.append(idx)
            continue
            
        r = http.request('GET', 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&mode=xml')
        forecast = str(r.data)    
        if "Error: Not found city" in forecast:
            print("%s wasn't found on %s, deleting..." %(city, weatherprovider))
            indices_to_be_deleted.append(idx)
    
    print('DONE CHECKING THE CITIES for %s' %weatherprovider)
    return indices_to_be_deleted



# get indices to cities to be deleted
indices_to_be_deleted = check_cities(cities_only, 'openweathermap')

indices_to_be_deleted.reverse()
for index in indices_to_be_deleted:
    del citylist[index]
    

pickle.dump(citylist, open('cityfile_checked.dump','wb'))