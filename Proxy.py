import signal
import socket
import threading
from Parsers.HttpParser import HttpParser
from ProxyFeatures.Log import Log
from ProxyFeatures.Privacy import Privacy
from ProxyFeatures.ResponseInjector import ResponseInjector
from ProxyFeatures.Alert import Alert
from ProxyFeatures.Accounting import Accounting
from ProxyFeatures.Cache import Cache

class Proxy:


    port = None
    hostName = None
    serverSocket = None
    maxRequestLength = 100000
    maxResponseLength = 100000
    connectionTimeout = 10

    privacy = None
    cache = None
    log = None
    responseInjector = None
    alert = None
    accounting = None

    browserSemaphore = None

    def __init__(self, config):
        # signal.signal(signal.SIGINT, self.shutdown)
        self.browserSemaphore = threading.Semaphore()
        self.privacy = Privacy(config['privacy'])
        self.cache = Cache(config['caching'])
        self.alert = Alert(config['restriction'])
        self.accounting = Accounting(config['accounting'])
        self.log = Log(config['logging'])
        self.log.addLaunchProxy()
        self.responseInjector = ResponseInjector(config['HTTPInjection'])
        self.setConfig(config) # Setting config to class fields
        self.socketInit()

    def socketInit(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log.addCreateSocket()

        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((self.hostName, self.port))
        self.log.addBindingSocket(port = self.port)

        self.serverSocket.listen(10)  # become a server socket
        self.log.addListeningForIncomings()

    def setConfig(self, config):
        self.port = config['port']
        self.hostName = '127.0.0.1'

    def acceptClients(self):
        self.log.addWaitForClientsToAccept()
        while True :
            (clientSocket, clientAddress) = self.serverSocket.accept()
            newThread = threading.Thread(target = self.clientThread,
                                         args = (clientSocket, clientAddress))
            newThread.setDaemon(True)
            newThread.start()

    def clientThread(self, clientSocket, clientAddress):
        self.log.addAcceptClient(clientAddress)
        request = clientSocket.recv(self.maxRequestLength)
        if len(request) <= 0:
            return
        self.log.addRequestClientHeaders(HttpParser.getResponseHeader(request).decode())

        url = HttpParser.getUrl(request.decode())
        host, port = HttpParser.getHostAndIp(url)

        newRequest = self.makeNewRequest(request)

        if self.alert.doesItRestricted(newRequest) :
            self.alert.handleRestrictedRequest(clientSocket, self.log, request)
        elif not self.accounting.doesUserCanGetData(clientAddress, self.log):
            self.accounting.restrictUser(clientSocket, clientAddress, self.log)
        # elif self.cache.doesRequestCached(newRequest):
        #     data = self.cache.getRequestData(newRequest)
        else:
            try:
                server = self.sendDataToServer(newRequest, host, port)
                self.waitForServer(clientSocket, server, newRequest, clientAddress)
            except:
                self.log.addTimeoutToConnectServer(url)

        clientSocket.close()

    def makeNewRequest(self, request):
        newRequest = HttpParser.changeHttpVersion(request)
        newRequest = HttpParser.removeHostname(newRequest)
        newRequest = HttpParser.removeProxyConnection(newRequest)
        newRequest = HttpParser.changeAcceptEncoding(newRequest)
        newRequest = self.privacy.setUserAgent(newRequest.decode())
        return newRequest

    #send a new request to website server
    def sendDataToServer(self, request, host, port):
        self.log.addOpeningConnection(host, port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(self.connectionTimeout)
        server.connect((host, port))
        self.log.addProxySentReq(request.decode())
        server.sendall(request)
        return server

    def waitForServer(self, clientSocket, server, request, clientAddress):
        firstPacket = True
        inject = False
        header = ""
        while True:
            # receive data from web server
            requestHeader = HttpParser.getResponseHeader(request)
            data = server.recv(self.maxResponseLength)
            if len(data) > 0:
                self.accounting.addUserDataConsume(clientAddress, len(data))
                if firstPacket :
                    header = HttpParser.getResponseHeader(data)
                    self.log.addServerSentResponse(header.decode())

                if not inject:
                    inject, data = self.responseInjector.injectPostBody(header, data, request)

                if self.cache.canCache(requestHeader.decode()):
                    self.cache.saveToCache(requestHeader , data)

                self.sendDataToBrowser(clientSocket, data)

                if firstPacket :
                    self.log.addProxySentResponse(header.decode())
                    firstPacket = False
            else:
                break

    def sendDataToBrowser(self, clientSocket, data):
        self.browserSemaphore.acquire()
        try:
            clientSocket.send(data)  # send to browser/client
        except:
            pass
        self.browserSemaphore.release()