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

#citieslist = get_cities('TU_Stundenwerte_Beschreibung_Stationen.txt')
