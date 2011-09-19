from __future__ import with_statement
import os, stat, site
from os.path import join, exists, abspath, splitext, split
from BeautifulSoup import BeautifulSoup

def expandPage(page_name,content,config=None):
	page_path = join(site.PARTS_DIR, "%s.page.html" % page_name)
	if not exists(page_path):
		return content

	with open(page_path,'rb') as f:
		header,rest = config.split_header_and_utf8_content(f.read(),{})
		soup = BeautifulSoup(rest)
		dest = soup.findAll('article')[0]
		print dir(dest)
		dest.setString(content)

		return soup.prettify()

