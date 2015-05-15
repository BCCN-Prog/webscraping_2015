from .plugins import *
import urllib.request
import time
import pickle
import os


def download_from_url(url):
    r = urllib.request.urlopen(url)
    data = str(r.read())

    return data


def generate_forecast_filepath(pname, city):
    """
    forecasts/pname/city/
    """
    posix_time = time.time()
    utc_posix_time = posix_time - time.timezone

    forecast_dir = os.path.join('forecasts', pname, city)
    if not os.path.exists(forecast_dir):
        os.makedirs(forecast_dir)

    filename = str(utc_posix_time).replace('.', 's', 1) + '.forecast'
    forecast_path = os.path.join(forecast_dir, filename)

    return forecast_path


def save_to_disk(data, filepath):
    fs = open(filepath, 'w')
    fs.write(data)
    fs.close()

print('plugins_master was run')

citylist = pickle.load(open(os.path.join('ws', 'citylist.dump'), 'rb'))

while True:
    if time.strftime("%H") == "03" and time.strftime("%M") == "00":
        for city in citylist:
            print("I'm working on city " + str(city))
            for pname in list_plugins():
                print('Working on ' +str(pname) + ' provider')
                p = load_plugin(pname)
                try:
                    url = p.build_url(str(city))
                except:
                    pass
                forecast_data = download_from_url(url)
                filepath = generate_forecast_filepath(pname, city)
                save_to_disk(forecast_data, filepath)
