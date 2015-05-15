import os
import re
import importlib as imp


def load_plugin(plugin):
    """Return instance of plugin.

    'plugin' is the package name as a string.
    """
    sub_package = None

    if re.match('^[\w-]+$', plugin):
        plugin_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   plugin)
        if os.path.isdir(plugin_path):
            # http://stackoverflow.com/a/10675081
            sub_package = imp.import_module('.' + plugin, package='ws.plugins')

    return sub_package


def _bad_plugins():
    """Return list with bad plugins from file NO_DIRS_ONLY_PLUGINS_HERE.

    NO_DIRS_ONLY_PLUGINS_HERE should have one directory per line.
    """
    my_dir = os.path.dirname(os.path.realpath(__file__))

    l = [line.strip() for line in open(os.path.join(my_dir,
                                                    'NO_DIRS_ONLY_PLUGINS_HERE'),
                                       'r')]

    return l


def list_plugins():
    """Return a list with all plugins."""
    l = []

    my_dir = os.path.dirname(os.path.realpath(__file__))
    for sub_package in os.listdir(my_dir):
        if (os.path.isdir(os.path.join(my_dir, sub_package)) and sub_package
                not in _bad_plugins()):
            l.append(sub_package)

    return sorted(l)
