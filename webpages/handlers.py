from cached import *

PORT = 9000

SITE = {
    #"path": join(script_path),
    "dirname": "wwwsite",
    "port":PORT,
    
    "author": "Henrik Vendelbo",
    "description": "CT4 Demo Site",
}

urls = [
	('^(/[^/]*)$',CachedHandler),
]

