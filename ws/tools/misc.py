import logging
import urllib.request


def save_to_disk(data, filepath):
    """Write data to filepath."""
    filepath = str(filepath)
    data = str(data)
    logging.debug('writing data of length %d to file %s', len(data), filepath)
    fs = open(filepath, 'w')
    fs.write(data)
    fs.close()


def download_from_url(url):
    """Download url and return the content."""
    logging.debug('url %s', url)
    r = urllib.request.urlopen(url)
    data = str(r.read())

    return data
