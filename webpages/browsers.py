from __future__ import with_statement
import os, stat, site
from os.path import join, exists, abspath, splitext, split
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from soupselect import select
from scss import Scss

class PartDocument(object):

	def __init__(self,specific,name,config):
		self.specific = specific
		self.name = name
		self.config = config
		self.header = {}
		self.rest = None
		self.parent = None

		path = join(site.PARTS_DIR, "%s/%s.document.html" % (specific.browser_type,name))
		if not exists(path):
			path = join(site.PARTS_DIR, "%s.document.html" % name)
		
		if exists(path):
			with open(path,'rb') as f:
				self.header,self.rest = config.split_header_and_utf8_content(f.read(),{})
			if "document" in self.header:
				parent_name = self.header["document"]
				if not parent_name:
					pass
				if parent_name == name:
					print "Recursive document reference in %s.document.html" % name
				else:
					self.parent = PartDocument(self.specific,parent_name,self.config)
		else:
			print "no part named", path

	def expandSoup(self,content):
		if not self.rest:
			return BeautifulSoup(content)

		part_content = self.rest
		if self.parent:
			part_content = self.parent.expandSoup(self.rest).prettify()

		soup = BeautifulSoup(part_content)
		content_tag = "content-tag" in self.header and self.header["content-tag"] or "body"
		dest = soup.findAll(content_tag)[0]
		text = NavigableString(content)
		dest.insert(0, text)

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