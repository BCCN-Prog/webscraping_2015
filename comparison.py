import os
import pickle
import pandas as pd
import datetime
import numpy as np
import click
import weather_loading as wl
import matplotlib.pyplot as plt
plt.style.use('ggplot')


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
    complete_errorpath = os.path.join(error_path, "errorfile.csv")
    with open(complete_errorpath,'rb') as f:
        error_data = pd.read_csv(f)
        
    # get rows with the correct city and provider
    error_data_city = error_data[error_data['city']==city]
    
    return error_data_city[error_data_city['Provider']==provider]
    

def get_score(dwd_data, forecast_data, provider):
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
    :return:dictionary of differences between dwd and forecast (dwd-forecast)
    for the columns/keys Air Temperature, Rel Humidity, Wind Speed, Max Air Temp, Min Air Temp
    Precipitation, Snow Depth
    openweathermap nan = 0 and rain in millimeters
    accuweather - rain in millimeters. only supplies min and max temperature
    weatherdotcom - gives rain only for today
    """

    if not len(forecast_data) or not len(dwd_data):
        return [None,None,None,None]
    temp = (dwd_data['Air Temperature'].values - forecast_data['Air Temperature'].values)

    if provider =='weatherdotcom':
        prec = [None]
        min_t = [None]
        max_t = [None]
    else:
        prec = (dwd_data['Precipitation'].values - forecast_data['Precipitation'].fillna(0).values)
        max_t = (dwd_data['Max Air Temp'].values - forecast_data['Max Air Temp'].values)
        min_t = (dwd_data['Min Air Temp'].values - forecast_data['Min Air Temp'].values)

    return [temp[0], max_t[0], min_t[0], prec[0]]

def get_data_dwd(city, start_date, end_date, dwd_path):
    """reads in the city, date and dwd_path and returns the data queried from the dwd path
    
    :param city: city for which the weather forecast is for
    :type string
    :param date: date for which the weather forecast is for
    :type datetime
    :param dwd_path: path to the database repository (where the file weather_loading.py is)
    :type string
    :return: dataFrame containing relevant dwd data
    """
    #curr_wd = os.getcwd()
    #os.chdir(dwd_path)

    dataFrame = wl.load_dataframe(city, start_date.replace('-', ''), end_date.replace('-', ''),True)

    #os.chdir(curr_wd)
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
    data_city = forecast_dataframe[forecast_dataframe['city']==city]
    data_prov = data_city[data_city['Provider']==provider]
    data_date = data_prov[data_prov['ref_date']==date]

    if provider == 'openweathermap':
        data_date[(data_date['pred_offset'].values-data_date['ref_date'])]
        
    return data_date[data_date['pred_offset'] == offset]



def update_errors(end_date, dwd_path, forecast_path, complete_errorpath, start_date='2015-06-01'):
    """adds to the errors file error entry for a specific date

    :param start_date: start of period to claculate erros
    :param end_date: end of period to claculate erros
    :type datetime (python package datetime.datetime)
    :param forecast_path: path to the forecast master dataframe. default - file is in the same directory
    :type string
    :param dwd_path: path to dwd downloaded data
    :type string
    :param errors_path: path to the errors file that should be updated
    :type string
    :return:
    """

    # load the forecasts file
    with open(forecast_path,'rb') as f:
        forecasts = pd.read_csv(f)

    dates = pd.date_range(start_date, end_date, freq='D')
    citylist = ['berlin','hamburg','bremen','stuttgart']
    providerlist = ['accuweather', 'openweathermap', 'weatherdotcom']
    values_names_list = ['Precipitation', 'Air Temperature', 'Max Air Temp', 'Min Air Temp']

    errors_cols = ['Provider', 'city', 'date', 'offset', 'Air Temperature', \
                        'Max Air Temp', 'Min Air Temp', 'Precipitation']
    errorData = pd.DataFrame(columns = errors_cols)
    for city in citylist:
        #print('city: ' + city)
        dwd_data = get_data_dwd(city,start_date, end_date, dwd_path)
        if not len(dwd_data):
            print("no dwd data was found")
            return
        else:
            #average across stations (super ugly code  :( )
            dwd_mat = []
            for val in values_names_list:
                dat = pd.concat([dwd_data[station].loc[:, val] for station in dwd_data],axis=1)
                dat_mean = pd.DataFrame(dat.mean(axis=1))
                dat_mean.columns = [val]
                dwd_mat.append(dat_mean)
            dwd_data = pd.concat(dwd_mat,axis=1)

            for date in dates:
                #print('date: '+str(date))
                for provider in providerlist:
                    #print('provider: '+provider)
                    dwd_data_date = dwd_data[dwd_data.index == date]
                    forecast_data = load_specific_forecast(city, provider, date, forecasts)
                    #print(forecast_data)
                    if len(forecast_data):
                        offset_range = 7
                        for offset in range(offset_range):
                            #print('offset: '+str(offset))
                            date_forecast = forecast_data[forecast_data['pred_offset'].astype(int) == int(offset)]
                            if len(date_forecast):
                                scores = [provider, city, date, offset]
                                scores += get_score(dwd_data_date, date_forecast, provider)
                                errorData = \
                                errorData.append(pd.DataFrame(columns = errors_cols, data = np.matrix(scores)))
                            else:
                                print('forecast not found for %s in %s during %s and offset %s' % (provider, city, date, offset))

    if os.path.getsize(complete_errorpath) > 0:
        errorData.to_csv(complete_errorpath, mode = 'a', header=False)
    else:
         errorData.to_csv(complete_errorpath)
    print("Saved error data to " + complete_errorpath)


def load_specific_forecast(city, provider, date, forecasts):
    """reads in the city, provider, date and forecast_path and returns the data queried from the forecast path

    :param city: city for which the weather forecast is for
    :type string
    :param provider: provider for which the weather forecast is for
    :type string
    :param date: date for which the weather forecast is for, e.g. '2015-06-29'
    :type datetime
    :param forecasts: dataframe containing all forecasts
    :type pandas dataframe
    :return: dataFrame containing relevant dwd data
    """

    # get rows with the correct city, provider and date
    data_city = forecasts[forecasts['city']==city]
    data_provider = data_city[data_city['Provider']==provider]

    if provider != 'openweathermap':
        # cut the time
        data_provider.loc[:, 'Date'] = data_provider.loc[:, 'Date'].map(cut_time, na_action='ignore')
        data_provider.loc[:, 'ref_date'] = data_provider.loc[:,'ref_date'].map(cut_time, na_action='ignore')

    else:
        data_provider.loc[:, 'ref_date'] = data_provider.loc[:,'ref_date'].map(cut_time,na_action='ignore')
        data_provider.loc[:, 'Date'] = data_provider.loc[:,'pred_offset'].map(cut_time, na_action='ignore')
        data_provider.loc[:, 'pred_offset'] = (data_provider.loc[:,'Date'] - data_provider['ref_date']).\
            map(lambda delta: delta/np.timedelta64(1, 'D'), na_action='ignore')
    
    return data_provider[data_provider['Date'] == date]

def cut_time(date_frmt):
    """ cuts the time of the datetime format
    
    :param date_frmt: date in the format %Y-%m-%d %H:%M:%S
    :type datetime or string
    :return: date in the format %Y-%m-%d
    """

    frmt = '%Y-%m-%d'
    if isinstance(date_frmt, str):
        res = datetime.datetime.strptime(date_frmt[:10], frmt)
    if isinstance(date_frmt, datetime.datetime):
        res = datetime.datetime.strptime(date_frmt.strftime(frmt),frmt)
    return res


@click.command()
@click.option("--errors_path", type=click.STRING, default="")
@click.option("--update_errors_file", type=click.BOOL, default=False)
@click.option("--forecast_path", type=click.STRING, default="master_pandas_file.csv")
@click.option("--dwd_path", type=click.STRING, default="/Users/smartMac/webscraping/")
def main(errors_path, forecast_path, dwd_path, update_errors_file):

    citylist = ['berlin']#,'hamburg','bremen','stuttgart']
    providerlist = ['accuweather' , 'openweathermap', 'weatherdotcom']
    complete_errorpath = os.path.join(errors_path, "errorfile.csv")

    #diffs = pd.read_csv(complete_errorpath)
    if update_errors_file:
        try:
            diffs = pd.read_csv(complete_errorpath)

            if len(diffs):
                start_date = cut_time(diffs.loc[:,'date'].max()) + datetime.timedelta(days = 1)
            else:
                start_date = '2015-06-01'
        except ValueError:
            start_date = '2015-06-01'

        end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
        update_errors(end_date, dwd_path, forecast_path , complete_errorpath, start_date)
    diffs = pd.read_csv(complete_errorpath)

    values_names_list = ['Precipitation', 'Air Temperature', 'Max Air Temp', 'Min Air Temp']
    res_cols = ['provider', 'city', 'offset', 'Precipitation', 'Air Temperature', 'Max Air Temp', 'Min Air Temp']
    res_frame_mean = pd.DataFrame(columns = res_cols)
    res_frame_bias = pd.DataFrame(columns = res_cols)
    res_frame_norm = pd.DataFrame(columns = res_cols)
    res_frame_abs_mean = pd.DataFrame(columns = res_cols)
    for provider in providerlist:
        diffs_prov = diffs[diffs.loc[:,'Provider']==provider]
        for city in citylist:
            diffs_prov_city = diffs_prov[diffs_prov.loc[:,'city']==city]
            groups = diffs_prov_city.groupby('offset')
            for offset in range(7):
                score = [provider, city, offset]
                g = groups.get_group(offset)
                score_mean = score + [g.loc[:, val].astype(float).mean() for val in values_names_list]
                res_frame_mean = res_frame_mean.append(pd.DataFrame(columns = res_cols, data = np.matrix(score_mean)))

                score_var = score + [g.loc[:,val].std() for val in values_names_list]
                res_frame_bias = res_frame_bias.append(pd.DataFrame(columns = res_cols, data = np.matrix(score_var)))

                score_norm = score + [np.sqrt(np.square(g.loc[:,val].dropna()).sum()) / np.sqrt(len(g.loc[:,val].dropna()))\
                                      for val in values_names_list]

                res_frame_norm = res_frame_norm.append(pd.DataFrame(columns = res_cols, data = np.matrix(score_norm)))

                score_abs_man = score + [np.abs(g.loc[:, val].dropna()).sum() / len(g.loc[:,val].dropna())\
                                      if len(g.loc[:,val].dropna()) > 0 else None for val in values_names_list]

                res_frame_abs_mean = res_frame_abs_mean.append(pd.DataFrame(columns = res_cols, data = np.matrix(score_abs_man)))



    print('mean error: ')
    print(res_frame_mean)
    print('error variance')
    print(res_frame_bias)
    print('RMS error')
    print(res_frame_norm)
    print('Mean abs')
    print(res_frame_abs_mean)

    #plot stuff
    df_a_mean = res_frame_mean[res_frame_mean['provider']=='openweathermap']
    df_a_bias = res_frame_bias[res_frame_bias['provider']=='openweathermap']

    df_o_mean = res_frame_mean[res_frame_mean['provider']=='accuweather']
    df_o_bias = res_frame_bias[res_frame_bias['provider']=='accuweather']

    plt.figure()
    plt.subplot(1,2,1)
    plt.errorbar(df_a_mean['offset'].astype('int'), df_a_mean['Precipitation'].astype('float'), yerr =df_a_bias['Precipitation'].astype('float'), fmt='o', capthick=2)
    plt.xlabel('offset in days')
    plt.xlim((-0.5,6.5))
    plt.title('openweathermap' + ': ' +'Precipitation')

    plt.subplot(1,2,2)
    plt.errorbar(df_o_mean['offset'].astype('int'), df_o_mean['Precipitation'].astype('float'), yerr =df_o_bias['Precipitation'].astype('float'), fmt='o', capthick=2)
    plt.xlabel('offset in days')
    plt.xlim((-0.5,6.5))
    plt.title('accuweather' + ': ' +'Precipitation')


    plt.figure()
    plt.subplot(1,2,1)
    plt.errorbar(df_o_mean['offset'].astype('int')+0.1, df_o_mean['Max Air Temp'].astype('float'), yerr =df_o_bias['Max Air Temp'].astype('float'), label = 'Max Air Temp', fmt='o', capthick=2)
    plt.errorbar(df_o_mean['offset'].astype('int'), df_o_mean['Min Air Temp'].astype('float'), yerr =df_o_bias['Min Air Temp'].astype('float'), label = 'Min Air Temp', fmt='o', capthick=2)
    plt.xlabel('offset in days')
    plt.title('openweathermap')
    plt.legend()

    plt.subplot(1,2,2)
    plt.errorbar(df_a_mean['offset'].astype('int')+0.1, df_a_mean['Max Air Temp'].astype('float'), yerr =df_a_bias['Max Air Temp'].astype('float'), label = 'Max Air Temp', fmt='o', capthick=2)
    plt.errorbar(df_a_mean['offset'].astype('int'), df_a_mean['Min Air Temp'].astype('float'), yerr =df_a_bias['Min Air Temp'].astype('float'), label = 'Min Air Temp', fmt='o', capthick=2)
    plt.xlabel('offset in days')
    plt.title('accuweather')
    plt.legend()



    plt.show()




if __name__ == '__main__':
    main()

