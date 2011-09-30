from __future__ import with_statement

import os, stat, logging, site
from os.path import join, exists, abspath, splitext, split
from fs import listdir, filters
import hashlib, json, datetime, time
import mimetypes

import redis

#from base import *
from config import *
from browsers import *

UNIT_SEP = "\x1F"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Redis connection
REDIS = redis.Redis(REDIS_HOST, REDIS_PORT, db=1)

ONE_YEAR_IN_SECONDS = 365 * 24 * 3600
IN_A_YEAR_STAMP = time.time() + ONE_YEAR_IN_SECONDS

BROWSER_SPECIFIC_HEADER = "header:%s:%s%s"
BROWSER_SPECIFIC_CONTENT = "content:%s:%s%s"

class FileExpander(object):
	"""
	Used to expand files in the site into the Redis cache.
	"""
	def __init__(self,base,relpath,prefix=None,config=None):
		self.config = config
		self.prefix = prefix
		self.base = base
		self.path = relpath
		self.name, self.ext = splitext(split(relpath)[1])

		path = abspath(join(base,relpath))
		stat_result = os.stat(path)
		self.modified = datetime.datetime.fromtimestamp(stat_result[stat.ST_MTIME])

		content = None
		with open(path, "rb") as f:
			content = f.read()

		self.expandScss = False
		self.expandPage = False

		# Load file into *header* and *content*
		if self.ext in self.FILE_EXTENSIONS:
			self.FILE_EXTENSIONS[self.ext](self,self.path)
		else:
			self._default_file(self.path)

	def __repr__(self):
		return "%s %s %s %s" % (self.urlpath,self.name,self.ext,self.header)

	def _get_published(self):
		if "published" in self.header:
			return self.header["published"]
		return True

	published = property(_get_published)

	def _get_header_and_content(self,relpath,defaultheader):
		content = None
		with open(abspath(join(self.base,relpath)), "rb") as f:
			content = f.read()
		return self.config.split_header_and_utf8_content(content,defaultheader)

	def _scss_file(self,relpath):
		header = {
			"Content-Type": "text/css",
		}
		self.header,self.content = self._get_header_and_content(relpath,header)
		   
		if "url" in self.header:
			self.urlpath = "/" + self.header["url"]
		else:
			self.urlpath = "/%s.css" % splitext(self.path)[0]

		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		self.expandScss = True

	def _xml_file(self,relpath):
		header = {
			"Content-Type": "text/xml",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
		else:
			self.urlpath = "/" + self.path

		self.header,self.content = self._get_header_and_content(relpath,header)
		self.content = self.content.lstrip()
		   
		if "url" in self.header:
			self.urlpath = "/" + self.header["url"]

		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		if "page" in self.header:
			self.expandPage = True

	def _text_file(self,relpath):
		header = {
			"Content-Type": "text/plain",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
			if self.urlpath[-1] != "/": self.urlpath += "/"
		else:
			self.urlpath = "/" + self.path

		self.header,self.content = self._get_header_and_content(relpath,header)
		   
		if "url" in self.header:
			self.urlpath = "/" + self.header["url"]

		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		if "page" in self.header:
			self.expandPage = True

	def _html_file(self,relpath):
		header = {
			"Content-Type": "text/html",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
			if self.urlpath[-1] != "/": self.urlpath += "/"
		else:
			self.urlpath = "/" + splitext(self.path)[0] + "/"

		self.header,self.content = self._get_header_and_content(relpath,header)
		   
		if "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			
		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		if "page" in self.header:
			self.expandPage = True

	def _markdown_file(self,relpath):
		header = {
			"Content-Type": "text/html",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
			if self.urlpath[-1] != "/": self.urlpath += "/"
		else:
			self.urlpath = "/" + splitext(self.path)[0] + "/"

		self.header,rest = self._get_header_and_content(relpath,header)

		if "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			
		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		if "page" in self.header:
			self.expandPage = True

		import markdown2
		extras = ["code-friendly","wiki-tables","cuddled-lists"]
		if "markdown-extras" in self.header:
			extras = self.header["markdown-extras"]
		self.content = markdown2.markdown(rest,extras)
		   
	def _default_file(self,relpath):
		header = {
			"Content-Type": "text/plain",
		}
		mime_type,encoding = mimetypes.guess_type(self.path)
		if mime_type:
			header["Content-Type"] = mime_type
		content = None
		with open(abspath(join(self.base,relpath)), "rb") as f:
			content = f.read()
		self.urlpath = "/" + self.path
		self.header = header
		self.content = content

	FILE_EXTENSIONS = {
		".scss" : _scss_file,
		".txt" : _text_file,
		".text" : _text_file,
		".html" : _html_file,
		".xml" : _xml_file,
		".md" : _markdown_file,
		".mdown" : _markdown_file,
		".markdown" : _markdown_file,
	}

	def cache(self,browser):
		if self.config["debug"]:
			domain = "localhost"
		else:
			domain = self.config["domain"]
		contentkey = BROWSER_SPECIFIC_CONTENT % (browser.browser_type , domain, self.urlpath) 
		headerkey = BROWSER_SPECIFIC_HEADER % (browser.browser_type , domain, self.urlpath) 

		if not self.published:
			if headerkey in REDIS:
				REDIS.delete(headerkey)
			if contentkey in REDIS:
				REDIS.delete(contentkey)
			return

		if self.expandScss:
			relpath = join(browser.browser_type,self.path)
			if exists(join(self.base,relpath)):
				header,content = self._get_header_and_content(relpath,self.header)
			else:
				header,content = self.header,self.content
			header = browser.expandHeader(header,config=self.config)
			content = browser.expandScss(header,content,config=self.config)
		elif self.expandPage:
			header = browser.expandHeader(self.header,config=self.config)
			content = browser.expandPage(header,self.content,config=self.config)
		else:
			header = self.header
			content = self.content

		REDIS[contentkey] = content
		REDIS.expire(contentkey,ONE_YEAR_IN_SECONDS)
		REDIS[headerkey] = json.dumps(header)
		REDIS.expire(headerkey,ONE_YEAR_IN_SECONDS)

from fs import filters as fs_filters, walk

def listdir(dir_path,filters=(fs_filters.no_hidden,fs_filters.no_system),full_path=False,recursed=False,followlinks=True):
    if recursed:
    	prefix = len(dir_path)
    	if dir_path[-1] != "/": 
	    	prefix += 1
        r = []
        for top,dirs,nondirs in walk(dir_path,use_nlink = followlinks and 2 or 1):
            if full_path:
                r.extend([os.path.join(top,nd) for nd in nondirs])
            else:
                r.extend([os.path.join(top[prefix:],nd) for nd in nondirs])
        return r
    if full_path:
        return [os.path.join(dir_path,name) 
                for name in os.listdir(dir_path) if fs_filters.check_filters(dir_path, name, os.lstat(os.path.join(dir_path,name)), filters)]
    return [name for name in os.listdir(dir_path) if fs_filters.check_filters(dir_path,name,os.lstat(os.path.join(dir_path,name)),filters)]
 

# populate with files that have an extension and do not start with _
def populate_cache(options):
	config = SiteConfig(options)

	import scss
	setattr(scss,"LOAD_PATHS",site.SCSS_DIR)
	""" TODO:
LOAD_PATHS = os.path.join(PROJECT_ROOT, 'sass/frameworks/')
# Assets path, where new sprite files are created:
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')
# Assets path, where new sprite files are created:
ASSETS_ROOT = os.path.join(PROJECT_ROOT, 'static/assets/')
# Urls for the static and assets:
STATIC_URL = '/static/'
ASSETS_URL = '/static/assets/'
"""


	for relpath in listdir(site.SCSS_DIR,filters=(filters.no_directories,filters.no_hidden,filters.no_system,filters.fnmatch("*.scss"))):
		if not relpath[0] == "_":
			expander = FileExpander(site.SCSS_DIR,relpath,config=config,prefix="css")
			#setattr(scss,"LOAD_PATHS",site.SCSS_DIR)
			for browser in browsers:
				expander.cache(browser) 
			logging.info("Cached %s as %s" % (relpath,repr(expander)))

	for relpath in listdir(site.SITE_DIR,recursed=True,filters=(filters.no_directories,filters.no_hidden,filters.no_system)):
		if not relpath[0] == "_":
			expander = FileExpander(site.SITE_DIR,relpath,config=config)
			if expander.ext != '':
				for browser in browsers:
					expander.cache(browser) 
				logging.info("Cached %s as %s" % (relpath,repr(expander)))
	# TODO track deleted files removing them from cache

