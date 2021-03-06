import json, logging

from base import get_browser_type, ObjectLike
from cached import *

import tornado.web
import tornado.template

class CachedHandler(tornado.web.RequestHandler):
    
    def head(self,path,browser_type=None):
        return self.get(path,browser_type,include_body=False)

    def is_binary_content(self,descr):
        if "Content-Type" not in descr: return False
        content_type = descr["Content-Type"]

        if content_type[:5] == "text/": return False
        if content_type[:22] == "application/javascript": return False
        if "page-data" in descr: return False
        if "page-head" in descr: return False
        if "page-tail" in descr: return False

        return True
        
    def is_templated(self,descr):
        if "templated" in descr:
            return descr["templated"]
        return True
    
    def get_redis_content(self,path,browser_type,domain,include_body=True):
        contentkey = BROWSER_SPECIFIC_CONTENT % (browser_type , domain, path) 
        descrkey = BROWSER_SPECIFIC_DESCR % (browser_type , domain, path) 
        #TODO etag and headers
        #TODO url type, inject state script
        descr = {}
        if descrkey not in REDIS:
            print "Content known but no descriptors", descrkey
        else:
            descr = json.loads(unicode(REDIS[descrkey],"utf-8"))
        for hn in self.HTTP_HEADER_NAMES:
            if hn in descr:
                self.set_header(hn,descr[hn])

        page_data = {}
        if "page-data" in descr:
            datakey = descr["page-data"]
            if datakey in REDIS:
                page_data = json.loads(REDIS[datakey])
        if "page-content" in descr and descr["page-content"] in REDIS:
            contentkey = descr["page-content"]

        page_head = u""
        if "page-head" in descr:
            headkey = descr["page-head"]
            if headkey in REDIS:
                page_head = json.loads(REDIS[headkey])

        page_tail = u"        \n\n\n           "
        if "page-tail" in descr:
            tailkey = descr["page-tail"]
            if tailkey in REDIS:
                page_tail = json.loads(REDIS[tailkey])

        if not include_body:
            self.flush()
            return

        lists = build_sitelists(domain)
        content = REDIS[contentkey]
        if not self.is_binary_content(descr):
            content = unicode(content,"utf-8")
            if self.is_templated(descr):
                #site_info = { "posts":[] } #TODO mix in SiteConfig and additional info
                site_object = self.application.config.site_object
                t = tornado.template.Template(page_head + content + page_tail)   
                self.write(t.generate(page=ObjectLike(page_data), list=lists, site=site_object))
            else:
                self.write(content)
        else:
            self.write(content)

        self.set_header("Cache-control","public") # https caching for FireFox             
        self.flush()

    def get(self,path,browser_type=None,include_body=True):
        if not browser_type:
            browser_type = get_browser_type( self.request.headers['User-Agent'] )

        domain = self.request.host.split(':')[0]
        domain = domain.replace(".local","") 
        if domain[:7] == "10.0.0." or domain[:8] == "192.168.":
            domain = "localhost"
        contentkey = BROWSER_SPECIFIC_CONTENT % (browser_type , domain, path) 
        if contentkey in REDIS:
            self.get_redis_content(path,browser_type,domain,include_body=include_body)
        else:
            logging.debug("404: %s" % path)
            raise tornado.web.HTTPError(404, "We couldn't find requested information")

    HTTP_HEADER_NAMES = [
        "Content-Type",
        "Content-Location",     # Do browser care?
        "Content-Disposition", # force download dialog
        "Content-Language",
        "Last-Modified",
        "Expires",
        "Location",         # for redirect
    ]
     
#TODO review tornado StaticFileHandler



urls = [
    ('^(/.*)$',CachedHandler),
]

