If you want to start the webscraping you should first start your Command Window
and go to this directory. From here you can use the following command (note that
you need to have Python 3 installed):

python webscraping.py --provider=my_provider --city=my_city --folder=my_folder

The flags have the following options(for providers and city several options are
possible, just separate them by a comma without spaces):

--provider:	accuweather,weatherdotcom,wunderground,openweathermap
			(default is all providers)
			
--city: 	almost any german city name(if misspelled
			or not included you will get an error,
			default is all cities)
			
--folder: 	specify the folder where you want to
			save the forecasts relative to the
			webscraping folder(if the folder does
			not exist it will be created, default is
			forecasts)

--verbosity:	set the amount of information printed on the command line.
			Possible levels are <=0, 1 and 2<=. The larger number
			the more verbose is the output. Programming wise these
			levels correspond to logging.WARNING, logging.INFO and
			logging.DEBUG. Default is 0.
			
For example, to get the forecasts from accuweather and wunderground for Berlin,
Bremen and Munich and save them into the folder myForecasts you have to
write:

python webscraping.py --provider=accuweather,wunderground --city=berlin,bremen,munich --folder=myForecasts
