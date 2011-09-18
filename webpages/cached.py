from __future__ import with_statement
from os.path import join, exists
from fs import listdir, filters
import hashlib
try:
    import json
except:
    import simplejson as json
import time

import tornado.web
import redis

UNIT_SEP = "\x1F"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Redis connection
REDIS = redis.Redis(REDIS_HOST, REDIS_PORT, db=0)

ONE_YEAR_IN_SECONDS = 365 * 24 * 3600
IN_A_YEAR_STAMP = time.time() + ONE_YEAR_IN_SECONDS


class CachedHandler(tornado.web.RequestHandler):
    
    def get(self,path):
    	if path in REDIS:
    		self.write(REDIS[path])
    		self.flush()
    	else:
    		raise tornado.web.HTTPError(404, "We couldn't find requested information")
        
