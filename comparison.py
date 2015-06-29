

def get_score_for_city(city, error_path):
    """reads in a city and the error_path and displays the score for all providers.
    score is a matrix (measures X offsets)
    for each entry in the matrix we will average over date, and get the standard deviation
    we will also display the average absolute error.

    :param city: city for which the weather forecast is for
    :type string
    :param error_path: path to error data
    :type string
    :return: None
    """

    pass


def load_error_data(city, provider, error_path):
    """

    :param city: city for which the weather forecast is for
    :type string
    :param provider: provider for which the weather forecast is for
    :type string
    :param error_path: path to error data
    :type string
    :return: dataFrame containing all errors for a city and provider
    """

    error_data = 0
    return error_data

def get_score(dwd_data, forecast_data):
    """Gets a single pandas table rows of the dwd data and forecast_data and
    returns scalar error-values for each column

    :param dwd_data:  single row of a pandas table with columns = ['Provider','ref_date','city','pred_offset','Station ID', 'Date', 'Quality Level', 'Air Temperature', \
    'Vapor Pressure', 'Degree of Coverage', 'Air Pressure', 'Rel Humidity', \
    'Wind Speed', 'Max Air Temp', 'Min Air Temp', 'Min Groundlvl Temp', \
    'Max Wind Speed', 'Precipitation', 'Precipitation Ind', 'Hrs of Sun', \
    'Snow Depth']
    :type: dataframe
    :param forecast_data: single row of a pandas table with columns = ['Provider','ref_date','city','pred_offset','Station ID', 'Date', 'Quality Level', 'Air Temperature', \
    'Vapor Pressure', 'Degree of Coverage', 'Air Pressure', 'Rel Humidity', \
    'Wind Speed', 'Max Air Temp', 'Min Air Temp', 'Min Groundlvl Temp', \
    'Max Wind Speed', 'Precipitation', 'Precipitation Ind', 'Hrs of Sun', \
    'Snow Depth']
    :type: dataframe
    :return:list of differences between dwd and forecast (dwd-forecast)
    for the columns Air Temperature, Rel Humidity, Wind Speed, Max Air Temp, Min Air Temp
    Precipitation, Snow Depth
    """

    errors = []
    comparison_columns = ['Air Temperature', 'Rel Humidity', 'Wind Speed', 'Max Air Temp', 'Min Air Temp',
    'Precipitation', 'Snow Depth']
    for col in comparison_columns:
        errors.append(dwd_data[col]-forecast_data[col])
    return errors

def get_data_dwd(city,date,dwd_path):
    """reads in the city, date and dwd_path and returns the data queried from the dwd path

    :param city: city for which the weather forecast is for
    :type string
    :param date: date for which the weather forecast is for
    :type datetime
    :param dwd_path: path to the corresponding dwd data
    :type string
    :return: dataFrame containing relevant dwd data
    """

    pass


def get_date_forecast(city, provider, date, offset, forecast_dataframe):
    """Returns the row of the forecast_dataframe corresponding to the given city, provider, date
    and offset.

    :param city: city name
    :type string
    :param provider: provider name
    :type string
    :param date: date of the day for which to get the forecast
    :type datetime (python package datetime.datetime)
    :param offset: day of forecast minus day where forecast was made
    :type int
    :param forecast_dataframe:
    :type pandas dataframe
    :return: pandas dataframe row of forecast_dataframe corresponding to the
    given parameters
    """
    pass


def update_forecasts(date, forecast_path, dwd_path, errors_path):
    """adds to the errors file error entry for a specific date

    :param date: date for which we want to calculate the errors
    :type datetime (python package datetime.datetime)
    :param forecast_path: path to the forecast master dataframe
    :type string
    :param dwd_path: path to dwd downloaded data
    :type string
    :param errors_path: path to the errors file that should be updated
    :type string
    :return:
    """
    pass

