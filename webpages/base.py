class ObjectLike(object):

    def __init__(self,d):
        self.data = d

    def __getitem__(self,key):
        if key not in self.data:
            return None
        return self.data[key]

    def __getattr__(self,key):
        if key not in self.data:
            return None
        return self.data[key]
        
   