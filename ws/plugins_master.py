from .plugins import *
import urllib.request
import time
import pickle
import os
import logging
import ws.bad as bad


def download_from_url(url):
    """Download url and return the content."""
    try:
        r = urllib.request.urlopen(url)
    except:
        return "Received errorcode from server"
    data = str(r.read())

    return data


def generate_forecast_filepath(pname, city, basepath=''):
    """Generate forecast filepath.

    basepath/forecasts/city/pname
    """
    posix_time = time.time()
    utc_posix_time = posix_time + time.timezone

    forecast_dir = os.path.join(basepath, 'forecasts', city, pname)
    if not os.path.exists(forecast_dir):
        os.makedirs(forecast_dir)

    filename = str(utc_posix_time).replace('.', 's', 1) + '.forecast'
    forecast_path = os.path.join(forecast_dir, filename)

    return forecast_path


def save_to_disk(data, filepath):
    """Write data to filepath."""
    fs = open(filepath, 'w')
    fs.write(data)
    fs.close()


def get_citylist():
    """Return list with all city names."""
    # XXX this is tmp solution, we should use a better format for storage
    fp = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'citylist.dump')
    citylist = pickle.load(open(fp, 'rb'))
    citylist = [str(i) for i in citylist]

    return citylist


def store_forecast(city, pname, basepath=''):
    """Store forecast for city from plugin pname."""
    logging.debug('store_forecast(city=%s,pname=%s,basepath=%s)', city, pname,
                 basepath)
    p = load_plugin(pname)

    # XXX tmp solution, we should handle this correctly
    try:
        url = p.build_url(city)
        forecast_data = download_from_url(url)
        
        # check whether downloading from url worked
        if forecast_data == "Received errorcode from server":
            raise RuntimeError()
        filepath = generate_forecast_filepath(pname, city, basepath)
        save_to_disk(forecast_data, filepath)
    except bad.City:
        logging.error('plugin %s cannot deal with city %s', pname, city)
    except:
        logging.error("Plugin %s received server error for city %s", pname, city)

    return forecast_data


def store_forecasts(cities, pnames, basepath=''):
    """store_forecast but takes list of cities and plugin names."""
    for city in cities:
        for pname in pnames:
            #logging.debug("")
            store_forecast(city, pname, basepath)
