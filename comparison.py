import os
import pickle

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
    """Loads the error file and returns the error data for the specific city and provider given in the query 

    :param city: city for which the weather forecast is for
    :type string
    :param provider: provider for which the weather forecast is for
    :type string
    :param error_path: path to error data
    :type string
    :return: dataFrame containing all errors for a city and provider
    """
    # load the file
    with open(error_path,'rb') as f:
        error_data = pickle.load(f)
        
    # get rows with the correct city and provider
    error_data_city = error_data[error_data['city']==city]
    
    return error_data_city[error_data_city['Provider']==provider]
    

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

    errors = {'Air Temperature':0, 'Rel Humidity':0, 'Wind Speed':0, 'Max Air Temp':0, 'Min Air Temp':0,
    'Precipitation':0, 'Snow Depth':0}
    for col in errors.keys():
       errors[col] = dwd_data[col]-forecast_data[col]
    return errors

def get_data_dwd(city,date,dwd_path):
    """reads in the city, date and dwd_path and returns the data queried from the dwd path
    
    :param city: city for which the weather forecast is for
    :type string
    :param date: date for which the weather forecast is for
    :type datetime
    :param dwd_path: path to the database repository (where the file weather_loading.py is)
    :type string
    :return: dataFrame containing relevant dwd data
    """
    curr_wd = os.getcwd()
    os.chdir(dwd_path)
            
    import weather_loading as wl
    yyyy =  str(date.year)
    mm = str(date.month)
    dd = str(date.day)
    if len(mm)==1:
        mm = '0'+mm
    if len(dd)==1:
        dd = '0'+dd
    date_for_wl = yyyy+mm+dd
    dataFrame = wl.weather_loading(city,date_for_wl,date_for_wl,False)

    os.chdir(curr_wd)
    return dataFrame


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


def update_errors(date, forecast_path, dwd_path, errors_path):
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
    citylist = getCitylist()
    providerlist = ['accuweather', 'openweathermap', 'weatherdotcom']
    
    for city in citylist:
        dwdData = get_data_dwd(city,date,dwd_path)
        
        for provider in providerlist:
            forecastData = load_forecasts(city,provider,date,forecast_path)
            offset_range = 7
            for offset in range(offset_range):
                
                date_forecast = get_date_forecast(city,provider,date,offset,forecastData)
                scores = get_score(dwdData,date_forecast)
                scores['offset'] = offset
                scores['city'] = city
                scores['date'] = date

                errorData.append(scores,ignore_index=True)               
    
    with open(error_path,'rb') as f:
        errorData = pickle.load(f)
    pickle.dump(errorData, open("master_errors_file.dump", "wb"))
    pass

def load_forecasts(city,provider,date,forecast_path):
    """reads in the city, provider, date and forecast_path and returns the data queried from the forecast path

    :param city: city for which the weather forecast is for
    :type string
    :param provider: provider for which the weather forecast is for
    :type string
    :param date: date for which the weather forecast is for, e.g. '2015-06-29'
    :type datetime
    :param dwd_path: path to the corresponding dwd data
    :type string
    :return: dataFrame containing relevant dwd data
    """
    
    # load the file
    with open(forecast_path,'rb') as f:
        data = pickle.load(f)
        
    # get rows with the correct city, provider and date
    data_city = data[data['city']==city]
    data_provider = data_city[data_city['Provider']==provider]
    
    # cut the time 
    data_provider['Date'] = data_provider['Date'].apply(cut_time)

    return data_provider[data_provider['Date']==date]
    
def cut_time(date_frmt):
    """ cuts the time of the datetime format
    
    :param date_frmt: date in the format %Y-%m-%d %H:%M:%S
    :type datetime
    :return: date in the format %Y-%m-%d
    """
    frmt = '%Y-%m-%d'
    return date_frmt.strftime(frmt)
    