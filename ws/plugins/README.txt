Weather underground:

1) Run it from the webscraping folder
2) Execute the following commands:
	from main import build_url
	import urllib
	import json
	page = urllib.request.urlopen(build_url('Berlin'))
	read = page.read()
	decoded = read.decode('utf8')
	data = json.loads(decoded)
3) Think of a cityname, e.g. 'Berlin'
4) And a date in datetime form, e.g.:
	from datetime import date
	date = date.today()
5) pandize(data,'Berlin',date)
