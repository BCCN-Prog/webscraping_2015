Weather underground:

1) Run it from the webscraping folder
2) Think of a cityname, e.g. 'Berlin'
3) And a date in datetime form, e.g.:
	from datetime import date
	date = date.today()
4) pandize(build_url('Berlin'),'Berlin',date)


Here are the standard columns that every plugins pandize function should have. Missing values should be denoted as NaNs.

['Provider','ref_date','city','pred_offset','Station ID', 'Date', 'Quality Level', 'Air Temperature', \
    'Vapor Pressure', 'Degree of Coverage', 'Air Pressure', 'Rel Humidity', \
    'Wind Speed', 'Max Air Temp', 'Min Air Temp', 'Min Groundlvl Temp', \
    'Max Wind Speed', 'Precipitation', 'Precipitation Ind', 'Hrs of Sun', \
    'Snow Depth']

meaning of the columns:
ref_date: day on which the forecast was pulled
prediction_offset: days from ref_date into the future
Quality Level: Qualitative description of the day's weather

units: C for temperature; mm for rain/precipitation; cm for snow; kmh for wind speed
