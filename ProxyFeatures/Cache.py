import collections
from Parsers.HttpParser import HttpParser

class Cache:
    enable = None
    cacheSize = None
    cacheData = None

    def __init__(self , config):
        self.enable = config['enable']
        self.cacheSize = config['size']
        self.cacheData = collections.OrderedDict()
    
    def canCache(self , request , log):
        if self.enable:
            lines = request.splitlines()
            for line in lines:
                if line.find("Pragma: no-cache") is not -1:
                    log.addResponceCannotCache()
                    return False
            log.addResponceCanCache()
            return True
        else:
            return False

    def saveToCache(self , request , data , log):
        if request in self.cacheData:
            self.cacheData[request] += data
            return 
        if len(self.cacheData) >= self.cacheSize:
            self.cacheData.popitem(last=False)
        log.addResponceToCacheData(HttpParser.getResponseHeader(data).decode())
        self.cacheData[request] = data

    def doesRequestCached(self , request , log):
        if self.enable:
            log.addSearchInCache()
            if request in self.cacheData:
                log.addFindRequestInCache()
                if self.isCacheDataExpire(HttpParser.getResponseHeader(self.cacheData[request]).decode()):
                    return False
                return True
            else:
                log.addNotFindRequestInCache()
                return False
        else:
            return False

    def getRequestData(self , request , log):
        data = self.cacheData.pop(request)
        self.cacheData[request] = data
        log.addProxyCachedDataSentResponse(HttpParser.getResponseHeader(data).decode())
        return data

    def isCacheDataExpire(self , request):
        lines = request.splitlines()
        for line in lines:
            if line.find("Expires:") is not -1:
                time = line[9:-4]

        return False
