If you want to start the webscraping you should
first start your Command Window and go to the
directory /webscraping. From here you can use
the following command (note that you need to
have Python 3 installed):
python webscraping --provider --city --folder

The flags have the following options(for
providers and city several options are possible,
just separate them by a comma without spaces):

--provider: accuweather,weatherdotcom,wunderground,openweathermap
			(default is all providers)
			
--city: 	almost any german city name(if misspelled
			or not included you will get an error,
			default is all cities)
			
--folder: 	specify the folder where you want to
			save the forecasts relative to the
			webscraping folder(if the folder does
			not exist it will be created,default is
			forecasts)
			
For example, to get the forecasts from accuweather
and wunderground for Berlin,Bremen and Munich and
save them into the folder ..\myForecasts you have
to write:
python webscraping --provider=accuweather,wunderground --city=berlin,bremen,munich --folder=myForecasts
