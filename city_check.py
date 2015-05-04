''' This script checks which cities are available from the weather
    providers and then dumps the final "cleaned" citylist into
    'cityfile_checked.dump'.'''


import pickle
import urllib3
import time
import string


#### FUNCTION DEFINITIONS #####################################################
    
def check_cities(http, citylist, weatherprovider):
    ''' This function returns indices of the cities that
        the given weatherprovider doesn't have. These
        cities/indices should be deleted from the citylist'''
    
    # get the second substring from every string in the list
    # the second substring is the one that contains the cities
    cities_only          = [item[1] for item in citylist] 
    indices_to_be_deleted = []
    
    for idx, city in enumerate(cities_only):
        print('Doing query nr %d to %s for %s' % (idx, weatherprovider, city))
        
        
        ## WE NEED TO FIND A METHOD THAT WORKS WITH GERMAN UMLAUT
        if 'ü' in city or 'ö' in city or 'ä' in city or 'ß' in city:
            print('Cityname (%s) contained illegal character, skipping' %city)
            indices_to_be_deleted.append(idx)
            continue
            
        r = http.request('GET',
                         'http://api.openweathermap.org/data/2.5/weather?q='+ \
                         city + \
                         ', Germany&mode=xml')
        forecast = str(r.data)    
        if "Error: Not found city" in forecast:
            print("%s wasn't found on %s, deleting..." %(city, weatherprovider))
            indices_to_be_deleted.append(idx)
    
    print('DONE CHECKING THE CITIES for %s' %weatherprovider)
    return indices_to_be_deleted



def delete_cities(citylist, indices_to_be_deleted):
    ''' This function deletes cities from the citylist.
        It deletes the cities specified in the second parameter '''

    # Reverse this list because we have to delete starting in the end
    # in the for lop
    indices_to_be_deleted.reverse()
    for index in indices_to_be_deleted:
        del citylist[index]    
        
    
    return citylist




#### IMPLEMENTATION ###########################################################

# Import the cities that are available from the Deutscher Wetterdienst
# The file 'current_cityfile.dump' is the output of the script 
# get_cities.py
citylist = pickle.load(open('current_cityfile.dump','rb'))

http = urllib3.PoolManager()

# get indices to cities to be deleted
indices_to_be_deleted = check_cities(http, citylist, 'openweathermap')
citylist              = delete_cities(citylist, indices_to_be_deleted)

 

pickle.dump(citylist, open('cityfile_checked.dump','wb'))