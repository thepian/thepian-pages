from os.path import exists,join

class ApplicationConfig(object):

    defaults = {
        "section-content-class": "section-content",
    }
    
    def __init__(self):
        self.config = {}

        import site, yaml
        with open(join(site.PROJECT_DIR,"_config.yml")) as f:
            self.config = yaml.load(f.read())

    def __getitem__(self,key):
        if key in self.config:
            return self.config[key]
        return self.defaults[key]
        
    def describe_area_matter(self,name):
        matter = {}

        import site, yaml, os.path
        path = join(site.CONF_DIR,"%s.area.yml" % name)
        if os.path.exists(path):
            with open(path) as f:
                matter = yaml.load(f.read())

        return matter

