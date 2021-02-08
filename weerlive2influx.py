# Use as your own risk! Created with limited to no experience with Python.
# Hey, I am not even a programmer, but it works! I run it every 10 mins on
# a Raspberry PI pumping data to an influx DB feeding a Grafana board.
# Tested with Python3.7.x and no errors yet. Using this in crontab as:
# */10 * * * * /usr/bin/python3 /home/pi/weerlive2influx.py >> /tmp/weerlive.output 2>&1
# Cheers,
# Remco / https://github.com/RemBrandNL/weerlive2influx

import requests
import time
import json
from influxdb import InfluxDBClient
from requests.exceptions import ConnectionError

InfluxHost = "x.x.x.x" # localhost or your ip 
InfluxUser = "username"
InfluxPass = "password"
InfluxDB = "database2store"
location = "Amsterdam" # any Dutch city in NL
APIkey = "demo" # Get a free key on https://weerlive.nl/api/toegang/

url = "https://weerlive.nl/api/json-data-10min.php?key=" + APIkey + "&locatie=" + location
response = requests.get(url)
data = response.json()
""" Below are all available keys, simply select the ones you want.
keyList = [
	'plaats','temp','gtemp','samenv','lv','windr','windms','winds','windk',
	'windkmh','luchtd','ldmmhg','dauwp','zicht','verw','sup','sunder',
	'image','d0weer','d0tmax','d0tmin','d0windk','d0windr','d0neerslag',
	'd0zon','d1weer','d1tmax','d1tmin','d1windk','d1windr','d1neerslag',
	'd1zon','d2tmax','d2tmin','d2weer','d2windk','d2windr','d2neerslag',
	'd2zon','alarm','alarmtxt']
"""
keyList = [
	'plaats','temp','gtemp','samenv','lv','windr','windms','winds','windk',
	'windkmh','luchtd','dauwp','zicht','verw','sup','sunder','d0tmax',
	'd0tmin','d0neerslag','d0zon','d1tmax','d1tmin','d1neerslag','d1zon',
	'd2tmin','d2tmax','d2neerslag','d2zon','alarm','alarmtxt'
]

weerDict = {}
print("Getting data for " + location)
for weer in data['liveweer']:
	print("Adding all fields as string first:", end = '')
	for key in keyList: 
		try:
			weerDict[key] = weer.get(key)
			print(" " + str(key), end = '')
		except:
			print("", end = '')
	print("\n\nThese look numbery, re-adding as float:", end = '')
	for key in keyList: 
		try:
			weerDict[key] = float(weer.get(key))
			print(" " + str(key), end = '')
		except:
			print("", end = '')
""" InfluxDB needs UTC data, the source has no timstamp, so create one. """
NanoUTC = time.clock_gettime_ns(time.CLOCK_REALTIME)
weerliveData = [
	{
	"measurement":"WeerliveData",
	"tags":
		{
			"Location": location
		},
	"time": NanoUTC,
	"fields": weerDict
	}
	]
print(json.dumps(weerliveData, indent=4))

try:
	dbClient = InfluxDBClient(InfluxHost, 8086, InfluxUser, InfluxPass, InfluxDB)
	dbClient.write_points(weerliveData)
	print("\n\nI saved Weerlive data!")
except ConnectionError as e:
	print("Can not connect to InfluxDB '" + InfluxDB + "' @" + InfluxHost + ", will try again next run.")
