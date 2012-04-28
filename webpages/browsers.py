from __future__ import with_statement
import os, stat, site, codecs, logging
from os.path import join, exists, abspath, splitext, split
from bs4 import BeautifulSoup, Tag, NavigableString
from soupselect import select
import html5lib

class AreaInfo(object):

	def __init__(self,name):
		self.name = name
		self.active = "inactive"
		self.idx = 0
		self.last = None

	def getAreaClasses(self):
		return ["%s-area-%s" % (self.name,self.active)]

	def getOrder(self,element):
		if not hasattr(element,"%s_index" % self.name) or getattr(element,"%s_index" % self.name) is None:
			setattr(element,"%s_index" % self.name,self.idx)
			self.idx += 1
			self.last = element
		return getattr(element,"%s_index" % self.name)

class HtmlContent(object):

	def __init__(self,html):
		self.soup = BeautifulSoup(html,"html5lib")

	def injectBody(self,dest):
		contents = self.soup.contents
		if self.soup.body: contents = self.soup.body.contents

		for c in reversed(contents):
			dest.insert(0,c)

	def injectHead(self,dest):
		if self.soup.head:
			for c in reversed(self.soup.head.contents):
				dest.insert(0,c)

class PartFile(object):
	""" Fetch Browser Specific Part
	"""

	def __init__(self,specific,name,tag):
	    if hasattr(self,"init_%s" % tag):
	        self.path = getattr(self,"init_%s" % tag)(specific,name,tag)
	    else:
	        self.path = self.init_html(specific,name,tag)

	def read(self):
		with open(self.path,'rb') as f:
			return f.read()
			
	def init_script(self,specific,name,tag):
		bits = name.split(u"/")
		prefix = join(site.PARTS_DIR,*bits[:-1])
		just_name = bits[-1]

		path = join(prefix, specific.browser_type, "%s.%s.js" % (just_name,tag))
		if not exists(path):
			path = join(prefix, "%s.%s.js" % (just_name,tag))
		return path
		
	def init_html(self,specific,name,tag):
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
		return path

class PartDocument(object):

	auto_config_id = 0 #TODO make it top doc unique
	auto_tracker_id = 0

	def __init__(self,specific,name,config):
		self.specific = specific
		self.name = name
		self.config = config
		self.header = {}
		self.rest = None
		self.parent = None
		self.statefulConfigs = {}
		self.areas = {}

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
			return BeautifulSoup(content,"html5lib")

		part_content = self.rest
		if self.parent:
			part_content = self.parent.wrapDocumentSoup(self.rest).prettify()

		soup = BeautifulSoup(part_content,"html5lib")

		# insert body / content
		content_tag = "content-tag" in self.header and self.header["content-tag"] or "body"
		dest = soup.findAll(content_tag)[0]

		htmlContent = HtmlContent(content)
		htmlContent.injectBody(dest)

		#TODO priority for links and scripts added
		htmlContent.injectHead(soup.find("head"))

		return soup

	def statefulConfigScript(self):
		import json

		STATEFUL_CONFIG_ENTRY = u"""\
declare("%(id)s",%(json)s);
"""

		lines = []
		for c in self.statefulConfigs:
			lines.append(STATEFUL_CONFIG_ENTRY % {
				"id": c,
				"value": self.statefulConfigs[c],
				"json": json.dumps(self.statefulConfigs[c], sort_keys=True),
				})
		if len(lines):
			return u"".join(lines)
		return None 

	def expandTags(self,soup,tagName,attrs=("id",)):
		tags = soup.findAll(tagName)
		for tag in tags:
			part = None
			config_id = None
			if tag.get("inline-src"):
				part = PartFile(self.specific,tag["inline-src"],tagName)
				del tag["inline-src"]
			elif tag.get("inline-id"):
				part = PartFile(self.specific,tag["inline-id"],tagName)
				del tag["inline-id"]
			else:
			    for attr in attrs:
			        if tag.get(attr):
			        	config_id = tag[attr]
				        part = PartFile(self.specific,tag[attr],tagName)
				        break

			if part and exists(part.path):
				header,rest = self.config.split_matter_and_utf8_content(part.read(),{})
				HtmlContent(rest).injectBody(tag)
				if config_id:
					setattr(tag,'config_id',config_id)
					self.statefulConfigs[config_id] = header
					#TODO list descendant nodes with names.
				#TODO parse with soup to support breaking out header/footer ?
				#TODO script
				
	def forceConfigId(self,element,forceAttribute=False):
		if not hasattr(element,'config_id') or getattr(element,'config_id') is None:
			if element.get("id"):
				setattr(element,'config_id',element["id"])
			else:
				self.auto_config_id += 1
				setattr(element,'config_id',"es-%s" % self.auto_config_id)
		if forceAttribute and ("id" not in element or element["id"] is None) and ("src" not in element or element["src"] is None):
			element["id"] = getattr(element,'config_id')
			
		return getattr(element,'config_id')

	def saveStageConfig(self,element,areaNames):
		config_id = self.forceConfigId(element)
		matter = self.statefulConfigs[config_id] = config_id in self.statefulConfigs and self.statefulConfigs[config_id] or {}
		matter["area-names"] = areaNames
		classNames = self.getAreaClasses(areaNames)
		if "class" in element: classNames = element["class"].split(" ") + classNames
		element["class"] = " ".join(classNames)
		if "layouter" not in matter:
			matter["layouter"] = "area-stage"

	def saveMemberConfig(self,element,areaNames):
		config_id = self.forceConfigId(element)
		matter = self.statefulConfigs[config_id] = config_id in self.statefulConfigs and self.statefulConfigs[config_id] or {}
		matter["area-names"] = areaNames
		classNames = []
		if "class" in element: classNames = element["class"].split(" ")
		for an in areaNames: 
			classNames.append("in-%s-area" % an)
			classNames.append("in-%s-order-%s" % (an,self.getAreaOrder(element,an)))

		element["class"] = " ".join(classNames)
		if "laidout" not in matter:
			matter["laidout"] = "area-member"

	def saveTrackerDrivenConfig(self,element,props,soup):
		config_id = self.forceConfigId(element,forceAttribute=True)
		matter = self.statefulConfigs[config_id] = config_id in self.statefulConfigs and self.statefulConfigs[config_id] or {}
		matter["tracker-driven"] = props

		tracker = soup.new_tag("div")
		self.auto_tracker_id += 1
		tracker["id"] = "trk-%s" % self.auto_tracker_id
		classNames = []
		if "class" in element: classNames = element["class"].split(" ")
		classNames += ["tracker", "%s-tracker" % element.name]
		if "area-names" in matter:
			for an in matter["area-names"]: 
				classNames.append("in-%s-area" % an)
				classNames.append("in-%s-order-%s" % (an,self.getAreaOrder(element,an)))
		tracker["class"] = " ".join(classNames)

		# if "tracker-parent" in element doesn't seem to work
		try:
			trackerParent = soup.find(id=element["tracker-parent"])
			if trackerParent:
				matter["tracker-parent"] = element["tracker-parent"]
				trackerParent.insert(0,tracker)
			else:
				element.insert_before(tracker)
			del element["tracker-parent"]
		except: #TODO more precise catch
			element.insert_before(tracker)

		matter["driven-by"] = tracker["id"]

	def getAreaOrder(self,element,areaName):
		if areaName not in self.areas:
			self.areas[areaName] = AreaInfo(areaName)
		return self.areas[areaName].getOrder(element)

	def addClassToLastInOrder(self):
		for an in self.areas:
			area = self.areas[an]
			if area.last:
				area.last["class"] += u" in-%s-order-last" % an

	def getAreaClasses(self,areaNames):
		classes = []
		for areaName in areaNames:
			if areaName not in self.areas:
				self.areas[areaName] = AreaInfo(areaName)
			classes += self.areas[areaName].getAreaClasses()
		return classes


	def expandSoup(self,content):
		"""Expand content into the body or content-tag of the PartDocument
			expand elements with id or src.
			construct areas and stages
			construct tracker driven
			"""
		import re
		soup = self.wrapDocumentSoup(content)

		# expand the outline elements
		self.expandTags(soup,"article", attrs=("src","id"))
		self.expandTags(soup,"aside", attrs=("src","id"))
		self.expandTags(soup,"section", attrs=("src","id"))
		self.expandTags(soup,"nav", attrs=("src","id"))
		self.expandTags(soup,"header", attrs=("src","id"))
		self.expandTags(soup,"footer", attrs=("src","id"))

		self.expandTags(soup,"script")
		self.expandTags(soup,"style")

		self.expandTags(soup,"form", attrs=("src","id"))

# def has_class_but_no_id(tag):
#     return tag.has_key('class') and not tag.has_key('id')

		stages = soup.findAll( attrs={"area-stage":re.compile(r".*")} )
		for stage in stages:
			self.saveStageConfig(stage,stage["area-stage"].split(" "))
			del stage["area-stage"]

		members = soup.findAll( attrs={"in-area":re.compile(r".*")} )
		for member in members:
			self.saveMemberConfig(member,member["in-area"].split(" "))
			del member["in-area"]

		self.addClassToLastInOrder()

		tracked = soup.findAll( attrs={"tracker-driven":re.compile(r".*")} )
		for t in tracked:
			self.saveTrackerDrivenConfig(t,t["tracker-driven"].split(" "),soup)
			del t["tracker-driven"]

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

	def __repr__(self):
		return "[%s specifics]" % self.browser_type

	def expand(self,header,content,markup=None,config=None):
		"""
		General header/content expansion replacing expandDocument and expandScss
		"""
		lists = {
			"offline": [],
		}

		if "charset" not in header and markup is not None:
			header["charset"] = config["charset"]
		parent_doc = None
		if "document" in header:
			parent_doc = self.partDocument(header["document"],config)
			header = parent_doc.get_collapsed_header(header=header)

		if markup is "scss":
			content = self.expandScss(header,content,config=config)
		elif markup in ("text","xml"):
			pass #TODO consider what to do
		elif markup is "html":
			soup = None
			if parent_doc:
				soup = parent_doc.expandSoup(content)
			else:
				soup = BeautifulSoup(content,"html5lib")

			# print soup.head
			stateful_doc = "stateful" in header and header["stateful"] is True

			if stateful_doc:
				script = parent_doc.statefulConfigScript()
				if script:
					script_tag = soup.new_tag("script")
					script_tag["type"] = "application/config"
					script_tag.string = script
					soup.body.append(script_tag)

			# fill in meta tags
			self._applyMetaAndTitle(soup,header,config)

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
			lists["offline"] = self._getOfflineList(soup,header)
			content = soup.encode()

		return header, content, lists


	#TODO obsolete, test that all functionality is done by expand
	def expandHeader(self,header,config=None):
		raise "obsolete"
		if "encoding" not in header:
			header["encoding"] = "utf-8"
		if "document" in header:
			part = self.partDocument(header["document"],config)
			return part.get_collapsed_header(header=header)

		return header

	#TODO obsolete, test that all functionality is done by expand
	def expandDocument(self,header,content,config=None):
		raise "obsolete"
		part = self.partDocument(header["document"],config)
		soup = part.expandSoup(content)
		header = part.get_collapsed_header(header=header)
		stateful_doc = "stateful" in header and header["stateful"] is True

		if stateful_doc:
			script = part.statefulConfigScript()
			if script:
				script_tag = soup.new_tag("script")
				script_tag["type"] = "application/config"
				script_tag.string = script
				soup.body.append(script_tag)

		# fill in meta tags
		self._applyMetaAndTitle(soup,header,config)

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
		lists = {
			"offline": self._getOfflineList(soup,header),
		}

		return soup.prettify(), lists

	#TODO obsolete, test that all functionality is done by expand
	def expandScss(self,header,content,config=None):
		from scss import Scss
		#TODO offline images
		css = Scss(scss_opts={
			"compress": config["css-compress"],
			})
		#TODO scss unicode call
		return unicode(css.compile(content))


	def partDocument(self,name,config):
		#TODO cache to avoid reloading (reload on change date)
		return PartDocument(self,name,config)

	def _applyMetaAndTitle(self,soup,header,config):
		charset = "charset" in header and header["charset"] or config["charset"]
		for charset in soup.find_all("meta",attrs={ "name": "charset"}):
			charset["content"] = charset

		description = "description" in header and header["description"] or None
		if description:
			for desc in soup.find_all("meta",attrs={ "name": "description" }):
				desc["content"] = description

		author = "author" in header and header["author"] or config["author"]
		if author:
			for desc in soup.find_all("meta",attrs={ "name": "author" }):
				desc["content"] = author

		if "title" in header:
			#TODO site.title-template "{{ page.title }} - My App"
			for t in select(soup,"title"):
				t.string = header["title"]
		#TODO elif site.title

	def _getOfflineList(self,soup,header):
		offline = []
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
		return offline



browsers = [
	BrowserSpecific('pocket'),
	BrowserSpecific('tablet'),
	BrowserSpecific('desktop'),
]