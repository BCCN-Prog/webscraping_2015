

def get_score_for_city(city, error_path):
    """reads in a city and the error_path and displays the score

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