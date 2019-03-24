import signal
import socket
import threading
from Parsers.HttpParser import HttpParser
from ProxyFeatures.Log import Log
from ProxyFeatures.privacy import Privacy

class Proxy:


    port = None
    hostName = None
    serverSocket = None
    maxRequestLength = 100000
    maxResponseLength = 10000000
    connectionTimeout = 10

    log = None

    def __init__(self, config):
        # signal.signal(signal.SIGINT, self.shutdown)
        self.privacy = Privacy(config['privacy'])
        self.log = Log(config['logging'])
        self.log.addLaunchProxy()
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
        self.log.addRequestClientHeaders(request.decode())

        url = HttpParser.getUrl(request.decode())
        host, port = HttpParser.getHostAndIp(url)
        #TODO : Remove hostname and proxy-connection

        newRequest = request
        newRequest = self.privacy.setUserAgent(newRequest.decode())

        try:
            server = self.sendDataToServer(newRequest, host, port)
            self.waitForServer(clientSocket, server)
        except:
            self.log.addTimeoutToConnectServer(url)


    #send a copy of request to website server
    def sendDataToServer(self, request, host, port):
        self.log.addOpeningConnection(host, port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(self.connectionTimeout)
        server.connect((host, port))
        self.log.addProxySentReq(request.decode())
        server.sendall(request)
        return server

    def waitForServer(self, clientSocket, server):
        while True:
            # receive data from web server
            data = server.recv(self.maxResponseLength)
            if len(data) > 0:
                header = HttpParser.getResponseHeader(data)
                if header is not None :
                    self.log.addServerSentResponse(header.decode())

                clientSocket.send(data)  # send to browser/client

                if header is not None:
                    self.log.addProxySentResponse(header.decode())
            else:
                break