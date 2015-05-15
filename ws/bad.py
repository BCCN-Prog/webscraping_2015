"""'bad' is our exceptions module, here are our package specific exceptions defined."""

class City(Exception):
    """Cannot fetch weather forcast for city."""
    print("Cannot fetch weather forcast for city.")
    
class Type(Exception):
    pass
