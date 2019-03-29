import collections

class Cache:
    enable = None
    cacheSize = None
    cacheData = None

    def __init__(self , config):
        self.enable = config['enable']
        self.cacheSize = config['size']
        self.cacheData = collections.OrderedDict()
    
    def canCache(self , request):
        if self.enable:
            lines = request.splitlines()
            for line in lines:
                if line.find("Pragma: no-cache") is not -1:
                    return False
            return True
        else:
            return False

    def saveToCache(self , request , data):
        if request in self.cacheData:
            self.cacheData[request] += data
            return 
        if len(self.cacheData) >= self.cacheSize:
            self.cacheData.popitem(last=False)
        self.cacheData[request] = data

    
