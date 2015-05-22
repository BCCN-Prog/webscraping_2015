def build_url(city):
    # check whether input is a string
    if type(city) != str:
        raise ValueError("The input city " + str(city) + " wasn't of type string")

    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' \
          + city \
          + '&mode=xml' \
          + '&units=metric' \
          + '&cnt=16' # 'cnt = 16' means next 16 days

    return url
