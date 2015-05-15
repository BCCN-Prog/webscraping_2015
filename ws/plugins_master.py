from .plugins import *
import urllib


l = list_plugins()
print(l)

o = load_plugin(l[0]).build_url('test')
print(o)

def download_from_url(url):
    http = urllib.PoolManager()
    r = http.request('GET', url)
    data = str(r.data)

    return data


def generate_forecast_filepath(pname, city, ):
    """
    forecasts/pname/city/
    """
    posix_time = time.time()
    utc_posix_time = posix_time - time.timezone
    # create directory

    if not os.path.exists(directory):
        os.makedirs(directory)


    filepath = city + '_' + current_time + \ '_openweathermap_16_days' + '.forecast'

def save_to_disk(data, filepath):
    text_file = open(, "w")
    text_file.write(forecast)
    text_file.close()

    return forecast


plugins = list_plugins()
for city in citylist:
    for pname in plugins:
        p = load_plugin(pname)
        url = p.build_url(city)
        weather_data = download_from_url(url)

