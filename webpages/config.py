from __future__ import with_statement

import yaml, re, os

from os.path import exists,join,splitext,split

class SiteConfig(object):

    defaults = {
        "domain": "localhost",
        "section-content-class": "section-content",
        "exclude": [],
        "appcache": True,
    }
    
    def __init__(self,options):
        self.config = {}
        self.configRe = {}

        import site, yaml
        with open(join(site.PROJECT_DIR,"_config.yml"),"rb") as f:
            raw = f.read()
            if raw:
                self.config = yaml.load(raw.decode("utf-8"))

        self.config["debug"] = options.debug
        self.config["appcache"] = options.appcache
        if hasattr(options,"pygments"):
            self.config["pygments"] = options.pygments
        self._seedTime()
        self._updateMatching()

    def __getitem__(self,key):
        if key in self.config:
            return self.config[key]
        return self.defaults[key]

    def __setitem__(self,key,value):
        self.config[key] = value
        self.configRe[key] = re.compile(r"{{\s*site.%s\s*}}" % key)

    def get_active_domain(self):
        if self.config["debug"]:
            return self.config["domain"] + ".local"
        else:
            return self.config["domain"]

    active_domain = property(get_active_domain)


    def _seedTime(self):
        try:
            from feed.date import rfc3339
            from feed.date import rfc822
            import time

            now = time.time()
            self.config["time"] = now
            self.config["time_rfc3339"] = rfc3339.timestamp_from_tf(now)        
            self.config["time_rfc822"] = rfc822.timestamp_from_tf(now)        
        except:
            pass

    def _updateMatching(self):
        for k in self.config.iterkeys():
            self.configRe[k] = re.compile(r"{{\s*site.%s\s*}}" % k)

    def expand_site_variables(self,content):
        for k in self.config.iterkeys():
            #print self.configRe[k].findall(content)
            content = self.configRe[k].sub(str(self.config[k]),content)
        return content

    def split_header_and_utf8_content(self,content,header):

        if content[:3] == "---":
            parts = content.split("---")
            matter = yaml.load(parts[1]) or {}
            for key in header.keys():
                matter[key] = header[key]
            encoding = 'utf-8'
            if 'encoding' in matter:
                encoding = matter['encoding']
            rest = u"---".join(parts[2:])
            #print "parts", parts
            return matter, self.expand_site_variables(rest.decode(encoding))

        #print "parts(1)", content
        return header, self.expand_site_variables(content)
        
    def describe_area_matter(self,name):
        matter = {}

        import site, yaml, os.path
        path = join(site.CONF_DIR,"%s.area.yml" % name)
        if os.path.exists(path):
            with open(path) as f:
                matter = yaml.load(f.read())

        return matter

    exclude_extensions = set([
        "py","pyc","pyo",
        "rb",
        "sh","exe",
        "",
    ])

    def exclude_filter(self):
        exclude_list = set(self.config["exclude"]) #TODO convert to path list and pass to listdir
        exclude_extensions = self.exclude_extensions

        def filter(base_path,rel_path,file_name,lstat_info):
            #TODO (base_path,rel_path,file_name,lstat_info)
            ext = splitext(file_name)[1]

            if ext[1:] in exclude_extensions:
                return False

            if file_name[0] == "_":
                return False

            dirs = rel_path.split(os.sep)
            for d in dirs:
                if len(d) and d[0] == "_":
                    return False
            if len(dirs)>0:
                if dirs[0] in exclude_list:
                    return False
            if split(base_path)[1] in exclude_list:
                return False
            
        return filter



