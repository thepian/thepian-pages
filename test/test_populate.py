from __future__ import with_statement
import sys,site
import shutil

from os.path import dirname, join, exists, getsize
pages_test_root = dirname(__file__)

def get_soup(path):
	from BeautifulSoup import BeautifulSoup
	assert exists(path)
	index_html = None
	with open(path) as f:
	    index_html = f.read()
	return BeautifulSoup(index_html)

def prep_site_config(rel_path,browser=None):
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	
	shutil.rmtree(join(pages_test_root,"output"), ignore_errors=True)

	apply_site_dirs("",force_project_path=join(pages_test_root,rel_path))

	config = SiteConfig({
		"dest": join(pages_test_root,"output"),
		"browser": browser,		
	})

	return config

def test_populate():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w1")

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
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w1",**{"browser": "desktop"})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","js","html5.js"))
	h5size = getsize(join(pages_test_root,"resources","html5-patch.js"))
	disclsize = getsize(join(pages_test_root,"resources","lead-disclaimer.js"))

	assert getsize(join(pages_test_root,"output","js","html5.js")) == disclsize + h5size

def test_populate_jquery():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w2")

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","desktop","js","jquery-1.5.1.js"))
	jqsize = getsize(join(pages_test_root,"w2","_libs","jquery-1.5.1.js"))
	assert getsize(join(pages_test_root,"output","desktop","js","jquery-1.5.1.js")) == jqsize
	assert getsize(join(pages_test_root,"output","desktop","js","jquery.js")) == jqsize
	jqminsize = getsize(join(pages_test_root,"w2","_libs","jquery-1.5.1.min.js"))
	assert getsize(join(pages_test_root,"output","desktop","js","jquery-1.5.1.min.js")) == jqminsize
	assert getsize(join(pages_test_root,"output","desktop","js","jquery.min.js")) == jqminsize

def test_populate_http_fetch():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w3",**{"browser": "desktop"})

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
			with open(join(pages_test_root,"resources","html5-patch.js")) as f:
				jsf = f.read()
			self.wfile.write(jsf)

	class TestServer(SocketServer.TCPServer):
	    allow_reuse_address = True
    
   	httpd = TestServer(("localhost", PORT), Handler)
	httpd_thread = threading.Thread(target=httpd.serve_forever)
	httpd_thread.setDaemon(True)
	httpd_thread.start()

	populate(save_expander,config)
	h5size = getsize(join(pages_test_root,"resources","html5-patch.js"))
	disclsize = getsize(join(pages_test_root,"resources","lead-disclaimer.js"))
	fofsize = getsize(join(pages_test_root,"resources","fourofour.html"))

	assert exists(join(pages_test_root,"output","js","html5.js"))
	assert getsize(join(pages_test_root,"output","js","html5.js")) == h5size # disclsize
	assert exists(join(pages_test_root,"output","html5.js"))
	assert getsize(join(pages_test_root,"output","html5.js")) == h5size
	assert exists(join(pages_test_root,"output","js","html5-2.js"))
	assert getsize(join(pages_test_root,"output","js","html5-2.js")) == h5size
	assert exists(join(pages_test_root,"output","404","index.html"))
	assert getsize(join(pages_test_root,"output","404","index.html")) == fofsize

	assert exists(join(pages_test_root,"output","js","test.js"))
	assert getsize(join(pages_test_root,"output","js","test.js")) == 0

	#httpd_thread.stop()

def test_populate_html_expansion():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w4")

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","desktop","about","index.html"))
	assert exists(join(pages_test_root,"output","desktop","301.html"))
	assert exists(join(pages_test_root,"output","desktop","404.html"))
	assert exists(join(pages_test_root,"output","desktop","with-ext.html"))

def test_populate_scss():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w5")

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","desktop","css","test.css"))

def test_populate_parts():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w6")

	populate(save_expander,config)

	soup = get_soup(join(pages_test_root,"output","desktop","index.html"))

	assert soup("article",id="a1")[0].contents[0].strip() == "myarticle"
	assert soup("article",id="a1")[0].contents[1].string.strip() == "section two"
	assert soup("article",id="a4")[0].contents[0].strip() == "myarticle"
	assert soup("article",id="a4")[0].contents[1].string.strip() == "section two"
	assert soup("aside",id="a2")[0].string.strip() == "myaside"
	assert soup("nav",id="n1")[0].string.strip() == "nav1"
	# assert soup("section",id="s1")[0].contents[1].string.strip() == "<h1>header1</h1>"
	
	assert soup("form",id="f1")[0].button.string.strip() == "submit 1"
	assert soup("form",id="f2")[0].button.string.strip() == "submit 1"
	
	assert soup("script",id="conf")[0].string.strip() == 'window.myconf = { "a":"a"};'
	assert "inline-src" not in soup("script",id="conf")[0]

def test_populate_exclude_published():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w6")

	populate(save_expander,config)

	assert not exists(join(pages_test_root,"output","desktop","not-published","index.html"))
	assert not exists(join(pages_test_root,"output","desktop","css","unpublished-test.css"))
	assert not exists(join(pages_test_root,"output","desktop","js","unpublished.js"))
	assert not exists(join(pages_test_root,"output","desktop","internal","page1","index.html"))
	
	#TODO fix base_path for filter calls in fs module
	#assert not exists(join(pages_test_root,"output","desktop","test","test","internal2","page2","index.html"))
	
	#TODO file ext, paths

def test_populate_assets():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w7",**{"browser": "desktop"})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","index.html"))
	assert exists(join(pages_test_root,"output","public","js","html5.js"))
	assert exists(join(pages_test_root,"output","public","css","test.css"))

def test_populate_stateful():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w8",**{"browser": "desktop"})

	populate(save_expander,config)

	soup = get_soup(join(pages_test_root,"output","index.html"))

	assert soup("article",id="a1")[0].contents[0].strip() == "myarticle"
	assert soup("article",id="a1")[0].contents[1].string.strip() == "section one"
	assert soup("script")[2].string.strip() == """\
declare("a1",{"encoding": "utf-8", "layouter": "deck", "stage": ["upper", "lower", "sides"]});
declare("s1",{"encoding": "utf-8", "laidout": "card"});
declare("a2",{"encoding": "utf-8", "layouter": "deck"});"""
	# assert False
	#TODO document properties if stateful

def test_populate_areas():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w9",**{"browser": "desktop"})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","index.html"))

	soup = get_soup(join(pages_test_root,"output","index.html"))

	assert soup("article",id="a1")[0].contents[0].strip() == "top bit"
	assert soup("article",id="a1")[0].contents[1].string.strip() == "section one"
	assert soup("article",id="a1")[0].contents[3].string.strip() == "section two"
	assert soup("script")[2].string.strip() == """\
declare("a1",{"area-names": ["upper", "lower"], "encoding": "utf-8", "layouter": "area-stage"});
declare("s2",{"area-names": ["lower"], "encoding": "utf-8", "laidout": "area-member"});
declare("s1",{"area-names": ["upper"], "encoding": "utf-8", "laidout": "area-member"});"""

	assert soup("article",id="a1")[0]["class"] == "upper-area-inactive lower-area-inactive"
	assert soup("section",id="s1")[0]["class"] == "in-upper-area in-upper-order-0"
	assert soup("section",id="s2")[0]["class"] == "in-lower-area in-lower-order-0"
	# assert False
	#TODO document properties if stateful

