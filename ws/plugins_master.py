from .plugins import *
import time
import pickle
import os
import logging
import ws.bad as bad
import urllib.error
import http.client
from tools import misc


def generate_forecast_filepath(pname, city, basepath=''):
    """Generate forecast filepath.

    basepath/city/pname
    """
    posix_time = time.time()
    utc_posix_time = posix_time + time.timezone

    forecast_dir = os.path.join(basepath, city, pname)
    if not os.path.exists(forecast_dir):
        os.makedirs(forecast_dir)

    filename = str(utc_posix_time).replace('.', 's', 1) + '.forecast'
    forecast_path = os.path.join(forecast_dir, filename)

    return forecast_path


def get_citylist():
    """Return list with all city names."""
    # XXX should we use another format than pickle?
    fp = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'citylist.dump')
    citylist = pickle.load(open(fp, 'rb'))
    citylist = [str(i) for i in citylist]

    return citylist


def store_forecast(city, pname, basepath=''):
    """Store forecast for city from plugin pname."""
    logging.debug('args city=%s pname=%s basepath=%s', city, pname,
                 basepath)

    forecast_data = None
    p = load_plugin(str(pname))

    try:
        url = p.build_url(str(city))
        forecast_data = misc.download_from_url(url)
        filepath = generate_forecast_filepath(pname, city, basepath)
        misc.save_to_disk(forecast_data, filepath)
    except bad.City:
        logging.error('plugin %s cannot deal with city %s', pname, city)
    except urllib.error.HTTPError as err:
        logging.error("%s for url %s", err, url)
    except http.client.IncompleteRead as err:
        logging.error("%s", err)

    return forecast_data


def store_forecasts(cities, pnames, basepath=''):
    """store_forecast but takes list of cities and plugin names."""
    for city in list(cities):
        for pname in list(pnames):
            store_forecast(city, pname, basepath)
