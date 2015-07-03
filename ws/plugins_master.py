from .plugins import *
import time
import pickle
import os
import logging
import ws.bad as bad
import urllib.error
import http.client
from .tools import misc
import multiprocessing
import pandas as pd
import datetime
import numpy as np
import shutil

def generate_forecast_filepath(pname, city, basepath=''):
    """Generate forecast filepath.

    basepath/city/pname
    """
    posix_time = time.time()
    utc_posix_time = posix_time + time.timezone

    forecast_dir = os.path.join(basepath, city, pname)
    # exist_ok=True to make the function thread safe.
    os.makedirs(forecast_dir, exist_ok=True)

    filename = str(utc_posix_time).replace('.', 's', 1) + '.forecast'
    forecast_path = os.path.join(forecast_dir, filename)

    return forecast_path


def get_citylist():
    """Return list with all city
    names."""
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
    except bad.City:
        logging.error('plugin %s cannot deal with city %s', pname, city)
        return -1

    failcounter = 0
    continue_loop = True
    while continue_loop:
        try:
            try:
                url = p.build_url(str(city))
            except bad.City:
                logging.error('plugin %s cannot deal with city %s', pname, city)
                return -1
            forecast_data = misc.download_from_url(url)
            continue_loop = False
            if failcounter == 0:
                logging.info('Queried %s for %s successfully', pname, city)
        except urllib.error.HTTPError as err:
            failcounter += 1
            logging.error("%s for url %s", err, url)
            logging.info("Trying again...")
            logging.info("This was attempt number " +str(failcounter))
        except http.client.IncompleteRead as err:
            logging.error("%s", err)

        if failcounter > 0 and continue_loop == False:
            logging.info("SUCCESS! This time querying %s worked", pname)

        if continue_loop == False:
            break
        
    # save the data to disk
    filepath = generate_forecast_filepath(pname, city, basepath)
    misc.save_to_disk(forecast_data, filepath)
    
    # save all the data also into a temporary directory
    basepath_temp = os.path.join(basepath, 'temp')
    filepath_temp = generate_forecast_filepath(pname, city, basepath_temp)
    misc.save_to_disk(forecast_data, filepath_temp)

    return forecast_data


def store_forecasts_loop(cities, pname, basepath=''):
    try:
        for city in list(cities):
            store_forecast(city, pname, basepath)
    except KeyboardInterrupt as err:
        raise KeyboardInterrupt(err)


def store_forecasts(cities, pnames, basepath=''):
    """store_forecast but takes list of cities and plugin names.

    Each plugin gets its own process. This way a plugin can rate limit without
    blocking the others.
    """

    
    for pname in list(pnames):
        p = multiprocessing.Process(target=store_forecasts_loop,
                                    args=(cities, pname, basepath))
        p.start()


def forecasts_newer_than(newer_than, basepath='', cities='all'):
    if cities == 'all':
        cities = os.listdir(basepath)

    forecast_lists = {}
    for city in cities:
        if city == 'temp':
            continue
        
        if city not in os.listdir(basepath):
            logging.info("One of the cities you wanted to pandize was not found in folder")
            continue

        for provider in os.listdir(os.path.join(basepath, city)):
            logging.debug(provider)
            if provider not in forecast_lists:
                forecast_lists[provider] = []
            for forecast in os.listdir(os.path.join(basepath, city, provider)):
                utc_posix_time = float(forecast.replace('s', '.',
                                                        1)[:-len('.forecast')])
                if utc_posix_time > newer_than:
                    filepath = os.path.join(basepath, city, provider, forecast)
                    with open(filepath, 'r') as fd:
                        forecast_lists[provider].append([fd.read(), city,
                                                         datetime.datetime.fromtimestamp(utc_posix_time)])

    return forecast_lists


def pandize_plugin_forecasts(forecast_lists, pname, database_filepath):
    p = load_plugin(str(pname))
    for forecast_list in forecast_lists:
        logging.debug('Pandizing provider %s city %s date %s', pname, forecast_list[1],
                      forecast_list[2])
        try:
            pandas_table = p.pandize(*forecast_list)
            insert_into_master_frame(pandas_table)
        except Exception:
            logging.error("Error while parsing one forecast in " + str(pname))
            
            
# this is the overall pandize function that will loop over all plugins
# and then call pandize_plugin_forecasts separately for each plugin
def pandize_forecasts(pnames, database_filepath='', basepath='', newer_than=0, cities='all'):
    global master_frame
    forecast_lists = forecasts_newer_than(newer_than, basepath, cities)
    logging.debug("pandize forecasts was called for the following providers (next line)")
    logging.debug(pnames)
    for pname in list(pnames):
        if pname in forecast_lists:
            pandize_plugin_forecasts(forecast_lists[pname], pname,
                                     database_filepath)
    
    # save the master pandas dataframe
    logging.info("Done with pandizing, saving to disk now!")
    pickle.dump(master_frame, open("master_pandas_file.dump", "wb"))
    master_frame.to_csv("master_pandas_file.csv")

def pandize_temporary_forecasts(pnames, database_filepath='', basepath='', cities='all'):
    basepath_temp = os.path.join(basepath,'temp')
    if os.path.exists(basepath_temp):
        logging.debug("Temporary files exist, starting to pandize them")
        pandize_forecasts(pnames, database_filepath, basepath_temp, 0, cities)
    else:
        logging.error("There are no temporary files in the basepath you provided")
    
    # delete the temporary directory that stores the just pandized forecasts
    if os.path.exists(basepath_temp):
        shutil.rmtree(basepath_temp)

def insert_into_master_frame(pandas_part):
    global master_frame
    
    if type(pandas_part) == pd.core.frame.DataFrame:
       master_frame = master_frame.append(pandas_part)
       logging.info("Pandized successfully")
    else:       
       logging.info("One pandized row not entered into master frame because" + \
               " received -1 from pandize function. This an expected problem" + \
               " unless you would see it happening a lots (hundreds) of times")
        

# yes, this solution  of having the master frame as a global variable is terrible,
# but there's no way around it (that's not extremely
# inconvenient).
if os.path.exists("master_pandas_file.dump"):
    logging.info("Found a pandas master frame, loading it..")
    master_frame = pickle.load(open("master_pandas_file.dump", "rb"))
else:
    logging.info("Didn't find a pandas master frame, creating one...")
    master_frame = pd.DataFrame(columns=
        np.array(['Provider','ref_date','city','pred_offset','Station ID', 'Date', \
            'Quality Level', 'Air Temperature', \
            'Vapor Pressure', 'Degree of Coverage', 'Air Pressure', 'Rel Humidity', \
            'Wind Speed', 'Max Air Temp', 'Min Air Temp', 'Min Groundlvl Temp', \
            'Max Wind Speed', 'Precipitation', 'Precipitation Ind', 'Hrs of Sun', \
            'Snow Depth']))