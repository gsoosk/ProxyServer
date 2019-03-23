from datetime import datetime


def writeToFile(originalFunction):
    def new_function(*args, **kwargs):
        logObject = args[0]
        if not logObject.enable:
            return

        originalFunction(*args, **kwargs)
        newLog = logObject.logs[-1]

        file = open(logObject.file, 'a+')
        file.write(newLog + "\n")

        print(newLog)

    return new_function


class Log:
    enable = None
    file = None
    logs = []
    def __init__(self, config):
        self.enable = config['enable']
        self.file = config['logFile']

    @staticmethod
    def getTime():
        currentDate = datetime.now()
        return currentDate.strftime("[%d/%b/%Y:%H:%M:%S] ")


    @writeToFile
    def addLaunchProxy(self):
        newLog = "=================================\n"
        newLog += Log.getTime() + "Proxy launched"
        self.logs.append(newLog)

    @writeToFile
    def addCreateSocket(self):
        self.logs.append(Log.getTime() + "Creating server socket")

    @writeToFile
    def addBindingSocket(self, port):
        self.logs.append(Log.getTime() + "Binding socket to port " + str(port))

    @writeToFile
    def addListeningForIncomings(self):
        self.logs.append(Log.getTime() + "Listening for incoming requests\n")

    @writeToFile
    def addWaitForClientsToAccept(self):
        self.logs.append(Log.getTime() + "Wait for clients to accept")

    @writeToFile
    def addAcceptClient(self, client):
        self.logs.append(Log.getTime() + "Accepted a request from client {}!".format(client))

    @writeToFile
    def addRequestClientHeaders(self, request):
        newLog = Log.getTime() + "Client sent request to proxy with headers:\n"
        newLog += "\n----------------------------------\n"
        newLog += request
        newLog += "----------------------------------"
        self.logs.append(newLog)

    @writeToFile
    def addOpeningConnection(self, host, port):
        self.logs.append(Log.getTime() + 'Proxy opening connection to server ' + str(host) + ' : ' + str(port))

    @writeToFile
    def addProxySentReq(self, request):
        newLog = Log.getTime() + 'Proxy sent request to server with headers:'
        newLog += "\n..................................\n"
        newLog += request
        newLog += ".................................."
        self.logs.append(newLog)

    @writeToFile
    def addTimeoutToConnectServer(self, url):
        self.logs.append(Log.getTime() + "Time out in request from {} ...".format(url))


    @writeToFile
    def addServerSentResponse(self, request):
        newLog = Log.getTime() + 'Server sent response to proxy with headers:'
        newLog += "\n++++++++++++++++++++++++++++++++\n"
        newLog += request
        newLog += "++++++++++++++++++++++++++++++++"
        self.logs.append(newLog)

    @writeToFile
    def addProxySentResponse(self, request):
        newLog = Log.getTime() + 'Proxy sent response to client with headers:'
        newLog += "\n++++++++++++++++++++++++++++++++\n"
        newLog += request
        newLog += "++++++++++++++++++++++++++++++++"
        self.logs.append(newLog)

    #TODO: Cache log



