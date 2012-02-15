from __future__ import with_statement
import sys,site
import shutil

from os.path import dirname, join, exists, getsize
pages_test_root = dirname(__file__)

def test_populate():
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander
	
	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,"w1"))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
	})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","desktop","js","html5.js"))
	assert exists(join(pages_test_root,"output","pocket","js","html5.js"))
	assert exists(join(pages_test_root,"output","tablet","js","html5.js"))

def test_populate_desktop_browser():

	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander

	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,"w1"))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
		"browser": "desktop",		
	})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","js","html5.js"))
	h5size = getsize(join(pages_test_root,"html5-patch.js"))
	disclsize = getsize(join(pages_test_root,"lead-disclaimer.js"))

	assert getsize(join(pages_test_root,"output","js","html5.js")) == disclsize + h5size

def test_populate_jquery():
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander
	
	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,"w2"))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
	})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","desktop","js","jquery-1.5.1.js"))
	jqsize = getsize(join(pages_test_root,"w2","_libs","jquery-1.5.1.js"))
	assert getsize(join(pages_test_root,"output","desktop","js","jquery-1.5.1.js")) == jqsize
	assert getsize(join(pages_test_root,"output","desktop","js","jquery.js")) == jqsize
	jqminsize = getsize(join(pages_test_root,"w2","_libs","jquery-1.5.1.min.js"))
	assert getsize(join(pages_test_root,"output","desktop","js","jquery-1.5.1.min.js")) == jqminsize
	assert getsize(join(pages_test_root,"output","desktop","js","jquery.min.js")) == jqminsize

def test_populate_http_fetch():
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander
	
	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,"w3"))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
		"browser": "desktop",		
	})

	import SimpleHTTPServer
	import SocketServer
	import threading

	PORT = 64321

	class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
		def do_GET(self):
			self.send_response(200)
			self.send_header('Content-type',"text/javascript")
			self.end_headers()
			jsf = None
			with open(join(pages_test_root,"html5-patch.js")) as f:
				jsf = f.read()
			self.wfile.write(jsf)

	class TestServer(SocketServer.TCPServer):
	    allow_reuse_address = True
    
   	httpd = TestServer(("localhost", PORT), Handler)
	httpd_thread = threading.Thread(target=httpd.serve_forever)
	httpd_thread.setDaemon(True)
	httpd_thread.start()

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","js","html5.js"))
	h5size = getsize(join(pages_test_root,"html5-patch.js"))
	disclsize = getsize(join(pages_test_root,"lead-disclaimer.js"))

	assert getsize(join(pages_test_root,"output","js","html5.js")) == h5size # disclsize

	#httpd_thread.stop()

