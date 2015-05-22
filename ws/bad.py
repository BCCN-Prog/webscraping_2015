"""'bad' is our exceptions module, here are our package specific exceptions defined."""

class City(Exception):
    """Cannot fetch weather forcast for city."""

class PluginExistsNot(Exception):
    """Plugin does not exist."""
    pass
