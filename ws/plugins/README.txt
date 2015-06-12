Here are the standard columns that every plugins pandize function should have. Missing values should be denoted as NaNs.

['Provider','ref_date','city','pred_offset','Station ID', 'Date', 'Quality Level', 'Air Temperature', \
    'Vapor Pressure', 'Degree of Coverage', 'Air Pressure', 'Rel Humidity', \
    'Wind Speed', 'Max Air Temp', 'Min Air Temp', 'Min Groundlvl Temp', \
    'Max Wind Speed', 'Precipitation', 'Precipitation Ind', 'Hrs of Sun', \
    'Snow Depth']

meaning of the columns:
ref_date: day on which the forecast was pulled
prediction_offset: days from ref_date into the future
Quality Level:

units: C for temperature; mm for rain/precipitation; cm for snow; kmh for wind speed
