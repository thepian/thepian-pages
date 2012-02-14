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

