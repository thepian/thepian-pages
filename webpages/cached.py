from __future__ import with_statement

import os, stat
from os.path import join, exists, abspath, splitext, split
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
    		print "Serving",path, REDIS[headerkey]
    		if not include_body:
	    		self.flush()
    			return
    		self.write(REDIS[contentkey])
    		self.flush()
    	else:
	        print path, contentkey, headerkey
    		raise tornado.web.HTTPError(404, "We couldn't find requested information")
     
#TODO review tornado StaticFileHandler

class FileExpander(object):

	def __init__(self,base,relpath):
		self.base = base
		self.path = relpath
		self.name, self.ext = splitext(split(relpath)[1])

		path = abspath(join(site.SITE_DIR,relpath))
		stat_result = os.stat(path)
		self.modified = datetime.datetime.fromtimestamp(stat_result[stat.ST_MTIME])

		content = None
		with open(path, "rb") as f:
			content = f.read()

		if self.ext in self.FILE_EXTENSIONS:
			self.header, self.content, self.urlpath = self.FILE_EXTENSIONS[self.ext](self,content)
		else:
			self.header, self.content, self.urlpath = self._default_file(content)


	def _html_file(self,content):
		header = {
			"Content-Type": "text/html",
		}
		if self.name == "index":
			urlpath = "/" + split(self.path)[0]
		else:
			urlpath = "/" + splitext(self.path)[0]
		return header,content,urlpath
		   
	def _markdown_file(self,content):
		header = {
			"Content-Type": "text/html",
		}
		if self.name == "index":
			urlpath = "/" + split(self.path)[0]
		else:
			urlpath = "/" + splitext(self.path)[0]

		import markdown2
		extras = ["code-friendly","wiki-tables","cuddled-lists"]
		content = markdown2.markdown(content,extras)
		#TODO convert markdown to html
		return header,content,urlpath
		   
	def _default_file(self,content):
		header = {
			"Content-Type": "text/plain",
		}
		mime_type,encoding = mimetypes.guess_type(self.path)
		if mime_type:
			header["Content-Type"] = mime_type
		urlpath = "/" + self.path
		return header,content,urlpath

	FILE_EXTENSIONS = {
		".html" : _html_file,
		".md" : _markdown_file,
		".mdown" : _markdown_file,
		".markdown" : _markdown_file,
	}


	def cache(self,browser_type):
		contentkey = BROWSER_SPECIFIC_CONTENT % (browser_type , self.urlpath) 
		REDIS[contentkey] = self.content
		REDIS.expire(contentkey,ONE_YEAR_IN_SECONDS)
		headerkey = BROWSER_SPECIFIC_HEADER % (browser_type , self.urlpath) 
		REDIS[headerkey] = json.dumps(self.header)
		REDIS.expire(headerkey,ONE_YEAR_IN_SECONDS)

def populate_cache():
	for relpath in listdir(site.SITE_DIR,filters=(filters.no_directories,filters.no_hidden,filters.no_system)):
		if not relpath[0] == "_":
			expander = FileExpander(site.SITE_DIR,relpath)
			expander.cache("pocket")
			expander.cache("tablet")
			expander.cache("desktop")
			print "Cached ",relpath, "as", expander.urlpath, expander.header, expander.name, expander.ext

