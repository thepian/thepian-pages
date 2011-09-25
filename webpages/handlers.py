import json, logging

from base import get_browser_type
from cached import *

import tornado.web

class CachedHandler(tornado.web.RequestHandler):
    
    def head(self,path,browser_type=None):
    	return self.get(path,browser_type,include_body=False)

    def get(self,path,browser_type=None,include_body=True):
        if not browser_type:
            browser_type = get_browser_type( self.request.headers['User-Agent'] )

        contentkey = BROWSER_SPECIFIC_CONTENT % (browser_type , path) 
        headerkey = BROWSER_SPECIFIC_HEADER % (browser_type , path) 
    	if contentkey in REDIS:
    		#TODO etag and headers
    		#TODO url type, inject state script
    		header = json.loads(REDIS[headerkey])
    		for hn in self.HTTP_HEADER_NAMES:
    			if hn in header:
    				self.set_header(hn,header[hn])

    		if not include_body:
	    		self.flush()
    			return
    		self.write(REDIS[contentkey])
    		self.flush()
    	else:
	        logging.debug("404: %s" % path)
    		raise tornado.web.HTTPError(404, "We couldn't find requested information")

    HTTP_HEADER_NAMES = [
    	"Content-Type",
    	"Content-Location",		# Do browser care?
    	"Content-Disposition", # force download dialog
    	"Content-Language",
    	"Last-Modified",
    	"Expires",
    	"Location",			# for redirect
    ]
     
#TODO review tornado StaticFileHandler



urls = [
	('^(/.*)$',CachedHandler),
]

