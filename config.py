# separator used by search.py, categories.py, ...
SEPARATOR = ";"

LANG            = "en_US" # can be en_US, fr_FR, ...
ANDROID_ID      = None # "xxxxxxxxxxxxxxxx"
GOOGLE_LOGIN    = None # "username@gmail.com"
GOOGLE_PASSWORD = None
AUTH_TOKEN      = None # "yyyyyyyyy"

# force the user to edit this file
if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("config.py not updated")

