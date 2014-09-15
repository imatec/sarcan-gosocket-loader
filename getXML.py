###########################################
# ImaTec Computacion SpA.
# goSocket custom API crawler
# SARCAN
#
import urllib2
import requests
try:
    import json
except ImportError:
    import simplejson as json
import csv
import os
from base64 import *

def getRows(data):
    # ?? this totally depends on what's in your data
    return []

url = "http://api.gosocket.net/api/App/GetXml?CountryId=cl&DocumentId=b258b4b1-52ff-43dd-8a7c-0e023852b0f8"
user = "6e140fe9-e493-4888-ad4b-cbf0e945aa5d"
password = "admin"

r = requests.get(url, auth=(user, password))
# print r.text
xml_data = r.text
xml_fname = "xml_test.xml"	

xml_file = open(xml_fname, "w")
xml_file.write(b64decode(xml_data))
xml_file.close()

# with open(xml_fname, "w") as outfile:
#	xml.dump(b64decode(xml_data), outfile)
