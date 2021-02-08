# weerlive2influx
Fire-and-forget script to get KNMI meteorological data from weerlive.

###### Preface
I am no programmer and lack any structured education in this field. Making my first (baby)steps into the Python world due to my interest in Raspberry Pi's and measuring the environment. This means, use this at your own risk, it works for me, doesn't mean it works for you!
At the same time, I am using this to get familiar with github. Never having worked in a project style set up for these kinds of things I have a lot to learn. Sames goes for the python script I wrote. Yes, it works like a charm for me, but I am sure I broke a gazillion best practise rules. I'll get there in the end!

## Background
I made an environmental sensor box and wanted to compare that with 'official' data. I live in The Netherlands and you can get the data from the royal meteorological instute for free via weerlive.nl.

## Prerequisites
Get a free API-key for personal use on https://weerlive.nl/api/toegang/. With this key, you can make 300 daily requests which would be every 5 minutes more or less. Since data is refreshed every 10 minutes, you only need to query 6 times an hour, starting at the hour. Data is renewed on 3, 13, 23, etc. 

**Note:** I am in no way affiliated with weerlive.nl / KNMI, I am an end-user using the data for personal use.

## Use
I use it on a Raspberry Pi zero to get the data. You can run it manually ot set it up via Crontab as:

***/10 * * * * /usr/bin/python3 /home/pi/weerlive2influx.py >> /tmp/weerlive.output 2>&1**

Using this with Python3.x and haven't tested it with older versions. Being a newbie with Python, I see comments everywhere not to work with 2.x... It runs it every 10 minutes and outputs data to /tmp/weerlive.output. I am not too confident yet, so I print a lot ot screen (and this log). Comment as you see fit, but it's easy for troubleshooting. Once it works, I would suggest to comment line 71 that prints out the complete json.

I have listed all available keys at the moment of writing (source: tab #3 on: https://weerlive.nl/delen.php). This may change without notice of course. Simply limit the keyList to the ones you want. If you only want temperature and humidity, _keyList = ['temp','lv']_ would already be enough.

First step is that I add all required values as string and then I loop over them again to see which ones are numeric. I convert all to floats and manage presentation and all in Grafana dashboards afterwards. Open to contructive comments and enjoy!

All the best from The Netherlands,
Remco
