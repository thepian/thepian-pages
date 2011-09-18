from __future__ import with_statement

import os
from os.path import join, exists, abspath, splitext
from fs import listdir, filters
import hashlib, json, datetime, time, site
import mimetypes

import tornado.web
import redis

from base import *

UNIT_SEP = "\x1F"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Redis connection
REDIS = redis.Redis(REDIS_HOST, REDIS_PORT, db=1)

ONE_YEAR_IN_SECONDS = 365 * 24 * 3600
IN_A_YEAR_STAMP = time.time() + ONE_YEAR_IN_SECONDS

BROWSER_SPECIFIC_HEADER = "header:%s%s"
BROWSER_SPECIFIC_CONTENT = "content:%s%s"

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
    		if not include_body:
	    		self.flush()
    			return
    		self.write(REDIS[contentkey])
    		self.flush()
    	else:
    		raise tornado.web.HTTPError(404, "We couldn't find requested information")
     
#TODO review tornado StaticFileHandler

def html_file(path,modified,content):
	header = {
		"Content-Type": "text/html",
	}
	return header,content
	   
def markdown_file(path,modified,content):
	header = {
		"Content-Type": "text/html",
	}
	#TODO convert markdown to html
	return header,content
	   
def default_file(path,modified,content):
	header = {
		"Content-Type": "text/plain",
	}
	mime_type,encoding = mimetypes.guess_type(path)
	if mime_type:
		header["Content-Type"] = mime_type
	return header,content

FILE_EXTENSIONS = {
	"html" : html_file,
	"md" : markdown_file,
	"mdown" : markdown_file,
	"markdown" : markdown_file,
}

class FileExpander(object):

	def __init__(self,base,relpath)
		self.base = base
		self.path = relpath

		path = abspath(join(site.SITE_DIR,relpath))
		stat_result = os.stat(path)
		modified = datatime.datetime.fromtimestamp(stat_result[stat.ST_MTIME])

		content = None
		with open(path, "rb") as f:
			content = f.read()

		ext = splitext(path)[1]
		if ext in FILE_EXTENSIONS:
			self.header, self.content = FILE_EXTENSIONS[ext](path,modified,content)
		else:
			self.header, self.content = default_file(path,modified,content)


	def cache(self,browser_type)
        contentkey = BROWSER_SPECIFIC_CONTENT % (browser_type , self.path) 
        REDIS[contentkey] = self.content
        headerkey = BROWSER_SPECIFIC_HEADER % (browser_type , self.path) 
        REDIS[headerkey] = self.header

def populate_cache():
	for relpath in fs.listdir(site.SITE_DIR,filters=filters.no_directories):
		if not relpath[0] == "_":
			expander = FileExpander(site.SITE_DIR,relpath)
			expander.cache("pocket")
			expander.cache("tablet")
			expander.cache("desktop")

