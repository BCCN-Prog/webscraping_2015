import urllib.request
import ws.bad as bad
import pandas as pd
import json
import logging
import re
import pprint
import numpy
import datetime
import numpy as np


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
                     today['wx'], today['tmpC'], np.nan, np.nan,
                     today['pres'], today['rH'], today['wSpdK'], np.nan,
                     np.nan, np.nan, np.nan, today['_prcp24Mm'], np.nan,
                     sunhrs, today['snwDep']])

    # Forecasts for upcoming days
    dig = data[3]['doc']['DIData']

    count = 1
    for i, fc in enumerate(dig):
        # We already have Today from above, also throw away the nights
        if fc['dyPrtNm'] == 'Today':
            continue
        elif fc['dyPrtNm'] == 'Tonight':
            continue
        elif 'night' in fc['dyPrtNm']:
            continue
        # We have two forecasts for Sundays, one 12h and one 24h.
        elif fc['dyPrtNm'] == 'Sunday' and fc['dur'] == 12:
            continue

        altPhrase = fc['altPhrase']

        # Temperature of the day (lows are for night according to the official
        # web interface)
        m1 = re.search('High (?:|near |around )([0-9]+)C', altPhrase)
        m2 = re.search('Highs ([0-9]+) to ([0-9]+)C', altPhrase)
        high_temp = np.nan
        if m1:
            high_temp = int(m1.group(1))
        elif m2:
            # This is what the official web interface does.
            high_temp = (int(m2.group(1)) + int(m2.group(2))) / 2

        if np.isnan(high_temp):
            logging.error('No temperature in the forecast! altPhrase = %s', altPhrase)

        table.loc[count] = ([provider, date, cityname, count, np.nan, date,
                     fc['snsblWx'], high_temp, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan])
        count += 1

    return table
