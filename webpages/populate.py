from __future__ import with_statement

import sys, os, stat, logging, site, re
from os.path import join, exists, abspath, realpath, splitext, split, dirname
from fs import listdir, filters
import mimetypes, codecs

from browsers import *

class UnversionedExpander(object):

	def __init__(self,original):
		self.original = original

		self.config = original.config
		self.prefix = original.prefix
		self.base = original.base
		self.path = original.path
		self.name = original.name
		self.ext = original.ext

		self.modified = original.modified
		self.domain = original.domain

		self.header = original.header
		self.content = original.content

		version = original.name_parts[1]
		self.urlpath = original.urlpath.replace("-%s" % version,"")
		self.outpath = original.outpath.replace("-%s" % version,"")

		self.published = original.published
		self.markup = original.markup
		self.fetchContent = original.fetchContent

		# print >>sys.stderr, self.outpath

	def __repr__(self):
		return repr(self.original)

	def get_name_parts(self):
		np = original.name_parts
		return [np[0], None, np[2]]
	name_parts = property(get_name_parts)

	def get_matter_and_content_for(self,browser_type):
		return self.original.get_matter_and_content_for(browser_type)


class FileExpander(object):
	"""
	Used to expand files in the site into the Redis cache.
	"""
	def __init__(self,base,relpath,prefix=None,config=None):
		import datetime

		self.config = config
		self.prefix = prefix
		self.base = base
		self.path = relpath
		self.name, self.ext = splitext(split(relpath)[1])
		if self.name[-4:] == ".min":
			self.name = self.name[:-4]
			self.ext = ".min%s" % self.ext

		path = abspath(join(base,relpath))
		stat_result = os.stat(path)
		self.modified = datetime.datetime.fromtimestamp(stat_result[stat.ST_MTIME])

		self.markup = None
		self.fetchContent = False

		self.domain = self.config["domain"]

		# Load file into *header* and *content*
		if self.ext in self.FILE_EXTENSIONS:
			self.FILE_EXTENSIONS[self.ext](self,self.path)
		else:
			self._default_file(self.path)

	def __repr__(self):
		return "%s %s %s %s" % (self.urlpath,self.name,self.ext,self.header)

	def get_name_parts(self):
		lib_ver = self.name.split("-")
		name = self.name
		version = None

		if re.match(r'(\d+\.?)+$',lib_ver[-1]):
			name = "-".join(lib_ver[:-1])
			version = lib_ver[-1]

		return [
			name,
			version,
			self.ext
		]

	name_parts = property(get_name_parts)

	def unversioned_copy(self):
		return UnversionedExpander(self)

	def get_matter_and_content_for(self,browser_type):
		relpath = join(browser_type,self.path)
		if self.fetchContent:
			header = self.header
			content = self._fetch_content(header)
		elif exists(join(self.base,relpath)) and self.markup == "scss":
			header,content,fetchContent = self._get_matter_and_content(relpath,self.header)
			if fetchContent:
				content = self._fetch_content(header)
		else:
			header,content = self.header,self.content

		return header,content

	def _fetch_content(self,header):
		#TODO joining strategies for different content, binary files - no shims
		fetch = "fetch" in header and header["fetch"] or header["content"]
		if type(fetch) == list:
			return u"".join([self._fetch_part(entry) for entry in fetch])
		else:
			return self._fetch_part(fetch)

	def _fetch_part(self, ref, basedir=None):
		basedir = dirname(join(self.base,self.path))
		if ref[:5] == "http:":
			from urllib2 import urlopen
			response = urlopen(ref)
			raw = response.read()
			charset = self.config["charset"] #TODO support matter in http source/http headers
			if "content-type" in response.headers:
				type_and_charset = response.headers['content-type'].split('charset=')
				if len(type_and_charset) > 1:
					charset = type_and_charset[-1]
			content = unicode(raw, charset)
			return content
		else:
			logging.info("Fetching %s from %s" % (ref,basedir))
			fetch_abs = abspath(join(basedir,ref))
			content = None
			with open(fetch_abs,"rb") as f:
				content = f.read()
			defaultheader = {}
			#TODO recursive fetch
			header,content = self.config.split_matter_and_utf8_content(content,defaultheader)
			return content

	def _get_published(self):
		if "published" in self.header:
			return self.header["published"]
		return True

	published = property(_get_published)

	def _get_matter_and_content(self,relpath,defaultheader):
		content = None
		with open(abspath(join(self.base,relpath)), "rb") as f:
			content = f.read()
		header,content = self.config.split_matter_and_utf8_content(content,defaultheader)
		fetchContent = False
		if "fetch" in header:
			fetchContent = True
		if "content" in header:
			fetchContent = True
		return header,content,fetchContent

	def _scss_file(self,relpath):
		header = {
			"Content-Type": "text/css",
		}
		self.header,self.content,self.fetchContent = self._get_matter_and_content(relpath,header)
		   
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
		self.markup = "scss"

	def _xml_file(self,relpath):
		header = {
			"Content-Type": "text/xml",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
		else:
			self.urlpath = "/" + self.path

		self.header,self.content,self.fetchContent = self._get_matter_and_content(relpath,header)
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
		self.markup = "xml"

	def _text_file(self,relpath):
		header = {
			"Content-Type": "text/plain",
		}
		if self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
			if self.urlpath[-1] != "/": self.urlpath += "/"
		else:
			self.urlpath = "/" + self.path

		self.header,self.content,self.fetchContent = self._get_matter_and_content(relpath,header)
		   
		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]

		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		self.outpath = self.urlpath
		self.markup = "text"

	def _html_file(self,relpath):
		header = {
			"Content-Type": "text/html",
		}
		self.header,self.content,self.fetchContent = self._get_matter_and_content(relpath,header)
		   
		outpath = None
		if "extension" in self.header:
			self.urlpath = "/" + splitext(self.path)[0] + "." + self.header["extension"]			
			outpath = self.urlpath
		elif self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
			if self.urlpath[-1] != "/": self.urlpath += "/"
			outpath = self.urlpath + "index.html"
		else:
			self.urlpath = "/" + splitext(self.path)[0] + "/"
			outpath = self.urlpath + "index.html"

		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			
		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		self.outpath = outpath or self.urlpath
		self.markup = "html"

	def _markdown_file(self,relpath):
		header = {
			"Content-Type": "text/html",
		}
		self.header,rest,self.fetchContent = self._get_matter_and_content(relpath,header)
		#TODO content/fetch ?

		outpath = None
		if "extension" in self.header:
			self.urlpath = "/" + splitext(self.path)[0] + "." + self.header["extension"]			
			outpath = self.urlpath
		elif self.name == "index":
			self.urlpath = "/" + split(self.path)[0]
			if self.urlpath[-1] != "/": self.urlpath += "/"
			outpath = self.urlpath + "index.html"
		else:
			self.urlpath = "/" + splitext(self.path)[0] + "/"
			outpath = self.urlpath + "index.html"

		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			
		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)

		self.outpath = outpath or self.urlpath

		self.markup = "html"

		import markdown2
		extras = ["code-friendly","wiki-tables","cuddled-lists"]
		if "markdown-extras" in self.header:
			extras = self.header["markdown-extras"]
		self.content = markdown2.markdown(rest,extras).encode("utf-8")
		   
	def _js_file(self,relpath):
		header = {
			"Content-Type": "application/javascript",
			"templated": False,
		}

		self.header,self.content,self.fetchContent = self._get_matter_and_content(relpath,header)
		self.urlpath = "/" + self.path
		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)
		self.outpath = self.urlpath

	def _default_file(self,relpath):
		header = {
			"Content-Type": "text/plain", "charset": False,
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

		self.header,rest,self.fetchContent = self._get_matter_and_content(relpath,header)
		self.content = rest.lstrip()

		self.urlpath = "/" + self.path
		self.outpath = self.path
		if "permalink" in self.header:
			#TODO if it doesn't start with / look up special meaning keyword
			#TODO replace :xxx with value of xxx (year,month,day,title,i_day,i_month,categories,tags)
			self.urlpath = self.header["permalink"]
			self.outpath = self.header["permalink"]
		elif "url" in self.header:
			self.urlpath = "/" + self.header["url"]
			self.outpath = self.header["url"]
			
		if self.prefix:
			self.urlpath = "/%s%s" % (self.prefix,self.urlpath)
			self.outpath = "%s%s" % (self.prefix,self.urlpath)


	FILE_EXTENSIONS = {
		".min.js": _js_file,
		".js" : _js_file,
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

def compare_version(a,b):
	from pkg_resources import parse_version
	if not a: return +1
	if not b: return -1
	return cmp(parse_version(a),parse_version(b))

class LibBuilder(object):

	def __init__(self,base,prefix=None,subdir=None,config=None):
		self.base = base
		self.subdir = subdir
		self.prefix = prefix
		self.config = config

		self.versions = {}
		self.mostRecent = None
		self.minVersions = {}
		self.mostRecentMin = None

	def addVersion(self,expander):
		version = expander.name_parts[1]
		if expander.ext == ".min.js":
			self._add("minVersions","mostRecentMin",expander,version)
		else:
			self._add("versions","mostRecent",expander,version)

	def _add(self,vers,mr,expander,version):
		versions = getattr(self,vers)
		versions[version] = expander
		if not getattr(self, mr):
			setattr(self, mr, expander)
		else:
			if compare_version(getattr(self, mr).name_parts[1],expander.name_parts[1]) > 0:
				setattr(self, mr, expander)

	def get_versions(self):
		#TODO minified versions & most recent version
		latest = None
		for name in self.versions.iterkeys():
			latest = self.versions[name]
			yield latest
		for name in self.minVersions.iterkeys():
			latest = self.minVersions[name]
			yield latest

		if self.mostRecent and (self.mostRecent != latest or latest.name_parts[1]):
			yield self.mostRecent.unversioned_copy()
		if self.mostRecentMin and (self.mostRecentMin != latest or latest.name_parts[1]):
			yield self.mostRecentMin.unversioned_copy()

	deployed_expanders = property(get_versions)


def save_expander(expander,browser,config):
	base_path = config["output"]
	file_path = join(base_path,browser.browser_type,expander.outpath[1:])
	if config["browser"]:
		file_path = join(base_path,expander.outpath[1:])
	dir_path = dirname(file_path)

	if not expander.published:
		if exists(file_path): os.remove(file_path)
		return
	if not exists(dir_path):
		os.makedirs(dir_path)

	header,content = expander.get_matter_and_content_for(browser.browser_type)
	header,content, lists = browser.expand(header,content,markup=expander.markup,config=expander.config) 
	try:
		if "charset" in header:
			content = content.encode(header["charset"])
	except Exception,e:
		print >>sys.stderr, "failed to encode", expander.path
	#expander.update_lists(header,{ "offline": [expander.urlpath] })

	charset = "charset" in header and header["charset"] or None
	print charset, type(content), file_path.replace(base_path,"")
	with open(file_path,"wb") as f:
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

	base_filters = [config.exclude_filter(),filters.no_hidden,filters.no_system]
	css_prefix = "css"
	js_prefix = "js"
	if config["assets-base"]:
		css_prefix = "%s/css" % config["assets-base"]
		js_prefix = "%s/js" % config["assets-base"]

	if site.SCSS_DIR:
		for relpath in listdir(site.SCSS_DIR,filters=base_filters+[filters.fnmatch("*.scss"),]):
			expander = FileExpander(site.SCSS_DIR,relpath,config=config,prefix=css_prefix)
			#setattr(scss,"LOAD_PATHS",site.SCSS_DIR)
			for browser in browsers:
				if not config["browser"] or config["browser"] == browser.browser_type:
					expander_writer(expander,browser,config) 
			logging.info("Cached %s for %s as %s" % (relpath,expander.domain,repr(expander)))

	if site.LIBS_DIR:
		builders = {}
		for relpath in listdir(site.LIBS_DIR, filters=[filters.only_directories,filters.fnmatch("*.js")]):
			libname = relpath[:-3]
			builder = LibBuilder(site.LIBS_DIR,subdir=libname,config=config)
			builders[libname] = builder
			#TODO figure out the relevant one

		for relpath in listdir(site.LIBS_DIR, filters=[filters.no_directories,filters.fnmatch("*.js")]):
			expander = FileExpander(site.LIBS_DIR,relpath,config=config,prefix=js_prefix)
			prefix = expander.name_parts[0]
			if prefix in builders:
				builder = builders[prefix]
			else:
				builder = LibBuilder(site.LIBS_DIR,prefix=prefix,config=config)
				builders[prefix] = builder
			builder.addVersion(expander)

		for name in builders.iterkeys():
			builder = builders[name]
			for expander in builder.deployed_expanders:
				for browser in browsers:
					if not config["browser"] or config["browser"] == browser.browser_type:
						#print >>sys.stderr, repr(expander)
						expander_writer(expander,browser,config)
		

	for relpath in listdir(site.SITE_DIR,recursed=True,filters=base_filters):
		expander = FileExpander(site.SITE_DIR,relpath,config=config)
		if relpath[0] != "_":
			for browser in browsers:
				if not config["browser"] or config["browser"] == browser.browser_type:
					expander_writer(expander,browser,config) 
			logging.info("Cached %s for %s as %s" % (relpath,expander.domain,repr(expander)))
		#TODO generate descr entries for urllists
	# TODO track deleted files removing them from cache

