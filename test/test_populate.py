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
	assert not exists(join(pages_test_root,"output","desktop","mymodule"))
	assert not exists(join(pages_test_root,"output","pocket","mymodule"))
	assert not exists(join(pages_test_root,"output","tablet","mymodule"))
	
	
#TODO try making all types of FileExpander
#TODO test presence of path, urlpath, outpath
#TODO test permlink, path overrides

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
	h5size = getsize(join(pages_test_root,"html5-patch.js"))
	disclsize = getsize(join(pages_test_root,"lead-disclaimer.js"))
	fofsize = getsize(join(pages_test_root,"fourofour.html"))

	assert exists(join(pages_test_root,"output","js","html5.js"))
	assert getsize(join(pages_test_root,"output","js","html5.js")) == h5size # disclsize
	assert exists(join(pages_test_root,"output","html5.js"))
	assert getsize(join(pages_test_root,"output","html5.js")) == h5size
	assert exists(join(pages_test_root,"output","js","html5-2.js"))
	assert getsize(join(pages_test_root,"output","js","html5-2.js")) == h5size
	assert exists(join(pages_test_root,"output","404","index.html"))
	assert getsize(join(pages_test_root,"output","404","index.html")) == fofsize

	#httpd_thread.stop()

def test_populate_html_expansion():
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander
	
	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,"w4"))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
	})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","desktop","about","index.html"))
	assert exists(join(pages_test_root,"output","desktop","301.html"))
	assert exists(join(pages_test_root,"output","desktop","404.html"))
	assert exists(join(pages_test_root,"output","desktop","with-ext.html"))

def test_populate_scss():
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander

	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,"w5"))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
	})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","desktop","css","test.css"))

def test_populate_parts():
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander

	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,"w6"))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
	})

	populate(save_expander,config)

	from BeautifulSoup import BeautifulSoup
	assert exists(join(pages_test_root,"output","desktop","index.html"))
	with open(join(pages_test_root,"output","desktop","index.html")) as f:
	    index_html = f.read()
	soup = BeautifulSoup(index_html)

	assert soup("article",id="a1")[0].string.strip() == "myarticle"
	assert soup("article",id="a4")[0].string.strip() == "myarticle"
	assert soup("aside",id="a2")[0].string.strip() == "myaside"
	assert soup("nav",id="n1")[0].string.strip() == "nav1"
	# assert soup("section",id="s1")[0].contents[1].string.strip() == "<h1>header1</h1>"
	
	assert soup("form",id="f1")[0].button.string.strip() == "submit 1"
	assert soup("form",id="f2")[0].button.string.strip() == "submit 1"

def test_populate_exclude_published():
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander

	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,"w6"))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
	})

	populate(save_expander,config)

	assert not exists(join(pages_test_root,"output","desktop","not-published","index.html"))
	assert not exists(join(pages_test_root,"output","desktop","css","unpublished-test.css"))
	assert not exists(join(pages_test_root,"output","desktop","js","unpublished.js"))
	assert not exists(join(pages_test_root,"output","desktop","internal","page1","index.html"))
	
	#TODO fix base_path for filter calls in fs module
	#assert not exists(join(pages_test_root,"output","desktop","test","test","internal2","page2","index.html"))
	
	#TODO file ext, paths

def test_populate_assets():
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander
	
	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,"w7"))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
		"browser": "desktop",		
	})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","index.html"))
	assert exists(join(pages_test_root,"output","public","js","html5.js"))
	assert exists(join(pages_test_root,"output","public","css","test.css"))

