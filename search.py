#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
from pprint import pprint

from config import *
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt

def print_header_line():
    l = [ "Title",
                "Package name",
                "Creator",
                "Super Dev",
                "Price",
                "Offer Type",
                "Version Code",
                "Size",
                "Rating",
                "Num Downloads",
             ]
    print SEPARATOR.join(l)

def print_result_line(c):
    #c.offer[0].micros/1000000.0
    #c.offer[0].currencyCode
    l = [ c.title,
                c.docid,
                c.creator,
                len(c.annotations.badgeForCreator), # Is Super Developer?
                c.offer[0].formattedAmount,
                c.offer[0].offerType,
                c.details.appDetails.versionCode,
                sizeof_fmt(c.details.appDetails.installationSize),
                "%.2f" % c.aggregateRating.starRating,
                c.details.appDetails.numDownloads]
    print SEPARATOR.join(unicode(i).encode('utf8') for i in l)


if (len(sys.argv) < 2):
    print "Usage: %s request [nb_results] [offset]" % sys.argv[0]
    print "Search for an app."
    print "If request contains a space, don't forget to surround it with \"\""
    sys.exit(0)

request = sys.argv[1]
nb_res = None
offset = None

if (len(sys.argv) >= 3):
    nb_res = int(sys.argv[2])

if (len(sys.argv) >= 4):
    offset = int(sys.argv[3])

api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

try:
    message = api.search(request, nb_res, offset)
except:
    print "Error: something went wrong. Maybe the nb_res you specified was too big?"
    sys.exit(1)

print_header_line()
doc = message.doc[0]
for c in doc.child:
    print_result_line(c)

