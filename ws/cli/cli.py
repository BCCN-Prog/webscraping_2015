from ws.plugins_master import get_citylist, store_forecasts
from ws.plugins_master import store_forecasts
from ws.plugins import list_plugins
import logging
import getopt
import textwrap
import sys
import os


def print_readme():
    """Print README.txt"""
    readme_file = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                '..', '..', 'README.txt'))
    with open(readme_file, 'r') as fp:
            print(fp.read())


def cli(argv):
    """The CLI, argv is sys.argv"""
    basepath = 'forecasts'
    pname = None
    city = None
    verbosity = logging.WARNING

    try:
        opts, args = getopt.getopt(argv[1:], 'h', ['verbosity=', 'provider=',
                                                  'city=', 'folder='])
    except getopt.GetoptError:
        print(('Because you obviously did not read README.txt, '
              'I will print it for you.'))
        print()
        print('------------README.txt------------')
        print_readme()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--verbosity':
            # levels https://docs.python.org/3/library/logging.html#logging-levels
            if int(arg) <= 0:
                # default
                pass
            if int(arg) == 1:
                verbosity = logging.INFO
            if int(arg) >= 2:
                verbosity = logging.DEBUG
        elif opt == '--city':
            city = arg
        elif opt == '--folder':
            basepath = arg
        elif opt == '-h':
            print_readme()
            sys.exit()
        elif opt == '--provider':
            pname = arg

    # attributes https://docs.python.org/3/library/logging.html#logrecord-attributes
    logging.basicConfig(format=("%(asctime)s "
                                "[%(levelname)s,%(filename)s,%(funcName)s]: "
                                "%(message)s"), level=verbosity)

    if city == None:
        city = get_citylist()
    else:
        city = city.split(",")

    if pname == None:
        pname = list_plugins()
    else:
        pname = pname.split(",")


    if len(city) < 10:
        logging.info('cities to fetch forcast for cities %s',  str(city))
    else:
        logging.info('will fetch forcast for %d cities',  len(city))
    logging.info('providers to use: %s',  str(pname))
    logging.info('verbosity level is %s', logging.getLevelName(verbosity))
    logging.info('folder to store forcasts in is %s', str(basepath))

    store_forecasts(city, pname, basepath)
