from ws.plugins_master import get_citylist, store_forecasts
from ws.plugins_master import store_forecasts
from ws.plugins import list_plugins
import logging
import getopt
import textwrap
import sys


def help_msg():
    help_str = textwrap.dedent("""\
                               Do you need help?
    """)
    print(help_str)


def cli(argv):
    basepath = ''
    pname = None
    city = None
    verbosity = logging.WARNING

    try:
        opts, args = getopt.getopt(argv[1:], 'h', ['verbosity=', 'provider=',
                                                  'city=', 'folder='])
    except getopt.GetoptError:
        logging.error("wrong usage")
        help_msg()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--verbosity':
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
            help_msg()
            sys.exit()
        elif opt == '--provider':
            pname = arg

    logging.basicConfig(format="%(levelname)s: %(message)s", level=verbosity)

    if city == None:
        city = get_citylist()
    else:
        city = city.split(",")

    if pname == None:
        pname = list_plugins()
    else:
        pname = pname.split(",")

    store_forecasts(city, pname, basepath)
