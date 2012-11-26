# Google Play Unofficial Python API

An unofficial Python API that let you search, browse and download Android apps from Google Play (formerly Android Market).

This library is inspired by those projects, working with the old version of the API:

* [Android Market Python API](https://github.com/liato/android-market-api-py)
* [Android Market Java API](http://code.google.com/p/android-market-api/)

## Disclaimer
**This is not an official API. I am not afiliated with Google in any way, and am not responsible of any damage that could be done with it. Use it at your own risk.**

## Dependencies
* [Python 2.5+](http://www.python.org)
* [Protocol Buffers](http://code.google.com/p/protobuf/)

## Requirements
You must edit `config.py` before using the provided scripts (`search.py`, `download.py`, `apishell.py`, etc.). First, you need to provide your phone's `androidID`:

    ANDROID_ID      = None # "xxxxxxxxxxxxxxxx"

To get your `androidID`, use `*#*#8255#*#*` on your phone to start *Gtalk Monitor*. The hex string listed after `aid` is your `androidID`.

In order to authenticate to Google Play, you also need to provide either your Google login and password, or a valid subAuthToken.

## Usage

### Searching

    $ python search.py
    Usage: search.py request [nb_results] [offset]
    Search for an app.
    If request contains a space, don't forget to surround it with ""

    $ python search.py earth
    Title;Package name;Creator;Super Dev;Price;Offer Type;Version Code;Size;Rating;Num Downloads
    Google Earth;com.google.earth;Google Inc.;1;Gratuit;1;53;8.6MB;4.46;10 000 000+
    Terre HD Free Edition;ru.gonorovsky.kv.livewall.earthhd;Stanislav Gonorovsky;0;Gratuit;1;33;4.7MB;4.47;1 000 000+
    Earth Live Wallpaper;com.seb.SLWP;unixseb;0;Gratuit;1;60;687.4KB;4.06;5 000 000+
    Super Earth Wallpaper Free;com.mx.spacelwpfree;Mariux;0;Gratuit;1;2;1.8MB;4.41;100 000+
    Earth And Legend;com.dvidearts.earthandlegend;DVide Arts Incorporated;0;5,99 €;1;6;6.8MB;4.82;50 000+
    [...]

Depending on the number of results you ask, you might get an error. My tests show that 100 search results are the maximum, but it may vary.

By default, all scripts have CSV output. You can use Linux's `column` to prettify the output:

    $ alias pp="column -s ';' -t"
    $ python search.py earth | pp
    Title                           Package name                            Creator                  Super Dev  Price    Offer Type  Version Code  Size     Rating  Num Downloads
    Google Earth                    com.google.earth                        Google Inc.              1          Gratuit  1           53            8.6MB    4.46    10 000 000+
    Terre HD Free Edition           ru.gonorovsky.kv.livewall.earthhd       Stanislav Gonorovsky     0          Gratuit  1           33            4.7MB    4.47    1 000 000+
    Earth Live Wallpaper            com.seb.SLWP                            unixseb                  0          Gratuit  1           60            687.4KB  4.06    5 000 000+
    Super Earth Wallpaper Free      com.mx.spacelwpfree                     Mariux                   0          Gratuit  1           2             1.8MB    4.41    100 000+
    Earth And Legend                com.dvidearts.earthandlegend            DVide Arts Incorporated  0          5,99 €   1           6             6.8MB    4.82    50 000+
    Earth 3D                        com.jmsys.earth3d                       Dokon Jang               0          Gratuit  1           12            3.4MB    4.05    500 000+
    [...]

### Browse categories

You can list all app categories this way:

    $ python categories.py | pp
    ID                   Name
    GAME                 Jeux
    NEWS_AND_MAGAZINES   Actualités et magazines
    COMICS               BD
    LIBRARIES_AND_DEMO   Bibliothèques et démos
    COMMUNICATION        Communication
    ENTERTAINMENT        Divertissement
    EDUCATION            Enseignement
    FINANCE              Finance

Sorry for non-French speakers!

### List subcategories and apps

All categories have subcategories. You can list them with:

    $ python list.py
    Usage: list.py category [subcategory] [nb_results] [offset]
    List subcategories and apps within them.
    category: To obtain a list of supported catagories, use categories.py
    subcategory: You can get a list of all subcategories available, by supplying a valid category

    $ python list.py WEATHER | pp
    Subcategory ID            Name
    apps_topselling_paid      Top payant
    apps_topselling_free      Top gratuit
    apps_topgrossing          Les plus rentables
    apps_topselling_new_paid  Top des nouveautés payantes
    apps_topselling_new_free  Top des nouveautés gratuites

And then list apps within them:

    $ python list.py WEATHER apps_topselling_free | pp
    Title                  Package name                                  Creator          Super Dev  Price    Offer Type  Version Code  Size    Rating  Num Downloads
    La chaine météo        com.lachainemeteo.androidapp                  METEO CONSULT    0          Gratuit  1           8             4.6MB   4.38    1 000 000+
    Météo-France           fr.meteo                                      Météo-France     0          Gratuit  1           11            2.4MB   3.63    1 000 000+
    GO Weather EX          com.gau.go.launcherex.gowidget.weatherwidget  GO Launcher EX   0          Gratuit  1           25            6.5MB   4.40    10 000 000+
    Thermomètre (Gratuit)  com.xiaad.android.thermometertrial            Mobiquité        0          Gratuit  1           60            3.6MB   3.78    1 000 000+

### Viewing permissions

You can use `permissions.py` to see what permissions are required by an app without downloading it:

    $ python search.py gmail 1 | pp
    Titre  Package name           Creator      Super Dev  Price    Offer Type  Version Code  Size   Rating  Num Downloads
    Gmail  com.google.android.gm  Google Inc.  1          Gratuit  1           403           2.7MB  4.32    100 000 000+

    $ python permissions.py com.google.android.gm
    android.permission.ACCESS_NETWORK_STATE
    android.permission.GET_ACCOUNTS
    android.permission.MANAGE_ACCOUNTS
    android.permission.INTERNET
    android.permission.READ_CONTACTS
    android.permission.WRITE_CONTACTS
    android.permission.READ_SYNC_SETTINGS
    android.permission.READ_SYNC_STATS
    android.permission.RECEIVE_BOOT_COMPLETED
    [...]

You can specify multiple apps, using only one request.

### Downloading apps

Downloading an app is really easy, just provide its package name. I only tested with free apps, but I guess it should work as well with non-free as soon as you have enough money on your Google account.

    $ python download.py com.google.android.gm
    Downloading 2.7MB... Done

    $ file com.google.android.gm.apk
    com.google.android.gm.apk: Zip archive data, at least v2.0 to extract

### Interactive shell
An interactive shell can be started using the `apishell.py` script. It initializes the `api` object and logs you in.

    $ python apishell.py

    Google Play Unofficial API Interactive Shell
    Successfully logged in using your Google account. The variable 'api' holds the API object.
    Feel free to use help(api).

    >>> print api.__doc__
    Google Play Unofficial API Class
      Usual APIs methods are login(), search(), details(), download(), browse() and list().
      toStr() can be used to pretty print the result (protobuf object) of the previous methods.
      toDict() converts the result into a dict, for easier introspection.

    >>> res = api.search("angry birds")
    >>> for i in res.doc[0].child:
    ...   print i.title.encode('utf8')
    ...
    Angry Birds
    Angry Birds Seasons
    Angry Birds Space
    Angry Birds Rio
    Angry Birds Space Premium
    Angry Birds - AngryBirdsBackup
    Angry Aviary LiteÔÿà Angry Birds
    [...]

All results returned by methods such as `search()`, `details()`, ..., are Protobuf objects. You can use `toStr` and `toDict` method from `GooglePlayAPI` to pretty-print them and make introspection easier if you're not familiar with Protobuf.

    >>> s = api.browse()
    >>> s
    <googleplay_pb2.BrowseResponse object at 0x025DBF48>
    >>> d = api.toDict(s)
    >>> d.keys()
    ['promoUrl', 'category', 'contentsUrl']
    >>> from pprint import pprint
    >>> pprint(d['category'])
    [{'dataUrl': u'browse?c=3&cat=GAME', 'name': u'Jeux'},
     {'dataUrl': u'browse?c=3&cat=NEWS_AND_MAGAZINES',
    [...]

### Using the API as a module in another project

You only need `googleplay.py` and `googleplay_pb2.py`. All other scripts are just front-ends.

    >>> from googleplay import GooglePlayAPI
    >>> help(GooglePlayAPI)

What else?

### To be continued

Feel free to extend the API, add command-line options to scripts, fork the project, and port it to any language.
You can generate Protobuf stubs from `googleplay.proto` file with Google's `protoc`:

    $ protoc -h
    Usage: protoc [OPTION] PROTO_FILES
    Parse PROTO_FILES and generate output based on the options given:
    [...]
      --cpp_out=OUT_DIR           Generate C++ header and source.
      --java_out=OUT_DIR          Generate Java source file.
      --python_out=OUT_DIR        Generate Python source file.

## License

This project is released under the BSD license.

