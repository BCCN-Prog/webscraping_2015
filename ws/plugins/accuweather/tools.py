

###  the folloowing is only here temporarily, delete when put into a package!!!!
#lookupmatrix = pickle.load(open( \
#                               'accuweather_location_codes.dump','rb'))
                               
#lookuplist = lookupmatrix.tolist()

from accuweather import lookuplist
print(lookuplist)
print('hello')


def build_url(city):
    
    # check whether input is a string
#    if type(city) != str:
#        raise(bad.type('input is not string'))
    
    index = lookuplist[1].index(city)
    accuweather_index = lookuplist[0][index]
    
    url = 'http://realtek.accu-weather.com/widget/realtek/weather-data.asp' \
          + '?location=cityId:' \
          + str(accuweather_index)
          
    type(str(accuweather_index))
          
    return url
    

#print(build_url('babelsberg'))