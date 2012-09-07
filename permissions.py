#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

from config import *
from pprint import pprint
from googleplay import GooglePlayAPI
from google.protobuf import text_format
import sys
import urlparse


if(len(sys.argv) < 2):
  print "Usage: %s packagename"
  print "Display permissions required to install an app."
  sys.exit(0)
  
packagename = sys.argv[1]

api = GooglePlayAPI()
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
response = api.details(packagename)

print "\n".join(i.encode('utf8') for i in response.docV2.details.appDetails.permission)
