import sys,site

from os.path import dirname, join
pages_test_root = dirname(__file__)
setattr(site,"PROJECT_DIR",join(pages_test_root,"web"))

def test_populate():
	from webpages import apply_site_dirs
	from webpages.config import SiteConfig
	from webpages.populate import populate, save_expander
	from webpages.base import ObjectLike
	
	# assert check_filters(base_dir, "dir1", "dir2", dir2_stats, filters=(only_directories,)) is True
	
	apply_site_dirs("")

	config = SiteConfig(ObjectLike({
		"dest": join(pages_test_root,"output")		
	}))

	populate(save_expander,config)
