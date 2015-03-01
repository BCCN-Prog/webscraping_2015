

from datetime import datetime
import time
import urllib3

http = urllib3.PoolManager()

def get_cities(filename):
    text_file = open(filename, 'r')
    text = text_file.read() #.decode('utf-8')
    print(text)
    
    
    
    
def check_cities(citieslist):
    
    r = http.request('GET', 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&mode=xml')
    forecast = str(r.data)    
    if "Error: Not found city" in forecast:
        print("City wasn't found")
#        continue

def get_xml_openweathermap(city):
    
    r = http.request('GET', 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&mode=xml')
    forecast = str(r.data)
    
    current_time = str(datetime.now())
    text_file = open(city + '__' + current_time + '.forecast', "w")
    text_file.write(forecast)
    text_file.close()
    
    return forecast



#citieslist = get_cities('TU_Stundenwerte_Beschreibung_Stationen.txt')
#while True:
#    time.sleep(5)


forecast = get_xml_openweathermap('Kaisersbach')

