###########################################
# ImaTec Computacion SpA.
# goSocket custom API crawler
# SARCAN
#
###########################################
try:
    import urllib.request as urllib2
except:
    import urllib2
import requests
try:
    import json
except ImportError:
    import simplejson as json
import os
from base64 import *
import sys
import codecs
#sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

def getRows(data):
    # ?? this totally depends on what's in your data
    return []

url2 = "http://api.gosocket.net/api/App/GetFederations?countryId=cl"
user = "6e140fe9-e493-4888-ad4b-cbf0e945aa5d"
password = "admin"
AccountId = "3580a591-fad4-4c18-9be3-a9e67488346b"

basepath = "gosocket_downloads/"

# Create basepath if does not exists
if not os.path.exists(basepath):
	os.makedirs(basepath)

# Iterate over federations
federations_resource = "http://api.gosocket.net/api/App/GetFederations?countryId=cl"
fr = requests.get(federations_resource, auth=(user, password))
f_data = fr.json()
# Copy federations list JSON

f_fname = "federations.json"	
with open(basepath + f_fname, "w") as outfile:
	json.dump(f_data, outfile)

for f_item in f_data["Items"]:
	FederationId = f_item["FederationId"]
	print (FederationId)
	# Create federation folder
	federation_path = basepath + FederationId
	if not os.path.exists(federation_path):
		os.makedirs(federation_path)

	# Get Federation pages amount
	documents_p_resource = "http://gosocketapi2.azurewebsites.net/api/App/GetSentDocuments?CountryId=cl&FederationId="+FederationId+"&AccountId=" + AccountId + "&Page=1"
	dpr = requests.get(documents_p_resource, auth=(user, password))
	dp_data = dpr.json()


	if os.path.isfile("gosocket_downloads/" + FederationId + "/lastpage"):	
		f = open("gosocket_downloads/" + FederationId + "/lastpage", "r")
		startingpage = int(f.readline())
		f.close()
	else:
		startingpage = 1

	for page in range(startingpage, int(dp_data["TotalPages"])):
		# Create page folder
		page_path = federation_path + "/p" + str(page) 
		if not os.path.exists(page_path):
			os.makedirs(page_path)

		print ("iterating page " + str(page))
		# Iterate over documents of a federation
		documents_resource = "http://gosocketapi2.azurewebsites.net/api/App/GetSentDocuments?CountryId=cl&FederationId="+FederationId+"&AccountId=" + AccountId + "&Page=" + str(page)
		dr = requests.get(documents_resource, auth=(user, password))
		d_data = dr.json()

		# Copy federation documents JSON
		d_fname = "federation_p" + str(page) + "_" + FederationId + ".json"	
		with open(federation_path + "/" + d_fname, "w") as outfile:
			json.dump(d_data, outfile)

		for d_item in d_data["Items"]:
			DocumentId = d_item["DocumentId"]
			print (" > " + DocumentId)

			# Create document folder
			document_path = page_path + "/" + DocumentId
			if not os.path.exists(document_path):
				os.makedirs(document_path)

			# Iterate over details of a document
			documentDetail_resource = "http://gosocketapi2.azurewebsites.net/api/App/GetDocumentDetail?CountryId=cl&DocumentId=" + DocumentId
			dDr = requests.get(documentDetail_resource, auth=(user, password))
			dD_data = dDr.json()
			# Copy document detail JSON
			dD_fname = "documentDetail_" + DocumentId + ".json"	
			with open(document_path + "/" + dD_fname, "w") as outfile:
				json.dump(dD_data, outfile)
			
			# Copy document detail XML
			url = "http://api.gosocket.net/api/App/GetXml?CountryId=cl&DocumentId=" + DocumentId

			xml_r = requests.get(url, auth=(user, password))
		    
			xml_data = xml_r.text

			xml_test = b64decode(xml_data)
			xml_fname = "xml_" + DocumentId + ".xml"
			xml_file = open(document_path + "/" + xml_fname, "wb")

			xml_file.write(xml_test)
			xml_file.close()
		f2 = open("gosocket_downloads/" + FederationId + "/lastpage", "w")
		f2.write(str(page))
		f2.close
