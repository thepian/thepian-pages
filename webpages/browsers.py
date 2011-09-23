from __future__ import with_statement
import os, stat, site
from os.path import join, exists, abspath, splitext, split
from BeautifulSoup import BeautifulSoup
from scss import Scss


class BrowserSpecific(object):

	def __init__(self,browser_type):
		self.browser_type = browser_type

	def expandHeader(self,header,config=None):
		#TODO extend with parts matter
		return header

	def expandPage(self,header,content,config=None):

		page_name = header["page"]
		page_path = join(site.PARTS_DIR, "%s/%s.page.html" % (self.browser_type,page_name))
		if not exists(page_path):
			page_path = join(site.PARTS_DIR, "%s.page.html" % page_name)
		if not exists(page_path):
			return content

		with open(page_path,'rb') as f:
			header,rest = config.split_header_and_utf8_content(f.read(),{})
			soup = BeautifulSoup(rest)
			dest = soup.findAll('article')[0]
			dest.setString(content)

			return soup.prettify()

	def expandScss(self,header,content,config=None):

		css = Scss()
		return css.compile(content)

browsers = [
	BrowserSpecific('pocket'),
	BrowserSpecific('tablet'),
	BrowserSpecific('desktop'),
]