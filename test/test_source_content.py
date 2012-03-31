import sys,site
from os.path import dirname, join, abspath

pages_test_root = dirname(__file__)

from webpages import apply_site_dirs, server_options_parser, populate_options_parser
from webpages.base import ObjectLike
from webpages.config import SiteConfig
from webpages.populate import FileExpander
from webpages.browsers import browsers

"""
encoding: .. specify the encoding of the content part and the destination encoding if not overridden if __name__ == '__main__':
	derived documents
internally always use utf-8	
"""
def test_split_matter_content():
	apply_site_dirs("",force_project_path=join(pages_test_root,"web"))
	options, r = server_options_parser.parse_args(args=["--nofork"])
	config = SiteConfig(options)

	header = {
		"Content-Type": "text/html",
	}
	content = None
	with open(abspath(join(site.PROJECT_DIR,"unicode.md")), "rb") as f:
		content = f.read()

	#expander = FileExpander(site.PROJECT_DIR,"unicode.md",config=config)
	#self.header,self.content,self.fetchContent = self._get_matter_and_content(relpath,header)
	header2,content2 = config.split_matter_and_utf8_content(content,header)	
	assert type(content2) == unicode
	assert "test" in header2
	assert type(header2["test"]) == unicode

def test_handler_content():
	pass

def test_double_dashes():
	apply_site_dirs("",force_project_path=join(pages_test_root,"web"))
	options, r = server_options_parser.parse_args(args=["--nofork"])
	config = SiteConfig(options)

	header = {
		"Content-Type": "text/html",
	}
	content = """---
test: test
---
abc---def
123---456
"""
	expected = """
abc---def
123---456
"""
	header2,content2 = config.split_matter_and_utf8_content(content,header)	
	#print >>sys.stderr, "from:", content2, "to:", expected, "end"
	assert content2 == expected

def notest_fetch_content():

	apply_site_dirs("",force_project_path=join(pages_test_root,"web"))
	config = SiteConfig({})

	basedir = join(pages_test_root,"web")
	header = {
		"Content-Type": "text/javascript",
		"content": ["../resources/html5-patch.js","abc_shim.js"]
	}
	content = browsers[0].fetchContent(header,config,basedir)
	assert type(content) == unicode
