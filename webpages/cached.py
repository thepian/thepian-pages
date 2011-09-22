from __future__ import with_statement

import os, stat
from os.path import join, exists, abspath, splitext, split
from fs import listdir, filters
import hashlib, json, datetime, time, site
import mimetypes

import tornado.web
import redis

from base import *
from config import *
from parts import *

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
	        print path, contentkey, headerkey
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

class FileExpander(object):
	"""
	Used to expand files in the site into the Redis cache.
	"""
	def __init__(self,base,relpath,config=None):
		self.config = config
		self.base = base
		self.path = relpath
		self.name, self.ext = splitext(split(relpath)[1])

		path = abspath(join(site.SITE_DIR,relpath))
		stat_result = os.stat(path)
		self.modified = datetime.datetime.fromtimestamp(stat_result[stat.ST_MTIME])

		content = None
		with open(path, "rb") as f:
			content = f.read()

		self.expandPage = False

		# Load file into *header* and *content*
		if self.ext in self.FILE_EXTENSIONS:
			self.FILE_EXTENSIONS[self.ext](self,content)
		else:
			self._default_file(content)

	def _get_published(self):
		if "published" in self.header:
			return self.header["published"]
		return True

	published = property(_get_published)

	def _xml_file(self,content):
		header = {
			"Content-Type": "text/xml",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
		else:
			self.urlpath = "/" + self.path

		self.header,self.content = self.config.split_header_and_utf8_content(content,header)
		self.content = self.content.lstrip()
		   
		if "url" in self.header:
			self.urlpath = "/" + self.header["url"]

		if "page" in self.header:
			self.expandPage = True

	def _text_file(self,content):
		header = {
			"Content-Type": "text/plain",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
		else:
			self.urlpath = "/" + splitext(self.path)[0] + "/"

		self.header,self.content = self.config.split_header_and_utf8_content(content,header)
		   
		if "url" in self.header:
			self.urlpath = "/" + self.header["url"]

		if "page" in self.header:
			self.expandPage = True

	def _html_file(self,content):
		header = {
			"Content-Type": "text/html",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
		else:
			self.urlpath = "/" + splitext(self.path)[0] + "/"

		self.header,self.content = self.config.split_header_and_utf8_content(content,header)
		   
		if "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			
		if "page" in self.header:
			self.expandPage = True

	def _markdown_file(self,content):
		header = {
			"Content-Type": "text/html",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
		else:
			self.urlpath = "/" + splitext(self.path)[0] + "/"

		self.header,rest = self.config.split_header_and_utf8_content(content,header)

		if "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			
		if "page" in self.header:
			self.expandPage = True

		import markdown2
		extras = ["code-friendly","wiki-tables","cuddled-lists"]
		if "markdown-extras" in self.header:
			extras = self.header["markdown-extras"]
		self.content = markdown2.markdown(rest,extras)
		   
	def _default_file(self,content):
		header = {
			"Content-Type": "text/plain",
		}
		mime_type,encoding = mimetypes.guess_type(self.path)
		if mime_type:
			header["Content-Type"] = mime_type
		self.urlpath = "/" + self.path
		self.header = header
		self.content = content

	FILE_EXTENSIONS = {
		".txt" : _text_file,
		".text" : _text_file,
		".html" : _html_file,
		".xml" : _xml_file,
		".md" : _markdown_file,
		".mdown" : _markdown_file,
		".markdown" : _markdown_file,
	}

	def cache(self,parts):
		contentkey = BROWSER_SPECIFIC_CONTENT % (parts.browser_type , self.urlpath) 
		headerkey = BROWSER_SPECIFIC_HEADER % (parts.browser_type , self.urlpath) 

		if not self.published:
			if headerkey in REDIS:
				REDIS.delete(headerkey)
			if contentkey in REDIS:
				REDIS.delete(contentkey)
			return

		if self.expandPage:
			header = parts.expandHeader(self.header,config=self.config)
			content = parts.expandPage(header,self.content,config=self.config)
		else:
			header = self.header
			content = self.content

		REDIS[contentkey] = content
		REDIS.expire(contentkey,ONE_YEAR_IN_SECONDS)
		REDIS[headerkey] = json.dumps(header)
		REDIS.expire(headerkey,ONE_YEAR_IN_SECONDS)


# populate with files that have an extension and do not start with _
def populate_cache():
	config = SiteConfig()

	for relpath in listdir(site.SITE_DIR,filters=(filters.no_directories,filters.no_hidden,filters.no_system)):
		if not relpath[0] == "_":
			expander = FileExpander(site.SITE_DIR,relpath,config=config)
			if expander.ext != '':
				for parts in browser_parts:
					expander.cache(parts) 
				print "Cached ",relpath, "as", expander.urlpath, expander.header, expander.name, expander.ext, expander.expandPage
	# TODO track deleted files removing them from cache

