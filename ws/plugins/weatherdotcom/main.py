import urllib.request
import ws.bad as bad
import json
import logging
import re


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

    index = get_city_index(city)
    url = ('http://dsx.weather.com/'
           + '%28wxd/v2/MORecord;wxd/v2/wwir;wxd/v2/'
           + 'PastFlu;wxd/v2/SkiResorts;wxd/v2/DIRecord;wxd/v2/'
           + 'DFRecord;wxd/v2/'
           + 'DHRecord;wxd/v2/BERecord;wxd/v2/Pollen;wxd/v2/'
           + 'airportDelays;wxd/v2/'
           + 'TIRecord;wxd/v2/WMRecord%29/%28en_US/' + index
           + ':1:GM%29?api=01119904-40b2-4f81-94a0-57867d0fd22c')

    return url
