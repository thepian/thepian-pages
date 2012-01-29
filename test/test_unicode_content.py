import sys,site
from os.path import dirname, join, abspath

pages_test_root = dirname(__file__)
setattr(site,"PROJECT_DIR",join(pages_test_root,"web"))

from webpages import apply_site_dirs, server_options_parser, populate_options_parser
from webpages.base import ObjectLike
from webpages.config import SiteConfig
from webpages.populate import FileExpander

"""
encoding: .. specify the encoding of the content part and the destination encoding if not overridden if __name__ == '__main__':
	derived documents
internally always use utf-8	
"""
def test_split_matter_content():
	apply_site_dirs("")
	options, r = server_options_parser.parse_args(args=["--nofork"])
	config = SiteConfig(options)

	header = {
		"Content-Type": "text/html",
	}
	content = None
	with open(abspath(join(site.PROJECT_DIR,"unicode.md")), "rb") as f:
		content = f.read()

	#expander = FileExpander(site.PROJECT_DIR,"unicode.md",config=config)
	#self.header,self.content = self._get_matter_and_content(relpath,header)
	config.split_matter_and_utf8_content(content,header)	

def test_handler_content():
	pass

def test_double_dashes():
	apply_site_dirs("")
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
