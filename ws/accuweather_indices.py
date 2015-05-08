''' This script will query accuweather for all cities in our citylist and 
    extract the index that accuweather uses for that city '''
    

from datetime import datetime
import urllib3
import pickle
import numpy as np


def get_indices(federal_state, http):
    url = 'http://www.accuweather.com/en/browse-locations/eur/de/bb'
    r = http.request('GET', url)
    
    forecast = str(r.data)
    
    url = 'http://www.accuweather.com/en/browse-locations/eur/de/' \
          + federal_state
    r = http.request('GET', url)
    
    forecast = str(r.data)
    splitstring = forecast.split('\\n')
    
    mystr = splitstring[1093]
    
    print('Querying for state ' + federal_state)    
    
    continue_loop = True
    idx = 0
    citylist = []
    idlist   = []
    while continue_loop == True:
        try:
            
            mystr = splitstring[1093+idx]
            mystrlist = mystr.split('/')
            city   = mystrlist[5]
            cityid = mystrlist[8].split('"')[0]
            citylist.append(city)
            idlist.append(cityid)
    #        print('current city and id: ' + city + '   ' + cityid)
            idx += 5
        except IndexError:
            continue_loop = False
    
    return np.array(citylist), np.array(idlist)
    

http = urllib3.PoolManager()

federal_states = ['bb', 'be', 'bw', 'by', 'hb', 'he', 'hh', 'mv', 'ni', 'nw', \
                  'rp', 'sh', 'sl', 'sn', 'st', 'th']
overall_citylist = np.array([])
overall_idlist   = np.array([])
for idx in range(len(federal_states)):
    citylist, idlist = get_indices(federal_states[idx], http)
    overall_citylist = np.hstack((overall_citylist, citylist))
    overall_idlist   = np.hstack((overall_idlist,   idlist))

location_matrix = np.vstack((overall_idlist, overall_citylist))
#dumpfile = open('accuweather_location_codes.dump', 'w')
pickle.dump(location_matrix, open('accuweather_location_codes.dump','wb'))