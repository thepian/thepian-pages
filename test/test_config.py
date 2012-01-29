import sys,site
from os.path import dirname, join
pages_test_root = dirname(__file__)
setattr(site,"PROJECT_DIR",join(pages_test_root,"web"))

from webpages import apply_site_dirs, server_options_parser, populate_options_parser
from webpages.base import ObjectLike
from webpages.config import SiteConfig

def test_config():
	apply_site_dirs("")
	options = ObjectLike({
		"source": None,
		"dest": None,
		"fork": True,
		"appcache": False,
		"debug": False,
		"pygments": False
	})
	config = SiteConfig(options)
	#print >>sys.stderr, config["source"]
	assert config["source"] == join(pages_test_root,"web")
	assert config["appcache"] == False
	assert config["debug"] == False

	options = ObjectLike({
		"source": None,
		"dest": None,
		"fork": True,
		"appcache": True,
		"debug": True,
		"pygments": False
	})
	config = SiteConfig(options)
	#print >>sys.stderr, config["source"]
	assert config["source"] == join(pages_test_root,"web")
	assert config["appcache"] == True
	assert config["debug"] == True

def test_source():
	apply_site_dirs("")
	options = ObjectLike({
		"source": "abc",
		"dest": None,
		"fork": True,
		"appcache": False,
		"debug": False,
		"pygments": False
	})
	config = SiteConfig(options)
	#print >>sys.stderr, config["source"]
	assert config["source"] == join(pages_test_root,"web","abc")

	options = ObjectLike({
		"source": "/",
		"dest": None,
		"fork": True,
		"appcache": False,
		"debug": False,
		"pygments": False
	})
	config = SiteConfig(options)
	assert config["source"] == "/"

def test_output():
	apply_site_dirs("")
	options = ObjectLike({
		"source": None,
		"dest": "_site",
		"fork": True,
		"appcache": False,
		"debug": False,
		"pygments": False
	})
	config = SiteConfig(options)
	assert config["output"] == join(pages_test_root,"web","_site")

	options = ObjectLike({
		"source": None,
		"dest": "../output",
		"fork": True,
		"appcache": False,
		"debug": False,
		"pygments": False
	})
	config = SiteConfig(options)
	assert config["output"] == join(pages_test_root,"output")

def test_exclude():

	apply_site_dirs("")
	options = ObjectLike({
		"source": None,
		"dest": "_site",
		"fork": True,
		"appcache": False,
		"debug": False,
		"pygments": False
	})
	config = SiteConfig(options)
	from fs import filters, listdir
	base_filters = [
		config.exclude_filter(),
		filters.no_hidden,filters.no_system]

	r = listdir(site.SITE_DIR,recursed=True,filters=base_filters)
	#print >>sys.stderr, r
	assert r == ["index.md","unicode.md","js/init.js"]

def test_server_options():
	options, r = server_options_parser.parse_args(args=["--nofork"])
	config = SiteConfig(options)
	assert config["port"] == 4444

	options, r = server_options_parser.parse_args(args=["--port=555"])
	config = SiteConfig(options)
	assert config["port"] == 555

def test_populate_options():
	options, r = populate_options_parser.parse_args(args=["--dest=./abc"])
	config = SiteConfig(options)

