#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
import urlparse
from pprint import pprint
from google.protobuf import text_format

from config import *
from googleplay import GooglePlayAPI

if (len(sys.argv) < 2):
    print "Usage: %s packagename1 [packagename2 [...]]" % sys.argv[0]
    print "Display permissions required to install the specified app(s)."
    sys.exit(0)

packagenames = sys.argv[1:]

api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

# Only one app
if (len(packagenames) == 1):
    response = api.details(packagenames[0])
    print "\n".join(i.encode('utf8') for i in response.docV2.details.appDetails.permission)

else: # More than one app
    response = api.bulkDetails(packagenames)

    for entry in response.entry:
        if (not not entry.ListFields()): # if the entry is not empty
            print entry.doc.docid + ":"
            print "\n".join("    "+i.encode('utf8') for i in entry.doc.details.appDetails.permission)
            print

