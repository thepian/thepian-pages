from __future__ import with_statement

import hashlib, json, datetime, time
import redis

from base import ObjectLike
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

SITELISTS = "sitelist:%s"
SITELIST = "sitelist:%s%s"
URLLISTS = "urllist:%s"
URLLIST = "urllist:%s"

BROWSER_SPECIFIC_LEAD = "lead:%s:%s%s"
BROWSER_SPECIFIC_REGEX = "regex:%s:%s%s"
BROWSER_SPECIFIC_DESCR = "descr:%s:%s%s"
BROWSER_SPECIFIC_HEAD = "head:%s:%s%s"
BROWSER_SPECIFIC_CONTENT = "content:%s:%s%s"
BROWSER_SPECIFIC_TAIL = "tail:%s:%s%s"

def wipe_sitelists(domain):
	#print "wiping ",domain,REDIS.smembers(SITELISTS % domain)
	for name in REDIS.smembers(SITELISTS % domain):
		cachelistkey = SITELIST % (domain,name)
		REDIS.delete(cachelistkey)
	REDIS.delete(SITELISTS % domain)

def build_sitelists(domain):
	lists = {}
	for name in REDIS.smembers(SITELISTS % domain):
		cachelistkey = SITELIST % (domain,name)
		if cachelistkey in REDIS:
			value = u"\n".join(REDIS.smembers(cachelistkey))
			lists[name] = value
		else:
			lists[name] = ''
	return ObjectLike(lists)

def build_template_vars(domain):
	lists = {}
	for name in REDIS.smembers(SITELISTS % domain):
		cachelistkey = SITELIST % (domain,name)
		if cachelistkey in REDIS:
			value = u"\n".join(REDIS.smembers(cachelistkey))
			lists["list.%s" % name] = value
	return lists

def update_lists(expander,header,lists):
	if "appcache" in header:
		appcache = header["appcache"].split(" ")
		for name in appcache:
			listname = "%s_appcache" % name
			REDIS.sadd(SITELISTS % expander.domain,listname)
			if expander.config["appcache"]:
				cachelistkey = SITELIST % (expander.domain,listname)
				if "offline" in lists:
					offline = lists["offline"]
					for path in offline:
						REDIS.sadd(cachelistkey,path)


def cache_expander(expander,browser,config):
	contentkey = BROWSER_SPECIFIC_CONTENT % (browser.browser_type , expander.domain, expander.urlpath) 
	descrkey = BROWSER_SPECIFIC_DESCR % (browser.browser_type , expander.domain, expander.urlpath) 

	if not expander.published:
		if descrkey in REDIS:
			REDIS.delete(descrkey)
		if contentkey in REDIS:
			REDIS.delete(contentkey)
		return

	header,content = expander.get_matter_and_content_for(browser.browser_type)
	header,content, lists = browser.expand(header,content,markup=expander.markup,config=expander.config) 
	try:
		if "charset" in header:
			content = content.encode(header["charset"])
	except Exception,e:
		print >>sys.stderr, "failed to encode", expander.path
	
	update_lists(expander,header,lists)

	REDIS[contentkey] = content
	REDIS.expire(contentkey,ONE_YEAR_IN_SECONDS)
	#TODO don't add descr entry if part of list
	REDIS[descrkey] = json.dumps(header)
	REDIS.expire(descrkey,ONE_YEAR_IN_SECONDS)




