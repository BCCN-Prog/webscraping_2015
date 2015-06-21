from .main import build_url, pandize, url_storage_function
wug_urls_book = pickle.load(open(os.path.join(mydir, 'cities_urls'), 'rb'))