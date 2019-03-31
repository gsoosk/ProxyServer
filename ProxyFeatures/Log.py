from datetime import datetime
from Parsers.JsonParser import JsonParser

def writeToFile(originalFunction):
    def new_function(*args, **kwargs):
        logObject = args[0]
        if not logObject.enable:
            return

        originalFunction(*args, **kwargs)
        newLog = logObject.logs[-1]

        file = open(logObject.file, 'a+')
        file.write(newLog)
        if printInTerminal:
            if not newLog is "":
                print(newLog , end="")
        

    return new_function

class Log:
    enable = None
    file = None
    logs = []
    def __init__(self, config):
        logConfigFile = open("./Config/logConfig.json","r")
        self.logConfig = JsonParser(logConfigFile.read()).__dict__
        global printInTerminal
        printInTerminal = self.logConfig["printInTerminal"]
        self.enable = config['enable']
        self.file = config['logFile']

    @staticmethod
    def getTime():
        currentDate = datetime.now()
        return currentDate.strftime("[%d/%b/%Y:%H:%M:%S] ")


    @writeToFile
    def addLaunchProxy(self):
        if not self.logConfig["addLaunchProxy"]:
            self.logs.append("")
            return
        newLog = "=================================\n"
        newLog += Log.getTime() + "Proxy launched\n"
        self.logs.append(newLog)

    @writeToFile
    def addCreateSocket(self):
        if not self.logConfig["addCreateSocket"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Creating server socket\n")

    @writeToFile
    def addBindingSocket(self, port):
        if not self.logConfig["addBindingSocket"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Binding socket to port " + str(port) + "\n")

    @writeToFile
    def addListeningForIncomings(self):
        if not self.logConfig["addListeningForIncomings"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Listening for incoming requests\n")

    @writeToFile
    def addWaitForClientsToAccept(self):
        if not self.logConfig["addWaitForClientsToAccept"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Wait for clients to accept\n")

    @writeToFile
    def addAcceptClient(self, client):
        if not self.logConfig["addAcceptClient"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Accepted a request from client {}!".format(client) + "\n")

    @writeToFile
    def addRequestClientHeaders(self, request):
        if not self.logConfig["addRequestClientHeaders"]:
            self.logs.append("")
            return
        newLog = Log.getTime() + "Client sent request to proxy with headers:\n"
        newLog += "\n----------------------------------\n"
        newLog += request
        newLog += "----------------------------------\n"
        self.logs.append(newLog)

    @writeToFile
    def addOpeningConnection(self, host, port):
        if not self.logConfig["addOpeningConnection"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + 'Proxy opening connection to server ' + str(host) + ' : ' + str(port) +"\n")

    @writeToFile
    def addProxySentReq(self, request):
        if not self.logConfig["addProxySentReq"]:
            self.logs.append("")
            return
        newLog = Log.getTime() + 'Proxy sent request to server with headers:'
        newLog += "\n..................................\n"
        newLog += request
        newLog += "..................................\n"
        self.logs.append(newLog)

    @writeToFile
    def addTimeoutToConnectServer(self, url):
        if not self.logConfig["addTimeoutToConnectServer"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Time out in request from {} ...".format(url) +"\n")

    @writeToFile
    def addServerSentResponse(self, request):
        if not self.logConfig["addServerSentResponse"]:
            self.logs.append("")
            return
        newLog = Log.getTime() + 'Server sent response to proxy with headers:'
        newLog += "\n++++++++++++++++++++++++++++++++\n"
        newLog += request
        newLog += "++++++++++++++++++++++++++++++++\n"
        self.logs.append(newLog)

    @writeToFile
    def addProxySentResponse(self, request):
        if not self.logConfig["addProxySentResponse"]:
            self.logs.append("")
            return
        newLog = Log.getTime() + 'Proxy sent response to client with headers:'
        newLog += "\n++++++++++++++++++++++++++++++++\n"
        newLog += request
        newLog += "++++++++++++++++++++++++++++++++\n"
        self.logs.append(newLog)

    @writeToFile
    def addRestricted(self):
        if not self.logConfig["addRestricted"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + 'User Restricted from website.\n')

    @writeToFile
    def addAdminNotified(self):
        if not self.logConfig["addAdminNotified"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + 'Admin notified with email\n')

    @writeToFile
    def addUserIsNotInProfiles(self, IP):
        if not self.logConfig["addUserIsNotInProfiles"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + 'User {} is not in proxy profiles and will restrict by proxy'.format(IP) +"\n")

    @writeToFile
    def addUserUsedDataIsExtended(self, IP):
        if not self.logConfig["addUserUsedDataIsExtended"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + 'User {} used data is over and will restrict by proxy'.format(IP) +"\n")

    @writeToFile
    def addMailLog(self, msg):
        if not self.logConfig["addMailLog"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + 'Mail ::: ' +msg + "\n")

    @writeToFile
    def addSearchInCache(self):
        if not self.logConfig["addSearchInCache"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Proxy search cached data for client request\n")
        
    @writeToFile
    def addFindRequestInCache(self):
        if not self.logConfig["addFindRequestInCache"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Proxy found client request in cache data\n")

    @writeToFile
    def addNotFindRequestInCache(self):
        if not self.logConfig["addNotFindRequestInCache"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Proxy couldn't find client request in cache data\n")

    @writeToFile
    def addProxyCachedDataSentResponse(self, request):
        if not self.logConfig["addProxyCachedDataSentResponse"]:
            self.logs.append("")
            return
        newLog = Log.getTime() + 'Proxy sent response from its cache data to client with headers:'
        newLog += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        newLog += request
        newLog += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        self.logs.append(newLog)

    @writeToFile
    def addResponceCannotCache(self):
        if not self.logConfig["addResponceCannotCache"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Proxy can not cache the responce of this request\n")
    
    @writeToFile
    def addResponceCanCache(self):
        if not self.logConfig["addResponceCanCache"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Proxy can cache the responce of this request\n")
    
    @writeToFile
    def addResponceToCacheData(self, request):
        if not self.logConfig["addResponceToCacheData"]:
            self.logs.append("")
            return
        newLog = Log.getTime() + 'Proxy cached response of server with headers:'
        newLog += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        newLog += request
        newLog += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        self.logs.append(newLog)

    @writeToFile
    def addCacheDataExpire(self):
        if not self.logConfig["addCacheDataExpire"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Proxy cache data expired\n")
    
    @writeToFile
    def addCacheDataNotExpire(self):
        if not self.logConfig["addCacheDataNotExpire"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Proxy cache data not expired\n")
    
    @writeToFile
    def addNeedCacheModification(self):
        if not self.logConfig["addNeedCacheModification"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Client request need cache modification\n")

    @writeToFile
    def addResponceShouldModify(self):
        if not self.logConfig["addResponceShouldModify"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Cache should modify its data\n")

    @writeToFile
    def addResponceShouldNotModify(self):
        if not self.logConfig["addResponceShouldNotModify"]:
            self.logs.append("")
            return
        self.logs.append(Log.getTime() + "Cache doesn't need to modify its data\n")
