#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
from pprint import pprint

from config import *
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt, print_header_line, print_result_line

if (len(sys.argv) < 2):
    print "Usage: %s category [subcategory] [nb_results] [offset]" % sys.argv[0]
    print "List subcategories and apps within them."
    print "category: To obtain a list of supported catagories, use categories.py"
    print "subcategory: You can get a list of all subcategories available, by supplying a valid category"
    sys.exit(0)

cat = sys.argv[1]
ctr = None
nb_results = None
offset = None

if (len(sys.argv) >= 3):
    ctr = sys.argv[2]
if (len(sys.argv) >= 4):
    nb_results = sys.argv[3]
if (len(sys.argv) == 5):
    offset = sys.argv[4]

api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
try:
    message = api.list(cat, ctr, nb_results, offset)
except:
    print "Error: HTTP 500 - one of the provided parameters is invalid"

if (ctr is None):
    print SEPARATOR.join(["Subcategory ID", "Name"])
    for doc in message.doc:
        print SEPARATOR.join([doc.docid.encode('utf8'), doc.title.encode('utf8')])
else:
    print_header_line()
    doc = message.doc[0]
    for c in doc.child:
        print_result_line(c)

