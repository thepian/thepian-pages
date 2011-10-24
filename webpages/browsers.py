from __future__ import with_statement
import os, stat, site, codecs
from os.path import join, exists, abspath, splitext, split
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from soupselect import select
from scss import Scss

class PartFile(object):
	""" Fetch Browser Specific Part
	"""

	def __init__(self,specific,name,tag):
		bits = name.split(u"/")
		prefix = join(site.PARTS_DIR,*bits[:-1])
		just_name = bits[-1]

		path = join(prefix, specific.browser_type, "%s.%s.markdown" % (just_name,tag))
		if not exists(path):
			path = join(prefix, "%s.%s.markdown" % (just_name,tag))
			if not exists(path):
				path = join(prefix, specific.browser_type, "%s.%s.html" % (just_name,tag))
				if not exists(path):
					path = join(prefix, "%s.%s.html" % (just_name,tag))

		self.path = path

	def read(self):
		with open(self.path,'rb') as f:
			return f.read()

class PartDocument(object):

	def __init__(self,specific,name,config):
		self.specific = specific
		self.name = name
		self.config = config
		self.header = {}
		self.rest = None
		self.parent = None

		doc = PartFile(specific,name,"document")
		
		if exists(doc.path):
			self.header,self.rest = config.split_matter_and_utf8_content(doc.read(),{})
			if "document" in self.header:
				parent_name = self.header["document"]
				if not parent_name:
					pass
				if parent_name == name:
					print "Recursive document reference in %s.document.html" % name
				else:
					self.parent = PartDocument(self.specific,parent_name,self.config)
		else:
			print "no part named", doc.path


	def wrapDocumentSoup(self,content):
		"""Wrap the chain of documents around content. Recursively calls itself to wrap parent chain."""
		if not self.rest:
			return BeautifulSoup(content)

		part_content = self.rest
		if self.parent:
			part_content = self.parent.wrapDocumentSoup(self.rest).prettify()

		soup = BeautifulSoup(part_content)

		# insert body / content
		content_tag = "content-tag" in self.header and self.header["content-tag"] or "body"
		dest = soup.findAll(content_tag)[0]

		nested = BeautifulSoup(content)
		for c in reversed(nested.contents):
			dest.insert(0,c)

		return soup

	def expandTags(self,soup,tagName):
		tags = soup.findAll(tagName)
		for tag in tags:
			part = None
			if tag.get("inline-id"):
				part = PartFile(self.specific,tag["inline-id"],tagName)
				del tag["inline-id"]
			elif tag.get("id"):
				part = PartFile(self.specific,tag["id"],tagName)

			if part and exists(part.path):
				header,rest = self.config.split_matter_and_utf8_content(part.read(),{})
				nested = BeautifulSoup(rest)
				for c in reversed(nested.contents):
					tag.insert(0,c)
				#TODO parse with soup to support breaking out header/footer ?
				


	def expandSoup(self,content):
		soup = self.wrapDocumentSoup(content)

		# expand the sections
		self.expandTags(soup,"article")
		self.expandTags(soup,"aside")
		self.expandTags(soup,"section")
		self.expandTags(soup,"nav")
		self.expandTags(soup,"header")
		self.expandTags(soup,"footer")

		self.expandTags(soup,"script")
		self.expandTags(soup,"style")

		return soup

	def get_collapsed_header(self,header=None):
		if self.parent:
			r = self.parent.get_collapsed_header()
		else:
			r = {}
		for k in self.header.keys():
			r[k] = self.header[k]
		if header:
			for k in header: r[k] = header[k]

		if "lang" in r:
			r["Content-Language"] = r["lang"]

		return r
	
class BrowserSpecific(object):

	def __init__(self,browser_type):
		self.browser_type = browser_type

	def expandHeader(self,header,config=None):
		if "document" in header:
			part = self.partDocument(header["document"],config)
			return part.get_collapsed_header(header=header)

		return header

	def expandDocument(self,header,content,config=None):
		part = self.partDocument(header["document"],config)
		soup = part.expandSoup(content)
		header = part.get_collapsed_header(header=header)

		# fill in meta tags
		if "description" in header:
			for desc in select(soup,"meta[name=description]"):
				desc["content"] = header["description"]
		if "author" in header:
			for desc in select(soup,"meta[name=author]"):
				desc["content"] = header["author"]
		if "title" in header:
			#TODO site.title-template "{{ page.title }} - My App"
			for t in select(soup,"title"):
				t.setString(header["title"])
		#TODO elif site.title

		if config["appcache"] == False:
			for h in select(soup,"html"):
				del h["manifest"]
		elif "manifest" in header:
			for h in select(soup,"html"):
				h["manifest"] = header["manifest"]

		if "Content-Language" in header:
			for h in select(soup,"html"):
				h["lang"] = header["Content-Language"]

		# offline markers
		offline = []
		lists = {
			"offline": offline,
		}
		if "appcache" in header:
			images = select(soup,"img[src]")
			for img in images:
				#TODO resolve with doc path
				offline.append(img["src"])
				del img["offline"]
			stylesheets = select(soup,"link[rel=stylesheet]")
			for s in stylesheets:
				#TODO resolve with doc path
				offline.append(s["href"])
				del s["offline"]
			scripts = select(soup,"script[offline]")
			for s in scripts:
				#TODO resolve with doc path
				offline.append(s["src"])
				del s["offline"]

		return soup.prettify(), lists

	def expandScss(self,header,content,config=None):
		#TODO offline images
		css = Scss()
		return css.compile(content)


	def partDocument(self,name,config):
		return PartDocument(self,name,config)


browsers = [
	BrowserSpecific('pocket'),
	BrowserSpecific('tablet'),
	BrowserSpecific('desktop'),
]