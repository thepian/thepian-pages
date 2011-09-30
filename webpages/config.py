from __future__ import with_statement

import yaml, re

from os.path import exists,join

class SiteConfig(object):

    defaults = {
        "domain": "localhost",
        "section-content-class": "section-content",
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
            matter = yaml.load(parts[1])
            for key in header.keys():
                matter[key] = header[key]
            encoding = 'utf-8'
            if 'encoding' in matter:
                encoding = matter['encoding']
            #print "parts", parts
            return matter, self.expand_site_variables(parts[2].decode(encoding))

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

def load_html(path,parser):
    doc = None
    matter = None

    with codecs.open(path,"r","utf-8") as f:
        s = f.read()
        parts = s.split("---")
        if len(parts) == 3 and len(parts[0]) == 0:
            s = parts[-1]
        if len(s) == 0:
            s = u'<body></body>'
        doc = etree.parse(StringIO(s),parser)
        if len(parts) > 1:
            matter = yaml.load(parts[1])

    return doc,matter
    
