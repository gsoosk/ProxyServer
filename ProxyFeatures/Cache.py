import collections
from Parsers.HttpParser import HttpParser
from Utilities.TimeUtilities import TimeUtilities

class Cache:
    enable = None
    cacheSize = None
    cacheData = None

    def __init__(self , config):
        self.enable = config['enable']
        self.cacheSize = config['size']
        self.cacheData = collections.OrderedDict()
    
    def requestCanCache(self , request , log):
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
        key = self.getCacheKey(request)
        if key in self.cacheData:
            self.cacheData[key] += data
            return 
        if len(self.cacheData) >= self.cacheSize:
            self.cacheData.popitem(last=False)
        log.addResponceToCacheData(HttpParser.getResponseHeader(data).decode())
        self.cacheData[key] = data
        print(len(self.cacheData))

    def doesRequestCached(self , request , log):
        key = self.getCacheKey(request)
        if self.enable:
            log.addSearchInCache()
            if key in self.cacheData:
                log.addFindRequestInCache()
                if self.isCacheDataExpire(HttpParser.getResponseHeader(self.cacheData[key]).decode() , log):
                    return False       
                return True
            else:
                log.addNotFindRequestInCache()
                return False
        else:
            return False

    def getRequestData(self , request , log):
        key = self.getCacheKey(request)
        data = self.cacheData.pop(key)
        self.cacheData[key] = data
        log.addProxyCachedDataSentResponse(HttpParser.getResponseHeader(data).decode())
        return data

    def isCacheDataExpire(self , request , log):
        lines = request.splitlines()
        for expireLine in lines:
            if expireLine.find("Expires:") is not -1:
                for modifiedLine in lines:
                    if modifiedLine.find("If-Modified-Since:") is not -1:
                        return False
                time = TimeUtilities.convertToDate(expireLine[9:])
                nowTime = TimeUtilities.nowTime()
                if time < nowTime:
                    log.addCacheDataExpire()
                    return True
        log.addCacheDataNotExpire()
        return False

    def getCacheKey(self , request):
        host = HttpParser.getHostName(request)
        url = HttpParser.getUrl(request.decode())
        return host + url

    def needCacheModification(self , request , log):
        lines = request.splitlines()
        for line in lines:
            if line.find("If-Modified-Since:") is not -1:
                    log.addNeedCacheModification()
                    return True
        return False

    def responseCanModified(self , request , log):
        if self.enable:
            lines = request.splitlines()
            for line in lines:
                if line.find("304 Not Modified") is not -1:
                    log.addResponceShouldNotModify()
                    return False
            log.addResponceShouldModify()
            return True
        else:
            return False

    def deleteOldCacheData(self , request):
        key = self.getCacheKey(request)
        if key in self.cacheData:
            self.cacheData[key] = None