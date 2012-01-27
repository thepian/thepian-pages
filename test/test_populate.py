import sys

from os.path import dirname, join
pages_test_root = dirname(__file__)

def test_populate():
	import site
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander
	from webpages.base import ObjectLike
	
	# assert check_filters(base_dir, "dir1", "dir2", dir2_stats, filters=(only_directories,)) is True

	setattr(site,"PROJECT_DIR",join(pages_test_root,"web"))
	apply_site_dirs("")
	setattr(site,"SCSS_DIR",None)

	config = SiteConfig(ObjectLike({
		"dest": join(pages_test_root,"output")		
	}))

	populate(save_expander,config)
