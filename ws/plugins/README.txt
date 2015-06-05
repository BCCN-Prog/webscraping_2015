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
