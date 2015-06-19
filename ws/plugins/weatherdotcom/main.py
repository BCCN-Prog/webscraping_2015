import urllib.request
import ws.bad as bad
import pandas as pd
import json
import logging
import re
import pprint
import numpy


def get_city_index(city):
    '''
    input must be a string, containing the city name alone
    '''

    url = ('http://wxdata.weather.com/wxdata/ta/' + city + ',germany' +
           '.js?locType=1&cb=twctacb_575661617_4&' +
           'key=2227ef4c-dfa4-11e0-80d5-0022198344f4&max=20&locale=en_US')

    logging.debug('city %s url %s', city, url)

    with urllib.request.urlopen(url) as response:
        data = response.read()
        data = data.decode(encoding='UTF-8')

        # Prune the data to a pure json string
        data = re.sub('^[a-z0-9_]+\(', '', data)
        data = re.sub('\)$', '', data)

        index_dict = json.loads(data)

        # Select the first match for this city. If there is no match, raise a
        # bad.City exception.
        num_results = len(index_dict['results'])
        if num_results > 0:
            first_match = index_dict['results'][0]
            index = first_match['key']
        else:
            raise bad.City

    logging.debug('index %s', index)

    return index


def build_url(city):
    '''
    input must be a string, containing the city name alone
    '''
    city_index = get_city_index(city)
    url = 'http://dsx.weather.com/%28wxd/v2/MORecord;wxd/v2/wwir;wxd/'\
    +'v2/PastFlu;wxd/v2/DIRecord;wxd/'\
    +'v2/DHRecord;wxd/v2/BERecord;wxd/v2/'\
    +'TIRecord;wxd/v2/WMRecord%29/%28en_US/'+city_index\
    +':1:GM%29?api=01119904-40b2-4f81-94a0-57867d0fd22c'
    return url

# DI Record is what we want (forecast for a week or so)

def pandize(data, cityname, date):
    """

    Column names
    ------------
    ref_date:           date                                        (argument)
    city:               cityname                                    (argument)
    pred_offset:        date + (locValDay - date)                   (integer)
    Station ID:         NaN
    Date:               ref_date + pred_offset
    Quality Level:      snsblWx
    Air Temperature:    Parse from altPhrase.   (MOData 'tmpC')
    Vapor Pressure:     NaN
    Degree of Coverage: ????
    Air Pressure:       NaN     (MOData 'pres')
    Rel Humidity:       NaN     (MOData 'rH')
    Wind Speed:         NaN     (MOData 'wSpdK')
    Max Air Temp:       Parse from altPhrase.   (MOData 'hIC')
    Min Air Temp:       Parse from altPhrase.
    Min Groundlvl Temp: NaN
    Max Wind Speed:     NaN
    Precipitation:              (MOdata '_prcp24Mm')
    Precipitation Ind:  ????
    Hrs of Sun:                 (MOData 'sunset' - 'sunrise')
    Snow Depth:                 (MOData 'snwDep')
    """

    nforecasts = 9
    provider = 'weatherdotcom'

    data = json.loads(data)
    table = pd.DataFrame(columns = (['Provider', 'ref_date', 'city',
                                     'pred_offset', 'Station ID', 'Date',
                                     'Quality Level', 'Air Temperature',
                                     'Vapor Pressure', 'Degree of Coverage',
                                     'Air Pressure', 'Rel Humidity', 'Wind Speed',
                                     'Max Air Temp', 'Min Air Temp',
                                     'Min Groundlvl Temp', 'Max Wind Speed',
                                     'Precipitation', 'Precipitation Ind',
                                     'Hrs of Sun', 'Snow Depth']))

    # Forecast for today
    today = data[0]['doc']['MOData']

    sunrise = datetime.datetime.strptime(today['_sunriseISOLocal'][:-len('.000+02:00')], "%Y-%m-%dT%H:%M:%S")
    sunset = datetime.datetime.strptime(today['_sunsetISOLocal'][:-len('.000+02:00')], "%Y-%m-%dT%H:%M:%S")
    sunhrs = (sunset - sunrise).total_seconds() / 3600


    table.loc[0] = ([provider, date, cityname, 0, np.nan, date,
                     today['snsblWx'], today['tmpC'], np.nan, np.nan,
                     today['pres'], today['rH'], today['wSpdK'], np.nan,
                     np.nan, np.nan, np.nan, today['_prcp24Mm'], np.nan,
                     sunhrs, today['snwDep']])

    # Forecasts for upcoming days
    dig = data[3]['doc']['DIData']

    for i in range(nforecasts):
        forecast = data["forecast"]["simpleforecast"]["forecastday"][i]


        table.loc[i] = ([provider, date, cityname, int(i), forecast["low"]['celsius'],
            forecast["high"]['celsius'], forecast["avewind"]['kph'],
            forecast["avewind"]['degrees'], forecast["maxwind"]['kph'],
            forecast["maxwind"]['degrees'], forecast["avehumidity"],
            forecast["qpf_allday"]["mm"], forecast["qpf_day"]["mm"],
            forecast["qpf_night"]["mm"], forecast["snow_allday"]["cm"],
            forecast["snow_day"]["cm"], forecast["snow_night"]["cm"]])
