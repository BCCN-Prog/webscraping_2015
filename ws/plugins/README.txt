Weather underground:

1) Run it from the webscraping folder
2) Think of a cityname, e.g. 'Berlin'
3) And a date in datetime form, e.g.:
	from datetime import date
	date = date.today()
4) pandize(build_url('Berlin'),'Berlin',date)
