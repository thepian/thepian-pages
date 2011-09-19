from __future__ import with_statement

import yaml

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

    def split_header_and_utf8_content(self,content,header):

        if content[:3] == "---":
            parts = content.split("---")
            matter = yaml.load(parts[1])
            for key in header.keys():
                matter[key] = header[key]
            encoding = 'utf-8'
            if 'encoding' in matter:
                encoding = matter['encoding']
            return matter, parts[2].decode(encoding)

        return header, content
        
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
    
