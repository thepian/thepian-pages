from __future__ import with_statement

import os, stat, logging, site
from os.path import join, exists, abspath, realpath, splitext, split, dirname
from fs import listdir, filters
import hashlib, json, datetime, time
import mimetypes

from browsers import *

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
		self.expandDocument = False

		self.domain = self.config["domain"]

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

	def _get_matter_and_content(self,relpath,defaultheader):
		content = None
		with open(abspath(join(self.base,relpath)), "rb") as f:
			content = f.read()
		return self.config.split_matter_and_utf8_content(content,defaultheader)

	def _scss_file(self,relpath):
		header = {
			"Content-Type": "text/css",
		}
		self.header,self.content = self._get_matter_and_content(relpath,header)
		   
		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]
		else:
			self.urlpath = "/%s.css" % splitext(self.path)[0]

		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		self.outpath = self.urlpath
		self.expandScss = True

	def _xml_file(self,relpath):
		header = {
			"Content-Type": "text/xml",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
		else:
			self.urlpath = "/" + self.path

		self.header,self.content = self._get_matter_and_content(relpath,header)
		self.content = self.content.lstrip()
		   
		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]

		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		self.outpath = self.urlpath
		if "document" in self.header and self.header["document"]:
			self.expandDocument = True

	def _text_file(self,relpath):
		header = {
			"Content-Type": "text/plain",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
			if self.urlpath[-1] != "/": self.urlpath += "/"
		else:
			self.urlpath = "/" + self.path

		self.header,self.content = self._get_matter_and_content(relpath,header)
		   
		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]

		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		self.outpath = self.urlpath
		if "document" in self.header:
			self.expandDocument = True

	def _html_file(self,relpath):
		header = {
			"Content-Type": "text/html",
		}
		outpath = None
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
			if self.urlpath[-1] != "/": self.urlpath += "/"
			outpath = self.urlpath + "index.html"
		else:
			self.urlpath = "/" + splitext(self.path)[0] + "/"

		self.header,self.content = self._get_matter_and_content(relpath,header)
		   
		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			
		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		self.outpath = outpath or self.urlpath
		if "document" in self.header:
			self.expandDocument = True

	def _markdown_file(self,relpath):
		header = {
			"Content-Type": "text/html",
		}
		outpath = None
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
			if self.urlpath[-1] != "/": self.urlpath += "/"
			outpath = self.urlpath + "index.html"
		else:
			self.urlpath = "/" + splitext(self.path)[0] + "/"

		self.header,rest = self._get_matter_and_content(relpath,header)

		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			
		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		self.outpath = outpath or self.urlpath

		if "document" in self.header:
			self.expandDocument = True

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
		self.outpath = self.urlpath
		self.header = header
		self.content = content

	def _appcache_file(self,relpath):
		header = {
			"Content-Type": "text/cache-manifest",
		}
		mime_type,encoding = mimetypes.guess_type(self.path)
		if mime_type:
			header["Content-Type"] = mime_type

		self.header,rest = self._get_matter_and_content(relpath,header)
		self.content = rest.lstrip()

		self.urlpath = "/" + self.path
		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			
		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)


	FILE_EXTENSIONS = {
		".scss" : _scss_file,
		".txt" : _text_file,
		".text" : _text_file,
		".html" : _html_file,
		".xml" : _xml_file,
		".md" : _markdown_file,
		".mdown" : _markdown_file,
		".markdown" : _markdown_file,
		".appcache" : _appcache_file,
	}

def save_expander(expander,browser,config):
	base_path = config["output"]
	file_path = join(base_path,browser.browser_type,expander.outpath[1:])
	dir_path = dirname(file_path)

	if not expander.published and exists(file_path):
		os.remove(file_path)
		return
	if not exists(dir_path):
		os.makedirs(dir_path)

	if expander.expandScss:
		relpath = join(browser.browser_type,expander.path)
		if exists(join(expander.base,relpath)):
			header,content = expander._get_matter_and_content(relpath,expander.header)
		else:
			header,content = expander.header,expander.content
		header = browser.expandHeader(header,config=expander.config)
		content = browser.expandScss(header,content,config=expander.config)
		#expander.update_lists(header,{ "offline": [expander.urlpath] })
	elif expander.expandDocument:
		header = browser.expandHeader(expander.header,config=expander.config)
		content, lists = browser.expandDocument(header,expander.content,config=expander.config)
		#expander.update_lists(header,lists)
	else:
		header = expander.header
		content = expander.content
		#expander.update_lists(header,{ "offline": [expander.urlpath] })

	with open(file_path,"wb") as f:
		# print "writing", file_path
		f.write(content)


# populate with files that have an extension and do not start with _
def populate(expander_writer,config):

	if site.SCSS_DIR:
		try:
			import scss
			setattr(scss,"LOAD_PATHS",site.SCSS_DIR)
		except ImportError:
			pass
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

	base_filters = [config.exclude_filter(),filters.no_directories,filters.no_hidden,filters.no_system]

	if site.SCSS_DIR:
		for relpath in listdir(site.SCSS_DIR,filters=base_filters+[filters.fnmatch("*.scss"),]):
			expander = FileExpander(site.SCSS_DIR,relpath,config=config,prefix="css")
			#TODO ensure that _x.scss is not published
			#setattr(scss,"LOAD_PATHS",site.SCSS_DIR)
			for browser in browsers:
				expander_writer(expander,browser,config) 
			logging.info("Cached %s for %s as %s" % (relpath,expander.domain,repr(expander)))

	for relpath in listdir(site.SITE_DIR,recursed=True,filters=base_filters):
		expander = FileExpander(site.SITE_DIR,relpath,config=config)
		if relpath[0] != "_":
			for browser in browsers:
				expander_writer(expander,browser,config) 
			logging.info("Cached %s for %s as %s" % (relpath,expander.domain,repr(expander)))
		#TODO generate descr entries for urllists
	# TODO track deleted files removing them from cache

