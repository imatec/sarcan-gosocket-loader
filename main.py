import urllib2
try:
    import json
except ImportError:
    import simplejson as json
import csv

def getRows(data):
    # ?? this totally depends on what's in your data
    return []
airportcode = "SCL"
url = "http://airportcode.riobard.com/airport/" + airportcode + "?fmt=JSON"
data = urllib2.urlopen(url).read()
data = json.loads(data)

fname = "datafrom-" + airportcode + ".json"

with open(fname, 'w') as outfile:
  json.dump(data, outfile)