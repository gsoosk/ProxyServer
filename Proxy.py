import signal
import socket
import threading
from Parsers.HttpParser import HttpParser

class Proxy:


    port = None
    hostName = None
    serverSocket = None
    maxRequestLength = 100000

    def __init__(self, config):
        # signal.signal(signal.SIGINT, self.shutdown)
        self.setConfig(config) # Setting config to class fields
        self.socketInit()


    @classmethod
    def socketInit(cls):
        print("Socket Init.....")
        # Create a TCP socket
        cls.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Re-use the socket
        cls.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to a public host, and a port
        cls.serverSocket.bind((cls.hostName, cls.port))

        cls.serverSocket.listen(10)  # become a server socket

        cls.clients = {}

    @classmethod
    def setConfig(cls, config):
        print("Setting Config.....")
        cls.port = config['port']
        cls.hostName = '127.0.0.1'

    @classmethod
    def acceptClients(cls):
        print("Accepting clients.....")
        while True :
            (clientSocket, clientAddress) = cls.serverSocket.accept()
            newThread = threading.Thread(target = cls.clientThread,
                                        args = (clientSocket, clientAddress) )
            newThread.setDaemon(True)
            newThread.start()

    @classmethod
    def clientThread(cls, clientSocket, clientAddress):
        print("New connection from {}....".format(clientAddress))
        request = clientSocket.recv(cls.maxRequestLength)
        url = HttpParser.getUrl(request.decode())
        print("requesting {}...".format(url))




