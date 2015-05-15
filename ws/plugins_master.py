from .plugins import *
import urllib
import time


def download_from_url(url):
    http = urllib.PoolManager()
    r = http.request('GET', url)
    data = str(r.data)

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

    filename = utc_posix_time.replace('.', 's', 1) + '.forecast'
    forecast_path = os.path.join(forecast_dir, filename)

    return forecast_path


def save_to_disk(data, filepath):
    fs = open(filepath, 'w')
    fs.write(data)
    fs.close()


citylist = pickle.load(open('citylist.dump', 'rb'))

for city in citylist:
    for pname in list_plugins():
        p = load_plugin(pname)
        url = p.build_url(city)
        forecast_data = download_from_url(url)
        filepath = generate_forecast_filepath(pname, city)
        save_to_disk(forecast_data, filepath)

