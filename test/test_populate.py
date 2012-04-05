from __future__ import with_statement
import sys,site,re
import shutil

from os.path import dirname, join, exists, getsize
pages_test_root = dirname(__file__)

def get_soup(*path):
	from bs4 import BeautifulSoup
	assert exists(join(*path))
	index_html = None
	with open(join(*path),"rb") as f:
	    index_html = f.read().decode("utf-8")
	return BeautifulSoup(index_html,"html5lib")

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

def eval_config_script(script):
	lines = script.strip().split("\n")
	config = {}
	def declare(key,val):
		config[key] = val
	for line in lines:
		eval(line.strip(";"), { "declare": declare })
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

	soup = get_soup(pages_test_root,"output","desktop","partless","index.html")
	assert soup.head == soup.find(id="h")
	assert soup.body == soup.find(id="b")
	assert soup.body.string.strip() == "body comes here"
	
	soup = get_soup(pages_test_root,"output","desktop","bodypart","index.html")
	assert soup.html == soup.find(attrs={ "class": "no-js desktop" })
	assert soup.html["class"].split() == [u"no-js",u"desktop"]
	assert soup.head == soup.find(id="h")
	assert soup.body == soup.find(id="b")
	assert soup.body.string.strip() == "in a body tag"
	soup_tablet = get_soup(pages_test_root,"output","tablet","bodypart","index.html")
	assert soup_tablet.html["class"].split() == [u"no-js",u"tablet"]
	soup_pocket = get_soup(pages_test_root,"output","pocket","bodypart","index.html")
	assert soup_pocket.html["class"].split() == [u"no-js",u"pocket"]

	soup = get_soup(pages_test_root,"output","desktop","mixinbody","index.html")
	assert soup.html == soup.find(attrs={ "class": "no-js desktop" })
	assert soup.head == soup.find(id="h")
	assert soup.body == soup.find(id="b")
	#TODO assert soup.find(attrs={ "src":"extra.js" })
	
	soup = get_soup(pages_test_root,"output","desktop","articlepart","index.html")
	assert soup.html == soup.find(attrs={ "class": "no-js desktop" })
	assert soup.head == soup.find(id="h")
	assert soup.body == soup.find(id="b")
	assert soup.article == soup.find(id="a")
	assert soup.article.h2.string.strip() == "Article"
	assert soup.article.p.string.strip() == "here is the article"

	pg_size = getsize(join(pages_test_root,"w1","assets","horizontal-rule.gif"))
	assert getsize(join(pages_test_root,"output","desktop","assets","horizontal-rule.gif")) == pg_size
	pg_size = getsize(join(pages_test_root,"w1","assets","input-background.png"))
	assert getsize(join(pages_test_root,"output","desktop","assets","input-background.png")) == pg_size
	pg_size = getsize(join(pages_test_root,"w1","assets","page-background.jpg"))
	assert getsize(join(pages_test_root,"output","desktop","assets","page-background.jpg")) == pg_size
	# assert False
	
	
#TODO expand parent document for XML
#TODO try making all types of FileExpander
#TODO test presence of path, urlpath, outpath
#TODO test permlink, path overrides
#TODO test that common file types work
#TODO config default, log charset encode errors rather than fail, test no failure

def test_populate_desktop_browser():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w1",**{"browser": "desktop"})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","js","html5.js"))
	h5size = getsize(join(pages_test_root,"resources","html5-patch.js"))
	disclsize = getsize(join(pages_test_root,"resources","lead-disclaimer.js"))

	assert getsize(join(pages_test_root,"output","js","html5.js")) == disclsize + h5size

	soup = get_soup(pages_test_root,"output","bodypart","index.html")
	assert soup.html == soup.find(attrs={ "class": "no-js desktop" })

def test_populate_tablet_browser():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w1",**{"browser": "tablet"})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","js","html5.js"))
	h5size = getsize(join(pages_test_root,"resources","html5-patch.js"))
	disclsize = getsize(join(pages_test_root,"resources","lead-disclaimer.js"))

	assert getsize(join(pages_test_root,"output","js","html5.js")) == disclsize + h5size

	soup = get_soup(pages_test_root,"output","bodypart","index.html")
	assert soup.html == soup.find(attrs={ "class": "no-js tablet" })

def test_populate_pocket_browser():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w1",**{"browser": "pocket"})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","js","html5.js"))
	h5size = getsize(join(pages_test_root,"resources","html5-patch.js"))
	disclsize = getsize(join(pages_test_root,"resources","lead-disclaimer.js"))

	assert getsize(join(pages_test_root,"output","js","html5.js")) == disclsize + h5size

	soup = get_soup(pages_test_root,"output","bodypart","index.html")
	assert soup.html == soup.find(attrs={ "class": "no-js pocket" })

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
	soup404 = get_soup(pages_test_root,"output","404","index.html")
	assert len(soup404.body.string.strip())+1 == fofsize

	assert exists(join(pages_test_root,"output","js","test.js"))
	assert getsize(join(pages_test_root,"output","js","test.js")) == 0
	assert exists(join(pages_test_root,"output","js","test-fetched.js"))
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

	soup = get_soup(pages_test_root,"output","desktop","about","index.html")
	assert soup.head.find("meta",attrs={ "name":"author" })["content"] == "Henrik Vendelbo"
	assert soup.head.find("meta",attrs={ "name":"description" })["content"] == "Information about the Product"
	assert soup.head.find("title").string.strip() == "About the Product"
	# assert soup.head.find("meta",attrs={ "name":"charset" })["content"] == "utf-8"

	soup = get_soup(pages_test_root,"output","desktop","iso-encoded","index.html")
	# assert soup.head.find("meta",attrs={ "name":"charset" })["content"] == "iso-8859-1"

	soup = get_soup(pages_test_root,"output","desktop","index.html")
	assert soup.script["src"] == "head.js"
	assert soup.body.contents[0].string.strip() == "index page"

	#TODO test that derived parts head is mixed in
	# assert False


def _assert_content_re(path,pattern):
	import re
	assert exists(path)
	with open(path,"r") as f:
		c = f.read()
		# print "content:", c, path, pattern
		assert re.search(pattern,c)

def test_populate_scss():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w5")

	populate(save_expander,config)
	_assert_content_re(join(pages_test_root,"output","desktop","css","test.css"),r"\.test\{")
	_assert_content_re(join(pages_test_root,"output","tablet","css","test.css"),r"\.test\{")
	_assert_content_re(join(pages_test_root,"output","pocket","css","test.css"),r"\.test2\{")

	_assert_content_re(join(pages_test_root,"output","desktop","css","desktop.css"),r"\.desktop2\{")
	_assert_content_re(join(pages_test_root,"output","tablet","css","desktop.css"),r"\.desktop\{")
	_assert_content_re(join(pages_test_root,"output","pocket","css","desktop.css"),r"\.desktop\{")

def test_populate_parts():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w6")

	populate(save_expander,config)

	soup = get_soup(pages_test_root,"output","desktop","index.html")

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

	soup = get_soup(pages_test_root,"output","index.html")

	assert soup("article",id="a1")[0].contents[0].strip() == "myarticle"
	assert soup("article",id="a1")[0].contents[1].string.strip() == "section one"
	assert soup("script")[2]["type"] == "application/config"
	assert soup("script")[2].string.strip() == """\
declare("a1",{"charset": "utf-8", "layouter": "deck", "stage": ["upper", "lower", "sides"]});
declare("s1",{"charset": "utf-8", "laidout": "card"});
declare("a2",{"charset": "utf-8", "layouter": "deck"});"""
	# assert False
	#TODO document properties if stateful

def test_populate_areas():
	from webpages.populate import populate, save_expander
	
	populate(save_expander,prep_site_config("w9",**{"browser": "desktop"}))
	assert exists(join(pages_test_root,"output","index.html"))

	soup = get_soup(join(pages_test_root,"output","index.html"))
	a1 = soup.find(id="a1")
	a2 = soup.find(id="a2")
	config = eval_config_script(soup("script")[2].string)

	# The elements with parts content and matter
	assert a1.contents[0].strip() == "top bit"
	assert a1.contents[1].string.strip() == "section one"
	assert a1.contents[3].string.strip() == "section two"
	assert a1["class"].split() == [u"splash-area-inactive", u"upper-area-inactive", u"lower-area-inactive"]
	assert soup.find("section",id="s1")["class"].split() == [u"in-splash-area", u"in-splash-order-0", u"in-upper-area", u"in-upper-order-0", u"in-upper-order-last"]
	assert soup.find("section",id="s2")["class"].split() == [u"in-splash-area", u"in-splash-order-1", u"in-lower-area", u"in-lower-order-0", u"in-lower-order-last", u"in-splash-order-last"]

	assert config["a1"] == {"area-names": ["splash","upper", "lower"], "charset": "utf-8", "layouter": "area-stage"}
	assert config["s2"] == {"area-names": ["splash","lower"], "charset": "utf-8", "laidout": "area-member"}
	assert config["s1"] == {"area-names": ["splash","upper"], "charset": "utf-8", "laidout": "area-member"}

	# The elements without parts, simply inline in HTML
	assert soup.find(id="a2")

	assert config["s4"] == {"area-names": ["second"], "laidout": "area-member"}
	assert config["s3"] == {"area-names": ["first"], "laidout": "area-member"}
	assert config["a2"] == {"area-names": ["first", "second"], "layouter": "area-stage"}
	# assert False
	#TODO document properties if stateful

def test_populate_trackers():
	from webpages.populate import populate, save_expander
	
	config = prep_site_config("w10",**{"browser": "desktop"})

	populate(save_expander,config)
	assert exists(join(pages_test_root,"output","index.html"))

	soup = get_soup(pages_test_root,"output","index.html")

	# print soup.find_all(attrs={ "tracker-parent":re.compile(r".*") })

	assert soup.find("article",id="a1").contents[0].strip() == "top bit"
	assert soup.find("section",id="s1").string.strip() == "section one"
	trackerTwo = soup.article.find_all("div")[0]
	sectionTwo = soup.article("section")[1]
	trackerThree = soup.article.find_all("div")[1]
	sectionThree = soup.article("section")[2]
	trackerFour = soup.article.find(id="other-trackers").div
	sectionFour = soup.article("section")[3]
	s2id = sectionTwo["id"].encode("utf-8")
	s2trk = trackerTwo["id"].encode("utf-8")
	s3id = sectionThree["id"].encode("utf-8")
	s3trk = trackerThree["id"].encode("utf-8")
	s4id = sectionFour["id"].encode("utf-8")
	s4trk = trackerFour["id"].encode("utf-8")
	assert s2id is not None
	assert s3id is not None

	config = eval_config_script(soup("script")[2].string)
	assert config["a1"] == {"area-names": ["upper", "lower"], "charset": "utf-8", "layouter": "area-stage"}
	assert config["s1"] == {"area-names": ["upper"], "charset": "utf-8", "laidout": "area-member"}
	assert config[s2id] == {"driven-by": s2trk, "tracker-driven": ["left", "top"]}
	assert config[s3id] == {"driven-by": s3trk, "tracker-driven": ["left", "top"], 
		# "tracker-parent": "other-trackers",
		"area-names": ["lower"], 
		#"charset": "utf-8", 
		"laidout": "area-member" }

	# assert soup("section",id="s2")[0]["class"] == "in-lower-area in-lower-order-0"
	assert trackerTwo["class"].split() == [u"tracker", u"section-tracker"]
	assert trackerThree["class"].split() == [u"tracker", u"section-tracker", u"in-lower-area",u"in-lower-order-0"]

	# print sectionFour, config[s4id]
	assert "tracker-parent" not in trackerFour
	assert config[s4id] == {"driven-by": s4trk, "tracker-driven": ["left", "top"], 
		"tracker-parent": "other-trackers",
		"area-names": ["upper"], 
		"laidout": "area-member" }

	# assert False
	#TODO test tracker-parent currectly used
	#TODO test tracker-driven attribute removed
	#TODO document properties if stateful

